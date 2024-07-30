import { StyleSheet, Text, TouchableOpacity, View } from 'react-native'
import React, { Component } from 'react'
import FontAwesome5 from 'react-native-vector-icons/FontAwesome5'
import { colors } from '../constants/colors'
import AntDesign from 'react-native-vector-icons/AntDesign'
import { iconSizes, spacing } from '../constants/dimension'

const Header = () => {
    return (
        <View style={styles.header}>
            <TouchableOpacity>
                <FontAwesome5 name={'grip-lines'} color={colors.iconPrimary} size={iconSizes.lg} />
            </TouchableOpacity>
            <TouchableOpacity>
                <AntDesign name={'search1'} color={colors.iconPrimary} size={iconSizes.lg} />
            </TouchableOpacity>
        </View>
    )
}

export default Header


const styles = StyleSheet.create({
    container: {
        backgroundColor: colors.background,
        flex: 1
    },
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        paddingVertical: spacing.md,
        paddingHorizontal: spacing.lg

    }
})