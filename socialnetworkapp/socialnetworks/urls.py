

from django.urls import path, include
from rest_framework import routers
from socialnetworks import views


router = routers.DefaultRouter()
router.register('posts', views.PostViewSet, basename='posts')
router.register('auctions', views.AuctionViewSet, basename='auctions')
router.register('users', views.UserViewSet, basename='users')
router.register('hashtags', views.HashtagViewSet, basename='hashtags')
router.register('images', views.ImageViewSet, basename='images')


urlpatterns = [
    path('', include(router.urls)),

]
