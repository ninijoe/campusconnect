# social_network/views.py
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect , HttpResponseForbidden
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
from django.db.models import Count
import logging
from .forms import ChangeUsernameForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
import re
from django.db.models import Q
import random
from django.contrib.auth.models import User
from django.http import Http404
from .models import Post , Comment , Mention, Message, ResharedPost 
from .forms import PostForm , FollowForm , CommentForm , ProfilePhotoForm, PostMediaForm
from django.db.models import F
from django.contrib import messages
from .models import User , Group
from datetime import datetime
from django.http import HttpResponseServerError
from django.utils import timezone
from django.utils.html import escape
from django.utils.safestring import mark_safe
from .forms import ChangeEmailForm
from django.contrib.auth.views import PasswordResetView
from .forms import CustomPasswordResetForm  # Import your custom form if needed
from django.contrib.auth.models import User  # Import the User model
from .models import User
from itertools import chain
from operator import attrgetter
from django.http import JsonResponse
from django.db.models.functions import Coalesce
from django.db.models import Count, F, Value
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.conf import settings
from django.core.mail import send_mail
from .forms import GroupForm
from .models import Group

@login_required
def change_email(request):
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['new_email']
            request.user.email = new_email
            request.user.save()
            messages.success(request, 'Email changed successfully.')
            return redirect('change_email')  # Redirect to the user's profile page
    else:
        form = ChangeEmailForm()

    return render(request, 'social_network/change_email.html', {'form': form,})





@login_required
def messages(request):
    conversations = set()
    messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    for message in messages:
        conversations.add(message.conversation_id)
    return render(request, 'social_network/messages.html', {'conversations': conversations})







@login_required
def message_detail(request, username):
    recipient = get_object_or_404(User, username=username)
    conversation_id = f"{request.user.id}-{recipient.id}"
    messages = Message.objects.filter(conversation_id=conversation_id).order_by('timestamp')

    decrypted_messages = []
    for message in messages:
        decrypted_content = message.get_decrypted_content()
        decrypted_messages.append((message.sender, decrypted_content, message.timestamp))

    return render(request, 'social_network/message_detail.html', {'recipient': recipient, 'messages': decrypted_messages})





@login_required
def send_message(request, username):
    if request.method == 'POST':
        content = request.POST.get('content')
        recipient = get_object_or_404(User, username=username)

        # Check if the recipient is blocked
        if recipient in request.user.blocked_users.all():
            messages.error(request, 'Unable to send a message to a blocked user.')
            return redirect('messages')

        # Check if a conversation already exists
        conversation_id = f"{request.user.id}-{recipient.id}"
        existing_messages = Message.objects.filter(conversation_id=conversation_id)

        if existing_messages.exists():
            # Conversation already exists, add the new message
            new_message = Message(
                sender=request.user,
                recipient=recipient,
                content=content,
                conversation_id=conversation_id,
            )
            new_message.save()
            return redirect('message_detail', username=recipient.username)
        else:
            # Conversation doesn't exist, create a new one
            new_message = Message(
                sender=request.user,
                recipient=recipient,
                content=content,
                conversation_id=conversation_id,
            )
            new_message.save()
            return redirect('message_detail', username=recipient.username)

    # Handle other cases or provide a default response
    return HttpResponse("Invalid request")




