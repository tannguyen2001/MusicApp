import { StyleSheet, Text, TouchableOpacity, View } from 'react-native'
import React from 'react'
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons'
import { colors } from '../constants/colors'
import { iconSizes } from '../constants/dimension'
import { useTrackPlayerRepeatMode } from '../hooks/useTrackPlayerRepeatMode'
import { RepeatMode } from 'react-native-track-player'

const PlayerRepeatToggle = () => {

    const {repeatMode,changeReapeatMode} = useTrackPlayerRepeatMode()

    const repeatOrder = [RepeatMode.Off,RepeatMode.Track,RepeatMode.Queue]

    const toggleRepeatMode = ()=>{
        const currentIndex = repeatOrder.indexOf(repeatMode)
        const nextIndex = (currentIndex + 1) % repeatOrder.length
        changeReapeatMode(repeatOrder[nextIndex])

    }

    let iconName = 'repeat'
    switch(repeatMode){
        case RepeatMode.Off:
            iconName = 'repeat-off'
            break
        case RepeatMode.Queue:
            iconName = 'repeat'
            break
        case RepeatMode.Track:
            iconName = 'repeat-once'
            break
    }


    return (
        <TouchableOpacity onPress={toggleRepeatMode}>
            <MaterialCommunityIcons name={iconName} color={colors.iconSecondary} size={iconSizes.lg} />
        </TouchableOpacity>
    )
}

export default PlayerRepeatToggle

const styles = StyleSheet.create({})