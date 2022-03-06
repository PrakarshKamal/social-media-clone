from django.http import HttpResponse,HttpResponseNotFound
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from datetime import datetime
from django.http import Http404
from . import models

def messages_view(request):
    """Private Page Only an Authorized User Can View, renders messages page
       Displays all posts and friends, also allows user to make new posts and like posts
    Parameters
    ---------
      request: (HttpRequest) - should contain an authorized user
    Returns
    --------
      out: (HttpResponse) - if user is authenticated, will render private.djhtml
    """
    if request.user.is_authenticated:
        user_info = models.UserInfo.objects.get(user=request.user)


        # TODO Objective 9: query for posts (HINT only return posts needed to be displayed)
        posts = []
        posts = list(models.Post.objects.all().order_by('-timestamp'))
        request.session['count'] = request.session.get('count', 1)
        # TODO Objective 10: check if user has like post, attach as a new attribute to each post

        context = { 'user_info' : user_info
                  , 'posts' : posts }
        return render(request,'messages.djhtml',context)

    request.session['failed'] = True
    return redirect('login:login_view')

def account_view(request):
    """Private Page Only an Authorized User Can View, allows user to update
       their account information (i.e UserInfo fields), including changing
       their password
    Parameters
    ---------
      request: (HttpRequest) should be either a GET or POST
    Returns
    --------
      out: (HttpResponse)
                 GET - if user is authenticated, will render account.djhtml
                 POST - handle form submissions for changing password, or User Info
                        (if handled in this view)
    """
    if not request.user.is_authenticated:
        redirect('login:login_view')

        # TODO Objective 3: Create Forms and Handle POST to Update UserInfo / Password

    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        return redirect('login:login_view')
    else:
        form = PasswordChangeForm(request.user)
        user_info = models.UserInfo.objects.get(user=request.user)
        context = { 'user_info' : user_info,
                    'form' : form }
    return render(request,'account.djhtml',context)

def update_view(request):
    if not request.user.is_authenticated:
        redirect('login:login_view')
    
    if request.method == 'POST':
        u_i = models.UserInfo.objects.get(user=request.user)
        employ = request.POST.get('employment', 'Unspecified')
        location = request.POST.get('location', 'Unspecified')
        bday = request.POST.get('birthday', 'None')
        intr = request.POST.get('interest')

        if models.Interest.objects.filter(label__iexact=intr):
            intr_instance = models.Interest.objects.filter(label__iexact=intr)
        else:
            intr_instance = models.Interest.objects.create(label=intr)

        u_i.employment = employ
        u_i.location = location
        u_i.birthday = bday
        u_i.interests.add(intr_instance)
        u_i.save()

        return redirect('social:messages_view')

    
    u_i = models.UserInfo.objects.get(user=request.user)

    context = {'user': request.user, 'update_form': form,
               'u_i': u_i, 
               'birth': birth, }
    return render(request, "account.djhtml", context)



def people_view(request):
    """Private Page Only an Authorized User Can View, renders people page
       Displays all users who are not friends of the current user and friend requests
    Parameters
    ---------
      request: (HttpRequest) - should contain an authorized user
    Returns
    --------
      out: (HttpResponse) - if user is authenticated, will render people.djhtml
    """
    if request.user.is_authenticated:

        user_info = models.UserInfo.objects.get(user=request.user)
        friends = list(user_info.friends.all())

        # TODO Objective 4: create a list of all users who aren't friends to the current user (and limit size)
        all_people = []
        size = []
        for p in models.UserInfo.objects.exclude(user=user_info.user):
            if p not in friends:
                all_people = all_people + [p]
        request.session['count'] = request.session.get('count', 1)
        i = request.session['count']
        all_people = all_people[:i]

        # TODO Objective 5: create a list of all friend requests to current user
        friend_requests = []
        for x in models.FriendRequest.objects.filter(to_user=models.UserInfo.objects.get(user=request.user)).all():
            friend_requests = friend_requests + [x.from_user]

        new = list(models.FriendRequest.objects.filter(from_user=user_info).all())

        for n in new:
            size = size + [n.to_user]
        
        context = { 'user_info' : user_info,
                    'all_people' : all_people,
                    'friend_requests' : friend_requests, 'size' : size}

        return render(request,'people.djhtml',context)

    request.session['failed'] = True
    return redirect('login:login_view')

def like_view(request):
    '''Handles POST Request recieved from clicking Like button in messages.djhtml,
       sent by messages.js, by updating the corrresponding entry in the Post Model
       by adding user to its likes field
    Parameters
	----------
	  request : (HttpRequest) - should contain json data with attribute postID,
                                a string of format post-n where n is an id in the
                                Post model

	Returns
	-------
   	  out : (HttpResponse) - queries the Post model for the corresponding postID, and
                             adds the current user to the likes attribute, then returns
                             an empty HttpResponse, 404 if any error occurs
    '''
    postIDReq = request.POST.get('likeID')
    if postIDReq is not None:
        # remove 'post-' from postID and convert to int
        # TODO Objective 10: parse post id from postIDReq
        

        if request.user.is_authenticated:
            r = postIDReq.split("#")
            u = models.UserInfo.objects.get(user=request.user)
            m = models.UserInfo.objects.get(user_id=int(r[1]))
            models.Post.objects.filter(owner=m).get(id=int(r[2])).likes.add(u)
            # TODO Objective 10: update Post model entry to add user to likes field

            # return status='success'
            return HttpResponse()
        else:
            return redirect('login:login_view')

    return HttpResponseNotFound('like_view called without postID in POST')

