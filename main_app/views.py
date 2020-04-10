from django.shortcuts import render, redirect
from .models import Flight


def home(request):
    return render(request, 'index.html', {'page_title': 'Flights'})


def flight(request, id):
    try:
        flight = Flight.objects.get(id=id)
    except:
        return redirect('/')
    return render(request, 'flight.html', {
        'page_title': f'Flight {id}',
        'flight_id': id,
        'dep_date': flight.departure_time.strftime("%A, %-m %B, %Y"),
        'dep_time': flight.departure_time.strftime("%H%Mhrs"),
        'arr_date': flight.arrival_time.strftime("%A, %-m %B, %Y"),
        'arr_time': flight.arrival_time.strftime("%H%Mhrs"),
        'flight_info': flight}
    )
