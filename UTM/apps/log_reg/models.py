from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['name']) < 5:
            errors["name"] = "Your name must be at least 6 characters"
        if len(postData['alias']) < 3:
            errors['alias'] = "Your alias name should be at least 3 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email must be valid"
        if len(postData['password']) < 1:
            errors['password'] = "Password cannot be blank"
        if postData['password'] != postData['passConfirm']:
            errors['confirm'] = "Password and confirm password do not match"
        if User.objects.filter(email=postData["email"]):
            errors['match'] = "This email already has an account"
        return errors

    def validLogin(self, postData, request):
        errors = {}
        if User.objects.filter(email=postData['emaillogin']):
            user = User.objects.get(email=postData['emaillogin'])
            if bcrypt.checkpw(request.POST['passwordlogin'].encode(), user.password.encode()):
                return errors
            errors['password'] = "Email and password do not match"
            return errors
        errors['email'] = "Email and password do not match"
        return errors


class User(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()