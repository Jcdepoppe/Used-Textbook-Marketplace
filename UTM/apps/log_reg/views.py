from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
    request.session['test'] = 0
    request.session.clear()
    return render(request, "log_reg/index.html")

def register(request):
    if request.method == "POST":
        errors = User.objects.validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        pass_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], college=request.POST['college'], password=pass_hash)
        user = User.objects.last()
        request.session['id'] = user.id
        request.session['name'] = user.name
        return redirect('/success')
    return redirect('/')

def login(request):
    if request.method =="POST":
        errors = User.objects.validLogin(request.POST, request)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        user = User.objects.get(email=request.POST['emaillogin'])
        request.session['id'] = user.id
        request.session['name'] = user.name
        return redirect('/success')
    return redirect('/')

def success(request):
    user = User.objects.get(id=request.session['id'])
    response = 'Main dashboard ' + user.name
    return HttpResponse(response)

def editpage(request, id):
    data = {
        'user': User.objects.filter(id = id)
    }
    return render(request, "log_reg/user.html", data)

