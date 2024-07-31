import React from 'react'
import { createDrawerNavigator } from '@react-navigation/drawer';
import StackNavigation from './StackNavigation';
import CustomDrawerContent from './CustomDrawerContent';


export type RootDrawerParamList = {
    DRAWER_HOME: undefined,
};


const Drawer = createDrawerNavigator<RootDrawerParamList>();

const DrawerNavigation = () => {
    return (
        <Drawer.Navigator initialRouteName="DRAWER_HOME"
            screenOptions={{
                headerShown: false,
                overlayColor: 'transparent',
                //drawerType: 'slide'
            }}
            drawerContent={(props) => <CustomDrawerContent {...props} />}
        >
            <Drawer.Screen name='DRAWER_HOME' component={StackNavigation} />
        </Drawer.Navigator>
    )
}

export default DrawerNavigation