import { Image, StyleSheet, Text, TouchableOpacity, View } from 'react-native'
import React from 'react'
import { colors } from '../constants/colors'
import { fontSizes, iconSizes, spacing } from '../constants/dimension'
import { fontFamilies } from '../constants/fonts'
import { GotoNextButton, GotoPreviousButton, PlayPauseButton } from './PlayerControls'
import MovingText from './MovingText'
import { useNavigation } from '@react-navigation/native'
import { NativeStackNavigationProp } from '@react-navigation/native-stack'
import { RootStackParamList } from '../navigation/StackNavigation'
import { useActiveTrack } from 'react-native-track-player'
import PlayerProgressBar from './PlayerProgressBar'


type NavigationProp = NativeStackNavigationProp<RootStackParamList>


const FloatingPlayer = () => {

    const activeTrack = useActiveTrack()
    const navigation = useNavigation<NavigationProp>()

    if (!activeTrack) {
        return <View></View>
    }

    return (
        <View>
            <View style={styles.wrapperSlider}>
                <PlayerProgressBar
                    styleSlider={styles.playerProgressBarSlider}
                    styleContainer={styles.playerProgressBarContainer}
                    thumbWidth={12}
                />
            </View>
            <TouchableOpacity style={styles.container}
                activeOpacity={0.6}
                onPress={() => navigation.navigate("PLAYER_SCREEN")}
            >
                <Image source={{ uri: activeTrack?.artwork }} style={styles.coverImage} />
                <View style={styles.titleContainer}>
                    <MovingText
                        text={"Chaff and Dust"}
                        animationThreshold={15}
                        style={styles.title}
                    />
                    <Text style={styles.artist}>{activeTrack?.artist}</Text>
                </View>
                <View style={styles.playerControlContainer}>
                    <GotoPreviousButton size={iconSizes.md} />
                    <PlayPauseButton size={iconSizes.lg} />
                    <GotoNextButton size={iconSizes.md} />
                </View>
            </TouchableOpacity>
        </View>
    )
}

export default FloatingPlayer

const styles = StyleSheet.create({
    container: {
        flexDirection: 'row',
        alignItems: 'center',
        overflow: 'hidden'
    },
    coverImage: {
        width: 60,
        height: 60,
        resizeMode: 'cover'
    },
    titleContainer: {
        flex: 1,
        paddingHorizontal: spacing.sm,
        overflow: 'hidden'
    },
    title: {
        color: colors.textPrimary,
        fontSize: fontSizes.lg,
        fontFamily: fontFamilies.medium,
    },
    artist: {
        color: colors.textSecondary,
        fontSize: fontSizes.md,

    },
    wrapperSlider: {
        zIndex: 1
    }
    ,
    playerControlContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 20,
        paddingRight: spacing.lg
    },
    playerProgressBarSlider: {
        marginVertical: 0
    },
    playerProgressBarContainer: {
        height: 6,
        borderRadius: 0,
    }

})