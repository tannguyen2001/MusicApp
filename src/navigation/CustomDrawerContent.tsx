import { View, Text, StyleSheet } from 'react-native'
import React from 'react'
import { DrawerContentScrollView, DrawerItem } from '@react-navigation/drawer'
import { colors } from '../constants/colors'
import { fontSizes, iconSizes, spacing } from '../constants/dimension'
import { TouchableOpacity } from 'react-native-gesture-handler'
import AntDesign from 'react-native-vector-icons/AntDesign'
import Octicons from 'react-native-vector-icons/Octicons'
import FontAwesome from 'react-native-vector-icons/FontAwesome'
import { fontFamilies } from '../constants/fonts'

const CustomDrawerContent = (props: any) => {

    const isDarkMode = true

    const toggleDrawer = () => {
        props.navigation.toggleDrawer()
    }

    return (
        <DrawerContentScrollView {...props} style={styles.container}>
            <View style={styles.headerIconContainer}>
                <TouchableOpacity onPress={toggleDrawer}>
                    <AntDesign
                        name={'close'}
                        color={colors.iconPrimary}
                        size={iconSizes.lg}
                    />
                </TouchableOpacity>
                <TouchableOpacity>
                    <Octicons
                        name={isDarkMode ? 'sun' : 'moon'}
                        color={colors.iconPrimary}
                        size={iconSizes.lg}
                    />
                </TouchableOpacity>
            </View>

            <View style={styles.drawerItemContainer}>
                <DrawerItem label={"Profile"} icon={() =>
                (<View style={styles.iconStyle}>
                    <FontAwesome
                        name={'user'}
                        size={iconSizes.md}
                        color={colors.iconSecondary}
                    />
                </View>)
                }
                    labelStyle={styles.labelStyle}
                    onPress={() => null}
                    style={styles.drawerItem}
                />

                <DrawerItem label={"Liked Songs"} icon={() => (
                    <View style={styles.iconStyle}>
                        <AntDesign
                            name={'hearto'}
                            size={iconSizes.md}
                            color={colors.iconSecondary}
                        />
                    </View>
                )}
                    labelStyle={styles.labelStyle}
                    onPress={() => props.navigation.navigate("LIKE_SCREEN")}
                    style={styles.drawerItem}
                />

                <DrawerItem label={"Language"} icon={() => (
                    <View style={styles.iconStyle}>
                        <FontAwesome
                            name={'language'}
                            size={iconSizes.md}
                            color={colors.iconSecondary}
                        />
                    </View>)}
                    labelStyle={styles.labelStyle}
                    onPress={() => null}
                    style={styles.drawerItem}
                />

                <DrawerItem label={"Contact us"} icon={() => (
                    <View style={styles.iconStyle}>
                        <FontAwesome
                            name={'envelope-o'}
                            size={iconSizes.md}
                            color={colors.iconSecondary}
                        />
                    </View>
                )}
                    labelStyle={styles.labelStyle}
                    onPress={() => null}
                    style={styles.drawerItem}
                />

                <DrawerItem label={"FAQs"} icon={() => (
                    <View style={styles.iconStyle}>
                        <FontAwesome
                            name={'question-circle-o'}
                            size={iconSizes.md}
                            color={colors.iconSecondary}
                        />
                    </View>
                )}
                    labelStyle={styles.labelStyle}
                    onPress={() => null}
                    style={styles.drawerItem}
                />

                <DrawerItem label={"Settings"} icon={() => (
                    <View style={styles.iconStyle}>
                        <FontAwesome
                            name={'cog'}
                            size={iconSizes.md}
                            color={colors.iconSecondary}
                        />
                    </View>
                )}
                    labelStyle={styles.labelStyle}
                    onPress={() => null}
                    style={styles.drawerItem}
                />

            </View>

        </DrawerContentScrollView>
    )
}

export default CustomDrawerContent


const styles = StyleSheet.create({
    container: {
        backgroundColor: colors.background,
        padding: spacing.lg
    },
    headerIconContainer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center'
    },
    drawerItemContainer: {
        marginVertical: spacing.xl
    },
    iconStyle: {
        width: iconSizes.md,
        height: iconSizes.md
    },
    labelStyle: {
        fontSize: fontSizes.md,
        color: colors.textPrimary,
        fontFamily: fontFamilies.medium,
    },
    drawerItem: {
        marginVertical: 0
    }
})