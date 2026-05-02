from django.contrib.auth.views import LoginView as BaseLoginView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

from .forms import ProfileUpdateForm, RegisterForm
from .models import Profile
from merchstore.models import Product, Transaction


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(
            user=user, display_name=user.username, email=user.email)
        return super().form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_update.html'
    slug_field = 'display_name'
    slug_url_kwarg = 'display_name'

    def get_success_url(self):
        return reverse_lazy('accounts:profile_update', kwargs={'display_name': self.object.display_name})


class CustomLoginView(BaseLoginView):
    def form_valid(self, form):
        result = super().form_valid(form)
        pending = self.request.session.get("pending_transaction")
        if pending:
            product = Product.objects.get(id=pending["product_id"])
            Transaction.objects.create(
                buyer = self.request.user.profile,
                product = product,
                amount = pending["amount"],
                status = "On cart"
            )
            del self.request.session["pending_transaction"]
            return redirect("merchstore:merchstore-cart")
        return result
