
import React from 'react';
import { StyleSheet, View, Text, Image, TouchableOpacity } from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome';

const Post = ({ username, content, image }) => (
    <View style={styles.postContainer}>
      <View style={styles.userInfo}>
        <Image source={{ uri: 'https://via.placeholder.com/50' }} style={styles.avatar} />
        <Text style={styles.username}>{username}</Text>
      </View>
      <Text style={styles.content}>{content}</Text>
      <Image source={{ uri: image }} style={styles.postImage} />
      <View style={styles.actions}>
        <TouchableOpacity style={styles.actionButton}>
          <Icon name="thumbs-o-up" size={20} color="blue" />
          <Text style={styles.actionText}>Like</Text>
        </TouchableOpacity>
  
        <TouchableOpacity style={styles.actionButton}>
          <Icon name="comment-o" size={20} color="green" />
          <Text style={styles.actionText}>Comment</Text>
        </TouchableOpacity>
  
        <TouchableOpacity style={styles.actionButton}>
          <Icon name="share-square-o" size={20} color="orange" />
          <Text style={styles.actionText}>Share</Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  export default Post;
  const styles = StyleSheet.create({
    
    postContainer: {
      padding: 10,
      borderBottomWidth: 1,
      borderBottomColor: '#ccc',
    },
    userInfo: {
      flexDirection: 'row',
      alignItems: 'center',
      marginBottom: 5,
    },
    avatar: {
      width: 50,
      height: 50,
      borderRadius: 25,
      marginRight: 10,
    },
    username: {
      fontWeight: 'bold',
    },
    content: {
      marginBottom: 10,
    },
    postImage: {
      width: '100%',
      height: 200,
      resizeMode: 'cover',
      marginBottom: 10,
    },
    actions: {
      flexDirection: 'row',
      justifyContent: 'space-around',
      alignItems: 'center',
      marginTop: 10,
    },
    actionButton: {
      flexDirection: 'row',
      alignItems: 'center',
    },
    actionText: {
      marginLeft: 5,
    },
   
    
  });