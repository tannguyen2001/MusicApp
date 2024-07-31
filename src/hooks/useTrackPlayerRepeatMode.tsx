import { useCallback, useEffect, useState } from "react"
import TrackPlayer, { RepeatMode } from "react-native-track-player"

export const useTrackPlayerRepeatMode = ()=>{
    const [repeatMode,setRepeatMode] = useState(RepeatMode.Off)
    const changeReapeatMode = useCallback(async (repeatMode:RepeatMode)=>{
        await TrackPlayer.setRepeatMode(repeatMode)
        setRepeatMode(repeatMode)
    },[])

    useEffect(()=>{
        TrackPlayer.getRepeatMode().then((res) => setRepeatMode(res))
    },[])

    return {repeatMode,changeReapeatMode}

}