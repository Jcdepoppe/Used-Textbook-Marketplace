from django.shortcuts import render, HttpResponse, redirect
from apps.log_reg.models import *
from .models import *
from django.core.urlresolvers import reverse
from apps.log_reg.models import *


def index(request):
	if 'id' not in request.session:
		return redirect('/')
	user=User.objects.get(id=request.session['id'])
	context ={
		"for_sale" : Sells.objects.filter(seller=user),
		"wish_list": Wants.objects.filter(buyer=user),
	}
	return render(request, "Textbooks/mainpage.html", context)


def show_sell(request, id):
	request.session['sells_id'] = id
	info = Sells.objects.get(id = id)
	data ={
		'info': info,
		'messages': Message.objects.filter(on_book = info),
		'comments': Comment.objects.filter(on_message = Message.objects.filter(on_book = info)),
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
	return redirect(reverse('show_sell', kwargs={'id': request.session['sells_id'] }))

def comment(request):
	Comment.objects.create(content = request.POST['comment'], on_message = Message.objects.get(id = request.POST['message_id']))
	return redirect(reverse('show_sell', kwargs={'id': request.session['sells_id'] }))


def sell_book(request):
	
	return render(request, 'Textbooks/sell_book.html')


def sell_book_process(request):
	if request.method == "POST":
		user=User.objects.get(id=request.session['id'])
		book_exists = Book.objects.filter(
			title=request.POST['title'], 
			author=request.POST['author'],
			edition=int(request.POST['edition']),
			publisher=request.POST['publisher'],
			ISBN=request.POST['ISBN'],
		)
		if len(book_exists)>0:
			book=book_exists[0]
		else:
			book=Book.objects.create(
				title=request.POST['title'],
				author=request.POST['author'],
				edition=float(request.POST['edition']),
				publisher=request.POST['publisher'],
				ISBN=request.POST['ISBN'],
			)
		if 'picture' in request.FILES:
			picture = request.FILES['picture']
		else:
			picture = None # I have a default pic...
		sell= Sells.objects.create(
			book=book, 
			seller=user, 
			condition=request.POST['condition'],
			price=float(request.POST['price'])*100,
			picture= picture,
			description=request.POST['description'],
		)
	return redirect('/books')


def edit_sell(request, id):
	data ={
		'book': Sells.objects.get(id = id)
	}
	return render(request, 'Textbooks/edit_sell.html', data)

def update_sell(request):
	if request.method =="POST":
		update = Sells.objects.get(id = request.POST['book_id'])
		update.condition = request.POST['condition']
		update.description = request.POST['description']
		if 'picture' in request.FILES:
			update.picture = request.FILES['picture']
		update.price = float(request.POST['price'])*100

		book_exists = Book.objects.filter(
			title=request.POST['title'], 
			author=request.POST['author'],
			edition=int(request.POST['edition']),
			publisher=request.POST['publisher'],
			ISBN=request.POST['ISBN'],
		)
		if len(book_exists)>0:
			book=book_exists[0]
		else:
			book=Book.objects.create(
				title=request.POST['title'],
				author=request.POST['author'],
				edition=int(request.POST['edition']),
				publisher=request.POST['publisher'],
				ISBN=request.POST['ISBN'],
			)
		update.book = book
		update.save()
	return redirect('/books')



def delete_sell(request, id):
	delete = Sells.objects.get(id = id)
	delete.delete()
	return redirect('/books')


def show_want(request, id):
	response = "Individual wishlist book page"
	return HttpResponse(response)


def want_book(request):
	response = "Add want book page"
	return HttpResponse(response)


def want_book_process(request):
	response = "Processing want book form"
	return HttpResponse(response)


def edit_want(request, id):
	response = "Edit want book page"
	return HttpResponse(response)


def delete_want(request, id):
	response = "Delete want book"
	return HttpResponse(response)
