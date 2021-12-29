from django.http import response
from django.test import Client, TestCase
import json

from .models import User, Following, Post

# Create your tests here.
class NetworkTestCase(TestCase):

    def setUp(self):
        
        #Create dummy users
        u1 = User.objects.create(username="user1")
        u2 = User.objects.create(username="user2")

        #Create dummy posts
        Post.objects.create(poster=u1, content="U1 post 1")
        Post.objects.create(poster=u1, content="U1 post 2")
        Post.objects.create(poster=u2, content="U2 post 1")

        #Create dummy following
        Following.objects.create(follower=u2, followed=u1)


    def test_users(self):
        self.assertEqual(User.objects.count(),2)

    def test_all_posts(self):
        c = Client()
        response = c.get("/posts/all")
        self.assertEqual(response.status_code, 201)
        #self.assertEqual(len(response.headers),3)

    def test_following_posts(self):
        c = Client()
        response = c.get("/posts/following")
        self.assertEqual(response.status_code, 400)
        #self.assertEqual(len(response.headers),3)

    def test_user_posts(self):
        c = Client()
        response = c.get("/posts/user1")
        self.assertEqual(response.status_code, 201)
        #self.assertEqual(len(response.headers),3)

    def test_following_true(self):
        u1 = User.objects.get(username="user1")
        u2 = User.objects.get(username="user2")
        self.assertTrue(u2.is_follower(u1))

    def test_following_false(self):
        u1 = User.objects.get(username="user1")
        u2 = User.objects.get(username="user2")
        self.assertFalse(u1.is_follower(u2))

    def test_like_true(self):
        u1 = User.objects.get(username="user1")
        u2 = User.objects.get(username="user2")
        post = Post.objects.get(poster=u1, content="U1 post 1")

        post.likes.add(u2)
        self.assertTrue(post.liked_by(u2))