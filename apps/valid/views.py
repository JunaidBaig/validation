from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# render home page
def home(request):
    return render(request, "valid/index.html")

#process registration and redirect
def register(request):
    errors = User.objects.register(request.POST)
    if len(errors) > 0:
        for key,error in errors.items():
            messages.error(request, error)
        return redirect("/")
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(email=request.POST['email'].lower(), password=pw_hash)
        request.session['user_id'] = user.id
        messages.success(request, "Registered successfully :)")
        return redirect("/success")    

# process login info and redirect
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

# logout and redirect
def logout(request):
    request.session.clear()
    messages.success(request, "Log out successful!")
    print(f"LOG - Log out successful, redirecting to home")  
    return redirect("/")

# render success page
def success(request):
    if 'user_id' not in request.session:
        messages.error(request, "Permission Denied")
        return redirect("/")
    context = {
        "user_id" : request.session['user_id']
    }
    print(f"LOG - Rendering success page")
    return render(request, "valid/success.html", context)