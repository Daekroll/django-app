from django.urls import path
from .views import BasedView

app_name = 'blogapp'

urlpatterns = [
    path('', BasedView.as_view(), name='article'),
]