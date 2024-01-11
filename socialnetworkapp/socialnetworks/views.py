from builtins import int

from django.db.models import Count
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, status, permissions, parsers
from rest_framework.response import Response

from socialnetworks.models import Post, Auction, User, Hashtag, Images
from socialnetworks import serializers, paginators, perms
from rest_framework.decorators import action


class PostViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Post.objects.filter(active=True).all().order_by('-created_date')
    serializer_class = serializers.PostSerializer
    # permission_classes = [perms.OwnerAuthenticated]

    # pagination_class = paginators.PostPaginator

    def get_queryset(self):
        queries = self.queryset

        q = self.request.query_params.get("q")
        if q:
            queries = queries.filter(post_hashtag__name__exact=q)

        return queries

    # Đăng bài viêt
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreatePostSerializer

        return self.serializer_class

    # add hashtag vào bài viết
    @action(methods=['POST'], detail=True, name='add_post_hashtag')
    def add_post_hashtag(self, request, pk):
        post = self.get_object()
        hashtag_list = request.data.get('post_hashtag')
        for hastag in hashtag_list:
            hastag, _ = Hashtag.objects.get_or_create(name=hastag)
            post.post_hashtag.add(hastag)
        post.save()

        return Response(serializers.PostSerializer(post, context={'request': request}).data)

    # cập nhật bài viết
    @action(methods=['POST'], detail=True, url_path='update')
    def update_post(self, request, pk):
        post_instance = self.get_object()  # Lấy instance của Post dựa trên pk

        # Cập nhật thông tin của bài viết từ dữ liệu mới
        post_instance.content = request.data.get('content', post_instance.content)
        post_instance.image = request.data.get('image', post_instance.image)
        # post_instance.post_hashtag = request.data.get('post_hashtag', post_instance.post_hashtag)
        # Bạn cần điều chỉnh các trường khác tương tự cho Post

        # Lưu các thay đổi vào bài viết
        post_instance.save()

        # Serialize bài viết đã được cập nhật và trả về response
        serialized_post = serializers.PostSerializer(post_instance)
        return Response(serialized_post.data, status=status.HTTP_200_OK)

    # Cập nhật hashtag theo bài viết
    @action(methods=['POST'], detail=True, url_path='update_hashtag')
    def update_post_hashtag(self, request, pk):
        post = self.get_object()
        hashtag_name = request.data.getlist('hashtag_name')
        hashtag_id = request.data.getlist('hashtag_id')

        for h, h_name in zip(hashtag_id, hashtag_name):
            try:
                hashtag = Hashtag.objects.get(pk=h, post=post)
            except Hashtag.DoesNotExist:
                return Response({"error": "Hashtag không tồn tại cho bài viết này"}, status=status.HTTP_404_NOT_FOUND)

            related_posts_count = hashtag.post_set.count()

            if related_posts_count > 1:
                post.post_hashtag.remove(hashtag)
                new_hashtag, _ = Hashtag.objects.get_or_create(name=h_name)
                post.post_hashtag.add(new_hashtag)
            else:
                hashtag.name = h_name
                hashtag.save()

        return Response({"message": "Cập nhật tên hashtag thành công"}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def comments(self, request, pk):
        comments = self.get_object().comments_set.all().order_by('-created_date')

        # import pdb
        # pdb.set_trace()

        return Response(serializers.CommentSerializer(comments, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def likes(self, request, pk):
        likes = self.get_object().like_set.all()
        return Response(serializers.LikeSerializers(likes, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)


class AuctionViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Auction.objects.all();
    serializer_class = serializers.AuctionSerializer
    # pagination_class = paginators.PostPaginator


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = serializers.UserSerialzier
    parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.action.__eq__('current_user'):
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_name='current-user', detail=False)
    def current_user(self, request):
        return Response(serializers.UserSerialzier(request.user).data)


class HashtagViewSet(viewsets.ViewSet, generics.ListAPIView, generics.UpdateAPIView):
    queryset = Hashtag.objects.all()
    serializer_class = serializers.HashtagSerializer


class ImageViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Images.objects.all()
    serializer_class = serializers.ImageSerializer
    parser_classes = [parsers.MultiPartParser]

    @swagger_auto_schema(
        operation_description="Push Images House",
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token",
                required=False,
                default="Bearer your_token_here"
            ),
            openapi.Parameter(
                name="image",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="Enter the image",
                required=True,
            ),
            openapi.Parameter(
                name="post",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_NUMBER,
                description="post_id",
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="Successful operation",
                # schema=serializers.UserSerializer
            )
        }
    )
    @action(methods=['post'], url_name='push-images-for-post', detail=False)
    def push_images_for_post(self, request):
        # user = request.user
        new_images = request.FILES.getlist('image')
        post_id = int(request.data.get('post'))

        if not new_images:
            return Response("Image is required.", status=status.HTTP_400_BAD_REQUEST)

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response("House does not exist.", status=status.HTTP_400_BAD_REQUEST)

        # self.serializer_class().push_images_for_house(house_id, new_image)
        check =False
        for image in new_images:
            img = Images.objects.create(post=post, image=image)
            img.save()
            check=True

        if check == True:
            return Response("Images for house created successfully.", status=status.HTTP_200_OK)
        else:
            return Response('Loi roi', status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['PATCH'], detail=False)
    def update_image(self, request):
        # if request.user.is_authenticated and perms.OwnerAuth:
        imgs_file = request.FILES.getlist('image')
        imgs_id = request.data.getlist('img_id')
        post_id = int(request.data.get('post'))

        for img_id, img_file in zip(imgs_id, imgs_file):
            image = Images.objects.get(pk=img_id, post=post_id)
            # breakpoint()
            if img_file:
                image.image = img_file
                image.save()
                serializer = serializers.ImageSerializer(image)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

