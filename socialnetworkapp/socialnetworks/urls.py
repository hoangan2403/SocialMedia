

from django.urls import path, include
from rest_framework import routers
from socialnetworks import views


router = routers.DefaultRouter()
router.register('posts', views.PostViewSet, basename='posts')
router.register('auctions', views.AuctionViewSet, basename='auctions')
router.register('users', views.UserViewSet, basename='users')
router.register('hashtags', views.HashtagViewSet, basename='hashtags')
router.register('images', views.ImageViewSet, basename='images')
router.register('comments', views.CommentViewSet, basename='comments')
router.register('likes', views.LikeViewSet, basename='likes')
router.register('notices', views.NoticeViewSet, basename='notices')
router.register('emails', views.SendEmailViewSet, basename='emails')
router.register('participateauctions', views.ParticipateAuctionViewSet, basename='participateauctions')
router.register('reports', views.ReportViewSet, basename='reports')
router.register('reportTypes', views.ReportTypeViewSet, basename='reportTypes')

urlpatterns = [
    path('', include(router.urls)),

]
