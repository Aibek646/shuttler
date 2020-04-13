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
        first_name = request.user.first_name
        last_name = request.user.last_name
        username = request.user.username
    else:
        first_name = ''
        last_name = ''

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
        'flight_info': flight,
        'first_name': first_name,
        'last_name': last_name}
    )


def make_booking(request):
    info = request.POST
    server_log(info)
    user = request.user
    flight = Flight.objects.get(id=info['flight_id'])
    server_log(flight)
    for i in range(0, int(info['seats'])):
        manifest = Manifest(user=user, person=user.person, flight=flight)
        manifest.save()
    return redirect('/flight/{}'.format(info['flight_id']))


def show_booking(request):
    pass


def account(request):
    if request.user.is_authenticated:
        return render(request, 'account.html', {
            'page_title': 'Account',
        })
    else:
        return render(request, 'account.html', {
            'page_title': 'Log In',
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
            'message': 'Must use the POST method',
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


def server_log(message):
    print('----------')
    print(message)
    print('----------')


def test(request):
    return
