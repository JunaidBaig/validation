from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def home(request):
    return render(request, "valid/index.html")

def register(request):
    errors = User.objects.register(request.POST)
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect("/")
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(email=request.POST['email'].lower(), password=pw_hash)
        request.session['user_id'] = user.id
        return redirect("/success")    

def login(request):
    errors = User.objects.login(request.POST)
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect("/")
    else:
        user = User.objects.filter(email=request.POST['email'].lower())
        if len(user) < 1:
            messages.error(request, "No User for that email")
            return redirect("/")
        
        if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
            print(f"LOG - Setting session value 'user_id' = {user[0].id}")
            request.session['user_id'] = user[0].id
            return redirect("/success")
        else:
            messages.error(request, "Incorrect Password!")
            return redirect("/")

def logout(request):
    request.session.clear()
    messages.success(request, "Log out successful!")
    print(f"LOG - Log out successful, redirecting to home")  
    return redirect("/")

def success(request):
    context = {
        "user_id" : request.session['user_id']
    }
    print(f"LOG - Rendering success page")
    return render(request, "valid/success.html", context)