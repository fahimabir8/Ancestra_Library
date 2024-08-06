from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    balance = models.DecimalField(decimal_places=2, max_digits=8, default=0.00)

class Transaction(models.Model):
    
    account = models.ForeignKey(Account,  on_delete = models.CASCADE) 
    time = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(decimal_places=2, max_digits = 8)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits = 8)
    
    def __str__(self):
        return f'Transaction done by - {self.account.user.username}'
    