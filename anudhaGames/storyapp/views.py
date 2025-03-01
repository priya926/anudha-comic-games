from django.shortcuts import render,redirect
from django.http import JsonResponse
import firebase_admin
from firebase_admin import auth,credentials
import os
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            print(email)
            user = auth.create_user(email=email, password=password)
            print(email)
            print(password)
            messages.success(request, "Registration successful. Please log in.")
            return redirect("index")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect("index")

    return render(request, "index.html")


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = auth.get_user_by_email(email)
            messages.success(request, "Login successful!")
            return redirect("storylist")
        except:
            messages.error(request, "Invalid credentials.")
            return redirect("index")

    return render(request, "index.html")

# Logout View (Clears the session)
# def logout_view(request):
#     request.session.flush()  # Clear session
#     return redirect('index')  # Redirect back to home

def storylist(request):
    return render(request, 'storylist.html')

def story(request):
    return render(request, 'story.html')

# def logout(request):
#     logout(request)
#     return JsonResponse({"Success":"User Logged out successfully!"})