@login_required
def index(request):
    # Check if the user has clicked on the "Home" link
    home_link_clicked = request.session.pop('home_link_clicked', False)

    # Use display_index_posts to get the posts
    posts = display_index_posts(request)
    # Get the reshared posts by user and user's followings
    reshared_posts = ResharedPost.objects.filter(Q(user=request.user) | Q(user__in=request.user.following.all()))

    form = PostForm()  # Include the form for creating a new post

    if request.method == "POST":
        # Check the age
        birthday_year = int(request.POST['birthday_year'])
        current_year = datetime.now().year
        age = current_year - birthday_year

        if age < 13:
            # Reject users under 13
            return render(request, 'signup.html', {'error_message': 'You must be at least 13 years old to sign up.'})

        # Check if the form is a signup form
        if 'signup' in request.POST:
            signup_form = SignupForm(request.POST)
            if signup_form.is_valid():
                # Process the signup form
                # ...

                # After signup, don't show signup content
                return redirect('index')

    # Pass the correct context to render
    context = {'form': form, 'home_link_clicked': home_link_clicked, 'posts': posts, 'reshared_posts': reshared_posts}
    return render(request, 'social_network/index.html', context)




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

    # Pass the user object to the template
    return render(request, 'social_network/my_profile.html', {
        'user': request.user,  # Include the user object in the context
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








@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Check if the user has already liked the comment
    if request.user in comment.likes.all():
        # User already liked, so unlike
        comment.likes.remove(request.user)
    else:
        # User hasn't liked, so like
        comment.likes.add(request.user)

    # Redirect back to the referring page (the page where the comment was liked/unliked)
    referring_page = request.META.get('HTTP_REFERER')
    if referring_page:
        return redirect(referring_page)

    # Handle other cases or return an error response if needed
    return HttpResponseServerError("Invalid request.")





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





def update_profile_photo(request):
    if request.method == 'POST':
        try:
            user = request.user

            # Check if 'profile-photo' is in the request.FILES
            if 'profile-photo' in request.FILES:
                

                # Remove the existing profile photo before saving the new one
                if user.profile_photo:
                    user.profile_photo.delete(save=False)

                profile_photo = request.FILES['profile-photo']

                # Save the uploaded profile photo to the user's profile
                user.profile_photo = profile_photo
                user.save()

                
                return redirect("my_profile")
            else:
                messages.error(request, "No profile photo provided.")
        except Exception as e:
            # Log the error for debugging
            messages.error(request, "An error occurred while updating the profile photo.")

    # Redirect back to the profile page even on error
    return redirect("my_profile") 







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

            print("Comment created successfully")

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
            # Redirect back to the referring page (the page where the comment was deleted from)
            referring_page = request.META.get('HTTP_REFERER')
            if referring_page:
                return HttpResponseRedirect(referring_page)
        
    except Comment.DoesNotExist:
        # Handle other cases or return an error response if needed
        return HttpResponseServerError("Invalid request.")

    

    










@login_required(login_url='login')
def create_post(request):
    user = request.user
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        media_form = PostMediaForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = user
            post.save()

            media = media_form.save()
            post.media = media
            post.save()

            # Extract mentions from the post content
            mentioned_users = find_mentions(post.content)

            # Save mentions in the Mention model
            for mentioned_user in mentioned_users:
                Mention.objects.create(post=post, user=user)
            
            # Redirect back to the referring page
            referring_page = request.META.get('HTTP_REFERER')
            return redirect(referring_page)
    
    # Handle the case where the form is not valid or when the request method is not POST
    # You might want to add additional context or logic here
    return HttpResponse("An error occurred while creating the post.")







@login_required
def unshare_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    try:
        # Get the ResharedPost object for the logged-in user and the specified post
        reshared_post = ResharedPost.objects.get(user=request.user, original_post=post)

        # Delete the ResharedPost
        reshared_post.delete()

        # Update the Post model to reflect unsharing
        post.reshared = False
        post.reshare_count -= 1
        post.save()

        
    except ResharedPost.DoesNotExist:
        print( "You have not reshared this post.")

    return redirect("reshare_index_post", post_id=post_id)








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

            
            return redirect("my_profile")

        except User.DoesNotExist:
            messages.error(request, "An error occurred while updating the bio.")

    # Handle other cases or return an error response if needed
    return HttpResponseServerError("Invalid request.")










        

    








def change_password(request):
    if request.method == "POST":
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password == confirm_password:
            # Change the user's password
            request.user.set_password(new_password)
            request.user.save()

            # Reauthenticate the user with the updated password
            user = authenticate(request, username=request.user.username, password=new_password)
            
            if user:
                login(request, user)

                messages.success(request, 'Password successfully changed.')
                return redirect('change_password')  # Redirect to the change password page
            else:
                messages.error(request, 'Failed to authenticate user with new password.')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'social_network/change_password.html')












@login_required
def display_index_posts(request):
    # Get the user's posts
    user_posts = Post.objects.filter(author=request.user)

    # Get the posts from user's followings
    following_posts = Post.objects.filter(author__in=request.user.following.all())

    # Get the reshared posts by user and user's followings
    reshared_posts = ResharedPost.objects.filter(Q(user=request.user) | Q(user__in=request.user.following.all()))

    # Combine user's posts and reshared posts
    combined_posts = []

    for reshared in reshared_posts:
        # Mark reshared posts
        reshared.original_post.is_reshared = True
        reshared.original_post.reshared_by = reshared.user  # Add the resharing user information
        combined_posts.append(reshared.original_post)

    for post in chain(user_posts, following_posts):
        # Mark original posts
        post.is_reshared = False
        combined_posts.append(post)

    # Order the posts by the created timestamp in descending order
    all_posts = sorted(combined_posts, key=lambda post: post.created, reverse=True)

    return all_posts

    











@login_required
def reshare_index_post(request, post_id):
    post_to_reshare = get_object_or_404(Post, id=post_id)

    # Check if the user has already reshared the post
    reshared_entry = ResharedPost.objects.filter(user=request.user, original_post=post_to_reshare).first()

    if reshared_entry:
        # User has already reshared, so unshare
        reshared_entry.delete()
        
    else:
        # User hasn't reshared, so reshare
        ResharedPost.objects.create(user=request.user, original_post=post_to_reshare)
        post_to_reshare.mark_as_reshared()
        post_to_reshare.increase_reshare_count()

    return redirect('index')











@login_required
def display_my_profile_posts(request):
    # Get the user's posts
    user_posts = Post.objects.filter(author=request.user)

    # Get the reshared posts by the user
    reshared_posts = ResharedPost.objects.filter(user=request.user)

    # Combine user's posts and reshared posts
    combined_posts = []

    for reshared in reshared_posts:
        # Mark reshared posts
        reshared.original_post.is_reshared = True
        reshared.original_post.reshared_by = reshared.user  # Add the resharing user information
        combined_posts.append(reshared.original_post)

    for post in chain(user_posts):
        # Mark original posts
        post.is_reshared = False
        combined_posts.append(post)

    # Order the posts by the created timestamp in descending order
    all_posts = sorted(combined_posts, key=lambda post: post.created, reverse=True)

    context = {'posts': all_posts}
    return render(request, 'social_network/my_profile.html', context)










@login_required
def display_user_profile_posts(request, username):
    # Get the user whose profile is being viewed
    user_profile = get_object_or_404(User, username=username)

    # Get the user's original posts
    user_posts = Post.objects.filter(author=user_profile)

    

    # Get the reshared posts by the user
    reshared_posts = ResharedPost.objects.filter(user=user_profile)

    

    # Combine user's original posts and reshared posts
    combined_posts = list(user_posts)

    for reshared in reshared_posts:
        # Mark reshared posts
        reshared.original_post.is_reshared = True
        reshared.original_post.reshared_by = reshared.user  # Add the resharing user information
        combined_posts.append(reshared.original_post)

    

    # Order the posts by the created timestamp in descending order
    all_posts = sorted(combined_posts, key=lambda post: post.created, reverse=True)

    context = {'posts': all_posts, 'user_profile': user_profile}
    return context











@login_required
def user_posts(request, username):
    # Call the display_user_profile_posts function to get the context
    context = display_user_profile_posts(request, username)

    # Render the user_profile.html template using the context
    return render(request, 'social_network/user_profile.html', context)










@login_required
def user_profile(request, username):
    # Call the display_user_profile_posts function to get the context
    posts_context = display_user_profile_posts(request, username)

    # Get the user separately
    user = get_object_or_404(User, username=username)

    # Merge the user data with the posts context
    context = {'user': user, **posts_context}

    # Render the user_profile.html template using the combined context
    return render(request, 'social_network/user_profile.html', context)









@login_required
def reshare_user_profile_post(request, post_id):
    post_to_reshare = get_object_or_404(Post, id=post_id)

    # Check if the user has already reshared the post
    reshared_entry = ResharedPost.objects.filter(user=request.user, original_post=post_to_reshare).first()

    if reshared_entry:
        # User has already reshared, so unshare
        reshared_entry.delete()
        
    else:
        # User hasn't reshared, so reshare
        ResharedPost.objects.create(user=request.user, original_post=post_to_reshare)
        

    # Redirect to the user_profile with the appropriate username (original post author)
    return redirect(reverse('user_profile', args=[post_to_reshare.author.username]))









@login_required
def discover(request):
    # Retrieve all users, including the current user
    all_users = User.objects.all()

    # Get the count of all users
    all_users_count = all_users.count()

    # Get the search query from the request
    search_query = request.GET.get('search', '')

    # Exclude users who have blocked the current user and who are blocked by the current user
    all_users = all_users.exclude(
        Q(blocked_users=request.user) | Q(blocked_by_users=request.user)
    )

    # Apply additional filtering based on username, first_name, and last_name
    if search_query:
        all_users = all_users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )

    context = {
        'all_users': all_users , 
        'all_users_count': all_users_count
    }

    # Render the template with the filtered queryset
    return render(request, 'social_network/discover.html', context)









