from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

from .forms import ProfileUpdateForm
from .models import Profile


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user, display_name=user.username, email='')
        return super().form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_update.html'
    slug_field = 'display_name'
    slug_url_kwarg = 'display_name'
    success_url = reverse_lazy('accounts:profile_update')
