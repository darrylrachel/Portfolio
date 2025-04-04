import { StyleSheet, Text, View } from "react-native";
import { useFonts } from '@expo-google-fonts/red-hat-text/useFonts';
import { RedHatText_300Light } from '@expo-google-fonts/red-hat-text/300Light';
import { RedHatText_400Regular } from '@expo-google-fonts/red-hat-text/400Regular';
import { RedHatText_500Medium } from '@expo-google-fonts/red-hat-text/500Medium';
import { RedHatText_600SemiBold } from '@expo-google-fonts/red-hat-text/600SemiBold';
import { RedHatText_700Bold } from '@expo-google-fonts/red-hat-text/700Bold';
import { RedHatText_300Light_Italic } from '@expo-google-fonts/red-hat-text/300Light_Italic';
import { RedHatText_400Regular_Italic } from '@expo-google-fonts/red-hat-text/400Regular_Italic';
import { RedHatText_500Medium_Italic } from '@expo-google-fonts/red-hat-text/500Medium_Italic';
import { RedHatText_600SemiBold_Italic } from '@expo-google-fonts/red-hat-text/600SemiBold_Italic';
import { RedHatText_700Bold_Italic } from '@expo-google-fonts/red-hat-text/700Bold_Italic';
import Card from "./components/Card";

export default function Index() {

   let [fontsLoaded] = useFonts({
    RedHatText_300Light, 
    RedHatText_400Regular, 
    RedHatText_500Medium, 
    RedHatText_600SemiBold, 
    RedHatText_700Bold, 
    RedHatText_300Light_Italic, 
    RedHatText_400Regular_Italic, 
    RedHatText_500Medium_Italic, 
    RedHatText_600SemiBold_Italic, 
    RedHatText_700Bold_Italic
  });

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Desserts</Text>
      <Card />
    </View>
  );
}

const styles = StyleSheet.create ({
  container: {
    flex: 1,
    padding: 30,
    backgroundColor: 'hsl(13, 31%, 94%)',
  },
  header: {
    fontSize: 40,
    fontFamily: 'RedHatText_700Bold',
  }
})
