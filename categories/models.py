from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=15)
    slug = models.SlugField(max_length=100, blank=True, null=True, unique=True)
    
    def __str__(self):
        return self.name