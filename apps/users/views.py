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
        return redirect('/pokes')
    except:
        messages.add_message(request, messages.INFO,"Please login\n")
        return redirect("/main")

def show(request,id):
    single_user = User.objects.get(id = id)
    data = {
        "single_user": single_user,
    }
    return render(request,'users/success.html',data)

def pokes(request):
    session_holder = User.objects.get(id = request.session['id'])
    result = Poke.objects.filter(poked = session_holder)

    poker_count = 0
    poked_list = {}
    for x in result:
        poker_count = poker_count + 1
        if poked_list.get(x.poker, 0) == 0:
            poked_list[x.poker] = 1
        else:    
            poked_list[x.poker] = poked_list[x.poker] + 1

    all_users = User.objects.exclude(id = request.session['id'])

    data = {
        "poker_count": poker_count,
        "all_users": all_users,
        "poked_list": poked_list,
    }
    print poker_count
    print all_users
    print poked_list
    return render(request,'users/pokes.html',data)

def poke(request):
    User.objects.poke(request.POST, request.session['id'])
    return redirect('/pokes')

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
        request.session['first_name'] = single_user.first_name
        request.session['last_name'] = single_user.last_name

        print request.session['id']
        print request.session['first_name']
        print request.session['last_name']
        return redirect("/users/success")

def login(request):
    single_user = User.objects.login_validate(request.POST)
    if single_user:
        request.session['id'] = single_user.id
        request.session['first_name'] = single_user.first_name
        request.session['last_name'] = single_user.last_name
        return redirect("/users/success")
    else:
        messages.add_message(request, messages.INFO,"Login fail\n")
        return redirect("/main")

def logout(request):
    request.session.clear()
    return redirect("/main")