@login_required
def search_group(request):
    # Retrieve all groups
    all_groups = Group.objects.all()

    # Get the count of all groups
    all_groups_count = all_groups.count()

    # Get the search query from the request
    search_query = request.GET.get('search', '')

    # Apply additional filtering based on group name and bio
    if search_query:
        all_groups = all_groups.filter(
            Q(name__icontains=search_query) |
            Q(bio__icontains=search_query)
        )

    context = {
        'groups': all_groups,
        'all_groups_count': all_groups_count
    }

    # Render the template with the filtered queryset
    return render(request, 'social_network/search_group.html', context)









@login_required
def groups(request):
    # Retrieve all groups
    all_groups = Group.objects.all()

    context = {
        'groups': all_groups,
    }

    # Render the template with the queryset of all groups
    return render(request, 'social_network/groups.html', context)








@login_required
def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        bio = request.POST.get('bio')

        # Assuming the creator is the current logged-in user
        creator = request.user

        # Create the group
        group = Group.objects.create(name=name, creator=creator, bio=bio)

        # Add the creator as a member and moderator
        group.members.add(creator)
        group.moderators.add(creator)

        return redirect('groups')

    return render(request, 'social_network/create_group.html')





@login_required
def view_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'social_network/view_group.html', {'group': group})







def settings(request):
    return render(request, 'social_network/settings.html')








