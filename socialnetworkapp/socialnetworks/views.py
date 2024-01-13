from builtins import int

from django.db.models import Count
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, status, permissions, parsers
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from socialnetworks.models import Post, Auction, User, Hashtag, Images, Comments, Like, LikeType, Notice
from socialnetworks import serializers, paginators, perms
from rest_framework.decorators import action


class PostViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Post.objects.filter(active=True).all().order_by('-created_date')
    serializer_class = serializers.PostSerializer
    # permission_classes = [perms.OwnerAuthenticated]

    # def get_owner(self):
    #     if self.action.__eq__('update_post'):
    #         return [perms.OwnerAuthenticated()]

    # pagination_class = paginators.PostPaginator
    # def get_permissions(self):
    #     if self.action in ('get_serializer_class', 'add_comment', 'like', 'update_post'):
    #         return [permissions.IsAuthenticated()]
    #
    #     return [permissions.AllowAny()]

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
    @action(methods=['POST'], detail=True, name='add_hashtag')
    def add_post_hashtag(self, request, pk):
        post = self.get_object()
        hashtag_list = request.data.get('post_hashtag')
        for hastag in hashtag_list:
            hastag, _ = Hashtag.objects.get_or_create(name=hastag)
            post.post_hashtag.add(hastag)
        post.save()

        return Response(serializers.PostSerializer(post, context={'request': request}).data)

    # cập nhật bài viết
    # @swagger_auto_schema(
    #     operation_description="Update Post",
    #     manual_parameters=[
    #         openapi.Parameter(
    #             name="Authorization",
    #             in_=openapi.IN_HEADER,
    #             type=openapi.TYPE_STRING,
    #             description="Bearer token",
    #             required=False,
    #             default="Bearer your_token_here"
    #         ),
    #         openapi.Parameter(
    #             name="content",
    #             in_=openapi.IN_FORM,
    #             type=openapi.TYPE_STRING,
    #             description="Enter the content",
    #             required=True,
    #         ),
    #     ],
    #     responses={
    #         200: openapi.Response(
    #             description="Successful operation",
    #             examples={
    #                 'application/json': {
    #                     'id': 1,
    #                     'user': 'user',
    #                     'content': 'updated_content',
    #                 }
    #             },
    #         ),
    #         400: "Bad Request. Content is required.",
    #         403: "Forbidden. Authorization token is missing or invalid.",
    #         404: "Not Found. The specified post does not exist.",
    #     }
    # )
    @action(methods=['PUT'], detail=True, url_path='update')
    def update_post(self, request, pk):
        post_instance = self.get_object()  # Lấy instance của Post dựa trên p

        post_instance.content = request.data.get('content', post_instance.content)
        post_instance.save()

        serialized_post = serializers.PostSerializer(post_instance)
        return Response(serialized_post.data, status=status.HTTP_200_OK)

    # Cập nhật hashtag theo bài viết
    @action(methods=['PUT'], detail=True, url_path='update_hashtag')
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

    @action(methods=['GET'], detail=True)
    def get_comments(self, request, pk):
        comments = self.get_object().comments_set.all().order_by('-created_date')

        # import pdb
        # pdb.set_trace()

        return Response(serializers.CommentSerializer(comments, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    # add comment
    @action(methods=['POST'], detail=True)
    def add_comment(self, request, pk):
        user = request.user
        post = self.get_object()
        content = request.data.get('content')
        if user != post.user:
            if content:
                c = Comments.objects.create(user=user, post=post, content=content)

                content = f"{request.user.username} đã bình luận bài viết của bạn "
                n = Notice.objects.create(content=content, post=post)
                n.save()

                return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)
            else:
                return Response("Content is required.", status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=True)
    def get_likes(self, request, pk):
        likes = self.get_object().like_set.all()
        return Response(serializers.LikeSerializers(likes, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    # add like
    @action(methods=['POST'], url_path='like', detail=True)
    def like(self, request, pk):
        like_type = int(request.data.get('liketype_id'))
        user = request.user
        post = self.get_object()

        try:
            like_type_instance = LikeType.objects.get(pk=like_type)
        except LikeType.DoesNotExist:
            return Response("Invalid LikeType ID", status=status.HTTP_400_BAD_REQUEST)
        # breakpoint()
        # like = Like.objects.filter(user=user, post=post)
        if user != post.user:
                like, created = Like.objects.get_or_create(user=user, post=post)
                if created:
                    content = f"{request.user.username} đã bày tỏ bài viết của bạn"
                    n = Notice.objects.create(content=content, post=post)
                    n.save()
                    like.like_type = like_type_instance
                    like.save()
                    return Response("Like", status=status.HTTP_201_CREATED)
                else:
                    if like_type_instance == like.like_type:
                        like.delete()
                        return Response("Un Like", status=status.HTTP_204_NO_CONTENT)
                        # breakpoint()
                    else:
                        like.like_type = like_type_instance
                        like.save()
                        return Response("Like", status=status.HTTP_200_OK)
                        # breakpoint()
        return Response("User Of Post ", status=status.HTTP_400_BAD_REQUEST)

    # Lấy hình ảnh theo bài post
    @action(methods=['GET'], url_path='get_images', detail=True)
    def get_post_images(self, request, pk):
        imgs = self.get_object().images_set.all()
        return Response(serializers.ImageSerializer(imgs, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    # Lấy hết của bài post
    @action(methods=['GET'], url_path='get_all_in_post', detail=False)
    def get_all_attribute_in_post(self, request):
        posts = Post.objects.all()
        serialized_posts = []
        for post in posts:
            images = post.images_set.all()  # Sử dụng related name "images" để lấy tất cả hình ảnh của bài viết

            post_serializer = serializers.PostSerializer(post)
            image_serializer = serializers.ImageSerializer(images, many=True)

            # Thêm trường images vào dữ liệu serialized của bài viết
            post_data = post_serializer.data
            post_data['images'] = image_serializer.data

            serialized_posts.append(post_data)

        return Response(serialized_posts, status=status.HTTP_200_OK)

    # Số lượng like của bài viết
    @action(methods=['GET'], detail=True, url_path='count_like')
    def count_like_of_post(self,request,pk):
        post = self.get_object()
        count_like = post.like_set.aggregate(count=Count("id"))
        return Response(count_like, status=status.HTTP_200_OK)

    # Số lượng comment của bài viết
    @action(methods=['GET'], detail=True, url_path="count_comment")
    def count_comment_of_post(self, request,pk):
        post = self.get_object()
        count_comment = post.comments_set.aggregate(count=Count("id"))
        return Response(count_comment, status=status.HTTP_200_OK)


class AuctionViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Auction.objects.all()
    serializer_class = serializers.AuctionSerializer
    # pagination_class = paginators.PostPaginator


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = serializers.UserSerialzier
    permission_classes = [perms.OwnerAuthenticated]
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
    # permission_classes = [perms.OwnerAuthenticated]


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
    @action(methods=['POST'], url_name='add-images-for-post', detail=False)
    def add_images_for_post(self, request):
        # user = request.user
        new_images = request.FILES.getlist('image')
        post_id = int(request.data.get('post'))

        if not new_images:
            return Response("Image is required.", status=status.HTTP_400_BAD_REQUEST)

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response("Post does not exist.", status=status.HTTP_400_BAD_REQUEST)

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

    @action(methods=['PUT'], detail=False)
    def update_image(self, request):
        # if request.user.is_authenticated and perms.OwnerAuth:
        imgs_file = request.FILES.getlist('img_file')
        imgs_id = request.data.getlist('img_id')
        post_id = int(request.data.get('post'))

        images = []
        for img_id, img_file in zip(imgs_id, imgs_file):
            image = Images.objects.get(pk=img_id, post=post_id)
            # breakpoint()
            if img_file:
                image.image = img_file
                image.save()
                images.append(image)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.ImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Comments.objects.all()
    serializer_class = serializers.CommentSerializer
    # permission_classes = [perms.OwnerAuthenticated]

    @action(methods=['PATCH'], detail=True)
    def update_comments(self, request, pk):
        content = request.data.get('content')
        comment = self.get_object()

        try:
            comments = Comments.objects.get(pk=comment.id)
        except Post.DoesNotExist:
            return Response("Post does not exist.", status=status.HTTP_400_BAD_REQUEST)

        if content:
            comments.content = content
            comments.save()
            serializer = serializers.CommentSerializer(comments)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True)
    def add_reply(self, request, pk):
        comment = self.get_object()
        content = request.data.get('content')
        user = request.user

        comments = Comments.objects.get(pk=comment.id)

        if content:
            c = Comments.objects.create(content=content, post=comments.post, user=user, comment=comments)
            c.save()
            serializer = serializers.CommentSerializer(c)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=True)
    def get_reply(self, request, pk):
        comment = self.get_object()

        c = Comments.objects.filter(comment=comment.id)
        # breakpoint()

        return Response(serializers.CommentSerializer(c, many=True, context={'request': request}).data, status=status.HTTP_200_OK)


class LikeViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Like.objects.all()
    serializer_class = serializers.LikeSerializers
    # permission_classes = [perms.OwnerAuthenticated]


class NoticeViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Notice.objects.all()
    serializer_class = serializers.NoticeSerializer

    # lấy thông báo theo user so huu bai viet
    @action(methods=['GET'], url_path='get_notice', detail=False)
    def get_notice_of_user(self, request):
        user = request.user
        posts = Post.objects.filter(user=user)
        notices = Notice.objects.filter(post__in=posts)

        serializer = serializers.NoticeSerializer(notices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



