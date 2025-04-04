import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  container: {
    aspectRatio: 1,
    width: '100%',
    borderRadius: 20,
    backgroundColor: 'red',
    
    
  },
  productImage: {
    width: '100%',
    height: '90%',
    resizeMode: 'contain',
    borderRadius: 20,
  },
  button: {
    backgroundColor: 'hsl(20, 50%, 98%)',
    borderRadius: 50,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    width: '50%',
    borderWidth: 1,
    borderColor: 'hsl(14, 65%, 9%)',
    position: 'absolute',
    top: 270,
    left: 93,
  },  
  buttonText: {
    fontSize: 16,
  },
  detailsText: {
    position: 'absolute',
    bottom: 0,
  }

});

export default styles;