@csrf_exempt
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        remember_me = request.POST.get("remember_me")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Set a longer session duration if "Remember Me" is checked
            if remember_me:
                request.session.set_expiry(1209600)  # 2 weeks in seconds

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "social_network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "social_network/login.html")
    





@login_required
def blocked_users_list(request):
    blocked_users = request.user.blocked_users.all()
    return render(request, 'social_network/blocked_users_list.html', {'blocked_users': blocked_users})







@login_required
def block_user(request, username):
    user_to_block = get_object_or_404(User, username=username)

    # Block the user (adjust this based on your actual implementation)
    request.user.blocked_users.add(user_to_block)

    # Unfollow the user if already following
    if user_to_block in request.user.following.all():
        request.user.following.remove(user_to_block)
        user_to_block.followers.remove(request.user)
        request.user.save()
        user_to_block.save()

    # Redirect back to the discover page, excluding the blocked user
    return redirect('discover')





@login_required
def unblock_user(request, username):
    user_to_unblock = User.objects.get(username=username)
    request.user.blocked_users.remove(user_to_unblock)
    return redirect('settings')  # Redirect to settings after unblocking





def logout_view(request):
    logout(request)
    return render(request, "social_network/login.html", {'csrf_token': csrf.get_token(request)})





@csrf_exempt
def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        #student_email = request.POST["student_email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "social_network/signup.html", {
                "message": "Passwords must match."
            })

        # Check if the user has agreed to the terms
        agree_to_terms = request.POST.get("agree_to_terms")
        if not agree_to_terms:
            return render(request, "social_network/signup.html", {
                "message": "Please agree to the Terms of Service."
            })

        """# Validate student_email format
        try:
            validate_email(student_email)

            # Check student_email against allowed patterns
            valid_email_format = any(
                student_email.lower().endswith(pattern) for pattern in settings.ALLOWED_SCHOOL_EMAIL_PATTERNS.values()
            )

            if not valid_email_format:
                raise ValidationError("Invalid student email format.")
        except ValidationError:
            return render(request, "social_network/signup.html", {
                "message": "Invalid student email format."
            })"""

        try:
            user = User.objects.create_user(username, email, password)
            #user.student_email = student_email
            user.save()
            """# Send verification email
            send_mail(
                'Verify Your Email',
                'We have sent you an email with a verification link. Click the link to complete the signup process.',
                'your@gmail.com',  # Sender's email (use the Gmail configured in settings)
                [email],
                fail_silently=False,
            )"""
            login(request, user)
            return redirect ('discover')
        except IntegrityError:
            return render(request, "social_network/signup.html", {
                "message": "Username or email already taken."
            })

    return render(request, "social_network/signup.html", {'csrf_token': csrf.get_token(request)})






def followers(request, username):
    user = get_object_or_404(User, username=username)
    followers = user.followers.all()
    return render(request, 'social_network/followers.html', {'user': user, 'followers': followers})






def followings(request, username):
    user = get_object_or_404(User, username=username)
    followings = user.following.all()
    return render(request, 'social_network/followings.html', {'user': user, 'followings': followings})







