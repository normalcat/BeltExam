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

        if len(post['first_name']) < 2:
            errors.append("First name should be longer than 2 characters\n")
        elif not post['first_name'].isalpha():
            errors.append("Fist name should not contain numbers\n")

        if len(post['last_name']) < 2:
            errors.append("Last name should be longer than 2 characters\n")
        elif not post['last_name'].isalpha():
            errors.append("Last name should not contain numbers\n")

        if len(post['alias']) < 2:
            errors.append("Alias should be longer than 2 characters\n")

        if len(post['password']) < 8:
            errors.append("Password needs to be at least 8 chars\n")
        elif post['password'] != post['cpassword']:
            errors.append("Password does not match\n")

        if len(post['email'])<1:
            errors.append("Email cannot be blank\n")
        elif not EMAIL_REGEX.match(post['email']):
            errors.append("Invalid email address\n")

        if  post['bday'] > str(date.today()):
            errors.append("Invalid birth day\n")

        if not errors:
            users = User.objects.filter(email=post['email'])
            if users:
                errors.append("This email has been registered")
        
        return errors

    def login_validate(self, post):
        try:
            single_user = User.objects.get(email=post['email'])
            if bcrypt.checkpw(post['password'].encode(), single_user.password.encode()):
                return single_user
        except:
            return False


    def new(self,post):
        X = bcrypt.hashpw(post['password'].encode(),bcrypt.gensalt())
        User.objects.create(first_name = post['first_name'],
                                last_name = post['last_name'],
                                alias = post['alias'],
                                email = post['email'].lower(),
                                bday = post['bday'],
                                password = X)
        new_user = User.objects.get(email = post['email'].lower())
        return new_user

    def poke(self, post, uid):
        poke_person = User.objects.get(id = uid)
        poked_person = User.objects.get(id = post['fid'])
        Poke.objects.create(poker = poke_person,
                            poked = poked_person)

        poke_person.poke_count = poke_person.poke_count + 1
        poke_person.save()
        poked_person.poked_by_count = poked_person.poked_by_count + 1
        poked_person.save()

        return self

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255, default="default")
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    friend_by = models.ManyToManyField("self", related_name = "friends")
    bday = models.DateField(default=0)
    poked_by_count = models.IntegerField(default = 0)
    poke_count = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Poke(models.Model):
    poker = models.ForeignKey(User, related_name = "pokes")
    poked = models.ForeignKey(User, related_name = "waspoked")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    