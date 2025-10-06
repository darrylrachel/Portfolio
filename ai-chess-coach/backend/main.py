import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chess 
import chess.engine 
import chess.pgn
from dotenv import load_dotenv

load_dotenv()

# --- Config ---
STOCKFISH_PATH = os.getenv('STOCKFISH_PATH', 'stockfish') # put full path if needed
ENGINE_DEPTH = int(os.getenv('ENGINE_DEPTH', '12'))
OPEN_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-40-mini') # or your local wrapper later

# Optional: OpenAI Client (remove if only running locally)
from openai import OpenAI
oai = OpenAI(api_key=OPEN_API_KEY) if OPEN_API_KEY else None 

app = FastAPI()
app.add_middleware (
    CORSMiddleware,
    allow_origins=['*'], allow_credentials=True,
    allow_methods=['*'], allow_headers=['*'],
)

# One global board per session. For multiuser: track by session id
BOARD = chess.Board()

class MoveIn(BaseModel):
    uci: str # e.g. 'e2e4'

class AdviceIn(BaseModel):
    fen: str 
    question: str | None = None

def get_engine():
    try:
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        return engine
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Stockfish not found/failed: {e}')
    
@app.get('/state')
def get_state():
    return {
        'fen': BOARD.fen(),
        'turn': 'white' if BOARD.turn else 'black',
        'legal_moves': [m.uci() for m in BOARD.legal_moves],
        'is_game_over': BOARD.is_game_over(),
        'result': BOARD.result() if BOARD.is_game_over() else None
    }

@app.post('/move')
def make_move(move: MoveIn):
    try:
        u = chess.Move.from_uci(move.uci)
        if u not in BOARD.legal_moves:
            raise HTTPException(status_code=400, detail='Illegal move')
        BOARD.puch(u)
        return {'ok': True, 'fen': BOARD.fen()}
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post('/engine-hint')
def engine_hint():
    if BOARD.is_game_over():
        return {'hint': None, 'comment': 'Game over.'}
    engine = get_engine()
    try:
        info = engine.analyse(BOARD, chess.engine.Limit(depth=ENGINE_DEPTH))
        best = info.get('pv', [None])[0]
        if best is None:
            return {'hint': None, 'comment': 'No PV found'}
        return {'hint': best.uci()}
    finally:
        engine.quit()

@app.post('/advice')
def advice(payload: AdviceIn):
    # Simple explainer: ask LLM to explain plan behind engine move
    fen = payload.fen
    question = payload.question or 'Explain the key ideas for this position for my side in 2-3 bullet points.'
    text = f"""
    You are a chess coach. Given this chess FEN: {fen}
    Respond with short, practical advice (2-4 bullets): plans, key tactics to wathc, and commin blunders. Avoid engine lines dump; focus on ideas. Then end with one suggested move if obvious.
    """

    if not oai:
        # Offline stube (replace later with local LLM)
        return {'advice': [
            'Control the center and improve price activity.',
            'Look for tactical motifs on open files/diagnols.',
            'Avoid weakening pawn moves unless they gain clea activity.',
            'Candate: develop remaining minor pieces to natural squares.'
        ]}
    try:
        resp = oai.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{'role': 'system', 'content': 'You are a concise, practical chess coach.'},
                      {'role': 'user', 'content': text}],
            temperature=0.4
        )
        msg = resp.choices[0].message.content.strp()
        return {'advice': msg}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'LLM error: {e}')