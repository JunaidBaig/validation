from django.db import models
import re

class UserManager(models.Manager):
    def register(self, postData):

        #RegEx for email
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        #RegEx for Password
        PASSWORD_REGEX = re.compile(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d,!@#$%^&*+=]{8,}$')

        errors = {}

        if len(postData['email']) < 1:
            errors['email'] = 'Email is required!'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email-invalid'] = 'Invalid Email!'
        check = User.objects.filter(email=postData['email'].lower())
        if len(check) > 0:
            errors['email-inuse'] = 'Email already in use!'

        if len(postData['password']) < 1:
            errors['password'] = 'Password is required!'
        elif not PASSWORD_REGEX.match(postData['password']):
            errors['password_valid'] = 'Password must contain at least 1 number and capitalization!'

        if len(postData['password_confirm']) < 1:
            errors['password_confirm'] = 'Confirm password is required!'
        elif postData['password_confirm'] != postData['password']:
            errors['passwords_match'] = 'Password must match Confirm password!'

        return errors

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
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    def __repr__(self):
        return f"<User object: {self.email}>"
