import { StyleSheet, Text, View } from 'react-native'
import React from 'react'
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HomeScreen from '../screens/HomeScreen';
import LikeScreen from '../screens/LikeScreen';
import PlayerScreen from '../screens/PlayerScreen';


export type RootStackParamList = {
    HOME_SCREEN: undefined;
    LIKE_SCREEN: undefined;
    PLAYER_SCREEN: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>()

const StackNavigation = () => {

    return (
        <Stack.Navigator
            screenOptions={{ headerShown: false }}
            initialRouteName='HOME_SCREEN'
        >
            <Stack.Screen name='HOME_SCREEN' component={HomeScreen} />
            <Stack.Screen name='LIKE_SCREEN' component={LikeScreen} />
            <Stack.Screen name='PLAYER_SCREEN' component={PlayerScreen} />
        </Stack.Navigator>
    )
}

export default StackNavigation

const styles = StyleSheet.create({})