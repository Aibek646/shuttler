from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('flight/<int:id>', views.flight, name='flight'),
    path('booking/', views.make_booking, name='make_booking'),
    path('booking/<int:id>', views.show_booking, name='show_booking'),
    path('about/', views.about, name='about'),
<<<<<<< HEAD
=======
    path('persons/', views.persons, name='persons'),
    path('persons/<int:id>', views.persons, name='modify_person'),
>>>>>>> e7648dceaf3a6bff1c09f8ebd40a529a4d2eb20d
]
