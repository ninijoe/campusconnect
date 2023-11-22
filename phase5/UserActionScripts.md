# User Action Scripts
This file details all the user action scripts that are apart of the Test plan. This is compiled into a single document as all test cases performed on CampusConnect are descriptive user scripts.

## Team and Project Information
- **Team Name**: [Cavemen Coders]
- **Project Name**: [Campus Connect]
- **Contact Information**: [josephephraim68@yahoo.com]

## Table of Contents 
- [Signup Tests]
- [Login Tests]
- [Home Page Tests]
- [My Profile Tests]
- [Discover Tests]
- [Settings Tests]

## Signup Tests
This section details all the user action scripts for the Signup page of CampusConnect.

### Redirection User Action Script
Reason:
To check whether the signup page works correctly and prompt user to the home page.

Action:
  Step 1: Fill necessary details in the spaces
  Step 2: Press “Signup” button

Expected action:
  IF 
the data already present in the database, break the process and notify the user
	ELSE
Frontend:
Takes the user to the homepage or “Home” aka(index.html)
Backend:
	Save the user-entered data in the database

### Login Redirection User Action Script
Reason:
To check whether the “Login here ”works correctly and prompts the user to the Login page.

Action:
	Step 1: Click “Login here”

Expected action:
	Takes the user to the Login page aka Login.html	

## Login Tests
This section details all the user action scripts for the Login page of CampusConnect.

### Login Redirection User Action Script
Reason:
To check whether the login page works correctly and prompts the user to the home page.

Action:
  Step 1: Fill necessary details in the spaces
  Step 2: Press the “Login” button

Expected action:
	IF 
the data couldn't be found in the database, break the process and notify the user
	ELSE
Takes the user to the homepage or “Home” aka(index.html)

### Signup Redirection User Action Script
Reason:
To check whether the “Signup here” works correctly and prompts the user to the Signup page. 

Action:
	Step 1: Click “Signup here”

Expected action:
	Takes the user to the Signup page aka Signup.html	

## Home Page Tests
This section details all the user action scripts for the Home page of CampusConnect.

### Buttons Check User Action Script
Reason:
To check whether the Buttons in the navigation bar page work correctly and give the expected result.

Test 1 (Profile click):
Action:
	Step 1: Press “My Profile”
Expected action:
	Opens “My Profile” section or my_profile.html

Test 2 (Home click):
Action:
	Step 1: Press “Home”
Expected outcome:
	Opens “Home” section or index.html

Test 3 (Discover click):
Action:
	Step 1: Press “Discover”
Expected outcome:
	Opens Discover section or discover.html

Test 4 (Settings click):
Action:
	Step 1: Press “Settings”
Expected outcome:
	Opens “Settings” section or settings.html

Test 5:
Action:
	Step 1: Press “Home”
Expected outcome:
	Opens “Home” section or index.html

### Create Post User Action Script
Reason: To check whether the user can successfully create a post and to make sure its dependent buttons are working correctly.

Test 1 (create post test):
Action:
	Step 1: Write stuff in the Text area(Big white box)
	Step 2: Click “Create Post Button”

Expected outcome:  
Creates a post with 2 buttons “View Comments” and “Delete”

Test 2 (view comments test):
Action:
	Step 1: Click “View Comments”
	
Expected outcome: Shows comments and gives an option to delete them

Test 3 (delete test):
Action:
  Step 1: Click “Delete”

Expected outcome: Deletes the particular post or comment the button is related to 

## My Profile Tests
This section details all the user action scripts for the My Profile page of CampusConnect.

### Profile Details User Action Script
Reason: To check whether the user input is saved correctly.

Action:
	Step 1: Press “Edit” button
	Step 2: Fill necessary details in the spaces provided
  Step 3: Press the “Save” button

Expected outcome:
	Frontend:
	The saved data should be reflected on the screen
	Backend:
	The user entered data should be stored in database

### Button Checks User Action Script
Reason:
To check whether the buttons in the My Profile page works correctly and achieve it’s task.

Test 1 (edit button):
Action:
  Step 1: Click the “Edit” button”

Expected outcome: 
Enables user to enter details in the required section

Test 2(save button):
Action:
	Step 1: Click the “Save” button
	
Expected outcome: Saves the user entered data in both frontend and backend

Test 3 (delete button):
Action:
  Step 1: Click “Delete” icon

Expected outcome: Deletes the profile photo

Test 4:
Action and outcome:
  Step 1: Click “Choose file” button
Expected outcome: Opens local computer and enables user to select the photo.
	Step 2: Click the “Edit Profile” icon
Expected outcome: displays the photo in the webpage
  Step 3: click “Save” button
Expected action: saves it  

Test 5(create post):
Action:
  Step 1: Click the “Create Post” button
 
Expected outcome:
Enables user to write a post and gives option to post it using “Post” button

Test 6(view posts):
Action:
  Step 1: Click the “View All Post” button
 
Expected outcome:
Enables user to view all posts.

## Discover Tests
This section details all the user action scripts for the Discover page of CampusConnect.

### All Users User Action Script
Reason: To check whether the Discover page shows “All Users” containers with their profile, account, and year.

Action: 
	Step 1: Click the “Discover” option located in the navbar.

Expected outcome:
Pops up the All User or content container showing the users with their account, profile and year.

### All User Profile User Action Script
Reason: To check whether the profiles shows in “All User” are working correctly and gives the correct respond upon particular actions.

Test 1 (profile interaction):	
Action:
	Step 1: Click the user profile “@foo” 

Expected outcome:
Pops up the container which has the users information from their respected profiles

Test 2 (follow button):
 Step 1: Click the “Follow” button

Expected outcome:
	Increments the value of followers of @foo by 1
	Increments the value of the following, in users profile by 1

Test 3 (unfollow button):

  Step 1: Click the “Unfollow” button

Expected outcome:
	Decrements the value of followers of @foo by 1
	Decrements the value of the following, in users profile by 1

## Settings Tests
This section details all the user action scripts for the Settings page of CampusConnect.

### Logout User Action Script
Reason: To give the user the ability to log out of the webpage.

Test 1 (Logout interaction):
Action:
  Step 1: Click the logout button

Expected outcome:
Redirects the user back to the login page of the website.


