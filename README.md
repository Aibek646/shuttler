# shuttler
<<<<<<< HEAD
Instalation
=======
Shuttler is a website, where a user can create account, and book a ticket for several people including himself. User also will have ability to manipulate with its attached people, delete, create, edit

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Installation
```bash
pip3 install Django
django-admin startproject shuttler
pip3 install virtualenv
virtualenv .env -p python3
pip3 install psycopg2
pip3 freeze > requirements.txt
python3 manage.py startapp main_app
```

## Usage
``` python
import random
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, UserManager
from .models import Flight, Person, Manifest

```
## Code Style
Bootstrap

## How to use?
User goes to a website and creates an account. As account has been created, he will be redirected to the main page. In main page for user will be displayed list of available flights. He will choose the liked flights and will be redirected to flight-detail page. In flight-detail page user will be able to book and add as many as passengers he wants. Apparently flight will have limited amount of seats. Since user adding passengers, in database seats are deacremented. User has ability go to account page, and perform CRUD functionality as EDIT, DELETE, CREATE and UPDATE.

## Contribute
Seanny Drakon Phoenix
Aibek Ramazanov
