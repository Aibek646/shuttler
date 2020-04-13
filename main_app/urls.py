from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('flight/<int:id>', views.flight, name='flight'),
    path('booking/', views.make_booking, name='make_booking'),
    path('booking/<int:id>', views.show_booking, name='show_booking'),
    path('account/', views.account, name='account'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('validate/', views.validate, name='validate'),
    path('about/', views.about, name='about'),
]
