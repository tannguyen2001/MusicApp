import React, { useEffect } from 'react'
import { NavigationContainer } from '@react-navigation/native'
import { GestureHandlerRootView } from 'react-native-gesture-handler'
import DrawerNavigation from './src/navigation/DrawerNavigation'
import TrackPlayer from 'react-native-track-player'



const App = () => {

  const setupPlayer = async () => {
    await TrackPlayer.setupPlayer()
    console.log("success setup player")
  }


  useEffect(() => {
    setupPlayer()
  }, [])



  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <NavigationContainer>
        <DrawerNavigation />
      </NavigationContainer>
    </GestureHandlerRootView>
  )
}

export default App