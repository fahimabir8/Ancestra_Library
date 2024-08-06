from django.db import models
from django.contrib.auth.models import User
from categories.models import Category

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=30,null=True,blank=True)
    price = models.IntegerField()
    description = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE , null=True, blank = True)
    image = models.ImageField(upload_to='./cores/static/image/',blank=True, null=True )
        
    def __str__(self):
        return self.title

class Reviews(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='reviews')
    area = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'comment by {self.user.username}'
    
class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='purchases')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_purchased = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Purchased by :- {self.user.username}'

