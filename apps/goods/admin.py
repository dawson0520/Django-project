from django.contrib import admin

# Register your models here.

class mymodel(models.model):
    name = models.charfield(max_length=20)

