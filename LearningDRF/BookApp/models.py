from os import name
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BookModel(models.Model):
    """Model definition for BookModel."""
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books', default=None, null=True)
    price = models.IntegerField(default=0)
    

    def __str__(self):
        """Unicode representation of BookModel."""
        return f'{self.name}'
