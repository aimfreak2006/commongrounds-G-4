from django.urls import path
from .views import (
    ProductListView,
    product_detail_view,
    ProductCreateView,
    ProductUpdateView,
    CartView,
    TransactionListView,

)

app_name = "merchstore"
urlpatterns = [
    path("items/", ProductListView.as_view(),
         name="merchstore-list"),
    path("item/<int:id>/", product_detail_view,
         name="merchstore-detail"),
    path("item/add/", ProductCreateView.as_view(),
         name="merchstore-create"),
    path("item/<int:id>/edit/", ProductUpdateView.as_view(),
         name="merchstore-update"),
    path("cart/", CartView.as_view(),
         name="merchstore-cart"),
    path("transactions/", TransactionListView.as_view(),
         name="merchstore-transactions"),

]
