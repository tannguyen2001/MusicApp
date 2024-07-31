import { TouchableOpacity, StyleSheet } from 'react-native'
import React, { useState } from 'react'
import { iconSizes } from '../constants/dimension'
import { colors } from '../constants/colors'
import FontAwesome6 from 'react-native-vector-icons/FontAwesome6'
import TrackPlayer, { useIsPlaying } from 'react-native-track-player'

const activeOpacity = 0.85

export const GotoPreviousButton = ({ size = iconSizes.lg }) => {

    const handleTogglePrevious = async ()=>{
        await TrackPlayer.skipToPrevious()
    }

    return (
        <TouchableOpacity activeOpacity={activeOpacity} onPress={handleTogglePrevious}>
            <FontAwesome6 name={'backward'} size={size}
                color={colors.iconPrimary}
            />
        </TouchableOpacity>
    )
}


export const PlayPauseButton = ({ size = iconSizes.lg }) => {

    const {playing} = useIsPlaying()

    const handleTogglePlay = async () =>{
        if(playing)
        {
            await TrackPlayer.pause()
        }else{
            await TrackPlayer.play()
        }
    }
    
    return (
        <TouchableOpacity activeOpacity={activeOpacity} onPress={handleTogglePlay}>
            <FontAwesome6 name={playing ? 'pause' : 'play'} size={size}
                color={colors.iconPrimary}
            />
        </TouchableOpacity>
    )
}

export const GotoNextButton = ({ size = iconSizes.lg }) => {

    const handleToggleGotoNext = async ()=>{
        await TrackPlayer.skipToNext()
    }

    return (
        <TouchableOpacity activeOpacity={activeOpacity} onPress={handleToggleGotoNext}>
            <FontAwesome6 name={'forward'} size={size}
                color={colors.iconPrimary}
            />
        </TouchableOpacity>
    )
}

