from django.contrib import admin
from .models import Craft, Port, Flight, Person, Manifest

admin.site.register(Craft)
admin.site.register(Port)
admin.site.register(Flight)
admin.site.register(Person)
admin.site.register(Manifest)
