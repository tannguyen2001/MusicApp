import { Text, Image, StyleSheet, TouchableOpacity } from 'react-native'
import React from 'react'
import { colors } from '../constants/colors'
import { fontFamilies } from '../constants/fonts'
import { fontSizes, spacing } from '../constants/dimension'


const imageUrl = "https://ncsmusic.s3.eu-west-1.amazonaws.com/tracks/000/001/644/1000x0/pretty-afternoon-1709859658-TKAtqZGQtZ.jpg"

interface SongCardProps {
    containerStyle?: object
    imageStyle?: object
}

const SongCard: React.FC<SongCardProps> = ({ containerStyle, imageStyle }) => {
    return (
        <TouchableOpacity style={[styles.container, containerStyle]}>
            <Image source={{ uri: imageUrl }} style={[styles.coverImage, imageStyle]} />
            <Text style={styles.title} numberOfLines={1}>Monster Go Home</Text>
            <Text style={styles.author}>Alan Walker</Text>
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
    author: {
        color: colors.textSecondary,
        fontSize: fontSizes.md,
        fontFamily: fontFamilies.regular,
        textAlign: 'center'
    }
})