from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Tweet, Like, Retweet, UserProfile
from .forms import TweetForm, UserRegistrationForm, UserProfileForm


# Auth Views
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('tweet_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# Home & Profile Views
def index(request):
    return redirect('tweet_list') if request.user.is_authenticated else redirect('login')


@login_required(login_url='login')
def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    context = {
        'tweets': tweets,
    }
    return render(request, 'tweet_list.html', context)


@login_required(login_url='login')
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    user_tweets = user.tweets.all()
    is_following = request.user in profile.followers.all() if request.user.is_authenticated else False
    
    context = {
        'profile_user': user,
        'user_profile': profile,
        'user_tweets': user_tweets,
        'is_following': is_following,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})


# Tweet Views
@login_required(login_url='login')
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})


@login_required(login_url='login')
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form, 'tweet': tweet})


@login_required(login_url='login')
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})


# Like/Unlike Views
@login_required(login_url='login')
@require_POST
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'like_count': tweet.like_count()
        })
    return redirect('tweet_list')


# Retweet/Unretweet Views
@login_required(login_url='login')
@require_POST
def retweet_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    
    if tweet.user == request.user:
        return JsonResponse({'error': 'Cannot retweet your own tweet'}, status=400)
    
    retweet, created = Retweet.objects.get_or_create(user=request.user, tweet=tweet)
    
    if not created:
        retweet.delete()
        retweeted = False
    else:
        retweeted = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'retweeted': retweeted,
            'retweet_count': tweet.retweet_count()
        })
    return redirect('tweet_list')


# Follow/Unfollow Views
@login_required(login_url='login')
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    profile = user_to_follow.profile
    
    if request.user == user_to_follow:
        return redirect('profile', username=username)
    
    if request.user in profile.followers.all():
        profile.followers.remove(request.user)
    else:
        profile.followers.add(request.user)
    
    return redirect('profile', username=username)