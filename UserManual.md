# Campus Connect - User Manual

## Table of Contents 
- [Product Usage]
    - [Getting Started / Account]
    - [Navigation]
    - [User Profiles]
    - [Posts]

- [Installation / Setup]

## Product Usage

### Getting Started / Account

#### Account Creation
Upon running the product, the user will be faced with the signup page.

To create an account, the user is prompted to enter:
- Unique Username
- Email
- Password (with confirmation)

If these details are entered correctly, the user can press the **Sign Up** button, which will then take them to their Home page.

#### Login

Alternatively, if the user already has an existing account, they can click the **Login here** button, which will take them to a Login Page.
From here, the user is propted to enter their:
- Username
- Password

If these details are entered correctly, the user can click the **Login** button, which will take them to their Home page.

#### Logout

The user can log out of their account by clicking the **Logout** button, located in the settings page.

### Navigation

#### Layout

The CampusConnect website is divided into 7 pages:
- Signup
- Login
- My Profile
- (Other) User Profile
- Home
- Discover
- Settings

#### Page Navigation

##### Signup

- Accesed upon startup.
- Can be navigated to using **Signup here** button on the Login page.

##### Login
- Accesed upon logout.
- Can be navigated to using **Login here** button, located on the Signup page.

##### Main Pages

Once the user has succesfully logged in, they can navigate to any page (excluding Signup, Login, and  (other) User Profiles) using its corresponding button, located in the navigation bar near the top of the page.

My Profile and (other) User Profile pages can be accessed by clicking on the associated user's username, wherever it appears.

#### Page Contents

##### Signup
See [**Getting Started / Account**]

##### Login
See [**Getting Started / Account**]

##### My Profile
See [**User Profiles**]

##### Other User Profiles
See [**User Profiles**]

##### Home
The Home page displays all posts made by the operating user, as well as those made by any followed user.

##### Discover
The Discover Page lists all user profiles. Specifically, it shows each profiles:
- Profile Photo
- Username
- Name(s)
- Department
- Year

##### Settings
The settings page contains the **Logout** button, which logs the user out of their account upon being clicked.


### User Profiles

#### Profile Information

Each user profile contains and displays the following information fields:
- First Name
- Last Name
- Gender
- Department
- Bio
- Followers (#)
- Following (#)

Additionally, each profile can optionally contain a profile photo.

#### Profile Interaction

##### All Profiles

The user can view all posts made by any user by clicking the **View All Posts** button, located near the bottom of the page.

##### My Profile

When viewing their own profile, the user can edit any of the text fields (excluding bio) after clicking the **Edit** button, and can subsequently save these changed using the **Save** button.

The user bio can be edited after clicking the **Edit Bio** button, and subsequently saved by clicking the **Save Bio** button.

Similarily, the user can upload, save, or delete a profile photo using the buttons located directly beneath the photo container.

The user can also create a post from their profile by clicking the **Create Post** button, located underneath the **View All Posts** button, at the bottom of the page.

##### Other Users

When viewing another users profile, the user has the option to follow the user by clicking the **Follow** button. This will increse the other users follower count by 1, increase the operating users following count by 1, as well as causing the other users posts to appear on the operating user's Home page.

Alternatively, if the operating user already follows the other user, they can unfollow the other user by pressing the **Unfollow** button, decreasing the associated followers and folowing counts by 1, and removing the other users posts from the operating users Home page.

### Posts
#### Creating a Post
Posts can be made by clicking the **Create Post** button on either the Home or My Profile pages after filling in the text field with the post content.

#### Deleting a Post
The operating user can delete any post they have made previously by pressing the **Delete** button, located underneath the post.

#### Comments
Post comments can be viewed by pressing the **View Comments** button, located underneath the post.

While viewing comments, Users can comment on any other users' posts by pressing the **Add Comment** button after filling in the text field.

The operating user can delete any comment they have made previously by pressing the **Delete** button, located directly under the comment.


## Installation / Setup

### Prerequisites
Before attempting to run the project, ensure you have installed:
- Python (version 3.7 or higher)
- Django
- Git

If not, you can install them here:
- Python - https://www.python.org/downloads/
- Django - https://www.djangoproject.com/download/
- Git - https://gitforwindows.org/ 

### Obtaining the Files
All required files for this project are located in the project repo on github.

The command to clone this project into your local workspace is:

*git clone https://github.com/ninijoe/campusconnect*

### Running the Project
Once you have all required files in a local directory, cd into the directory from a terminal, and run the command:

*python# manage.py runserver* (where # is your python version number).

This will create a local server.

Paste the provided link into your browser to access the site.