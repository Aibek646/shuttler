from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('flight/<int:id>', views.flight, name='flight'),
    path('booking/', views.make_booking, name='make_booking'),
    path('booking/<int:id>', views.show_booking, name='show_booking'),
    path('account/', views.account, name='account'),
    path('about/', views.about, name='about'),
]
