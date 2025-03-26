# views.py
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from user_app   .models import UserProfile
from django.contrib.auth import login, logout
from admin_app.models import UserActivity

# define page renders here
def home(request):
    return render(request, 'tripcraft.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# Handle user registration (Atheen)
def user_register(request):
    if request.method == "POST":
        # Retreive data from register form
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        gender = request.POST.get("gender")
        terms = request.POST.get("agree")

        # Validation Checks
        # Empty fields?
        if not all ([username, email, password, gender]):
            messages.error(request, "Please fill out all fields")
        # Agreed to terms?
        elif not terms:
            messages.error(request, "You must agree to the terms of service to make an account")
        # Email/Username already taken?
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username taken")
        # If all pass
        else:
            # Create user instance
            user = User.objects.create_user(username=username, email=email, password=password)
            # Create profile
            UserProfile.objects.create(user=user, gender=gender)
            # Log in new user
            login(request, user)
            UserActivity.objects.create(user=request.user)
            # [[[Replace HttpResponse with a redirect to the dashboard once it's linked (Atheen)]]]
            return HttpResponse("User signed up")
    return render(request, 'register.html')

# Handle user login (Atheen)
def user_login(request):
    if request.method == "POST":
        # Retrieve identifier (email/username) and password from login form
        identifier = request.POST.get("identifier")
        password = request.POST.get("password")

        # Validation checks
        # Empty fields?
        if not all([identifier, password]):
            messages.error(request, "Please fill out all fields")
        # Incorrect identifier or password?
        else:
            user = User.objects.filter(email=identifier).first() or User.objects.filter(username=identifier).first()
            
            # If information is correct, log in
            if user and (user := authenticate(request, username=user.username, password=password)):
                login(request, user)
                UserActivity.objects.create(user=request.user)

                # [[[Replace HttpResponse with a redirect to the dashboard once it's linked (Atheen)]]]
                # Admin login
                if user.is_staff:
                    return redirect('analytics')
                    # User login - redirect to user dashboard (or home for now)
                else:
                    return redirect('home')  # Change this to user dashboard when available
                
            # If incorrect, show an error message
            else:
                messages.error(request, "Information incorrect")
                
    return render(request, 'login.html')

# Handle user logout (Atheen)
def user_logout(request):
    if request.method == "POST":
        logout(request)
    # Redirect to home page
    return redirect('/')