import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt




from .models import Post, User


def index(request):
    return render(request, "network/index.html")


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

    return JsonResponse({"message": "Post saveds successfully."}, status=201)

@login_required
def get_posts(request, set_name):
    
    #Filter posts based on set_name
    if set_name == "all":
        posts = Post.objects.all()
    elif set_name == "following":
        posts = Post.objects.filter(poster__in = request.user.follows.all())
    elif set_name == "own":
        posts = Post.objects.filter(poster = request.user)
    else:
        return JsonResponse({"error": "Invalid set of posts"}, status=400)

    #return posts in reverse chronological order
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)