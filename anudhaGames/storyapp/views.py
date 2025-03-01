from django.shortcuts import render,redirect
from .forms import ContactForm
from django.http import JsonResponse
import firebase_admin
from firebase_admin import auth,credentials,firestore
import os
from django.contrib import messages

db=firestore.client()
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


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract form data
            uname = form.cleaned_data['uname']
            uemail = form.cleaned_data['uemail']
            phone_number = form.cleaned_data['phone_number']
            message = form.cleaned_data['message']

            # Prepare data for Firestore
            contact_data = {
                "uname": uname,
                "uemail": uemail,
                "phone_number": phone_number,
                "message": message
            }

            # Store data in Firestore (inside 'contacts' collection)
            db.collection('contacts').add(contact_data)

            messages.success(request, "Your message has been submitted successfully!")
            return redirect("index")  # Redirect to contact page after submission

    else:
        form = ContactForm()

    return render(request, "index.html", {"form": form})

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