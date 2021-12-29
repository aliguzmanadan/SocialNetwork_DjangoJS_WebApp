import json
from django.contrib.auth import authenticate, login, logout
from django.core import paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import Following, Post, User


def index(request):
    all_posts = Post.objects.all()
    all_posts = all_posts.order_by("-timestamp").all()
    paginator = Paginator(all_posts, 10)

    if request.GET.get('page'):
        page_number = request.GET.get('page')
    else: 
        page_number = 1

    page_obj = paginator.get_page(page_number)
    return render(request, 'network/index.html', {
        'page_obj': page_obj
    })
  
def following(request):

    #Get the posts of followed users, if no posts display message
    posts = Post.objects.filter(poster__in = request.user.set_following())
    if posts.count() == 0:
        return render(request, 'network/following.html', {
            "message": "No users followed so far"
        })

    posts = posts.order_by("-timestamp").all()
    paginator = Paginator(posts, 10)

    if request.GET.get('page'):
        page_number = request.GET.get('page')
    else: 
        page_number = 1

    page_obj = paginator.get_page(page_number)
    return render(request, 'network/following.html', {
        'page_obj': page_obj
    })


def user_page(request, username):

    #Get user and check if it is being followed
    user_to_view = User.objects.get(username = username)
    if request.user.is_authenticated:
        followed_status = request.user.is_follower(user_to_view)
    else:
        followed_status = None

    #Get posts, if no posts display message
    posts = Post.objects.filter(poster = user_to_view)
    if posts.count() == 0:
        return render(request, 'network/user_page.html', {
            "user_to_view": user_to_view,
            "message": "No posts so far for this user",
            "followed_status": followed_status
        })

    posts = posts.order_by("-timestamp").all()
    paginator = Paginator(posts, 10)

    if request.GET.get('page'):
        page_number = request.GET.get('page')
    else: 
        page_number = 1
    
    page_obj = paginator.get_page(page_number)

    return render(request, "network/user_page.html", {
        "user_to_view": user_to_view, 
        'page_obj': page_obj,
        "followed_status": followed_status
    })


def follow_unfollow(request, username):
    another_user=User.objects.get(username=username)
    if request.user.is_follower(another_user):
        Following.objects.filter(followed = another_user, follower = request.user).delete()
    else:
        f = Following(followed = another_user, follower = request.user)
        f.save()
    
    return HttpResponseRedirect(reverse("user_page", args=(username,)))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")




#########################################################################
#API views

@csrf_exempt
@login_required
def new_post(request):

    #making new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    # Get content of post
    data = json.loads(request.body)
    content = data["content"]
    
    #Create and save new post
    new_post = Post(poster = request.user, content=content)
    new_post.save()

    return JsonResponse({"message": "Post saved successfully."}, status=201)


def get_posts(request, set_name):
    
    #Filter posts based on set_name
    if set_name == "all":
        posts = Post.objects.all()
    elif set_name == "following":
        try: 
            posts = Post.objects.filter(poster__in = request.user.set_following())
        except:
            return JsonResponse({"error": "No users followed so far"}, status=400)
    else:
        #Check for particular user
        try: 
            user = User.objects.get(username = set_name)
        except User.DoesNotExist:
            return JsonResponse({"error": "Set of posts not found"}, status=400)

        #If the user exists then take all posts made by him
        posts = Post.objects.filter(poster = user)

    #return posts in reverse chronological order
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False, status=201)

@csrf_exempt
@login_required
def individual_post(request, post_id):

    #Querey for requested post
    try:
        post = Post.objects.get(poster=request.user, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    #Update content of post
    if request.method == "PUT":
        data = json.loads(request.body)
        post.content = data["content"]
        post.save()
        return JsonResponse({"message": "Post edited successfully."}, status=201)

    #Request musb use only put request
    else:
        return JsonResponse({"error": "PUT request reqired"}, status=400)