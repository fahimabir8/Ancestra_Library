from django.shortcuts import render,redirect,get_object_or_404 
from .models import Book,Purchase 
from categories.models import Category
from authenticate.models import Transaction,Account
from django.views.generic import DetailView
from django.contrib import messages
from .forms import ReviewForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string



# Create your views here.
def home(request, category_slug=None):
    books = Book.objects.all()
    if category_slug:
        category = Category.objects.get(slug=category_slug)
        books = books.filter(category=category)
    
    categories = Category.objects.all()
    return render(request, 'home.html', {'books': books, 'categories': categories})


class details(LoginRequiredMixin,DetailView):
    model = Book
    pk_url_kwarg = 'id'
    template_name = 'details.html'
    
    def post(self, request, *args, **kwargs):
        review_form = ReviewForm(data=request.POST)
        self.object = self.get_object()  
        if request.user.is_authenticated:
            if review_form.is_valid():
                new_review = review_form.save(commit=False)
                new_review.book = self.object
                new_review.user = request.user
                new_review.save()
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.comments.all()
        context['review_form'] = ReviewForm()
        context['user_purchased'] = Purchase.objects.filter(user=self.request.user, book=self.object).exists() 
        return context

class buybookview(LoginRequiredMixin, DetailView):
    model = Book
    pk_url_kwarg = 'id'
    template_name = 'details.html'
    
    def post(self, request, *args, **kwargs):
        book = self.get_object()
        if request.user.is_authenticated:
            user_account = get_object_or_404(Account, user=request.user)
            if book.price <= user_account.balance:
                user_account.balance -= book.price
                user_account.save(update_fields=['balance'])
                
                Transaction.objects.create(
                    account=user_account,
                    balance_after_transaction=user_account.balance,
                    amount=book.price
                )

                Purchase.objects.create(user=request.user, book=book)
                
                messages.success(request, f'You have successfully bought the book "{book.title}".')
                mail_subject = "Purchase Message"
                message = render_to_string('purchase_mail.html' , {
                    'user': self.request.user,
                    'amount': book.price,
                    'book': self.get_object()
                })
                to_email = self.request.user.email 
                send_email = EmailMultiAlternatives(mail_subject, message, '' ,to = [to_email])
                send_email.attach_alternative(message, "text/html")
                send_email.send()
                return redirect('profile')
            else:
                messages.error(request, 'You donot have enough balance to buy this book.')
        else:
            messages.error(request, 'You need to be logged in to buy a book.')
        
        return redirect('details', id=book.id)
    


            
            
    