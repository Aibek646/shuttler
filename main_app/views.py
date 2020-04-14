from django.shortcuts import render, redirect
from .models import Flight


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


def show_booking(request, id):
    manifest1 = Manifest.objects.filter(flight__id = id, user = request.user)
    print(manifest1)
    return render(request, 'flights/bookShow.html', {'manifest1': manifest1} )


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
