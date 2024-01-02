import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { StyleSheet, View, ScrollView, TextInput } from 'react-native';
import Auction from '../components/Auction';
import Header from '../components/Header';

const HomeAuction = ( { navigation } ) => (
    <View style={styles.container}>
      <StatusBar style="auto" />
      <View style={styles.searchBar}>
        
        <TextInput
          style={styles.searchInput}
          placeholder="Search..."
          placeholderTextColor="#888"

        />
      </View>
      <ScrollView>
        <Auction
          username="John Doe"
          content="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
          image="https://via.placeholder.com/300"
        />
        
      </ScrollView>
      <Header navigation={navigation}/>
    </View>
  );
  export default HomeAuction;

  const styles = StyleSheet.create({
    container: {
      marginTop: 40,
      flex: 1,
      backgroundColor: '#fff',
    },
    searchBar: {
      padding: 10,
      backgroundColor: '#eee',
      borderBottomWidth: 1,
      borderBottomColor: '#ccc',
    },
    searchInput: {
      backgroundColor: '#fff',
      paddingHorizontal: 10,
      paddingVertical: 8,
      borderRadius: 5,
    },
    
  });