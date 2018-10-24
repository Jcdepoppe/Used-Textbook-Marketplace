from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
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
    return redirect('/books')

def editpage(request, id):
    user = User.objects.get(id=id)
    data = {
        'name': user.name,
        'alias': user.alias,
        'email': user.email,
        'college': user.college,
    }
    return render(request, "log_reg/user.html", data)

def edit(request):
    if request.method =="POST":
        errors = User.objects.validEdit(request.POST, request)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(reverse('editpage', kwargs={'id': request.session['id'] }))
        update = User.objects.get(id = request.session['id'])
        update.name = request.POST['name']
        update.alias = request.POST['alias']
        update.email = request.POST['email']
        update.college = request.POST['college']
        update.save()
    return redirect('/books')

