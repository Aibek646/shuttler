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
    remaining = flight.craft.seats - len(manifest)

    passengers = manifest.filter(user=request.user.id)
    passengers = passengers.values()
    passenger_dict = {}
    for passenger in passengers:
        passenger_dict[passenger['id']] = passenger

    return JsonResponse({
        'total': flight.craft.seats,
        'remaining': remaining,
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
                flight=flight
            )
            seat.save()

    return redirect('/flight/{}'.format(info['flight_id']))


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


def persons(request, **kwargs):
    if request.user.is_authenticated:
        if request.method == "GET":
            person_dict = {}
            persons = Person.objects.filter(user=request.user.id)
            persons = persons.values()
            for person in persons:
                person_dict[person['id']] = person
            return JsonResponse(person_dict)

        elif request.method == "POST":
            server_log(request.content_params)
            data = json.loads(request.body.decode("utf-8"))
            server_log(data)
            if data['action'] == 'create':
                newPerson = Person(
                    request.user,
                    data['first_name'],
                    data['last_name'],
                    'PA'
                )
                newPerson.save()
                return JsonResponse({'created': {
                    'id': newPerson.id,
                    'first_name': newPerson.first_name,
                    'last_name': newPerson.last_name,
                }})
            elif data['action'] == 'update':
                server_log(request.body)
                data = request.PUT
                updatePerson = Person.objects.get(id=data['id'])
                updatePerson.first_name = data['first_name']
                updatePerson.last_name = data['last_name']
                return JsonResponse({'created': {
                    'id': updatePerson.id,
                    'first_name': updatePerson.first_name,
                    'last_name': updatePerson.last_name,
                }})

        elif request.method == "DELETE":
            deletePerson = Person.objects.get(id=kwargs['id'])
            deletePerson.delete()
            return JsonResponse({'deleted': deletePerson.first_name})
    else:
        return JsonResponse({})


def server_log(message):
    print('----------')
    print(message)
    print('----------')


def test(request):
    return
