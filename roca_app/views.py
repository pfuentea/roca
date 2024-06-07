from django.shortcuts import render

# Create your views here.

def index(request):

    context = {
        'saludo': 'Hola'
    }
    return render(request, 'index.html', context)