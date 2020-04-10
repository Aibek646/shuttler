from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('flight/<int:id>', views.flight, name='flight')
]
