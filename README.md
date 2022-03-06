# CS1XA3 Project03 - Social Media Clone


## Usage
* **Install** the conda environment with `conda install -c anaconda django`
* **Activate** the django environment with `conda activate djangoenv`
* **Run** the server from your *local machine* with `python manage.py runserver localhost:8000`
* **Run** the project on the *mac1xa3.ca* server with `python manage.py runserver localhost:10051`
* Initial Login Credentials(already set-up):
  * Username - ***Merlin***
  * Password - '**pf2Yc9xvAS**'
* **Navigate** throughout the project using the *Navbar*
* **Quit** the server by pressing `CTRL-C` in the terminal

--------------------------------------------------------------------

### Objective 1

~**Description**: Objective 1 is responsible for properly logging in existing users or routing to a signup page for new users.
Initially a new user was created using the python shell (`python manage.py shell`) and the **UserInfo** class in `models.py`
The signup page is implemented using appropriate forms and url routing.
* #### Login/Logout
   * Uses the in-built form for authenticating the user (`from django.contrib.auth.forms import AuthenticationForm`)
   * The `login_view` function handles the **POST** request and authenticates the user and redirects them to the *messages* page.
   * The `logout_view` function using the logout request redirects the user back to the login page.
   * The `from django.contrib.auth import authenticate, login, logout` module is important to properly authenticate, login and logout the user.
   * The `login.djhtml` file renders the views using some css assets.
   * The url path is routed as `path('logout/', views.logout_view,name='logout_view')` in the `login/urls.py` file.

* #### Signup
  * Uses the in-built form for adding a new user (`from django.contrib.auth.forms import UserCreationForm`)
  * The `signup_view` and `create_view` functions handle the **POST** request and create the signup form for new users. It also uses the UserInfo class `models.UserInfo.objects.create_user_info(username=username,password=raw_password)`to add the user credentials. Redirects to the *messages* page.
  * The `signup.djhtml` file renders the views and also uses a `{% csrf_token %}` to prevent *csrf attacks*
  * The url path is routed as `path('create/', views.create_view, name='create_view')`

~**Exceptions**: If the `/e/macid/...` is incorrect, the script redirects to the login page

---------------------------------------------------

### Objective 2

~**Description**: Objective 2 is responsible for adding User Profiles and Interests.

* Uses the variables in the **UserInfo** class to display the currently logged in user's attributes including *Employment, Location, Birthday* and *Interests*
* The variables are used in the `socical_base.djhtml` file so they are displayed upon rendering
* A `for loop` is used to display the user's interests which makes use of the *label* in the **Interest** class

--------------------------------------------------------------------

### Objective 3

~**Description**: Objective 3 is resposible for providing the user with forms to change their current password and update their personal attributes

* #### Password Change
  *  Uses the in-built form for changing the password (`from django.contrib.auth.forms import PasswordChangeForm`)
  * The `account_view` function handles the password change form using the `update_session_auth_hash` module and renders the `account.djhtml` file
  * The `account.djhtml` file displays the view and uses a `{% csrf_token %}` to prevent csrf attacks
  * The url path is routed as `path('account/', views.account_view,name='account_view')`

* #### Update
  * Uses HTML input fields to add and display user information
  * The `update_view` function handles the **POST** request, update form and renders the `account.djhtml` file
  * `request.POST.get` is used to retrieve the user attributes from the **UserInfo** class
  * Instances are made to filter and add the interests of the user
  * All *interest* submissions are added to the list of interests
  * The corresponding variables are placed in the `account.djhtml` file to display them.
  * Once the user clicks submit, they are redirected back to the `messages` page 
  * The url path is routed as `path('change_u/', views.update_view, name='update_view')`

~**Exception**: In the PasswordChange form, if the user's entered password does not match twice, they will be redirected back to the login page.

--------------------------------------------------------------------

### Objective 4
~**Description**: Objective 4 is responsible for displaying people on the `People` page

* The `people_view` function uses lists and session variables to display users who are **NOT** friends of the currently logged in user
* The page displays 1 person at first and more are revealed upon clicking the **More** button
* The **More** button is linked to send an **AJAX POST** from the `people.js` file to the `people_view`
* The `people.djhtml` file renders the view and displays the other user's attributes
* The url path is routed as `path('people/', views.people_view,name='people_view')`

--------------------------------------------------------------------

