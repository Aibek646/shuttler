from django.db import models
from django.contrib.auth.models import User


class Craft(models.Model):
    model = models.CharField(max_length=20)
    serialNumber = models.CharField(max_length=10) 
    numberOfSeats = models.IntegerField(default=10)

    def __str__(self):
        return self.model


class Port(models.Model):
    name = models.CharField(max_length=30)
    abbr = models.CharField(max_length=4)

    def __str__(self):
        return f'{self.name} ({self.abbr})'


class Flight(models.Model):
    craft = models.ForeignKey(Craft, on_delete=models.PROTECT)
    departure_time = models.DateTimeField()
    departure_port = models.ForeignKey(
        Port, on_delete=models.PROTECT, related_name='departure')
    arrival_time = models.DateTimeField()
    arrival_port = models.ForeignKey(
        Port, on_delete=models.PROTECT, related_name='arrival')

    def __str__(self):
        return f'{self.departure_port.abbr} to {self.arrival_port.abbr} at {self.departure_time.strftime("%Y-%m-%d %H%Mhrs")}'


class Person(models.Model):
    class Role(models.IntegerChoices):
        STAFF = 1
        CREW = 2
        PASSENGER = 3
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    role = models.CharField(max_length=2, choices=(
        ('ST', 'Staff'),
        ('CR', 'Crew'),
        ('PA', 'Passenger')
    ))

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Manifest(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return f"flight {self.flight} and person {self.person}"
