from django.test import Client, TestCase

from .models import User, Following, Post

# Create your tests here.
class NetworkTestCase(TestCase):

    def setUp(self):
        
        #Create dummy users
        u1 = User.objects.create(username="user1")
        u2 = User.objects.create(username="user2")

    def test_users(self):
        self.assertEqual(User.objects.count(),2)
