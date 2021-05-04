from django.db import models
import re
import bcrypt
from datetime import datetime, timedelta
    # Create your models here.


class UserManager(models.Manager):
    def register_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters"

        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"

        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email "

        if len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"

        if post_data['password'] != post_data['confirm_pw']:
            errors['confirm_pw'] = "Confirm password does not match your Password"

        # year = timedelta(days=365)
        # thirteen_years = 13 * year
        # birthday = datetime.strptime(post_data['birthday'], '%Y-%m-%d')
        # if birthday > datetime.today() - thirteen_years:
        #             errors['birthday'] = "You must be at least 13 years old"

        user_list = User.objects.filter(email=post_data['email'])
        if len(user_list) > 0:
            errors['not_unique'] = "Email is already registered "
        return errors

    def login_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email format"

        if len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"

        user_list = User.objects.filter(email=post_data['email'])
        if len(user_list) == 0:
            errors['email_2'] = "Email was not found in database"
        elif not bcrypt.checkpw(post_data['password'].encode(), user_list[0].password.encode()):
            errors['match'] = "Password does not match the database"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45, unique=True)
    birthday = models.DateField(default=datetime.now())
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class WishManager(models.Manager):
    def wish_validator(self, post_data):
        errors = {}
        if len(post_data['name']) == 0:
            errors['name2'] = "A wish must be provided !"
        elif len(post_data['name']) < 3:
            errors['name'] = "A wish must consist of  at least 3 characters"
        if len(post_data['desc']) == 0 :
            errors['desc'] = "A description must be provided !"
        elif len(post_data['desc']) < 3:
            errors['desc2'] = "A description must at least 3 characters"

        return errors

class Wish(models.Model):
    item_name = models.CharField(max_length=45)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    add_by = models.ForeignKey(User, related_name="wish", on_delete=models.CASCADE)
    granted_by =  models.BooleanField(default=False)
    liked_by = models.ManyToManyField(User, related_name="liked_wish")
    objects = WishManager()
