# social_network/views.py
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.shortcuts import redirect
from django.middleware import csrf
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import datetime
import logging
import re
from django.db.models import Q
import random
from django.contrib.auth.models import User
from django.http import Http404
from .models import Post , Comment , Mention
from .forms import PostForm , FollowForm , CommentForm
from django.db.models import F
from django.contrib import messages
from .models import User
from datetime import datetime
from django.http import HttpResponseServerError
from django.utils import timezone
from django.utils.html import escape
from django.utils.safestring import mark_safe

@login_required
def index(request):
    show_signup_content = not request.user.is_authenticated

    # Get the posts by the user and the users they follow
    user = request.user
    following = user.following.all()
    posts = Post.objects.filter(Q(author=user) | Q(author__in=following)).order_by('-created')
    form = PostForm()  # Include the form for creating a new post

    if request.method == "POST":
        # Handle user signup
        # ...

        show_signup_content = False  # After signup, don't show signup content

    return render(request, 'social_network/index.html', {'form': form,'show_signup_content': show_signup_content, 'posts': posts})


def find_mentions(text):
    # Use a regular expression to find all mentions in the text
    # Mentions typically start with "@" followed by the username
    mention_pattern = r"(@\w+)"

    # Find all matches in the text
    mentions = re.findall(mention_pattern, text)
    
    # Extract usernames by removing the "@" symbol
    usernames = [mention[1:] for mention in mentions]
    
    # Get the User objects for the mentioned usernames
    mentioned_users = []
    for username in usernames:
        username = username.strip()  # Remove leading/trailing spaces
        try:
            user = User.objects.get(username=username)
            mentioned_users.append(user)
        except User.DoesNotExist:
            # Handle the case where the user with the mentioned username does not exist
            pass

    print("Mentioned users:", mentioned_users)  # Debug: Print mentioned users

    return mentioned_users






@login_required
def my_profile(request):
    if request.method == "POST":
        # Get the current user
        user = request.user

        # Update the user fields based on form input, but only if a value is provided
        user.first_name = request.POST.get("first-name", user.first_name)
        user.last_name = request.POST.get("last-name", user.last_name)
        user.gender = request.POST.get("gender", user.gender)
        user.department = request.POST.get("department", user.department)
        user.year_of_study = request.POST.get("year-of-study", user.year_of_study)

        # Handle profile photo upload
        if 'profile-photo' in request.FILES:
            profile_photo = request.FILES['profile-photo']
            user.profile_photo = profile_photo

        # Save the user object
        user.save()

    # Get the following and follower counts for the current user
    following_count = request.user.following.count()
    followers_count = request.user.followers.count()

    return render(request, 'social_network/my_profile.html', {
        'following_count': following_count,
        'followers_count': followers_count,
    })

@login_required
def user_profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User does not exist.")

    return render(request, 'social_network/user_profile.html', {'user': user})

@login_required(login_url='login')
def create_comment(request, post_id):
    # Retrieve the post object using the post_id
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  # Assign the current user as the comment author
            comment.post = post
            comment.save()

            # Find mentions in the comment text and create Mention objects
            mentioned_users = find_mentions(comment.text)
            for mentioned_user in mentioned_users:
                Mention.objects.create(user=mentioned_user, comment=comment)

    # Redirect back to the referring page (the page where the comment was posted)
    referring_page = request.META.get('HTTP_REFERER')
    if referring_page:
        return HttpResponseRedirect(referring_page)
    # Handle other cases or return an error response if needed
    return HttpResponseServerError("Invalid request.")

@login_required
def delete_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)

        # Check if the current user is the author of the comment
        if comment.user == request.user:
            comment.delete()
            messages.success(request, "Comment deleted successfully.")
        else:
            messages.error(request, "You do not have permission to delete this comment.")

    except Comment.DoesNotExist:
        messages.error(request, "Comment does not exist.")

    # Redirect back to the referring page (the page where the comment was deleted from)
    referring_page = request.META.get('HTTP_REFERER')
    if referring_page:
        return HttpResponseRedirect(referring_page)

    # Handle other cases or return an error response if needed
    return HttpResponseServerError("Invalid request.")

