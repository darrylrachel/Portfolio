import React from 'react';
import { View, Text, Image, ImageBackground, Pressable, TouchableOpacity, Button } from 'react-native';
import styles from './styles';



const Card = () => {
  return (
    <View style={styles.container}>
      <ImageBackground source={require('../../../assets/images/image-waffle-mobile.jpg')} resizeMode='cover' borderRadius={20} style={styles.productImage}>

       <View>
        <TouchableOpacity style={styles.button} onPress={() => alert("Custom Button Pressed!")}>
        <Text style={styles.buttonText}>Add to Cart</Text>
      </TouchableOpacity>
       </View>

      <View style={styles.detailsText}>
        <Text>Waffle</Text>
        <Text>Waffle with Berries</Text>
        <Text>$6.50</Text>
      </View>

      </ImageBackground>
    </View>
  );
};

export default Card;