from django.urls import path
from .views import home,details,buybookview
urlpatterns = [
    path('',home, name='homepage'),
    path('category/<slug:category_slug>/', home, name='category_home'),
    path('details/<int:id>/',details.as_view(), name='details'),
    path('details/buy/<int:id>/',buybookview.as_view(), name='buy_book'),

]
