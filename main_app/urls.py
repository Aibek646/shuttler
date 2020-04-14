from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('flight/<int:id>', views.flight, name='flight'),
    path('seats/<int:id>', views.seats, name='seats'),
    path('booking/', views.make_booking, name='make_booking'),
    path('account/', views.account, name='account'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('validate/', views.validate, name='validate'),
    path('about/', views.about, name='about'),
    path('persons/', views.persons, name='persons'),
    path('persons/<int:id>', views.persons, name='modify_person'),
]
