import React, { Component } from 'react'
import { NavigationContainer } from '@react-navigation/native'
import { createNativeStackNavigator } from '@react-navigation/native-stack'
import HomeScreen from './src/screens/HomeScreen'
import { GestureHandlerRootView } from 'react-native-gesture-handler'
import LikeScreen from './src/screens/LikeScreen'
import PlayerScreen from './src/screens/PlayerScreen'


export type RootStackParamList = {
  HOME_SCREEN: undefined;
  LIKE_SCREEN: undefined;
  PLAYER_SCREEN: undefined;
};


const Stack = createNativeStackNavigator<RootStackParamList>()

export class App extends Component {
  render() {
    return (
      <GestureHandlerRootView style={{ flex: 1 }}>
        <NavigationContainer>
          <Stack.Navigator
            screenOptions={{ headerShown: false }}
            initialRouteName='HOME_SCREEN'
          >
            <Stack.Screen name='HOME_SCREEN' component={HomeScreen} />
            <Stack.Screen name='LIKE_SCREEN' component={LikeScreen} />
            <Stack.Screen name='PLAYER_SCREEN' component={PlayerScreen} />
          </Stack.Navigator>
        </NavigationContainer>
      </GestureHandlerRootView>
    )
  }
}

export default App