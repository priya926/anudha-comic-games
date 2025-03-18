from django.shortcuts import render,redirect
from .forms import *
from django.http import JsonResponse
import firebase_admin
from firebase_admin import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .story import *
from firebase_config import db


def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            # Create user in Firebase Auth
            user = auth.create_user(email=email, password=password)
            user_id = user.uid  # Get the unique Firebase user ID
            
            # Store user data in Firestore
            user_ref = db.collection("User").document(user_id)
            user_ref.set({
                "username": "user",  # Default username
                "email": email,
                "userpoints": 0  # Default points
            })

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
            # Fetch user details from Firestore
            user_ref = db.collection("User").where("email", "==", email).stream()
            user_data = None
            for doc in user_ref:
                user_data = doc.to_dict()
                break  # Get the first matching user
            
            if user_data:
                # Store user data in session
                request.session["user_id"] = user.uid
                request.session["email"] = user.email
                request.session["username"] = user_data.get("username", "user")
                request.session["userpoints"] = user_data.get("userpoints", 0)

                messages.success(request, "Login successful!")
                return redirect("storylist")
            else:
                messages.error(request, "User not found in database.")
                return redirect("index")
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
def logout(request):
    request.session.flush()  # Clear session
    messages.success(request,"Logged Out Successfully.")
    return redirect('index')  # Redirect back to home 


def storylist(request):
    stories_ref = db.collection('stories')  # Get 'stories' collection
    docs = stories_ref.get()  # Fetch all documents
    stories = []
    for doc in docs:
        data = doc.to_dict()
        story_id = doc.id
        story_name = data.get('story_name', 'Unknown Story')
        image = data['nodes'].get('1', {}).get('image_url', '')

        print(f"Story: {story_name}, Image URL: {image}")  # Debugging output

        stories.append({'id': story_id, 'story_name': story_name, 'image': image})

    if "email" in request.session:
        user_email = request.session.get("email")
        username = request.session.get("username", "user")
        userpoints = request.session.get("userpoints", 0)

        return render(request, "storylist.html", {"stories": stories, "email": user_email, "username": username, "userpoints": userpoints})
    else:
        messages.error(request, "Please log in first.")
        return redirect("index")
   

def story(request): 
    if "email" in request.session:  # Check if user is logged in
        user_email = request.session.get("email")
        username = request.session.get("username", "user")
        userpoints = request.session.get("userpoints", 0)

        return render(request, "story.html", {"email": user_email, "username": username, "userpoints": userpoints})
    else:
        messages.error(request, "Please log in first.")
        return redirect("index")

# def logout(request):
#     logout(request)
#     return JsonResponse({"Success":"User Logged out successfully!"})

# @login_required
def profile(request):
    user_id = request.session.get("user_id")  # Get logged-in user ID
    user_ref = db.collection("User").document(user_id)
    user_doc = user_ref.get()

    if user_doc.exists:
        user_data = user_doc.to_dict()
    else:
        user_data = {}

    if request.method == "POST":
        new_username = request.POST.get("username")
        new_email = request.POST.get("email")

        try:
            # Update Firestore username
            user_ref.update({"username": new_username})

            # Update Firebase Auth email
            auth.update_user(user_id, email=new_email)

            # Update Firestore email
            user_ref.update({"email": new_email})

            messages.success(request, "Profile updated successfully!")
            return redirect("profile")

        except Exception as e:
            messages.error(request, f"Error updating profile: {str(e)}")

    return render(request, "profile.html", {"user": user_data})


def story_selection(request):
    user_id = request.session.get("user_id", "default_user")
    user_points = get_user_points(user_id)
    stories = get_all_stories(user_points)
    
    return render(request, "storylist.html", {"stories": stories, "user_points": user_points})

def story_page(request, story_id, node_id="1"):
    user_id = request.session.get("user_id", "default_user")
    story_node, required_points = get_story_node(story_id, node_id)

    if not story_node:
        return render(request, "error.html", {"message": "Story node not found."})

    user_points = get_user_points(user_id)

    # Ensure the user has enough points to view this story
    if user_points < required_points:
        return render(request, "error.html", {"message": "You need more points to access this story!"})

    # Add points if the node has any
    points = story_node.get("points", 0)
    if points:
        update_user_points(user_id, user_points + points)

    return render(request, "story.html", {
        "story_node": story_node,
        "story_id": story_id,
        "node_id": node_id,
        "user_points": user_points + points
    })

def handle_choice(request, story_id, node_id):
    chosen_option = request.GET.get("choice")
    story_node, _ = get_story_node(story_id, node_id)

    if not story_node or "choices" not in story_node:
        return render(request, "error.html", {"message": "Invalid choice."})

    next_node = story_node["choices"].get(chosen_option, "1")
    return redirect("story", story_id=story_id, node_id=next_node)