@login_required
def change_username(request):
    if request.method == 'POST':
        form = ChangeUsernameForm(request.POST, instance=request.user)
        if form.is_valid():
            # Check if the provided password is correct
            password = form.cleaned_data['password']
            user = request.user

            if not user.check_password(password):
                messages.error(request, 'Incorrect password. Username not changed.')
            else:
                # Save the changes only if the password is correct
                form.save()

            return render(request, 'social_network/change_username.html', {'form': form})
    else:
        form = ChangeUsernameForm(instance=request.user)

    return render(request, 'social_network/change_username.html', {'form': form})







def terms_of_service(request):
    return render(request, 'social_network/terms_of_service.html')







def privacy_policy(request):
    return render(request, 'social_network/privacy_policy.html')






@login_required
def notifications(request):
    # Retrieve all mentions
    mentions = Mention.objects.all().order_by('-created')

    # Get mentions in posts
    post_mentions = [mention for mention in mentions if mention.post and request.user.username in mention.post.content]

    # Get mentions in comments
    comment_mentions = [mention for mention in mentions if mention.comment and request.user.username in mention.comment.text]

    # Get likes on user's posts with user details
    user_post_likes = Post.objects.filter(author=request.user).annotate(
        num_likes=Count('likes'),
        liked_users_username=F('likes__username'),
        liked_users_profile_photo=F('likes__profile_photo'),
        liked_users_created=F('created')  # Use the 'created' field of Post
    ).values('id', 'num_likes', 'liked_users_username', 'liked_users_profile_photo', 'liked_users_created')

    # Get likes on user's comments with user details
    user_comment_likes = Comment.objects.filter(user=request.user).annotate(
        num_likes=Count('likes'),
        liked_users_username=F('likes__username'),
        liked_users_profile_photo=F('likes__profile_photo'),
        liked_users_created=F('created')  # Use the 'created' field of Comment
    ).values('id', 'num_likes', 'liked_users_username', 'liked_users_profile_photo', 'liked_users_created')

    
    # Get new followers
    new_followers = User.objects.filter(following=request.user)

    # Calculate the count of unseen notifications
    unseen_notification_count = len(post_mentions) + len(comment_mentions) + len(user_post_likes) + len(user_comment_likes)

    print(unseen_notification_count)
      
    # Pass the unseen_notification_count to the notification_count view
    request.unseen_notification_count = unseen_notification_count

    return render(request, 'social_network/notifications.html', {
        'unseen_notification_count': unseen_notification_count,
        'post_mentions': post_mentions,
        'comment_mentions': comment_mentions,
        'user_post_likes': user_post_likes,
        'user_comment_likes': user_comment_likes,
        'new_followers': new_followers,
    })





@login_required
def reset_notification_count(request):
    # Reset the count in the database
    unseen_notification_count = Count(
        F('post_mentions') + F('comment_mentions') + F('user_post_likes') + F('user_comment_likes') + F('new_followers'),
        Value(0)
    )
    unseen_notification_count = 0
    
    return JsonResponse({'success': True})


@login_required
def notification_count(request):
    # Retrieve the unseen_notification_count passed from the notifications view
    unseen_notification_count = getattr(request, 'unseen_notification_count', 0)
    return render(request, 'social_network/notification_count.html', {'unseen_notification_count': unseen_notification_count})





  







@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('index')  # You can redirect to the post details or another page









@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)

    return redirect('index')  # You can redirect to the post details or another page




@login_required
def delete_account(request):
    if request.method == 'POST':
        # Check if the entered password matches the user's password
        entered_password = request.POST.get('password')
        user = request.user

        if user.check_password(entered_password):
            # Password is correct, proceed to delete the account
            user.delete()
            logout(request)
            return redirect('signup')
        
    return redirect('signup')  # Redirect to the signup page






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



def user_statistics_view(request):
    # Total number of users
    total_users = User.objects.all().count()

    # Number of users logged in within the last 24 hours
    login_cutoff_time = timezone.now() - timezone.timedelta(days=1)
    active_users = User.objects.filter(last_login__gte=login_cutoff_time).count()

    # Number of newly signed up users within the last 24 hours
    signup_cutoff_time = timezone.now() - timezone.timedelta(days=1)
    new_signups = User.objects.filter(date_joined__gte=signup_cutoff_time).count()

    # Print the statistics (you can replace this with any output mechanism you prefer)
    print(f"Total Users: {total_users}")
    print(f"Active Users (last 24 hours): {active_users}")
    print(f"New Signups (last 24 hours): {new_signups}")

    # You can also pass these statistics to a template if you want to display them in a webpage
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'new_signups': new_signups,
    }

    return render(request, 'social_network/statistics_template.html', context)

