from django.shortcuts import render, HttpResponse, redirect
from apps.log_reg.models import *
from .models import *
from django.core.urlresolvers import reverse
from apps.log_reg.models import *
from django.db.models import Count


def index(request):
	if 'id' not in request.session:
		return redirect('/')
	user=User.objects.get(id=request.session['id'])
	wish_list = Wants.objects.filter(buyer=user)
	books_in_sales= Book.objects.annotate(sales=Count('for_sale')).filter(sales__gt=0)
	# items on my wishlist that have a matching for-sale item
	with_matches = wish_list.filter(book__id__in=books_in_sales)
	no_match = wish_list.exclude(id__in=with_matches)

	for_sale = Sells.objects.filter(seller=user).annotate(num_msg=Count('messages'))
	# items for sale with messages that have not been answered (will have a badge):
	with_unread_message = for_sale.filter(num_msg__gt=0).filter(messages__comments__isnull=True)
	rest_for_sale=for_sale.exclude(id__in=with_unread_message)
	context ={
		"fs_badge" : with_unread_message,
		"fs_rest" : rest_for_sale,
		"wl_badge": with_matches,
		"wl_rest" : no_match,

	}
	return render(request, "Textbooks/mainpage.html", context)


def show_sell(request, id):
	if 'id' not in request.session:
		return redirect('/')
	request.session['sells_id'] = id
	info = Sells.objects.get(id = id)
	data ={
		'info': info,
		'messages': Message.objects.filter(on_book = info),
		'comments': Comment.objects.filter(on_message = Message.objects.filter(on_book = info)),
	}
	return render(request, 'Textbooks/showbook.html', data)


# def addNewbook(request):
# 	if 'id' not in request.session:
# 		return redirect('/')
# 	response = "Add new book"
# 	return HttpResponse(response)


# def editBookInfo(request, id):
# 	if 'id' not in request.session:
# 		return redirect('/')
# 	response = "Edit book page"
# 	return HttpResponse(response)


# def deleteBook(request, id):
# 	if 'id' not in request.session:
# 		return redirect('/')
# 	response = "Delete book"
# 	return HttpResponse(response)

def message(request):
	if 'id' not in request.session:
		return redirect('/')
	Message.objects.create(content = request.POST['message'], posted_by = User.objects.get(id = request.session['id']), on_book = Sells.objects.get(id = request.session['sells_id']))
	return redirect(reverse('show_sell', kwargs={'id': request.session['sells_id'] }))

def comment(request):
	if 'id' not in request.session:
		return redirect('/')
	Comment.objects.create(content = request.POST['comment'], on_message = Message.objects.get(id = request.POST['message_id']))
	return redirect(reverse('show_sell', kwargs={'id': request.session['sells_id'] }))


def sell_book(request):
	if 'id' not in request.session:
		return redirect('/')
	
	return render(request, 'Textbooks/sell_book.html')


