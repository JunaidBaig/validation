from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# regex requires at least 1 number, capital letter, lower case letter, permits some special characters !@#$%^&*+= and must be 8 characters or longer
PASSWORD_REGEX = re.compile(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d,!@#$%^&*+=]{8,}$')

class UserManager(models.Manager):
    def register(self, postData):
        alerts = []

        if len(postData['email']) < 1:
            messages.append('Email is required!')
        elif not EMAIL_REGEX.match(postData['email']):
            messages.append('Invalid Email!')
        else:
            check = User.objects.filter(email=postData['email'].lower())
            if len(check) > 0:
                messages.append('Email already in use!')

        if len(postData['password']) < 1:
            messages.append('Password is required!')
        elif not PASSWORD_REGEX.match(postData['password']):
            messages.append('Password must contain at least 1 number and capitalization!')

        if len(postData['password_confirm']) < 1:
            messages.append('Confirm password is required!')
        elif postData['password_confirm'] != postData['password']:
            messages.append('Password must match Confirm password!')

        return messages

    def login(self, postData):
        messages = []

        if len(postData['email']) < 1:
            messages.append('Email is required!')

        if len(postData['password']) < 1:
            messages.append('Password is required!')

        return messages

class User(models.Model):
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    def __repr__(self):
        return f"<User object: {self.email}>"
