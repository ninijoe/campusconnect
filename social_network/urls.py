from django.urls import path, include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from social_network.views import user_profile

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
    
    # URL for displaying posts
    path("display_posts/", views.display_posts, name="display_posts"),

    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),

    # Add this URL pattern for the user profile page
    path('user_profile/<str:username>/', views.user_profile, name='user_profile'),

    path('user/<str:username>/posts/', views.user_posts, name='user_posts'),

    path('follow_user/', views.follow_user, name='follow_user'),

    path('<str:username>/followers/', views.followers, name='followers'),
    
    path('<str:username>/followings/', views.followings, name='followings'),

    # URL pattern for creating comments on a post
    path('create_comment/<int:post_id>/', views.create_comment, name='create_comment'),

    # Add this URL pattern for comment deletion
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    # URL for Notifications
    path('notifications/', views.notifications, name='notifications'),

    path('save_department/', views.save_department, name='save_department'),


]
