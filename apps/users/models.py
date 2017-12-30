from __future__ import unicode_literals

from django.db import models
import bcrypt
import re
from django.contrib import messages
from datetime import date, datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def validate(self,post):
        errors = []

        if len(post['name']) < 2:
            errors.append("First name should be longer than 2 characters\n")
        elif not post['name'].isalpha():
            errors.append("Fist name should not contain numbers\n")

        if len(post['username']) < 5:
            errors.append("Username should be at least 5 characters\n")

        if len(post['password']) < 8:
            errors.append("Password needs to be at least 8 chars\n")
        elif post['password'] != post['cpassword']:
            errors.append("Password does not match\n")

        if not errors:
            users = User.objects.filter(username=post['username'])
            if users:
                errors.append("This username has been registered")
        
        return errors

    def login_validate(self, post):
        try:
            single_user = User.objects.get(username=post['username'].lower())
            if bcrypt.checkpw(post['password'].encode(), single_user.password.encode()):
                return single_user
        except:
            return False


    def new(self,post):
        X = bcrypt.hashpw(post['password'].encode(),bcrypt.gensalt())
        User.objects.create(name = post['name'],
                            username = post['username'].lower(),
                            password = X)
        new_user = User.objects.get(username = post['username'].lower())
        return new_user

class TripManager(models.Manager):
    def trip_validate(self,post):
        errors = []

        if len(post['dest']) < 2:
            errors.append("Destination name should be at least 2 characters\n")

        if len(post['desc']) < 2:
            errors.append("Please give a short description about this trip\n")

        if  post['travel_from'] < str(date.today()):
            errors.append("Invalid travel start date\n")

        if post['travel_from'] > post['travel_end']:
            errors.append("Invalid travel end date\n")

        return errors

    def trip_new(self,post,uid):
        created_user = User.objects.get(id = uid)
        trip = Trip.objects.create(destination = post['dest'],
                                    description = post['desc'],
                                    travel_from = post['travel_from'],
                                    travel_end = post['travel_end'],
                                    created_by = created_user)
        trip.joined_by.add(created_user)
        return self

    def join_trip(self,tid,uid):
        single_user = User.objects.get(id = uid)
        single_trip = Trip.objects.get(id = tid)
        single_trip.joined_by.add(single_user)
        return self

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, default="default")
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    travel_from = models.DateField(default=0)
    travel_end = models.DateField(default=0)
    created_by = models.ForeignKey(User, related_name = "creates")
    joined_by = models.ManyToManyField(User, related_name = "joins")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TripManager()
