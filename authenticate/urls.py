from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.sign_up, name='register'),
    path('profile/', views.profile, name='profile'),
    path("deposit/",views.DepositMoneyView.as_view(),name = 'deposit_money'),
   
]
