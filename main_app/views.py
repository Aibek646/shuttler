from django.shortcuts import render
from .models import Flight


def home(request):
    return render(request, 'index.html', {'page_title': 'Flights'})


def flight(request, id):
    flight = Flight.objects.get(id=id)
    return render(request, 'flight.html', {
        'page_title': f'Flight {id}',
        'flight_id': id,
        'flight_info': flight}
    )
