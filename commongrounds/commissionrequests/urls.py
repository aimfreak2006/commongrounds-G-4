from django.urls import path
from .views import list_view, detail_view

urlpatterns = [
    path('/commissions/requests', list_view, name='list_view'),
    path('/commissions/request/1', detail_view, name='detail_view'),
] 

app_name = 'ledger'