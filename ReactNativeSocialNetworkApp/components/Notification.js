import React from 'react';
import { StyleSheet, View, Text, TouchableOpacity, Image } from 'react-native';



const Notification = ({ username, message, avatar, timestamp }) => (
    <TouchableOpacity style={styles.notificationItem}>
        <Image source={{ uri: avatar }} style={styles.avatar} />
        <View style={styles.notificationContent}>
            <Text style={styles.username}>{username}</Text>
            <Text>{message}</Text>
            <Text style={styles.timestamp}>{timestamp}</Text>
        </View>
    </TouchableOpacity>
);

export default Notification;
const styles = StyleSheet.create({

    container: {
        flex: 1,
        padding: 10,
    },
    notificationItem: {
        flexDirection: 'row',
        alignItems: 'center',
        borderBottomWidth: 1,
        borderBottomColor: '#ccc',
        paddingVertical: 10,
    },
    avatar: {
        width: 50,
        height: 50,
        borderRadius: 25,
        marginRight: 10,
    },
    notificationContent: {
        flex: 1,
    },
    username: {
        fontWeight: 'bold',
    },
    timestamp: {
        color: 'gray',
        fontSize: 12,
    },


});