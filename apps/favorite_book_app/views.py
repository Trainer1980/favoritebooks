from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
    return render(request, 'index.html')

def registration(request):
    errors = User.objects.regis_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = pw_hash)
        messages.success(request, "Registered Successfully. Log in to continue.")
        return redirect('/')

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user'] = user.id
            request.session['first_name'] = user.first_name
            return redirect('/books')
        else:
            messages.error(request, "Wrong password")
            return redirect('/')
    else:
        messages.error(request, "Email not registered")
        return redirect('/')

def main(request):
    if 'user' in request.session:
        user = User.objects.get(id=request.session['user'])
        books = Book.objects.all().order_by('-created_at')
        context = {
            "user" : user,
            "books" : books,
        }
        return render (request, 'main.html', context)
    else:
        return redirect('/')

def fav(request, id):
    if 'user' in request.session:
        this_user = User.objects.get(id=request.session['user'])
        this_book = Book.objects.get(id=id)
        if 'user' in Book.objects.get(id=id).users_who_like.all():
            this_user.liked_books.remove(this_book)
            return redirect(f'/books/{id}')
        elif 'user' not in Book.objects.get(id=id).users_who_like.all():
            this_user.liked_books.add(this_book)
            return redirect(f'/books/{id}')
    else:
        return redirect('/')

def new(request):
    if 'user' in request.session:
        errors = Book.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books')
        else:
            title = request.POST['title']
            desc = request.POST['desc']
            this_user = User.objects.get(id=request.session['user'])
            this_book = Book.objects.create(title=title, desc=desc, uploaded_by=this_user)
            this_user.liked_books.add(this_book)
            messages.success(request, "Book was successfully added")
            return redirect('/books')
    else:
        return redirect('/')

def book(request, id):
    if 'user' in request.session:
        user = User.objects.get(id=request.session['user'])
        book = Book.objects.get(id=id)
        users = Book.objects.get(id=id).users_who_like.all()
        context = {
            'user' : user,
            'book' : book,
            'users' : users,
        }
        if book in user.books_uploaded.all():
            return render(request, 'book_info_user.html', context)
        else:
            return render(request, 'book_info.html', context)
    else:
        return redirect('/')
            
def update(request, id):
    if 'user' in request.session:
        errors = Book.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            book = Book.objects.get(id=id)
            return redirect(f'/books/{id}')
        else:
            if 'update' in request.POST:
                this_book = Book.objects.get(id=id)
                this_book.title = request.POST['title']
                this_book.desc = request.POST['desc']
                this_book.save()
                messages.success(request, "Book updated successfully")
                return redirect('/books')
            elif 'delete' in request.POST:
                this_book = Book.objects.get(id=id)
                this_book.delete()
                messages.success(request, "Book successfully deleted")
                return redirect('/books')
    else:
        return redirect('/')

def user(request):
    user = User.objects.get(id=request.session['user'])
    books = User.objects.get(id=request.session['user']).liked_books.all()
    context = {
        'user' : user,
        'books' : books,
    }
    return render(request, 'user.html', context)

def logout(request):
    if 'user' in request.session:
        request.session.clear()
        messages.success(request, "You have successfully signed out")
        return redirect('/')
    else:
        return redirect('/')
