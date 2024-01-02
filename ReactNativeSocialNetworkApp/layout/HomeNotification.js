import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { StyleSheet, View, ScrollView, TextInput } from 'react-native';
import Header from '../components/Header';
import Notification from '../components/Notification';
import Icon from 'react-native-vector-icons/FontAwesome';

const HomeNotification = ( { navigation } ) => (
    <View style={styles.container}>
      <StatusBar style="auto" />
      <View style={styles.searchBar}>
        
        <TextInput
          style={styles.searchInput}
          placeholder="Search..."
          placeholderTextColor="#888"
        />
        <Icon name="cog" size={30} color="black" />
      </View>
      <ScrollView>
        <Notification
          username= 'John Doe'
          message= 'You have a new friend request.'
          avatar= 'https://via.placeholder.com/50'
          timestamp= '2 hours ago'
        />
        <Notification
          username= 'John Doe'
          message= 'You have a new friend request.'
          avatar= 'https://via.placeholder.com/50'
          timestamp= '2 hours ago'
        />
        <Notification
          username= 'John Doe'
          message= 'You have a new friend request.'
          avatar= 'https://via.placeholder.com/50'
          timestamp= '2 hours ago'
        />
        
      </ScrollView>
      <Header navigation={navigation}/>
    </View>
  );
  export default HomeNotification;

  const styles = StyleSheet.create({
    container: {
      marginTop: 40,
      flex: 1,
      backgroundColor: '#fff',
    },
    searchBar: {
        flexDirection: 'row', // Hiển thị các thành phần theo chiều ngang
        alignItems: 'center', // Căn chỉnh các thành phần theo trục dọc
        justifyContent: 'space-between', // Căn chỉnh các thành phần theo chiều ngang, khoảng cách đều
        paddingHorizontal: 10, // Khoảng cách lề ngang
        borderWidth: 1,
        borderColor: '#ccc',
        borderRadius: 5,
        height: 40,
      },
      searchInput: {
        flex: 8, // Chiếm 80% chiều rộng của parent (searchBar)
        paddingHorizontal: 8,
        fontSize: 16,
        color: 'black',
      },
    
  });