import { TouchableOpacity, StyleSheet } from 'react-native'
import React, { useState } from 'react'
import { iconSizes } from '../constants/dimension'
import { colors } from '../constants/colors'
import FontAwesome6 from 'react-native-vector-icons/FontAwesome6'

const activeOpacity = 0.85

export const GotoPreviousButton = ({ size = iconSizes.lg }) => {
    return (
        <TouchableOpacity activeOpacity={activeOpacity}>
            <FontAwesome6 name={'backward'} size={size}
                color={colors.iconPrimary}
            />
        </TouchableOpacity>
    )
}


export const PlayPauseButton = ({ size = iconSizes.lg }) => {

    const [isPlaying, setIsPlaying] = useState(false)

    const handlerPressPlayPause = () => {
        setIsPlaying(prev => !prev)
    }

    return (
        <TouchableOpacity activeOpacity={activeOpacity} onPress={handlerPressPlayPause}>
            <FontAwesome6 name={isPlaying ? 'pause' : 'play'} size={size}
                color={colors.iconPrimary}
            />
        </TouchableOpacity>
    )
}

export const GotoNextButton = ({ size = iconSizes.lg }) => {
    return (
        <TouchableOpacity activeOpacity={activeOpacity}>
            <FontAwesome6 name={'forward'} size={size}
                color={colors.iconPrimary}
            />
        </TouchableOpacity>
    )
}