def post_submit_view(request):
    '''Handles POST Request recieved from submitting a post in messages.djhtml by adding an entry
       to the Post Model
    Parameters
	----------
	  request : (HttpRequest) - should contain json data with attribute postContent, a string of content

	Returns
	-------
   	  out : (HttpResponse) - after adding a new entry to the POST model, returns an empty HttpResponse,
                             or 404 if any error occurs
    '''
    postContent = request.POST.get('postContent')
    if postContent is not None:
        if request.user.is_authenticated:
            s = datetime.now().timestamp()
            m = models.UserInfo.objects.get(user=request.user)
            
            models.Post.objects.create(owner=m, content=postContent, timestamp=s)
            # TODO Objective 8: Add a new entry to the Post model

            # return status='success'
            return HttpResponse()
        else:
            return redirect('login:login_view')

    return HttpResponseNotFound('post_submit_view called without postContent in POST')

def more_post_view(request):
    '''Handles POST Request requesting to increase the amount of Post's displayed in messages.djhtml
    Parameters
	----------
	  request : (HttpRequest) - should be an empty POST

	Returns
	-------
   	  out : (HttpResponse) - should return an empty HttpResponse after updating hte num_posts sessions variable
    '''
    if request.user.is_authenticated:
        request.session['count'] += 1
        # update the # of posts dispalyed

        # TODO Objective 9: update how many posts are displayed/returned by messages_view

        # return status='success'
        return HttpResponse()

    return redirect('login:login_view')

def more_ppl_view(request):
    '''Handles POST Request requesting to increase the amount of People displayed in people.djhtml
    Parameters
	----------
	  request : (HttpRequest) - should be an empty POST

	Returns
	-------
   	  out : (HttpResponse) - should return an empty HttpResponse after updating the num ppl sessions variable
    '''
    if request.user.is_authenticated:
        request.session['count'] += 1
        # update the # of people dispalyed

        # TODO Objective 4: increment session variable for keeping track of num ppl displayed

        # return status='success'
        return HttpResponse()

    return redirect('login:login_view')

def friend_request_view(request):
    '''Handles POST Request recieved from clicking Friend Request button in people.djhtml,
       sent by people.js, by adding an entry to the FriendRequest Model
    Parameters
	----------
	  request : (HttpRequest) - should contain json data with attribute frID,
                                a string of format fr-name where name is a valid username

	Returns
	-------
   	  out : (HttpResponse) - adds an etnry to the FriendRequest Model, then returns
                             an empty HttpResponse, 404 if POST data doesn't contain frID
    '''
    frID = request.POST.get('frID')
    if frID is not None:
        frID = request.POST.get('frID')
        # remove 'fr-' from frID
        username = frID[3:]

        if request.user.is_authenticated:
            # TODO Objective 5: add new entry to FriendRequest
            username = frID[3:]
            f1 = models.UserInfo.objects.get(user=request.user)
            f2 = models.UserInfo.objects.get(user_id=username)
            f3 = models.FriendRequest.objects.create(to_user=f2, from_user=f1)
            # return status='success'
            return HttpResponse()
        else:
            return redirect('login:login_view')

    return HttpResponseNotFound('friend_request_view called without frID in POST')

def accept_decline_view(request):
    '''Handles POST Request recieved from accepting or declining a friend request in people.djhtml,
       sent by people.js, deletes corresponding FriendRequest entry and adds to users friends relation
       if accepted
    Parameters
	----------
	  request : (HttpRequest) - should contain json data with attribute decision,
                                a string of format A-name or D-name where name is
                                a valid username (the user who sent the request)

	Returns
	-------
   	  out : (HttpResponse) - deletes entry to FriendRequest table, appends friends in UserInfo Models,
                             then returns an empty HttpResponse, 404 if POST data doesn't contain decision
    '''
    data = request.POST.get('decision')
    if data is not None:
        # TODO Objective 6: parse decision from data

        if request.user.is_authenticated:
            if data[0] == "D":
                d = models.FriendRequest.objects.get(to_user=models.UserInfo.objects.get(user=request.user), from_user=models.UserInfo.objects.get(user_id=data[2:]))
                d.delete()
            elif data[0] == "A":
                models.UserInfo.objects.get(user=request.user).friends.add(models.UserInfo.objects.get(user_id=data[2:]))
                models.UserInfo.objects.get(user_id=data[2:]).friends.add(models.UserInfo.objects.get(user=request.user))
                a = models.FriendRequest.objects.get(to_user=models.UserInfo.objects.get(user=request.user), from_user=models.UserInfo.objects.get(user_id=data[2:]))
                a.delete()

            # TODO Objective 6: delete FriendRequest entry and update friends in both Users

            # return status='success'
            return HttpResponse()
        else:
            return redirect('login:login_view')

    return HttpResponseNotFound('accept-decline-view called without decision in POST')
