from django.shortcuts import render
from .models import Flight

# Create your views here.
def home(request):
    flights = Flight.objects.all()
    return render(request, 'flights/index.html', {'flights': flights})