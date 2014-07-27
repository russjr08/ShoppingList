from django.contrib import admin

# Register your models here.
from app.models import Item


class ItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(Item, ItemAdmin)