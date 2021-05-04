from django.shortcuts import render, redirect
from .models import User, Wish
from django.contrib import messages
import bcrypt
from datetime import date
        # Create your views here.


def index(request):
    if 'user_id' in request.session:
        return redirect("/wishes")
    context = {
        'today': date.today()
    }
    return render(request, "index.html", context)


def wishes(request):
    if 'user_id' not in request.session:
        return redirect("/")
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "all_wishes": Wish.objects.all(),
        "user_Add_whish": Wish.objects.filter(add_by=User.objects.get(id=request.session['user_id'])),
    }
    return render(request, "wishes.html", context)


def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                
            return redirect("/")
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()).decode()  

        new_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            birthday=request.POST['birthday'],
            password=pw_hash)
        request.session['user_id'] = new_user.id
        return redirect("/wishes")  


def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        logged_user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = logged_user.id
        return redirect('/wishes')
    return redirect("/")
def index2(request):
    request.session.flush()
    return redirect("/")  

def new_wish(request):
    if 'user_id' not in request.session:
        return redirect("/")
    context={
        "user": User.objects.get(id=request.session['user_id']),
    }
    return render(request,"new_wish.html",context)
def creat_wish(request):
    if request.method == "POST":
        errors = Wish.objects.wish_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/wishes/new")
        Wish.objects.create(
            item_name =request.POST['name'],
            description =request.POST['desc'],
            add_by = User.objects.get(id=request.session['user_id'])
        )
    return redirect("/wishes")

def edit_wish(request, w_id):
    context = {
        'wish': Wish.objects.get(id= w_id)
    }
    return render(request, "edit.html", context)

def update_wish(request, w_id):
    if request.method == "POST":
        errors = Wish.objects.wish_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f"/wishes/{w_id}/edit")
        wish = Wish.objects.get(id= w_id)
        wish.item_name =request.POST['name']
        wish.description =request.POST['desc']
        wish.save()
    return redirect("/wishes")

def delete_wish(request, w_id):
    whish = Wish.objects.get(id= w_id)
    whish.delete()
    return redirect("/wishes")
def granted_wish(request, w_id):
    wish = Wish.objects.get(id= w_id)
    wish.granted_by = True
    wish.save()
    return redirect("/wishes")
def states(request):
    user = User.objects.get(id=request.session['user_id'])
    
    context ={
        "user": User.objects.get(id=request.session['user_id']),
        "all_user" :User.objects.all(),
        "all_wishes": Wish.objects.all(), 
        "all_granted_by": Wish.objects.filter(granted_by=True),
        "user_add_whish": Wish.objects.filter(granted_by=True , add_by= user.id), 
        "user_add_whishf": Wish.objects.filter(granted_by=False , add_by= user.id), 

            }
    return render(request,"states.html", context )

def like(request, w_id):
    user = User.objects.get(id=request.session['user_id'])
    wish = Wish.objects.get(id=w_id)
    wish.liked_by.add(user)
    return redirect("/wishes")
