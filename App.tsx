import React from 'react'
import { NavigationContainer } from '@react-navigation/native'
import { GestureHandlerRootView } from 'react-native-gesture-handler'
import DrawerNavigation from './src/navigation/DrawerNavigation'
import { useSetupPlayer } from './src/hooks/useSetupTrackPlayer'



const App = () => {

  const onLoad = () =>{
    console.log('Success setup player')
  }

  //setup track player app
  useSetupPlayer({onLoad})

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <NavigationContainer>
        <DrawerNavigation />
      </NavigationContainer>
    </GestureHandlerRootView>
  )
}

export default App