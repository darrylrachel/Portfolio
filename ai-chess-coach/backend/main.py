import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BasrModel
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
    uci: str # e.g.m 'e2e4'

class AdviceIn(BasrModel):
    fen: str 
    question: str | None = None

def get_engine():
    try:
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        return engine
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Stockfish not found/failed: {e}')