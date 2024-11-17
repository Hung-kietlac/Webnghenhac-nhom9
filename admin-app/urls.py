from django.urls import path
from . import views

app_name = 'admin-app'
urlpatterns = [
    path('', views.home, name='home'),
    path('user/', views.user, name='user'),
    path('song/', views.song, name='song'),
    path('artist/', views.artist, name='artist'),
    path('playlist/', views.playlist, name='playlist'),
    path('category/', views.category, name='category'),
]
