from django.contrib import admin
from shophubapp.models import console, game

# Register your models here.
class ConsoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'pdetails', 'cat', 'is_active']
    list_filter = ['cat', 'price', 'is_active']

admin.site.register(console, ConsoleAdmin)

class GameAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'gdetails', 'pltfrm', 'is_active']
    list_filter = ['pltfrm', 'price', 'is_active']

admin.site.register(game, GameAdmin)

