from django import forms
from django.forms import ModelForm
from ..models import Genre, Game

class newGameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['name',
                  'description',
                  'price',
                  'url',
                  'genreID',
                  'image',
                  'visible']
        help_texts = {
            'url': 'Please use https for the url',
        }