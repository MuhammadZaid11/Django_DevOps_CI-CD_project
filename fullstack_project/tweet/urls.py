from . import views
from django.urls import path

urlpatterns = [
    # Auth URLs
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Home & Profile URLs
    path('', views.index, name='index'),
    path('feed/', views.tweet_list, name='tweet_list'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    # Tweet URLs
    path('create/', views.tweet_create, name='tweet_create'),
    path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
    path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),
    
    # Like/Retweet URLs
    path('<int:tweet_id>/like/', views.like_tweet, name='like_tweet'),
    path('<int:tweet_id>/retweet/', views.retweet_tweet, name='retweet_tweet'),
    
    # Follow URLs
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
]
