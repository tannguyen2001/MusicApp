import { View, Text, StyleSheet, FlatList } from 'react-native'
import React from 'react'
import { colors } from '../constants/colors'
import { TouchableOpacity } from 'react-native-gesture-handler'
import AntDesign from 'react-native-vector-icons/AntDesign'
import { fontSizes, iconSizes, spacing } from '../constants/dimension'
import SimpleLineIcons from 'react-native-vector-icons/SimpleLineIcons'
import { fontFamilies } from '../constants/fonts'
import SongCard from '../components/SongCard'
import FloatingPlayer from '../components/FloatingPlayer'

const LikeScreen = () => {
    return (
        <View style={styles.container}>
            <View style={styles.headerContailer}>
                <TouchableOpacity>
                    <AntDesign name='arrowleft' color={colors.iconPrimary} size={iconSizes.md} />
                </TouchableOpacity>
                <TouchableOpacity>
                    <SimpleLineIcons name='equalizer' color={colors.iconPrimary} size={iconSizes.md} />
                </TouchableOpacity>
            </View>

            <FlatList
                ListHeaderComponent={
                    <Text style={styles.headingText}>Liked Songs</Text>
                }

                data={[1, 2, 3, 4, 5]}
                renderItem={() => <SongCard
                    containerStyle={{ width: '47%' }}
                    imageStyle={{
                        height: 160,
                        width: 160
                    }}
                />}
                numColumns={2}
                contentContainerStyle={{
                    paddingBottom: 200,
                    paddingHorizontal: spacing.lg
                }}

                columnWrapperStyle={{
                    justifyContent: 'space-between',
                    marginVertical: spacing.lg
                }}
            />

            <FloatingPlayer />
        </View>
    )
}

export default LikeScreen

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: colors.background
    },
    headerContailer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingVertical: spacing.md,
        paddingHorizontal: spacing.md
    },
    headingText: {
        fontSize: fontSizes.lg,
        color: colors.textPrimary,
        fontFamily: fontFamilies.bold,
    }
})