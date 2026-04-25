from django.urls import path
from .views import list_view, detail_view, add_view, edit_view

urlpatterns = [
    path('requests/', list_view, name='list_view'),
    path('request/<int:pk>', detail_view, name='detail_view'),
    path('request/add', add_view, name='add_view'),
    path('request/<int:pk>/edit', edit_view, name='edit_view')
]

app_name = 'commissions'
