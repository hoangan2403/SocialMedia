from socialnetworks.models import Category, Product, User, Auction, ParticipateAuction, Post, Report, ReportType, Notice, Hashtag, LikeType, Like, Comments,Images
from rest_framework import serializers


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id', 'name']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class UserSerialzier(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


# Tạo bài viết
class CreatePostSerializer(serializers.ModelSerializer):
    # post_hashtags = HashtagSerializer(many=True, required=False)
    class Meta:
        model = Post
        fields = ['content', 'user']


class PostSerializer(serializers.ModelSerializer):
    post_hashtag = HashtagSerializer(many=True)
    user = UserSerialzier(read_only=True)
    image = ImageSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = '__all__'


class AuctionSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    user_care = UserSerialzier(many = True, read_only=True)
    owner = UserSerialzier(read_only=True)
    buyer = UserSerialzier(read_only=True)

    class Meta:
        model = Auction
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerialzier(read_only=True)
    # post = PostSerializer()
    class Meta:
        model = Comments
        fields = '__all__'


class LikeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeType
        fields = ['id', 'name']


class LikeSerializers(serializers.ModelSerializer):
    user = UserSerialzier(read_only=True)
    liketype = LikeTypeSerializer(read_only=True)
    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        data = validated_data.copy()

        user = User(**data)
        user.set_password(data['password'])
        user.save()

        return user


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'


class ParticipateAuctionSerializer(serializers.ModelSerializer):
    auction = AuctionSerializer(read_only=True)
    user = UserSerialzier(read_only=True)

    class Meta:
        model = ParticipateAuction
        fields = '__all__'


class ReportTypeSerializer(serializers.ModelSerializer):
    report = ReportType()

    class Meta:
        model = ReportType
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    report_type = ReportTypeSerializer(read_only=True)
    class Meta:
        model = Report
        fields = '__all__'








