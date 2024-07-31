import { StyleSheet, Text, View } from 'react-native'
import React from 'react'
import { colors } from '../constants/colors'
import { fontFamilies } from '../constants/fonts'
import { fontSizes, spacing } from '../constants/dimension'
import { Slider } from 'react-native-awesome-slider'
import { useSharedValue } from 'react-native-reanimated'
import TrackPlayer, { useProgress } from 'react-native-track-player'
import { formatSecondsToMinutes } from '../utils'

const PlayerProgressBar = ({ timeRow, styleContainer, styleSlider, thumbWidth = 18 }: any) => {

    const { duration, position } = useProgress()

    const progress = useSharedValue(0);
    const min = useSharedValue(0);
    const max = useSharedValue(1);

    const isSliding = useSharedValue(false)

    if (!isSliding.value) {
        progress.value = duration > 0 ? position / duration : 0

    }

    return (
        <View>
            {timeRow &&
                <View style={styles.timeRow}>
                    <Text style={styles.timeText}>{formatSecondsToMinutes(position)}</Text>
                    <Text style={styles.timeText}>{"-"}{formatSecondsToMinutes(duration - position)}</Text>
                </View>}
            <Slider
                style={[styles.sliderContainer, styleSlider]}
                containerStyle={[{
                    height: 8,
                    borderRadius: spacing.sm,
                }, { ...styleContainer }]}
                theme={{
                    maximumTrackTintColor: colors.maximumTintColor,
                    minimumTrackTintColor: colors.minimumTintColor
                }}
                progress={progress}
                minimumValue={min}
                maximumValue={max}
                thumbWidth={thumbWidth}
                renderBubble={() => null}
                onSlidingStart={() => isSliding.value}
                onValueChange={async (value) => {
                    await TrackPlayer.seekTo(value * duration)
                }}
                onSlidingComplete={async (value) => {
                    if (!isSliding.value) {
                        return
                    }
                    isSliding.value = false
                    await TrackPlayer.seekTo(value * duration)
                }}

            />
        </View>
    )
}

export default PlayerProgressBar

const styles = StyleSheet.create({
    timeRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginTop: spacing.xl
    },
    timeText: {
        color: colors.textPrimary,
        fontFamily: fontFamilies.regular,
        fontSize: fontSizes.md,
        opacity: 0.75
    },
    sliderContainer: {
        marginVertical: spacing.lg
    }
})