@login_required
def follow_user(request):
    if request.method == "POST":
        follow_form = FollowForm(request.POST)
        if follow_form.is_valid():
            user_to_follow_id = follow_form.cleaned_data.get('user_to_follow')
            user_to_follow = User.objects.get(pk=user_to_follow_id)

            if user_to_follow == request.user:
                # Prevent following oneself
                raise Http404("Invalid request")

            if user_to_follow in request.user.following.all():
                # User is already following, so unfollow
                request.user.following.remove(user_to_follow)
                user_to_follow.followers.remove(request.user)
            else:
                # User is not following, so follow
                request.user.following.add(user_to_follow)
                user_to_follow.followers.add(request.user)

            # Update the following and follower counts
            request.user.save()
            user_to_follow.save()

            # Render the user_profile page of the user they followed or unfollowed
            return render(request, 'social_network/user_profile.html', {
                'user': user_to_follow,
                'follow_form': follow_form,
            })

    # Handle other cases or errors here if needed
    raise Http404("Invalid request")

@login_required
def update_profile_photo(request):
    if request.method == 'POST':
        try:
            user = request.user

            # Check if 'profile-photo' is in the request.FILES
            if 'profile-photo' in request.FILES:
                profile_photo = request.FILES['profile-photo']

                # Save the uploaded profile photo to the user's profile
                user.profile_photo = profile_photo
                user.save()

                messages.success(request, "Profile photo updated successfully.")
                return redirect("my_profile")
            else:
                messages.error(request, "No profile photo provided.")
        except Exception as e:
            # Log the error for debugging
            messages.error(request, "An error occurred while updating the profile photo.")

    # Redirect back to the profile page even on error
    return redirect("my_profile")

@login_required
def remove_profile_photo(request):
    user = request.user

    # Remove the user's profile photo
    user.profile_photo.delete(save=False)
    user.save()

    messages.success(request, "Profile photo removed successfully.")
    return redirect("my_profile")

@login_required(login_url='login')
def delete_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        if post.author == request.user:
            post.delete()
            messages.success(request, 'Post successfully deleted')
        else:
            messages.error(request, 'Post deletion unsuccessful. You do not have permission to delete this post.')

        # Check the Referer header to determine the previous page
        referer = request.META.get('HTTP_REFERER')
        if referer:
            # Redirect the user back to the previous page
            return redirect(referer)
        else:
            # If no referer is provided, redirect to a default page (e.g., my_profile)
            return redirect('my_profile')  # Change 'my_profile' to the appropriate URL name
    except Post.DoesNotExist:
        raise Http404("Post does not exist.")

@login_required
def update_profile(request):
    if request.method == 'POST':
        user_id = request.POST.get('user-id')
        new_first_name = request.POST.get('first-name')
        new_last_name = request.POST.get('last-name')
        new_gender = request.POST.get('gender')
        new_department = request.POST.get('department')
        new_year_of_study = request.POST.get('year-of-study')

        try:
            user = User.objects.get(id=user_id)

            # Update fields if new values are provided
            if new_first_name is not None:
                user.first_name = new_first_name
            if new_last_name is not None:
                user.last_name = new_last_name
            if new_gender is not None:
                user.gender = new_gender
            if new_department is not None:
                user.department = new_department
            if new_year_of_study is not None:
                user.year_of_study = new_year_of_study

            # Handle profile photo upload
            if 'profile-photo' in request.FILES:
                profile_photo = request.FILES['profile-photo']
                user.profile_photo = profile_photo

            # Save the updated user object
            user.save()

            messages.success(request, "Profile updated successfully.")
            return redirect("my_profile")

        except User.DoesNotExist:
            messages.error(request, "An error occurred while updating the profile.")

    # Handle other cases or return an error response if needed
    return HttpResponseServerError("Invalid request.")

@login_required
def update_bio(request):
    if request.method == 'POST':
        user_id = request.user.id
        new_bio = request.POST.get('bio')

        try:
            user = User.objects.get(id=user_id)

            # Update the bio field if a new value is provided
            if new_bio is not None:
                user.bio = new_bio

            # Save the updated user object
            user.save()

            messages.success(request, "Bio updated successfully.")
            return redirect("my_profile")

        except User.DoesNotExist:
            messages.error(request, "An error occurred while updating the bio.")

    # Handle other cases or return an error response if needed
    return HttpResponseServerError("Invalid request.")

