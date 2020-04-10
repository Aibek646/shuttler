from django.db import models
from django.contrib.auth.models import User


class Craft(models.Model):
    pass


# Seanny
class Port(models.Model):
    name = models.CharField(max_length=30)
    abbr = models.CharField(max_length=4)

# Seanny


class Flight(models.Model):
    craft = models.ForeignKey(Craft, on_delete=models.PROTECT)
    departure_time = models.DateTimeField()
    departure_port = models.ForeignKey(
        Port, on_delete=models.PROTECT, related_name='departure')
    arrival_time = models.DateTimeField()
    arrival_port = models.ForeignKey(
        Port, on_delete=models.PROTECT, related_name='arrival')

# Seanny


class Person(models.Model):
    class Role(models.IntegerChoices):
        STAFF = 1
        CREW = 2
        PASSENGER = 3
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=(
        ('ST', 'Staff'),
        ('CR', 'Crew'),
        ('PA', 'Passenger')
    ))


class Manifest(models.Model):
    pass
