from django.shortcuts import render, HttpResponse, redirect
# from apps.login_reg.models import *
# from .models import *


def index(request):
	response = "Welcome to the dashboard";
	return render(request, "Textbooks/mainpage.html");


def showbook(request, id):
	response = "Individual book page";
	return HttpResponse(response);


def addAbook(request):
	response = "Add new book";
	return HttpResponse(response);


def editBookInfo(request, id):
	response = "Edit book page";
	return HttpResponse(response);