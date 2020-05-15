from django.contrib import admin

# Register your models here.

class mymodel(models.model):
    name = models.charfield(max_length=20)


class GoodsCategoryAdmin(object):
    list_display = ["name", "category_type", "parent_category", "add_time"]
    list_filter = ["category_type", "parent_category", "name"]
    search_fields = ['name', ]

