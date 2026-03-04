from django.urls import path
from .views import (
    MerchStoreListView,
    MerchStoreDetailView,
)

app_name = 'merchstore'
urlpatterns = [
    path('items/', MerchStoreListView.as_view(),
         name='merchstore-list'),
    path('item/<int:id>/', MerchStoreDetailView.as_view(),
         name='merchstore-detail'),
]
