import { StyleSheet, Text, TouchableOpacity, View } from 'react-native'
import React from 'react'
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons'
import { colors } from '../constants/colors'
import { iconSizes } from '../constants/dimension'

const PlayerSuffleToggle = () => {
    return (
        <TouchableOpacity>
            <MaterialCommunityIcons name={'shuffle'} color={colors.iconSecondary} size={iconSizes.lg} />
        </TouchableOpacity>
    )
}

export default PlayerSuffleToggle

const styles = StyleSheet.create({})