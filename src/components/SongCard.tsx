import { Text, Image, StyleSheet, TouchableOpacity, View } from 'react-native'
import React from 'react'
import { colors } from '../constants/colors'
import { fontFamilies } from '../constants/fonts'
import { fontSizes, spacing } from '../constants/dimension'



const SongCard = ({ item, containerStyle, imageStyle, handlePlay }: any) => {

    return (
        <TouchableOpacity style={[styles.container, containerStyle]}
            onPress={() => handlePlay(item)}
        >
            <Image source={{ uri: item.artwork }} style={[styles.coverImage, imageStyle]} />
            <Text style={styles.title} numberOfLines={1}>{item?.title}</Text>
            <Text style={styles.artist}>{item?.artist}</Text>
        </TouchableOpacity>
    )
}

export default SongCard

const styles = StyleSheet.create({
    container: {
        width: 270
    }
    ,
    coverImage: {
        width: 250,
        height: 250,
        borderRadius: 10
    },
    title: {
        color: colors.textPrimary,
        fontFamily: fontFamilies.medium,
        textAlign: 'center',
        fontSize: fontSizes.lg,
        paddingVertical: spacing.sm,

    },
    artist: {
        color: colors.textSecondary,
        fontSize: fontSizes.md,
        fontFamily: fontFamilies.regular,
        textAlign: 'center'
    }
})