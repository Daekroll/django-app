from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from .models import Profile


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('myauth:login')


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'

    def get_success_url(self):
        user = self.object
        Profile.objects.create(user=user)
        return reverse('myauth:about', kwargs={'pk': self.object.pk})


class UpdateProfileView(UserPassesTestMixin, UpdateView):
    model = Profile
    fields = 'bio', 'age', 'avatar',

    def get_success_url(self):
        return reverse('myauth:about', kwargs={'pk': self.object.user.pk})

    def get_object(self, queryset=None):
        profile_id = self.kwargs.get('pk')
        return get_object_or_404(Profile, pk=profile_id)

    def test_func(self):
        profile = self.get_object()
        return self.request.user.is_superuser or profile.user == self.request.user


class ListProfileView(ListView):
    queryset = User.objects.select_related('profile').all()
    context_object_name = 'profiles'
    template_name = 'myauth/user_list.html'


class AboutView(DetailView):
    template_name = 'myauth/about_me.html'
    model = User

    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        profile, created = Profile.objects.get_or_create(user=user)
        return user


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default value')
    return HttpResponse(f"cookie value:{value!r}")


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default')
    return HttpResponse(f"session value:{value!r}")


def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['foobar'] = 'spameggs'
    return HttpResponse("session set")
