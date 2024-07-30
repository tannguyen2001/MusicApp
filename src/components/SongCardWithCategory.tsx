import { FlatList, StyleSheet, Text, View } from 'react-native'
import React from 'react'
import SongCard from './SongCard'
import { fontSizes, spacing } from '../constants/dimension'
import { colors } from '../constants/colors'
import { fontFamilies } from '../constants/fonts'

const SongCardWithCategory = () => {
    return (
        <View style={styles.container}>
            <Text style={styles.headingText}>Recommended for you</Text>
            <FlatList data={[1, 2, 3, 4, 5]}
                renderItem={() => <SongCard />}
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