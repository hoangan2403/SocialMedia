
import React from 'react';
import { StyleSheet, View, Text, TouchableOpacity } from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome';

const Header = ( { navigation } ) => (
    <View style={styles.bottomNavigation}>
        <TouchableOpacity style={styles.navItem}
         onPress={() => navigation.navigate('Home')}>
          <Icon name="home" size={25} color="black" /> 
          <Text>Home</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.navItem} onPress={() => navigation.navigate('HomeAuction')}>
          <Icon name="gavel" size={25} color="black" /> 
          <Text>Đấu Giá</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.navItem} onPress={() => navigation.navigate('HomeNotification')}>
          <Icon name="bell" size={25} color="black" /> 
          <Text>Notifications</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.navItem}>
          <Icon name="envelope" size={25} color="black" /> 
          <Text>Messages</Text>
          
        </TouchableOpacity>
        <TouchableOpacity style={styles.navItem} onPress={() => navigation.navigate('Profile')}>
          <Icon name="user" size={25} color="black" /> 
          <Text>Profile</Text>

        </TouchableOpacity>
      </View>
);
export default Header;

const styles = StyleSheet.create({
    
    bottomNavigation: {
      flexDirection: 'row',
      justifyContent: 'space-around',
      alignItems: 'center',
      backgroundColor: '#f0f0f0',
      paddingVertical: 10,
      position: 'absolute',
      bottom: 0,
    },
    navItem: {
      flex: 1,
      alignItems: 'center',
    },
  });