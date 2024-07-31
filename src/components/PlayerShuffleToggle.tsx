import { StyleSheet, Text, TouchableOpacity, View } from 'react-native'
import React from 'react'
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons'
import { colors } from '../constants/colors'
import { iconSizes } from '../constants/dimension'
import TrackPlayer from 'react-native-track-player'

const PlayerSuffleToggle = () => {

    const shfulleSongs = async () =>
    { 
        let queue = await TrackPlayer.getQueue()
        
        await TrackPlayer.reset()
        queue.sort(() => Math.random() - 0.5)
        await TrackPlayer.add(queue)
        await TrackPlayer.play()
    }



    return (
        <TouchableOpacity onPress={shfulleSongs}>
            <MaterialCommunityIcons name={'shuffle'} color={colors.iconSecondary} size={iconSizes.lg} />
        </TouchableOpacity>
    )
}

export default PlayerSuffleToggle

const styles = StyleSheet.create({})