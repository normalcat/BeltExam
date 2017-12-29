from django.shortcuts import render, redirect
import bcrypt
import re
from models import *
from django.contrib import messages

#=============================================================#
#                       RENDER METHODS                        #
#=============================================================#
def index(request):
    return render(request,"users/index.html")

def success(request):
    try:
        single_user = User.objects.get(id = request.session['id'])
        data = {
            "single_user": single_user
        }
        return redirect('/dashboard')
    except:
        messages.add_message(request, messages.INFO,"Please login\n")
        return redirect("/main")

def show(request,id):
    single_item = Wishitem.objects.get(id = id)
    wished_by_list = single_item.wished_by.all()

    data = {
        "single_item": single_item,
        "wished_by_list": wished_by_list,
    }
    return render(request,'users/success.html',data)

def dashboard(request):
    user = User.objects.get(id = request.session['id'])
    wish_list = Wishitem.objects.filter(wished_by=user)
    all_wishes = Wishitem.objects.exclude(wished_by=user)

    data = {
        "all_wishes": all_wishes,
        "wish_list": wish_list,
    }
    return render(request,'users/dashboard.html',data)

def insert(request):
    users = User.objects.exclude(id=request.session['id'])
    data = {
        'users' : users,
    }
    return render(request,'users/add_item.html',data)

def add_item(request):
    print request.POST['item_name']
    error = Wishitem.objects.item_validate(request.POST)
    if error:
        for x in error:
            messages.add_message(request, messages.INFO,x)
        return redirect("users/add_item.html")
    Wishitem.objects.item_new(request.POST, request.session['id'])
    return redirect('/dashboard')

def add_wish(request):
    Wishitem.objects.add_wish(request.POST['iid'], request.session['id'])
    return redirect('/dashboard')

def del_wish(request):
    Wishitem.objects.del_wish(request.POST['iid'], request.session['id'])
    return redirect('/dashboard')

def del_item(request):
    Wishitem.objects.del_item(request.POST['iid'], request.session['id'])
    return redirect('/dashboard')


#=============================================================#
#                      PROCESS METHODS                        #
#=============================================================#
def create(request):
    error = User.objects.validate(request.POST)
    if error:
        for x in error:
            messages.add_message(request, messages.INFO,x)
        return redirect("/main")
    else:
        single_user = User.objects.new(request.POST)
        request.session['id'] = single_user.id
        request.session['name'] = single_user.name

        return redirect("/users/success")

def login(request):
    single_user = User.objects.login_validate(request.POST)
    if single_user:
        request.session['id'] = single_user.id
        request.session['name'] = single_user.name
        print request.session['name']
        return redirect("/users/success")
    else:
        messages.add_message(request, messages.INFO,"Login fail\n")
        return redirect("/main")

def logout(request):
    request.session.clear()
    return redirect("/main")

