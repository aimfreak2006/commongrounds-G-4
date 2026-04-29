from django.shortcuts import redirect


class BaseTransactionStrategy():
    def execute(self, request, product, form):
        raise NotImplementedError()


class AuthenticatedPurchaseStrategy(BaseTransactionStrategy):
    def execute(self, request, product, form):
        form.instance.product = product
        form.instance.status = "On cart"
        form.instance.buyer = request.user.profile
        form.save()
        return redirect("merchstore:merchstore-cart")


class GuestPurchaseStrategy(BaseTransactionStrategy):
    def execute(self, request, product, form):
        request.session["pending_transaction"]={"product_id": product.id, "amount": form.cleaned_data["amount"]}
        return redirect("accounts:login")
