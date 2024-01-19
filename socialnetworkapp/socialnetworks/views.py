import datetime
from builtins import int

from django.core import mail
from django.db.models import Count
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, status, permissions, parsers
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from socialnetworks.models import (Post, Auction, User, Hashtag, Images,
                                   Comments, Like, LikeType, Notice, Product, Category, ParticipateAuction, Report, ReportType)
from socialnetworks import serializers, paginators, perms
from rest_framework.decorators import action


class SendEmailViewSet(viewsets.ViewSet):
    def create(self, request):
        auction_id = request.data.get("id_auction")
        buyer_id = request.data.get("id_buyer")

        try:
            auction = Auction.objects.get(pk=auction_id, buyer=buyer_id)
        except Auction.DoesNotExist:
            return Response({'message': 'Auction not found.'}, status=status.HTTP_404_NOT_FOUND)

        buyer_username = auction.buyer.username
        buyer_email = auction.buyer.email
        user_of_username = auction.owner.username
        date_of_payment = auction.date_of_payment
        link_thanhtoan = 'nhap'  # Replace with your actual link
        tieude_baiviet = 'nhap'  # Replace with your actual title

        subject = f"{buyer_username} có tin mới !!!"
        ten_nguoi_gui = buyer_username

        html_content = f"""
                    <p>Xin chào {ten_nguoi_gui},</p>
                    <p>Chúng tôi xin thông báo rằng bạn đã chiến thắng cuộc đấu giá. Chúng tôi xin chúc mừng bạn.</p>
                    <p>Hãy truy cập vào <a href="{link_thanhtoan}">{tieude_baiviet}</a> để thanh toán sản phẩm.</p>
                    <p>Xin chân thành cảm ơn và hy vọng bạn thanh toán cho chúng tôi trước ngày {date_of_payment}.</p>
                    <p>Chúc bạn một ngày tốt lành!</p>
                """

        from_email = "vphan2270@gmail.com"
        to = [buyer_email]

        try:
            with mail.get_connection() as connection:
                msg = mail.EmailMessage(subject, html_content, from_email, to, connection=connection)
                msg.content_subtype = "html"
                success_count = msg.send()

            if success_count == 1:
                return Response({'message': 'Email sent successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Failed to send email.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'message': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Post.objects.filter(active=True).all().order_by('-created_date')
    serializer_class = serializers.PostSerializer
    # parser_classes = [parsers.MultiPartParser]
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

    @action(methods=['GET'], detail=True)
    def get_by_id(self, request, pk):
        post = self.get_object()

        get_post = Post.objects.get(pk=post.id)

        serializer_post = serializers.PostSerializer(get_post)

        get_image = Images.objects.filter(post=post)
        serializer_img = serializers.ImageSerializer(get_image, many=True)

        response_data = {
            'post': serializer_post.data,
            'images': serializer_img.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)



    # Đăng bài viêt
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreatePostSerializer

        return self.serializer_class

    @action(methods=['POST'], detail=False, url_path='create')
    def add_post(self, request):
        user = request.user
        content = request.data.get('content')
        images = request.FILES.getlist('image')
        hashtags = request.data.getlist('name_hashtag')


        image_data = []

        post, created = Post.objects.get_or_create(content=content, user=user)

        if created:
            for image in images:
                cloudinary_base_url = "https://res.cloudinary.com/dhcvsbuew/"
                full_cloudinary_url = f"{cloudinary_base_url}{image}"
                new_image = Images.objects.create(image=full_cloudinary_url, post=post)
                serializer_img = serializers.ImageSerializer(new_image)
                image_data.append(serializer_img.data)

            for hashtag in hashtags:
                new_hashtag, _ = Hashtag.objects.get_or_create(name=hashtag)
                post.post_hashtag.add(new_hashtag)

            post.save()
            serializer_post = serializers.PostSerializer(post)

            response_data = {
                'post': serializer_post.data,
                'images': image_data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Post not created'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False, url_path='add_hashtag')
    def add_post_hashtag(self, request, pk):
        post = self.get_object()
        hashtag_list = request.data.getlist('name')
        for hastag in hashtag_list:
            get_hastag, _ = Hashtag.objects.get_or_create(name=hastag)
            post.post_hashtag.add(get_hastag)
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

    @action(methods=['GET'], detail=False)
    def get_post_by_user(self, request):
        user = request.user
        posts = Post.objects.filter(user=user).all()
        data = []
        # breakpoint()
        for post in posts:
            imgs = Images.objects.filter(post=post).all()
            response_data = {
                'post': serializers.PostSerializer(post).data,
                'image': serializers.ImageSerializer(imgs, many=True).data,
            }

            data.append(response_data)
        return Response(data, status=status.HTTP_200_OK)


class AuctionViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Auction.objects.all()
    serializer_class = serializers.AuctionSerializer
    parser_classes = [parsers.MultiPartParser]
    # pagination_class = paginators.PostPaginator

    @action(methods=['GET'], detail=False)
    def get_auction_by_user(self, request):
        user = request.user

        auction = Auction.objects.filter(owner=user)
        # content = f"{request.user.username} đã bày tỏ bài viết của bạn"
        # n = Notice.objects.create(content=content, post=post)
        # n.save()
        serializer = serializers.PostSerializer(auction, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, url_path='create')
    def add_auction(self, request):
        user = request.user
        content = request.data.get('content')
        starting_price = request.data.get('starting_price')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        date_of_payment = request.data.get('date_of_payment')

        name = request.data.get('name_product')
        description = request.data.get('description_product')
        image = request.FILES.get('image_product')
        category = int(request.data.get('category'))
        cloudinary_base_url = "https://res.cloudinary.com/dhcvsbuew/"
        full_cloudinary_url = f"{cloudinary_base_url}{image}"

        auction, created = Auction.objects.get_or_create(owner=user, content=content, starting_price=starting_price,
                                                         start_date=start_date, end_date=end_date, date_of_payment=date_of_payment)
        # breakpoint()
        if created:
            category_id = Category.objects.get(pk=category)
            new_product = Product.objects.create(name=name, description=description, image=full_cloudinary_url, category=category_id)
            serializer_product = serializers.ProductSerializer(new_product)

            auction.product = new_product
            auction.save()

            serializer_auction = serializers.AuctionSerializer(auction)

            response_data = {
                'auction': serializer_auction.data,
                'product': serializer_product.data,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response('Auction not created', status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True)
    def update_auction(self, request, pk):
        auction = self.get_object()
        user = request.user
        content = request.data.get('content')
        starting_price = request.data.get('starting_price')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        date_of_payment = request.data.get('date_of_payment')

        name = request.data.get('name_product')
        description = request.data.get('description_product')
        image = request.FILES.get('image_product')
        category = int(request.data.get('category'))

        auctions = Auction.objects.get(pk=auction.id)
        if content:
            auctions.content = content
            auctions.save()
        if starting_price:
            auctions.starting_price = starting_price
            auctions.save()
        if start_date:
            auctions.start_date = start_date
            auctions.save()
        if end_date:
            auctions.end_date = end_date
            auctions.save()
        if date_of_payment:
            auctions.date_of_payment = date_of_payment
            auctions.save()
        if name:
            auctions.product.name = name
            auctions.product.save()
        if description:
            auctions.product.description = name
            auctions.product.save()
        if image:
            auctions.product.image = image
            auctions.product.save()
        if category:
            categorys = Category.objects.get(pk=category)
            auctions.product.category = categorys
            auctions.product.save()

        return Response(serializers.AuctionSerializer(auctions).data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=True, url_path="")
    def get_by_id(self, request, pk):
        auction = self.get_object()

        get_auction = Auction.objects.get(pk=auction.id)
        return Response(serializers.AuctionSerializer(get_auction).data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def add_participateauction(self, request, pk):
        auction = self.get_object()
        user = request.user
        price = request.data.get('price')
        date = datetime.datetime.now()
        # breakpoint()
        day = date.strftime("%Y-%m-%d")

        if day > str(auction.end_date):
            return Response('Auction has already ended', status=status.HTTP_400_BAD_REQUEST)
        else:
            participateauction = ParticipateAuction.objects.create(user=user, auction=auction, price=price)

            serializer = serializers.ParticipateAuctionSerializer(participateauction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=True)
    def get_participateauction(self, request, pk):
        participateauction = self.get_object().participateauction_set.all().order_by('-price')

        return Response(serializers.ParticipateAuctionSerializer(participateauction, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['PATCH'], detail=True)
    def add_buyer(self, request, pk):
        auction = self.get_object()
        buyer = request.user

        get_auction = Auction.objects.get(pk=auction.id)

        if get_auction.owner != buyer:
            get_auction.buyer = buyer
            get_auction.save()
            serializer = serializers.AuctionSerializer(get_auction)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("Buyer of auction", status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=True)
    def count_participateauction(self, request, pk):
        auction = self.get_object().participateauction_set.all()

        return Response({'count': auction.count()}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def report(self, request, pk):
        auction = self.get_object()
        r = int(request.data.get('report_type'))
        user = request.user

        if auction:
            a = Auction.objects.get(pk=auction.id)
        else:
            return Response("Auction is not", status=status.HTTP_404_NOT_FOUND)

        report = ReportType.objects.get(pk=r)

        created = Report.objects.create(user=user, auction=a, report_type=report)

        serializer = serializers.ReportSerializer(created)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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

    @action(methods=['GET'], detail=True)
    def get_post_by_hashtag(self, request, pk):
        hashtag = self.get_object()

        if hashtag:
            post = Post.objects.filter(post_hashtag=hashtag.id)

        return Response(serializers.PostSerializer(post, many=True).data, status=status.HTTP_200_OK)


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

        if not user.is_authenticated:
            return Response("Anonymous comments are not allowed.", status=status.HTTP_400_BAD_REQUEST)

        comments = Comments.objects.get(pk=comment.id)
        # breakpoint()

        if content:
            c = Comments.objects.create(content=content, post=comments.post, user=user, comment=comments)
            c.save()
            serializer_comment = serializers.CommentSerializer(c)
            if c:
                content = f"{request.user.username} đã nhắc đến bạn"
                n = Notice.objects.create(content=content, post=comment.post)
                n.save()
                serializer_notice = serializers.NoticeSerializer(n)

            response_data = {
                'comment': serializer_comment.data,
                'notice': serializer_notice.data,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
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
    @swagger_auto_schema(
        operation_description="Push Images House",
        manual_parameters=[
                              openapi.Parameter(
                                  name="Authorization",
                                  in_=openapi.IN_HEADER,
                                  type=openapi.TYPE_STRING,
                                  description="Bearer token",
                                  required=True,
                                  default="Bearer your_token_here"
                              ),
            ],
        responses={
            200: openapi.Response(
                description="Successful operation",
                # schema=serializers.UserSerializer
            )
        }
    )
    @action(methods=['GET'], url_path='get_notice', detail=False)
    def get_notice_of_user(self, request):
        user = request.user
        posts = Post.objects.filter(user=user)
        notices = Notice.objects.filter(post__in=posts).order_by('-created_date')

        serializer = serializers.NoticeSerializer(notices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Push Images House",
        manual_parameters=[
                              openapi.Parameter(
                                  name="Authorization",
                                  in_=openapi.IN_HEADER,
                                  type=openapi.TYPE_STRING,
                                  description="Bearer token",
                                  required=True,
                                  default="Bearer your_token_here"
                              ),
            ],
        responses={
            200: openapi.Response(
                description="Successful operation",
                # schema=serializers.UserSerializer
            )
        }
    )
    @action(methods=['GET'], detail=False)
    def count_notice_by_user(self, request):
        user = request.user

        # breakpoint()
        notices = Notice.objects.filter(post__user=user, active=True)

        # serializer_data = serializers.NoticeSerializer(notices, many=True,  context={'request': request}).data
        # response_data = {
        #     'notices': serializer_data,
        #     'count': notices.count(),
        # }
        return Response({'count': notices.count()}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Push Images House",
        manual_parameters=[
            openapi.Parameter(
                name="pk",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Id notice",
                required=False,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Successful operation",
                # schema=serializers.UserSerializer
            )
        }
    )
    @action(methods=['POST'], detail=True)
    def set_active(self, request, pk):
        notice = self.get_object()

        notice.active = False
        notice.save()

        serializer = serializers.NoticeSerializer(notice)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ParticipateAuctionViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = ParticipateAuction.objects.all()
    serializer_class = serializers.ParticipateAuction

    @action(methods=['POST'], detail=True)
    def update_participateauction(self, request, pk):
        p = self.get_object()
        price = request.data.get('price')

        participateauction = ParticipateAuction.objects.get(pk=p.id)
        # breakpoint()
        if price:
            participateauction.price = price
            participateauction.save()

        return Response(serializers.ParticipateAuctionSerializer(participateauction).data, status=status.HTTP_200_OK)


class ReportViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Report.objects.all()
    serializer_class = serializers.ReportSerializer


class ReportTypeViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = ReportType.objects.all()
    serializer_class = serializers.ReportTypeSerializer






