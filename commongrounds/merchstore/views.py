from django.shortcuts import render, get_object_or_404

from django.views.generic import (
    ListView,
    DetailView,
)
from .models import Product, ProductType


class MerchStoreListView(ListView):
    template_name = 'merchstore/merchstore_list.html'
    # queryset = Product.objects.all()
    model = ProductType

    def get_queryset(self):
        return ProductType.objects.prefetch_related("products").order_by("name")


class MerchStoreDetailView(DetailView):
    template_name = 'merchstore/merchstore_detail.html'
    # queryset = Article.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Product, id=id_)
