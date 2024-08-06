from django.contrib import admin
from .models import Book,Reviews,Purchase
# Register your models here.
admin.site.register(Book)
admin.site.register(Reviews)
admin.site.register(Purchase)