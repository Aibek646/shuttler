import random
from django.shortcuts import render, redirect
from .models import Flight, Person, Manifest
from django.contrib.auth.models import User, UserManager
from django.contrib.auth import authenticate, login


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
    users = User.objects.filter(
        first_name=info['first_name'],
        last_name=info['last_name'],
    )
    if len(users) > 0:
        user = users[0]
        server_log(user)
        login(request, user)

    else:
        user = User.objects.create_user(
            str(random.randint(100000, 999999)),
            first_name=info['first_name'],
            last_name=info['last_name'],
        )
        Person.objects.create(user=user, role='PA')
    flight = Flight.objects.get(id=info['flight_id'])
    server_log(flight)
    for i in range(0, int(info['seats'])):
        manifest = Manifest(person=user.person, flight=flight)
        manifest.save()
    return redirect('/flight/{}'.format(info['flight_id']))


def show_booking(request, id):
    manifest1 = Manifest.objects.filter(flight__id = id, user = request.user)
    print(manifest1)
    return render(request, 'flights/bookShow.html', {'manifest1': manifest1} )


def account(request):
    if request.user.is_authenticated:
        return render(request, 'account.html', {
            'page_title': 'Log In',
            'login_form': True,
        })
    else:
        return render(request, 'account.html', {
            'page_title': 'Account',
            'login_form': False,
        })


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
