import random
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, UserManager
from .models import Flight, Person, Manifest


def home(request):
    flights = Flight.objects.all()
    return render(request, 'flights/index.html', {
        'page_title': 'Home',
        'flights': flights
    })


def flight(request, id):
    if request.user.is_authenticated:
        persons = Person.objects.filter(user=request.user.id)
    else:
        persons = []
    try:
        flight = Flight.objects.get(id=id)
    except:
        return redirect('/')

    return render(request, 'flights/show.html', {
        'page_title': f'Flight {id}',
        'scripts': ['flight'],
        'flight_id': id,
        'dep_date': flight.departure_time.strftime("%A, %-m %B, %Y"),
        'dep_time': flight.departure_time.strftime("%H%Mhrs"),
        'arr_date': flight.arrival_time.strftime("%A, %-m %B, %Y"),
        'arr_time': flight.arrival_time.strftime("%H%Mhrs"),
        'flight_info': flight,
        'persons': persons,
    })


def seats(request, id):
    flight = Flight.objects.get(id=id)
    manifest = Manifest.objects.filter(flight=id)
    total = flight.craft.seats - len(manifest)

    passengers = manifest.filter(user=request.user.id)
    passengers = passengers.values()
    passenger_dict = {}
    for passenger in passengers:
        passenger_dict[passenger['id']] = passenger

    return JsonResponse({
        'total': total,
        'remaining': flight.craft.seats,
        'passengers': passenger_dict,
    })


def make_booking(request):
    info = request.POST
    user = request.user
    flight = Flight.objects.get(id=info['flight_id'])
    # total_seats = flight.craft.seats
    manifest = Manifest.objects.filter(flight_id=info['flight_id'])
    for seat in manifest:
        seat.delete()

    for item in info:
        if item[0:4] == "seat":
            person = Person.objects.get(id=info[item])
            seat = Manifest(
                user=user,
                person=person,
                flight=flight)
            seat.save()

    return redirect('/flight/{}'.format(info['flight_id']))


def show_booking(request, id):
    manifest1 = Manifest.objects.filter(flight__id = id, user = request.user)
    print(manifest1)
    return render(request, 'flights/bookShow.html', {'manifest1': manifest1} )


def account(request):
    scripts = ['account']
    if request.user.is_authenticated:
        page_title = 'Account'
    else:
        page_title = 'Log In'

    return render(request, 'account.html', {
        'page_title': page_title,
        'scripts': scripts,
    })


def login_user(request):
    if request.method != "POST":
        return JsonResponse({
            'login': False,
            'message': 'Must use the POST method',
        })
    else:
        login_data = json.loads(request.body)
        username = login_data['username']
        password = login_data['password']
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user is not None:
            login(request, user)
            return JsonResponse({
                'login': True,
            })
        else:
            response = {
                'login': False,
                'message': 'Invalid credentials',
            }
            return JsonResponse(response)


def logout_user(request):
    if request.method != "DELETE":
        return JsonResponse({
            'logout': False,
            'message': 'Must use the DELETE method',
        })
    else:
        logout(request)
        return JsonResponse({
            'logout': True
        })


def validate(request):
    user = request.user
    if user.is_authenticated:
        return JsonResponse({
            'username': user.username,
            'firstName': user.first_name,
            'lastName': user.last_name,
        })
    else:
        return JsonResponse(None, safe=False)


def about(request):
    admins = Person.objects.filter(role='AD')
    return render(request, 'about.html', {
        'page_title': 'About',
        'admins': admins,
    })


def persons(request):
    if request.user.is_authenticated:
        persons = Person.objects.filter(user=request.user.id)
    else:
        persons = []

    persons = persons.values()
    person_dict = {}
    for person in persons:
        person_dict[person['id']] = person

    return JsonResponse(person_dict)


def server_log(message):
    print('----------')
    print(message)
    print('----------')


def test(request):
    return
