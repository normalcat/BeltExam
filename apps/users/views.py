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
        return redirect('/travels')
    except:
        messages.add_message(request, messages.INFO,"Please login\n")
        return redirect("/main")

def destination(request,tid):
    single_trip = Trip.objects.get(id = tid)
    joined_by_list = single_trip.joined_by.all()

    data = {
        "single_trip": single_trip,
        "joined_by_list": joined_by_list,
    }
    return render(request,'users/destination.html',data)

def travels(request):
    user = User.objects.get(id = request.session['id'])
    trip_list = Trip.objects.filter(joined_by=user)
    all_trips = Trip.objects.exclude(joined_by=user)

    data = {
        "all_trips": all_trips,
        "trip_list": trip_list,
    }
    return render(request,'users/travels.html',data)

def insert(request,tid):
    Trip.objects.join_trip(tid, request.session['id'])
    return redirect('/travels')

def add(request):
    data = {

    }
    return render(request,'users/add.html',data)

def create_trip(request):
    error = Trip.objects.trip_validate(request.POST)
    if error:
        for x in error:
            messages.add_message(request, messages.INFO,x)
        return redirect("/travels/add")
    Trip.objects.trip_new(request.POST, request.session['id'])
    return redirect('/travels')

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

