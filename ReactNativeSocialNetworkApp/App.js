import React from 'react';
import Home from './layout/Home';
import Profile from './layout/Profile';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import HomeAuction from './layout/HomeAuction';
import HomeNotification from './layout/HomeNotification';
import Login from './layout/Login';

const Stack = createStackNavigator();


export default function SocialApp() {
  return (
    <NavigationContainer>
      <Stack.Navigator >
        <Stack.Screen name="Login" component={Login} />
        <Stack.Screen name="Home" component={Home} />
        <Stack.Screen name="Profile" component={Profile} />
        <Stack.Screen name="HomeAuction" component={HomeAuction} />
        <Stack.Screen name="HomeNotification" component={HomeNotification} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

