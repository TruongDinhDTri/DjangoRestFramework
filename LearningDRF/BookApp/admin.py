from django.contrib import admin
from .models import BookModel

# Register your models here.
class BookModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'author', 'price']
    search_fields = ['name', 'author__username'] # Search by book name and author's username
    list_filter = ['author']  # Filter by author
    
admin.site.register(BookModel, BookModelAdmin)
