from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'admin-app/home.html')

def user(request):
    return render(request, 'admin-app/user.html')  

def song(request):
    return render(request, 'admin-app/song.html')  

def artist(request):
    return render(request, 'admin-app/artist.html') 

def playlist(request):
    return render(request, 'admin-app/playlist.html') 

def category(request):
    return render(request, 'admin-app/category.html') 