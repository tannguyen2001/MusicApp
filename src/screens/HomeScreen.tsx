import { FlatList, StyleSheet, Text, TouchableOpacity, View } from 'react-native'
import React, { Component } from 'react'
import { colors } from '../constants/colors'
import Header from '../components/Header'
import { fontFamilies } from '../constants/fonts'
import { fontSizes, spacing } from '../constants/dimension'
import SongCard from '../components/SongCard'
import SongCardWithCategory from '../components/SongCardWithCategory'
import FloatingPlayer from '../components/FloatingPlayer'

const HomeScreen = () => {
    return (
        <View style={styles.container}>
            <Header />
            <FlatList
                data={[1, 2, 3, 4, 5, 6, 7]}
                renderItem={SongCardWithCategory}
                contentContainerStyle={{
                    paddingBottom: 100
                }}
            />
            <FloatingPlayer />
        </View>
    )
}

export default HomeScreen


const styles = StyleSheet.create({
    container: {
        backgroundColor: colors.background,
        flex: 1
    },

})