### Objective 5
~**Description**: Objective 5 is responsible for allowing the user to send friend requests
* The `id` in `people.djhtml` is made unique to each username using the `forloop`
* The **Friend Request** button is disabled after it is clicked
* A `for loop` is used in the `people.djhtml` file to iterate over the `friend_requests` list and display the username of the people in that list
* The `friend_request_view` function uses the **UserInfo** and **FriendRequest** class to assign variables with list slicing to get the required fields.
* The `people_view` function uses the **FriendRequest** class to render the list in the loop and add it to our empty `size` list which is used in `people.djhtml` to display the users
* The url path is routed as `path('friendrequest/', views.friend_request_view,name='friend_request_view')`

--------------------------------------------------------------------

### Objective 6
~**Description**: Objective 6 is responsible for allowing the user to Accept or Decline the friend requests they receive.
* The `id` in `people.djhtml` is made unique to each username using the `forloop`
* The functions in `people.js` allow the user to Accept or Decline the request by sending **POST** requests to the `accept_decline_view` function with the corresponding button id
* The `accept_decline_view` function retrieves the `data` variable(`'decision'`), checking it's first and second index to then add the user who sent the friend request to the list of current user's friends, updating both their interfaces. Otherwise if the current user declined the request, it deletes it.
* The url path is routed as `path('acceptdecline/', views.accept_decline_view,name='accept_decline_view')`

~**Exception**: A `HttpResponseNotFound` is returned if a **POST** method was prematurely called without a `decision`

~**NOTE**: The user might have to double click the accept/decline button to allow the decision.

--------------------------------------------------------------------

### Objective 7
~**Description**: Objective 7 displays all the friends of the currently logged in user
* A `for loop` is used in `messages.djhtml` (`for f in user_info.friends.all)` to display the list of friends of the currently logged in user

--------------------------------------------------------------------

### Objective 8
~**Description**: Objective 8 allows the user the accesibility to submitting posts
* The functions in `messages.js` handle the **AJAX POST** request when the **Post** button is clicked. The contents are routed to `post_submit_view`
* The page is reloaded using `location.reload()` if the post was a success
* The `post_submit_view` function handles the submission of the post. A **POST** request is assigned to the `postContent` variable and using the **Post** class and it's attributes, it is added , then displayed on the *messages* page
* The contents of the **post-text** id are routed to the `post_submit_view`
* The url path is routed as `path('postsubmit/', views.post_submit_view,name='post_submit_view')`

~**Exception**: A `HttpResponseNotFound` is returned if a **POST** method was prematurely called without referencing `postContent`

--------------------------------------------------------------------

### Objective 9
~**Description**: Objective 9 handles the display of all the posts, inlcuding the logged in user's and their friend's.

* A `for loop` is used in `messages.djhtml` which uses the **Post** class to get the `owner, timestamp` and `content` of the post
* The `messages_view` function queries the posts and sorts them by recently posted using `timestamp` as the *primary key* and `order_by`
* Initially, the *messages* page displays only one post. Each time the **More** button is clicked, posts are displayed incrementally. 
* The **More** button is linked to the `more_post_view` function which uses a session counter to increment it by 1
* Once the user has logged out, the number of posts displayed are **reset**
* The url path is routed as `path('postsubmit/', views.post_submit_view,name='post_submit_view')`

~**Exceptions** If the session count is less than the `forloop counter`, the posts will not be displayed and instead the user will be redirected to the *login* page

--------------------------------------------------------------------

### Objective 10
~**Description**: Objective 10 gives the user the accessbility to like posts and view the likes count
* All posts initially have a like count of 0
* `messages.djhtml` contains the substituted variables and id for posts and the like count
* The user can only like a post **once** after which the like button is disabled
* A variable in the `like_view` function, `postIDReq` is assigned to retrieve the **POST** request of the `postID` and using the **Post** and **UserInfo** class splits at "_" and then added to the likes
* A boolean is used to check if a post has already been liked by the user and disables the button if it has
* The url path is routed as ` path('like/', views.like_view,name='like_view')`

~**Exceptions**: A `HttpResponseNotFound` is returned if a **POST** method is called prematurely without referencing the `postID` in `like_view`

--------------------------------------------------------------------

### Objective 11
~**Description**: Objective 11 is a Test Database containing pre-existing users, login credentials, user attributes, user friends, user posts and all the various functionality of the project.
#### Users and Login Credentials

|  Usernames    | Passwords   |
| ------------- |:-----------:|
| ***Merlin***  | pf2Yc9xvAS  |
| ***Dave***    | FcPYVZMsB6  |             
| ***Edwin***   | c4FPuPUCqW  |
| ***Candice*** | 6PFyBSt8V8  |
| ***Harry***   | rk4t9YpMxg  |
