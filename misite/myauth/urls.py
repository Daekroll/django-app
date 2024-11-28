from django.contrib.auth.views import LoginView
from django.urls import path


from .views import (MyLogoutView,
                    get_cookie_view,
                    set_cookie_view,
                    get_session_view,
                    set_session_view,
                    RegisterView,
                    AboutView, UpdateProfileView, ListProfileView)


app_name = 'myauth'
urlpatterns = [
    path('login/',
         LoginView.as_view(
             template_name='myauth/login.html',
             redirect_authenticated_user=True
         ), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('about/<int:pk>', AboutView.as_view(), name='about'),
    path('update/<int:pk>', UpdateProfileView.as_view(), name='update'),
    path('profiles/', ListProfileView.as_view(), name='profiles'),

    path('get_cookie/', get_cookie_view, name='get_cookie'),
    path('set_cookie/', set_cookie_view, name='set_cookie'),

    path('get_session/', get_session_view, name='get_session'),
    path('set_session/', set_session_view, name='set_session'),
]