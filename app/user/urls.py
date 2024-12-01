"""
URL mappings for the user API
"""
from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('users/', views.ListUsersView.as_view(), name='list-users'),
    path('follow/', views.FollowUserView.as_view(), name='follow-user'),
    path('unfollow/', views.UnFollowUserView.as_view(), name='unfollow-user'),
    path('followers/', views.FollowersListView.as_view(), name='followers-list'),
    path('following/', views.FollowingListView.as_view(), name='following-list'),
]
