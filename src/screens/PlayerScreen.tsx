import { View, Text, StyleSheet, Image } from 'react-native'
import React from 'react'
import { colors } from '../constants/colors'
import { TouchableOpacity } from 'react-native-gesture-handler'
import AntDesign from 'react-native-vector-icons/AntDesign'
import { fontSizes, iconSizes, spacing } from '../constants/dimension'
import { fontFamilies } from '../constants/fonts'
import Feather from 'react-native-vector-icons/Feather'
import PlayerRepeatToggle from '../components/PlayerRepeatToggle'
import PlayerSuffleToggle from '../components/PlayerShuffleToggle'
import PlayerProgressBar from '../components/PlayerProgressBar'
import { GotoNextButton, GotoPreviousButton, PlayPauseButton } from '../components/PlayerControls'


const imageUrl = "https://ncsmusic.s3.eu-west-1.amazonaws.com/tracks/000/001/644/1000x0/pretty-afternoon-1709859658-TKAtqZGQtZ.jpg"

const PlayerScreen = () => {

  const isLiked = false
  const isMute = false

  return (
    <View style={styles.container}>
      <View style={styles.headerContainer}>
        <TouchableOpacity>
          <AntDesign name='arrowleft' color={colors.iconPrimary} size={iconSizes.md} />
        </TouchableOpacity>
        <Text style={styles.headerText}>Playing Now</Text>
      </View>
      <View style={styles.coverImageContainer}>
        <Image source={{ uri: imageUrl }} style={styles.coverImage} />
      </View>
      <View style={styles.titleRowHeartContainer}>
        <View style={styles.titleContainer}>
          <Text style={styles.title}>Believer</Text>
          <Text style={styles.artist}>IMAGIEN DRAGON</Text>
        </View>
        <TouchableOpacity>
          <AntDesign name={isLiked ? 'heart' : 'hearto'} color={colors.iconPrimary} size={iconSizes.md} />
        </TouchableOpacity>
      </View>

      <View style={styles.playerControlContainer}>
        <TouchableOpacity style={styles.volumeWrapper}>
          <Feather name={isMute ? 'volume-x' : 'volume-1'} size={iconSizes.lg} color={colors.iconSecondary} />
        </TouchableOpacity>
        <View style={styles.repeatShuffleWrapper} >
          <PlayerRepeatToggle />
          <PlayerSuffleToggle />
        </View>
      </View>

      <PlayerProgressBar />

      <View style={styles.playPauseContainer}>
        <GotoPreviousButton size={iconSizes.xl} />
        <PlayPauseButton size={iconSizes.xl} />
        <GotoNextButton size={iconSizes.xl} />
      </View>
    </View>
  )
}

export default PlayerScreen

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
    padding: spacing.lg
  },
  headerContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    width: '100%'
  },
  headerText: {
    color: colors.textPrimary,
    fontSize: fontSizes.lg,
    fontFamily: fontFamilies.medium,
    flex: 1,
    textAlign: 'center'

  },
  coverImageContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    marginVertical: spacing.xl
  },
  coverImage: {
    height: 300,
    width: 300,
    borderRadius: 10
  },
  titleRowHeartContainer: {
    flexDirection: 'row',
    alignItems: 'center'
  },
  titleContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center'
  },
  title: {
    fontSize: fontSizes.xl,
    color: colors.textPrimary,
    fontFamily: fontFamilies.medium
  },
  artist: {
    fontSize: fontSizes.lg,
    color: colors.textSecondary
  },
  playerControlContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginVertical: spacing.lg
  },
  volumeWrapper: {
    flex: 1,

  },
  repeatShuffleWrapper: {
    flexDirection: 'row',
    gap: spacing.md
  },
  playPauseContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: spacing.xl,
    flex: 1
  }
})