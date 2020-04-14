from django.db import models
from django.contrib.auth.models import User


class Craft(models.Model):
    model = models.CharField(max_length=20)
    serial_number = models.CharField(max_length=10)
    seats = models.IntegerField(default=10)

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
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=2, choices=(
        ('ST', 'Staff'),
        ('CR', 'Crew'),
        ('PA', 'Passenger'),
        ('AD', 'Admin')
    ))
    pic = models.CharField(max_length=225, blank=True)
    bio = models.TextField(blank=True)
    linkedin_username = models.CharField(max_length=225, blank=True)
    github_uername = models.CharField(max_length=225, blank=True)
    twitter_username = models.CharField(max_length=225, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} --> {self.user}'


class Manifest(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return f"flight {self.flight} and person {self.person}"
