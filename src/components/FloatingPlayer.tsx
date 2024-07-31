import { Image, StyleSheet, Text, TouchableOpacity, View } from 'react-native'
import React from 'react'
import { colors } from '../constants/colors'
import { fontSizes, iconSizes, spacing } from '../constants/dimension'
import { fontFamilies } from '../constants/fonts'
import { GotoNextButton, GotoPreviousButton, PlayPauseButton } from './PlayerControls'
import { useSharedValue } from 'react-native-reanimated'
import { Slider } from 'react-native-awesome-slider'
import MovingText from './MovingText'
import { useNavigation } from '@react-navigation/native'
import { NativeStackNavigationProp } from '@react-navigation/native-stack'
import { RootStackParamList } from '../navigation/StackNavigation'

const imagrUrl = "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRQhktRe3VcuAHtvJ0MPkU6z2MHKvlYWYzSUTNidnBPvwQuZMb4"



type NavigationProp = NativeStackNavigationProp<RootStackParamList>


const FloatingPlayer = () => {

    const navigation = useNavigation<NavigationProp>()

    const progress = useSharedValue(0.2)
    const min = useSharedValue(0)
    const max = useSharedValue(1)

    const handleOpenPlayerScreen = () => {
        navigation.navigate("PLAYER_SCREEN")
    }

    return (
        <View>
            <Slider
                style={{ flex: 1, zIndex: 1 }}
                progress={progress}
                minimumValue={min}
                maximumValue={max}
                theme={{
                    minimumTrackTintColor: colors.minimumTintColor,
                    maximumTrackTintColor: colors.maximumTintColor
                }}

                renderBubble={() => <View />}

            />
            <TouchableOpacity style={styles.container}
                activeOpacity={0.6}
                onPress={handleOpenPlayerScreen}
            >
                <Image source={{ uri: imagrUrl }} style={styles.coverImage} />
                <View style={styles.titleContainer}>
                    <MovingText
                        text={"Chaff and Dust"}
                        animationThreshold={15}
                        style={styles.title}
                    />
                    <Text style={styles.artist}>Alan Walker</Text>
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
    playerControlContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 20,
        paddingRight: spacing.lg
    }

})