from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from . import forms
from django.urls import reverse_lazy 
from django.contrib.auth.views import LoginView
from .models import Transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from book.models import Purchase 
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# Create your views here.
def sign_up(request):
    if request.method == "POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created Successfully')
            return redirect('homepage')
    else:
        form = forms.RegistrationForm()
        
    return render(request, 'register.html', {'form': form })


class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    
    def get_success_url(self):
        return reverse_lazy('profile')
    def form_valid(self, form):
        messages.success(self.request, 'Logged in successful')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, 'Logged in information incorrect')
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
      
def user_logout(request):
    logout(request)
    return redirect('login')


def profile(request):
    current_user = request.user
    book = Purchase.objects.filter(user = current_user)
            
    return render(request, 'profile.html' , {'books': book, 'user': request.user} )

class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions_form.html'
    model = Transaction
    success_url = reverse_lazy('homepage')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class DepositMoneyView(TransactionCreateMixin):
    form_class = forms.DepositForm
    reverse_lazy = 'homepage'

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount 
        account.save(
            update_fields=[
                'balance'
            ]
        )
        messages.success(
            self.request,
            f'{amount}$ was deposited to your account successfully'
        )
        mail_subject = "Deposit Message"
        message = render_to_string('deposit_mail.html' , {
            'user': self.request.user,
            'amount': amount
        })
        to_email = self.request.user.email 
        send_email = EmailMultiAlternatives(mail_subject, message, '' ,to = [to_email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()
        
        return super().form_valid(form)

