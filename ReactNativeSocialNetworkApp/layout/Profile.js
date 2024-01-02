import Header from '../components/Header';
import { StyleSheet, View, Text, Image, ScrollView } from 'react-native';

const Profile = ({ navigation }) => (
  <View style={styles.container}>
    <View style={styles.user}>
      <View style={styles.userInfo}>
        <Image source={{ uri: 'https://via.placeholder.com/50' }} style={styles.avatar} />
        <Text style={styles.title}>Thông tin cá nhân</Text>
        <Text style={styles.username}>Phạm Hoàng Ân</Text>
        <Text style={styles.auctionCount}>Đã Đấu Giá: 5</Text>
        {/* Thêm thông tin cá nhân khác của người dùng */}
        <Text style={styles.additionalInfo}>Ngày sinh: 01/01/1990</Text>
        <Text style={styles.additionalInfo}>Email: example@email.com</Text>
        <Text style={styles.additionalInfo}>Địa chỉ: Hà Nội, Việt Nam</Text>
      </View>
      <View style={styles.userStats}>
        <Text style={styles.statText}>Posts: 15</Text>
        <Text style={styles.statText}>Successful Auctions: 13</Text>
        {/* Thêm thông tin thống kê khác của người dùng */}
      </View>
    </View>
    <Header navigation={navigation} />
  </View>
);

export default Profile;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingBottom: 20,
  },
  avatar: {
    width: 50,
    height: 50,
    borderRadius: 25,
    marginRight: 10,
  },
  user: {
    margin: 15,
  },
  userInfo: {
    marginBottom: 20,
  },
  userStats: {
    // Kiểu dáng của phần thống kê người dùng
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  username: {
    fontSize: 16,
    marginBottom: 3,
  },
  auctionCount: {
    marginBottom: 3,
  },
  additionalInfo: {
    marginBottom: 3,
    // Kiểu dáng của thông tin cá nhân khác
  },
  statText: {
    fontSize: 16,
    marginBottom: 5,
    // Kiểu dáng của văn bản thống kê
  },
});
