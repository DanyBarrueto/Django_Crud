from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm

# Create your views here

# Ruta principal
def home(request):
    return render(request, 'home.html',)

# Configuración de la ruta para registrarse
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # registrar usuario
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'la Contraseña no coincide'
        })

# Ruta task
def tasks(request):
    return render(request, 'tasks.html')

# Configuración de la ruta para poder cerrar sesión
def signout(request):
    logout(request)
    return redirect('home')

# Configuración de la ruta para poder iniciar sesión
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{
            'form': AuthenticationForm,
            'error': 'Usuario o contraseña incorrecta'
        })
        else:
            login(request, user)
            return redirect('tasks')

#Para crear tareas
def create_task(request):

    if request.method == 'GET':
        return render(request, 'create_task.html',{
            'form': TaskForm
        })
    else:
        print(request.POST)
        return render(request, 'create_task.html',{
            'form': TaskForm
        })