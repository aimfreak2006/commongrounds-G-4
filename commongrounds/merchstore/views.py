from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, CreateView, UpdateView

from accounts.decorators import role_required
from accounts.mixins import RoleRequiredMixin
from .forms import TransactionForm
from .models import Product, Transaction
from .strategies import AuthenticatedPurchaseStrategy, GuestPurchaseStrategy


class ProductListView(ListView):
    template_name = 'merchstore/merchstore_list.html'
    model = Product

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            my_products = Product.objects.filter(
                owner=self.request.user.profile)
            all_products = Product.objects.exclude(
                owner=self.request.user.profile)
        else:
            my_products = None
            all_products = Product.objects.all()

        context = super().get_context_data(**kwargs)
        context["my_products"] = my_products
        context["all_products"] = all_products
        return context


def product_detail_view(request, id):
    product = get_object_or_404(Product, id=id)
    is_owner = (
        request.user.is_authenticated and
        request.user.profile == product.owner
    )

    form = TransactionForm()
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["amount"] > product.stock:
                form.add_error("amount", "not enough stock")
            else:
                if request.user.is_authenticated:
                    strategy = AuthenticatedPurchaseStrategy()
                else:
                    strategy = GuestPurchaseStrategy()
                return strategy.execute(request, product, form)

    return render(request, "merchstore/merchstore_detail.html", {
        "object": product,
        "form": form,
        "is_owner": is_owner,
    })


class ProductCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    template_name = "merchstore/merchstore_create.html"
    model = Product
    allowed_roles = ["Market Seller"]
    form_class = CustomProductCreateForm

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    template_name = "merchstore/merchstore_update.html"
    model = Product
    allowed_roles = ["Market Seller"]
    form_class = CustomProductCreateForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Product, id=id_)

    def form_valid(self, form):
        if form.instance.stock == 0:
            form.instance.status = "Out of Stock"
        else:
            form.instance.status = "Available"
        return super().form_valid(form)


class CartView(LoginRequiredMixin, ListView):
    template_name = "merchstore/merchstore_cart.html"
    context_object_name = "transactions"

    def get_queryset(self):
        return Transaction.objects.filter(
            buyer=self.request.user.profile
        ).order_by("product__owner")


@login_required
@role_required(["Market Seller"])
def transaction_list_view(request):
    transactions = Transaction.objects.filter(
        product__owner=request.user.profile
    ).order_by("buyer")
    return render(request, "merchstore/merchstore_transactions.html", {
        "transactions": transactions
    })
