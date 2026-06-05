from django.contrib import admin
from .models import Tweet, Like, Retweet, UserProfile

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'created_at', 'like_count', 'retweet_count')
    list_filter = ('created_at',)
    search_fields = ('text', 'user__username')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'tweet', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'tweet__text')


@admin.register(Retweet)
class RetweetAdmin(admin.ModelAdmin):
    list_display = ('user', 'tweet', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'tweet__text')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'created_at')
    search_fields = ('user__username', 'bio')