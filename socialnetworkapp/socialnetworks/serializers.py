from socialnetworks.models import Category, Product, User, Auction, ParticipateAuction, Post, Report, ReportType, Notice, Hashtag, LikeType, Like, Comments,Images
from rest_framework import serializers


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id', 'name']


# Tạo bài viết
class CreatePostSerializer(serializers.ModelSerializer):
    # post_hashtags = HashtagSerializer(many=True, required=False)
    class Meta:
        model = Post
        fields = ['content', 'user', 'post_hashtag']


class PostSerializer(serializers.ModelSerializer):
    post_hashtag = HashtagSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class UserSerialzier(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()

        user = User(**data)
        user.set_password(data['password'])
        user.save()

        return user


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'
