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

        if  post['date_hired'] > str(date.today()):
            errors.append("Invalid hired date\n")

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
                            date_hired = post['date_hired'],
                            password = X)
        new_user = User.objects.get(username = post['username'].lower())
        return new_user

class ItemManager(models.Manager):
    def item_validate(self,post):
        errors = []

        if len(post['item_name']) < 2:
            errors.append("Item name should be at least 2 characters\n")

        if not errors:
            item = Wishitem.objects.filter(item_name=post['item_name'])
            if item:
                errors.append("This item has been created by other users")

    def item_new(self,post,uid):
        created_user = User.objects.get(id = uid)
        item = Wishitem.objects.create(item_name = post['item_name'],
                                created_by = created_user)
        item.wished_by.add(created_user)
        return self

    def add_wish(self,iid,uid):
        single_user = User.objects.get(id = uid)
        item = Wishitem.objects.get(id = iid)
        item.wished_by.add(single_user)
        return self

    def del_wish(self,iid,uid):
        single_user = User.objects.get(id = uid)
        item = Wishitem.objects.get(id = iid)
        item.wished_by.remove(single_user)
        return self

    def del_item(self,iid):
        item = Wishitem.objects.get(id = iid)
        item.delete()
        return self

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, default="default")
    password = models.CharField(max_length=255)
    date_hired = models.DateField(default=0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Wishitem(models.Model):
    item_name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name = "creates")
    wished_by = models.ManyToManyField(User, related_name = "wishes")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ItemManager()
    