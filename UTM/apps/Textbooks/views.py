from django.shortcuts import render, HttpResponse, redirect
from apps.log_reg.models import *
from .models import *
from django.core.urlresolvers import reverse


def index(request):
	context ={
				"books" : Book.objects.all()
	}
	return render(request, "Textbooks/mainpage.html", context)


def show_sell(request, id):
	request.session['sells_id'] = id
	data ={
		'sells': Sells.objects.filter(id = id),
		'messages': Message.objects.filter(on_book = Sells.objects.get(id = id)),
		'comments': Comment.objects.filter(on_message = Message.objects.filter(on_book = Sells.objects.get(id = id))),
	 }
	return render(request, 'Textbooks/showbook.html', data)


def addNewbook(request):
	response = "Add new book"
	return HttpResponse(response)


def editBookInfo(request, id):
	response = "Edit book page"
	return HttpResponse(response)


def deleteBook(request, id):
	response = "Delete book"
	return HttpResponse(response)

def message(request):
	Message.objects.create(content = request.POST['message'], posted_by = User.objects.get(id = request.session['id']), on_book = Sells.objects.get(id = request.session['sells_id']))
	return redirect(reverse('showbook', kwargs={'id': request.session['sells_id'] }))

def comment(request):
	Comment.objects.create(content = request.POST['comment'], on_message = Message.objects.get(id = request.POST['message_id']))
	return redirect(reverse('showbook', kwargs={'id': request.session['sells_id'] }))
