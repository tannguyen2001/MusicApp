import { FlatList, StyleSheet, Text, View } from 'react-native'
import React from 'react'
import SongCard from './SongCard'
import { fontSizes, spacing } from '../constants/dimension'
import { colors } from '../constants/colors'
import { fontFamilies } from '../constants/fonts'
import TrackPlayer from 'react-native-track-player'

const SongCardWithCategory = ({ item }: any) => {

    const handlePlayTrack = async (selectedTrack: any) => {

        const songs = item.songs
        //tạo hàng đợi để chơi nhạc
        const trackIndex = songs.findIndex((track: any) => track.url === selectedTrack.url)
        if (trackIndex === -1) {
            return
        }

        //Lấy list nhạc trước và sau bài hát
        const beforeTracks = songs.slice(0, trackIndex)
        const afterTracks = songs.slice(trackIndex + 1)

        await TrackPlayer.reset()
        await TrackPlayer.add(selectedTrack)
        await TrackPlayer.add(afterTracks)
        await TrackPlayer.add(beforeTracks)

        await TrackPlayer.play()

    }

    return (
        <View style={styles.container}>
            <Text style={styles.headingText}>{item.title}</Text>
            <FlatList data={item.songs}
                renderItem={({ item }) => <SongCard
                    item={item}
                    handlePlay={(selectedTrack: any) => {
                        handlePlayTrack(selectedTrack)
                    }}
                />}
                ItemSeparatorComponent={() => <View style={{ marginHorizontal: spacing.sm }} />}
                horizontal={true}
                contentContainerStyle={{
                    paddingHorizontal: spacing.lg
                }}
            />
        </View>
    )
}

export default SongCardWithCategory

const styles = StyleSheet.create({
    container: {
        flex: 1
    },
    headingText: {
        fontSize: fontSizes.xl,
        color: colors.textPrimary,
        fontFamily: fontFamilies.bold,
        marginVertical: spacing.lg,
        marginHorizontal: spacing.lg
    }
})