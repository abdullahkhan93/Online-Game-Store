from django.urls import path
from . import views

urlpatterns = [
    path('', views.library, name='library'),
    path('game/<int:gameid>/', views.gamepage, name='gamepage'),
    path('game/<int:gameid>/save', views.save, name='save'),
    path('game/<int:gameid>/load', views.load, name='load'),
    path('game/<int:gameid>/score', views.submitScore, name='submitScore'),
    path('game/<int:gameid>/gethighscore', views.refreshScoreboard, name='getHighscore'),
]