"""
URL configuration for anudhaGames project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from storyapp import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),

    # path('verify-token/', views.verify_token, name='verify_token'),
    
    path('logout/', views.logout, name='logout'),

    path('storylist/', views.storylist, name='storylist'),
    path('story/<str:story_id>/<str:node_id>/', views.story, name='story'),

    # Story page - starts from the first node (default: img1)
    # path("story/<str:story_id>/", views.story, name="story"),

    # Load a specific node within a story
    # path("story/<str:story_id>/<str:node_id>/", views.story, name="story"),

    # Handle choices and move to the next story node dynamically
    path("choice/<str:story_id>/<str:node_id>/", views.handle_choice, name="handle_choice"),

    path('contact/', views.contact, name='contact'),
    path("profile/", views.profile, name="profile"),
]
