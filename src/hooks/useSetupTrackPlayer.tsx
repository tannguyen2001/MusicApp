import { useEffect } from "react"
import TrackPlayer, { Capability, RatingType, RepeatMode } from "react-native-track-player"

const setupPlayer = async () => {
    await TrackPlayer.setupPlayer({
        maxCacheSize: 1024 * 10
    })

    await TrackPlayer.updateOptions({
        ratingType: RatingType.Heart,
        capabilities: [
            Capability.Play,
            Capability.Pause,
            Capability.SkipToNext,
            Capability.SkipToPrevious,
            Capability.Stop,
        ],
        compactCapabilities: [Capability.Play, Capability.Pause],
    })

    await TrackPlayer.setVolume(0.5)
    await TrackPlayer.setRepeatMode(RepeatMode.Queue)
}


export const useSetupPlayer = () => {



    //add logic for setup
    useEffect(() => {
        setupPlayer().then(() => {
            console.log("player success setup")
        })
    }, [])

}