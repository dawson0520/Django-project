from django.contrib import admin

# Register your models here.

class ShoppingCartAdmin(object):
    list_display = ["user", "goods", "nums", ]
