from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import Transaction,Account

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget= forms.TextInput(attrs={'id':'required'}))
    last_name = forms.CharField(widget= forms.TextInput(attrs={'id':'required'}))
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        
    def save(self, commit = True):
        user = super().save(commit = False)
        if commit:
            user.save()
            Account.objects.create(user = user)
        return user
    
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount',]
    
    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)
       
    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()
    
class DepositForm(TransactionForm):
    def clean_amount(self):
        min_deposit_amount = 500
        amount = self.cleaned_data.get('amount')
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount}$'
            )
            
        return amount 

