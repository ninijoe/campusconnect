from django.urls import path, include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from social_network.views import user_profile
from .views import change_username
from .views import terms_of_service, privacy_policy
from .views import like_comment
from .views import display_index_posts, reshare_index_post, delete_post
from .views import follow_user
from .views import search_group



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_network.urls')),  # Include your app's URLs here
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [

    

    # URL for the signup view
    path("", views.signup, name="signup"),

    # URL for the index view (requires login)
    path("index/", views.index, name="index"),

    path("reshare_index_post/<int:post_id>/", views.reshare_index_post, name='reshare_index_post'),

    path("reshare_user_profile_post/<int:post_id>/", views.reshare_user_profile_post, name='reshare_user_profile_post'),

    # URL for the login view
    path("login/", views.login_view, name="login"),

    path("update_bio/", views.update_bio, name="update_bio"),

    path("update_profile_photo/", views.update_profile_photo, name="update_profile_photo"),
    
    path("remove_profile_photo/", views.remove_profile_photo, name="remove_profile_photo"),

    # URL for the logout view
    path("logout_view/", views.logout_view, name="logout_view"),

    # URL for My Profile
    path("my_profile/", views.my_profile, name="my_profile"),

    # URL for Discover
    path("discover/", views.discover, name="discover"),

    # URL for Settings
    path("settings/", views.settings, name="settings"),

    path("update_profile/", views.update_profile, name="update_profile"),

    # URL for creating a new post
    path("create_post/", views.create_post, name="create_post"),
    
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),

    # Add this URL pattern for the user profile page
    path('user_profile/<str:username>/', views.user_profile, name='user_profile'),

    path('user/<str:username>/posts/', views.user_posts, name='user_posts'),
    
    path('user/<str:username>/', views.user_profile, name='user_profile'),

    path('follow_user/<str:username>/', views.follow_user, name='follow_user'),

    path('<str:username>/followers/', views.followers, name='followers'),
    
    path('<str:username>/followings/', views.followings, name='followings'),

    path('my_profile_posts/', views.display_my_profile_posts, name='display_my_profile_posts'),


    # URL pattern for creating comments on a post
    path('create_comment/<int:post_id>/', views.create_comment, name='create_comment'),

    # Add this URL pattern for comment deletion
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    # URL for Notifications
    path('notifications/', views.notifications, name='notifications'),

    path('save_department/', views.save_department, name='save_department'),

    path('delete_account/', views.delete_account, name='delete_account'),

    path('like_post/<int:post_id>/', views.like_post, name='like_post'),

    path('change-username/', change_username, name='change_username_view'),

    path('dislike_post/<int:post_id>/', views.dislike_post, name='dislike_post'),

    path('change-email/', views.change_email, name='change_email'),

    path('terms-of-service/', terms_of_service, name='terms_of_service'),

    path('privacy-policy/', privacy_policy, name='privacy_policy'),

    path('change_password/', views.change_password, name='change_password'),

    path('block_user/<str:username>/', views.block_user, name='block_user'),

    path('unblock_user/<str:username>/', views.unblock_user, name='unblock_user'),

    path('blocked-users/', views.blocked_users_list, name='blocked_users_list'),  # Add this line

    path('like_comment/<int:comment_id>/', views.like_comment, name='like_comment'),

    path('messages/', views.messages, name='messages'),

    path('send_message/<str:username>/', views.send_message, name='send_message'),

    path('messages/<str:username>/', views.message_detail, name='message_detail'),

    path('unshare_post/<int:post_id>/', views.unshare_post, name='unshare_post'),

    path('reset_notification_count/', views.reset_notification_count, name='reset_notification_count'),
    
    path('notification_count/', views.notification_count, name='notification_count'),

    path('create_group/', views.create_group, name='create_group'),

    path('view_group/<int:group_id>/', views.view_group, name='view_group'),
  
    path('user_statistics/', views.user_statistics_view, name='user_statistics'),

    path('search_group/', views.search_group, name='search_group'),

    # Add the URL for the groups view
    path('groups/', views.groups, name='groups'),

    path('create_group/', views.create_group, name='create_group'),

    path('delete_group/<int:group_id>/', views.delete_group, name='delete_group'),

    path('groups/<int:group_id>/edit/', views.update_group, name='update_group'),
    
    path('groups/<int:group_id>/posts/', views.group_posts, name='group_posts'),
    path('groups/<int:group_id>/create_post/', views.create_group_post, name='create_group_post'),
    path('groups/<int:group_id>/delete_post/<int:group_post_id>/', views.delete_group_post, name='delete_group_post'),
    path('groups/<int:group_id>/like_post/<int:group_post_id>/', views.like_group_post, name='like_group_post'),

]
