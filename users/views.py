from .forms import CustomUserCreationForm, CustomUserChangeForm
from .forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import UserPassesTestMixin

class SignUpView(UserPassesTestMixin, generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    login_url = 'login'

    def test_func(self):
        return self.request.user.role == 'Admin' 
