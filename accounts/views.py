from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import login, logout
from django.contrib import messages


def login_view(request):

    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect("home")
        
    else:
       
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})

def register_view(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(request, "Registration successful! You are now logged in.")

            return redirect("home")

    else:

        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


def logout_view(request):
    
    logout(request)
    return redirect("home")