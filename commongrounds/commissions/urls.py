from django.urls import path
from .views import list_view, detail_view

urlpatterns = [
    path('requests/', list_view, name='list_view'),
    path('request/<int:pk>', detail_view, name='detail_view'),
] 

app_name = 'commissions'