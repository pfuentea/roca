from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms.user_creation import UserCreationForm

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.contrib import messages
# Create your views here.

from .models import *

def index(request):

    context = {
        'saludo': 'Hola'
    }
    return render(request, 'index.html', context)

@login_required
def dashboard_redirect(request):
    if request.user.is_superuser:
        return redirect('panel_admin')
    else:
        return redirect('panel_usuario')

def login_view(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                
                messages.success(request, f"Bienvenido, {username}!")
                login(request, user)
                return redirect('dashboard')  # Reemplaza 'home' con el nombre de la URL a la que quieres redirigir
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Formulario no válido.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def cotizaciones(request):
    context={}
    return render(request, 'cotizaciones.html', context)

def crear_usuario(request):

    context={}
    return render(request, 'crear_usuario.html',context)

def crear_producto(request):
    context={}
    return render(request, 'crear_producto.html', context)




def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Redirige al usuario a la página de login o donde desees
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})




def panel_usuario(request):
    context={}
    return render(request, 'usuario_cotizacion.html', context)

def usuario_producto(request):
    diametros=Diametro.objects.all()
    rollers = Roller.objects.values_list('nombre', flat=True).distinct()  # Obtén nombres únicos de rollers
    motores= Motor.objects.all()
    cenefas=Cenefa.objects.all()
    gateways=Gateway.objects.all()
    controles=Control.objects.all()

    context={
        "diametros":diametros,
        'rollers': rollers,
        'motores': motores,
        'cenefas': cenefas,
        'gateways': gateways,
        'controles': controles,
    }
    return render(request, 'usuario_producto.html', context)

def cotizacion_export(request):
    context={}
    return render(request, 'cotizacion_export.html', context)
    

def panel_admin(request):
    context={}
    return render(request, 'panel_admin.html', context)

def admin_cotizaciones(request):
    context={}
    return render(request, 'admin_cotizaciones.html', context)

def panel_admin(request):
    context={}
    return render(request, 'panel_admin.html', context)