def sell_book_process(request):
	if 'id' not in request.session:
		return redirect('/')
	if request.method == "POST":
		user=User.objects.get(id=request.session['id'])
		#  We should search for ISBN number only (since it is unique to every book type and edition)
		book_exists = Book.objects.filter(
			# title=request.POST['title'], 
			# author=request.POST['author'],
			# publisher=request.POST['publisher'],
			ISBN=request.POST['ISBN'],
		)
		if len(book_exists)>0:
			book=book_exists[0]
		else:
			book=Book.objects.create(
				title=request.POST['title'],
				author=request.POST['author'],
				publisher=request.POST['publisher'],
				ISBN=request.POST['ISBN'],
				cover=request.POST['cover']
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
	context ={
		'sale': Sells.objects.get(id = id)
	}
	return render(request, 'Textbooks/edit_sell.html', context)

def update_sell(request):
	if 'id' not in request.session:
		return redirect('/')
	if request.method =="POST":
		update = Sells.objects.get(id = request.POST['sale_id'])
		update.condition = request.POST['condition']
		update.description = request.POST['description']
		if 'picture' in request.FILES:
			update.picture = request.FILES['picture']
		update.price = float(request.POST['price'])*100

		book_exists = Book.objects.filter(
			# title=request.POST['title'], 
			# author=request.POST['author'],
			# publisher=request.POST['publisher'],
			ISBN=request.POST['ISBN'],
		)
		if len(book_exists)>0:
			book=book_exists[0]
		else:
			book=Book.objects.create(
				title=request.POST['title'],
				author=request.POST['author'],
				publisher=request.POST['publisher'],
				ISBN=request.POST['ISBN'],
				cover= request.POST['cover']
			)
		update.book = book
		update.save()
	return redirect('/books')



def delete_sell(request, id):
	if 'id' not in request.session:
		return redirect('/')
	delete = Sells.objects.get(id = id)
	delete.delete()
	return redirect('/books')


def show_want(request, id):
	if 'id' not in request.session:
		return redirect('/')
	request.session['sells_id'] = id
	want = Wants.objects.get(id = id)
	matches = Sells.objects.filter(book=want.book).filter(price__lte=want.price).filter(condition__gte=want.condition)
	number_of_matches = matches.count()
	context ={
		'info': want,
		'sells_info' : matches,
		'number_of_matches' : number_of_matches
	}
	return render(request, 'Textbooks/view_wantbook.html', context)


def want_book(request):
	if 'id' not in request.session:
		return redirect('/')
	
	return render(request, 'Textbooks/want_book.html')

def want_book_process(request):
	if 'id' not in request.session:
		return redirect('/')
	if request.method == "POST":
		user = User.objects.get(id=request.session['id'])
		book_exists = Book.objects.filter(
			# title=request.POST['title'],
			# author=request.POST['author'],
			# publisher=request.POST['publisher'],
			ISBN=request.POST['ISBN'],
		)
		if len(book_exists) > 0:
			book = book_exists[0]
		else:
			book = Book.objects.create(
				title=request.POST['title'],
				author=request.POST['author'],
				publisher=request.POST['publisher'],
				ISBN=request.POST['ISBN'],
			)
		want = Wants.objects.create(
			buyer=user,
			book=book,
			condition=request.POST['condition'],
			price=float(request.POST['price'])*100
		)
	return redirect('/books')



def edit_want(request, id):
	if 'id' not in request.session:
		return redirect('/')

	context={
		'item': Wants.objects.get(id=id),
	}
	return render(request, 'Textbooks/edit_wantbook.html', context)


def want_book_update(request):
	if 'id' not in request.session:
		return redirect('/')
	user = User.objects.get(id=request.session['id'])
	want = Wants.objects.get(id=id)
	book_exists = Book.objects.filter(
			ISBN=request.POST['ISBN'],
        )
	if len(book_exists) > 0:
		book = book_exists[0]
	else:
		book = Book.objects.create(
			title=request.POST['title'],
			author=request.POST['author'],
			publisher=request.POST['publisher'],
			ISBN=request.POST['ISBN'],
		)
	
	want.buyer = user
	want.book = book
	want.condition = request.POST['condition']
	want.price = float(request.POST['price'])*100
	want.save()
	return redirect('/books')


def delete_want(request, id):
	if 'id' not in request.session:
		return redirect('/')
	want = Wants.objects.get(id=id)
	want.delete()
	return redirect('/books')


def sold(request):
	if 'id' not in request.session:
		return redirect('/')
	if request.method == "POST":
		user = User.objects.get(id=request.session['id'])
		buyer = User.objects.get(id=request.POST['buyer_id'])
		item = Sells.objects.get(id=request.POST['item_id'])
		item.sold = True
		item.buyer_email = buyer.email
		item.save()
		sold_comment = "SOLD to " + buyer.alias 
		Comment.objects.create(content=sold_comment, on_message=Message.objects.get(
			id=request.POST['message_id']))
		# request.session['buyer_id']=request.POST['buyer_id']
		return redirect('/books/sell/'+str(item.id)+'/show')
	return redirect('/books')
