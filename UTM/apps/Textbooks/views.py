from django.shortcuts import render, HttpResponse, redirect
from apps.log_reg.models import *
from .models import *


def index(request):
	context ={
				"books" : Book.objects.all()
	}
	return render(request, "Textbooks/mainpage.html", context);


def showbook(request, id):
	response = "Individual book page";
	return HttpResponse(response);


def addNewbook(request):
	response = "Add new book";
	return HttpResponse(response);


def editBookInfo(request, id):
	response = "Edit book page";
	return HttpResponse(response);


def deleteBook(request, id):
	response = "Delete book";
	return HttpResponse(response);