@login_required(login_url='login')
def create_post(request):
    user = request.user
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = user
            post.save()

            # Extract mentions from the post content
            mentioned_users = find_mentions(post.content)

            # Save mentions in the Mention model
            for mentioned_user in mentioned_users:
                Mention.objects.create(post=post, user=user)


            messages.success(request, 'Post successfully created')
        else:
            messages.error(request, 'Post creation unsuccessful')

    # Check the Referer header to determine the previous page
    referer = request.META.get('HTTP_REFERER')
    if referer:
        # Redirect the user back to the previous page
        return redirect(referer)
    else:
        # If no referer is provided, redirect to a default page (e.g., index)
        return redirect('index')  # Change 'index' to the appropriate URL name



@login_required(login_url='login')
def display_posts(request):
    user = request.user
    posts = Post.objects.filter(author=user).order_by('-created')
    form = PostForm()

    return render(request, 'social_network/my_profile.html', {'form': form, 'posts': posts})

def discover(request):
    # Retrieve all users
    all_users = list(User.objects.all())  # Replace with your custom user profile model if needed
    # Shuffle the list to randomize the order
    random.shuffle(all_users)
    return render(request, 'social_network/discover.html', {'all_users': all_users})

def settings(request):
    return render(request, 'social_network/settings.html')

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        # Attempt to sign the user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication was successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "social_network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "social_network/login.html", {'csrf_token': csrf.get_token(request)})

def logout_view(request):
    logout(request)
    return render(request, "social_network/login.html", {'csrf_token': csrf.get_token(request)})

@csrf_exempt  # You may need to exempt CSRF protection for this view
def signup(request):
    if request.method == "POST":
        # Take in the user username and email submitted in the signup form
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure the password matches the confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "social_network/signup.html", {
                "message": "Passwords must match."
            })

        # Attempt to create a new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "social_network/signup.html", {
                "message": "Username already taken."
            })

        # Log the user in
        login(request, user)

        # Render the index page with the specified content
        return render(request, 'social_network/index.html', {
            "show_content": True  # Add this context variable
        })
    else:
        return render(request, "social_network/signup.html", {'csrf_token': csrf.get_token(request)})

def discover(request):
    # Retrieve all users
    all_users = list(User.objects.all())  # Replace with your custom user profile model if needed
    # Shuffle the list to randomize the order
    random.shuffle(all_users)
    return render(request, 'social_network/discover.html', {'all_users': all_users})

def user_posts(request, username):
    try:
        user = User.objects.get(username=username)
        posts = Post.objects.filter(author=user).order_by('-created')
        return render(request, 'social_network/user_profile.html', {'user': user, 'posts': posts})
    except User.DoesNotExist:
        raise Http404("User does not exist.")

def followers(request, username):
    user = get_object_or_404(User, username=username)
    followers = user.followers.all()
    return render(request, 'social_network/followers.html', {'user': user, 'followers': followers})

def followings(request, username):
    user = get_object_or_404(User, username=username)
    followings = user.following.all()
    return render(request, 'social_network/followings.html', {'user': user, 'followings': followings})




@login_required
def notifications(request):
    # Retrieve all mentions
    mentions = Mention.objects.all().order_by('-created')

    # Get mentioned users using the find_mentions function for all mentions
    mention_texts = [mention.post.content if mention.post else mention.comment.post.content for mention in mentions]
    mentioned_users = find_mentions(" ".join(mention_texts))

    # Filter mentioned users to only include the currently logged-in user
    mentioned_user = [user for user in mentioned_users if user.username == request.user.username]

    print("Logged-in User:", request.user.username)
    print("Mentioned User:", [user.username for user in mentioned_user])

    return render(request, 'social_network/notifications.html', {'user': request.user, 'mentions': mentions, 'mentioned_users': mentioned_user})





def save_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            new_department = form.cleaned_data['department']
            request.user.department = new_department
            request.user.save()
            return redirect('my_profile')  # Redirect back to the profile page

    # If the form is not valid or it's a GET request, render the profile page
    form = DepartmentForm(initial={'department': request.user.department})
    return render(request, 'my_profile.html', {'form': form})