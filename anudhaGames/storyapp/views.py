from django.shortcuts import render,redirect


# Create your views here.
def index(request):
    return render(request, 'index.html')

def storylist(request):
    return render(request, 'storylist.html')

def story(request):
    return render(request, 'story.html')