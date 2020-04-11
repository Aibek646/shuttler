from django.shortcuts import render, redirect
from .models import Flight, Person


def home(request):
    flights = Flight.objects.all()

    return render(request, 'flights/index.html', {'flights': flights})


def flight(request, id):
    try:
        flight = Flight.objects.get(id=id)
    except:
        return redirect('/')
    return render(request, 'flights/show.html', {
        'page_title': f'Flight {id}',
        'flight_id': id,
        'dep_date': flight.departure_time.strftime("%A, %-m %B, %Y"),
        'dep_time': flight.departure_time.strftime("%H%Mhrs"),
        'arr_date': flight.arrival_time.strftime("%A, %-m %B, %Y"),
        'arr_time': flight.arrival_time.strftime("%H%Mhrs"),
        'flight_info': flight}
    )


def make_booking(request):
    pass


def show_booking(request):
    pass


def about(request):
    admins = Person.objects.filter(role='AD')
    return render(request, 'about.html', {
        'page_title': about,
        'admins': admins,
    })
