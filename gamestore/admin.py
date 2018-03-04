from django.contrib import admin
from .models import Game, Genre, GamePurchase, GameStats, UserAttributes


admin.site.register(Game)
admin.site.register(Genre)
admin.site.register(GamePurchase)
admin.site.register(GameStats)
admin.site.register(UserAttributes)