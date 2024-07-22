from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms.user_creation import UserCreationForm

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.contrib import messages
# Create your views here.

from .models import *
from .forms.clienteForm import ClienteForm
from .forms.resumenCotizacionForm import ResumenCotizacionForm
from .forms.cotizacionForm import DetalleCotizacionForm
from django.http import JsonResponse
from .models.diametro import Diametro
from django.db.models import Max
from django.template.loader import render_to_string,get_template
#importacion a pdf
from django.conf import settings
import os
from xhtml2pdf import pisa
from io import BytesIO
#from django.template.loader import render_to_string
#from .utils import html_to_pdf
#from django.views.generic import View
from .models.generatepdf import GeneratePdf
from .utils import link_callback

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
                
                #messages.success(request, f"Bienvenido, {username}!")
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





@login_required(login_url='/')
def panel_usuario(request):
    context={
        'usuario': request.user,
    }
    print(f"R.user:{request.user}")
    if request.method == "POST":
        print("crear")
        form = ClienteForm(request.POST)
        if form.is_valid():
            print("guardando cliente")
            cliente = form.save()
            print("guardando cliente:sucess")
            print("creando resumen")
            #print(f"cliente:{cliente}")
            print(f"User:{request.user}")
            try:
                resumen = ResumenCotizacion.objects.create(
                    cliente=cliente,
                    usuario_generador=request.user,
                    total=0,
                )
            except Exception as e:
                print(f"Error al crear ResumenCotizacion: {e}")

            print("resumen listo")
            
            resumen.cotizacion_id=str(resumen.id).zfill(4)
            resumen.save()
            print("go to:usuario_producto")
            return redirect('usuario_producto',  cliente_id=cliente.id, resumen_id=resumen.id)
        else:
            for field, errors in form.errors.items():
                print(f"Error en el campo {field}: {errors}")
            return render(request, 'usuario_cotizacion.html', context)
    else:
        
        return render(request, 'usuario_cotizacion.html', context)
    
@login_required(login_url='/')
def usuario_producto(request, cliente_id,resumen_id):
    print("Init:usuario_producto(2)")
    resumen = get_object_or_404(ResumenCotizacion, id=resumen_id)
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        print(request.POST)
        roller_name = request.POST.get('roller_name').strip()
        diametro_id = request.POST.get('diametro_id')
        print(f"roller:{roller_name}-{diametro_id}")
        roller = get_object_or_404(Roller, nombre=roller_name, diametro_id=diametro_id)
        form = DetalleCotizacionForm(request.POST)
        if form.is_valid():
            detalle_cotizacion = form.save(commit=False)
            detalle_cotizacion.roller_id=roller.id
            detalle_cotizacion.resumen_cotizacion_id = resumen.id
            detalle_cotizacion.cliente_id = cliente.id
            detalle_cotizacion.motor_id = request.POST.get('motor_id')
            detalle_cotizacion.cenefa_id = request.POST.get('cenefa_id')
            detalle_cotizacion.control_id = request.POST.get('control_id')
            detalle_cotizacion.diametro_id = diametro_id
            detalle_cotizacion.gateway_id = request.POST.get('gateway_id')
            detalle_cotizacion.save()
        else:
            for field, errors in form.errors.items():
                print(f"Error en el campo {field}: {errors}")
        
    
    num_items = DetalleCotizacion.objects.filter(resumen_cotizacion_id=resumen.id).count()

    diametros=Diametro.objects.all()
    rollers = Roller.objects.values_list('nombre', flat=True).distinct().order_by('nombre')  # Obtén nombres únicos de rollers
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
        'cliente':cliente,
        'resumen':resumen,
        'num_items':num_items,
    }
    return render(request, 'usuario_producto.html', context)

def roller_price(roller,ancho,alto):
    print(f"roller:{roller.id}-A:{ancho}-T:{alto}")
    precio = Precio.objects.get(
            roller_id=roller.id,
            ancho_inicial__lte=ancho,
            ancho_final__gte=ancho,
            alto_inicial__lte=alto,
            alto_final__gte=alto
        )
    resultado=precio.precio
    return resultado

@login_required(login_url='/')
def cotizacion_export(request,resumen_id):
    #tenemos que calcular el total
    resumen = get_object_or_404(ResumenCotizacion, id=resumen_id)    
    detalles = DetalleCotizacion.objects.filter(resumen_cotizacion=resumen)
    total_resumen=0
    for item in detalles:
        total_item=0
        cantidad=item.cantidad
        print(f"cantidad:{cantidad}")
        precio_motor=0
        if(item.motor_id is not None):
            precio_motor = Motor.objects.get(id=item.motor_id).precio
        print(f"motor:{precio_motor}")
        precio_cenefa=0
        if(item.cenefa_id is not None):
            cenefa=Cenefa.objects.get(id=item.cenefa_id)
            precio_cenefa = cenefa.precio * (item.ancho)/1000
            print(f"cenefa:{cenefa.precio}")
            print(f"ancho:{item.ancho}")
            print(f"total cenefa:{precio_cenefa}")
        precio_control=0
        if(item.control_id is not None):
            precio_control = Control.objects.get(id=item.control_id).precio
        print(f"cont:{precio_control}")
        precio_gateway=0
        if(item.gateway_id is not None):
            precio_gateway = Gateway.objects.get(id=item.gateway_id).precio
        print(f"gat:{precio_gateway}")

        precio_roller=roller_price(item.roller,item.ancho,item.alto)
        print(f"roller:{precio_roller}")

        
        precio_instalacion=item.costo_instalacion_motor+item.costo_instalacion_cenefa+item.costo_instalacion_roller
        print(f"i-roller:{item.costo_instalacion_roller}")
        print(f"i-cen:{item.costo_instalacion_cenefa}")
        print(f"i-mot:{item.costo_instalacion_motor}")
        print(f"INST:{precio_instalacion}")
        total_item=(precio_motor*cantidad)+(precio_cenefa*cantidad)+(precio_control*cantidad)+(precio_gateway*cantidad)+precio_instalacion+(precio_roller*cantidad)
    
        print(f"total item:{total_item}")
        item.total=total_item
        item.save()
        total_resumen+=total_item

    resumen.total=total_resumen
    cotizacion_id=str(resumen.id).zfill(4)
    resumen.cotizacion_id=cotizacion_id
    resumen.save()
    resumen_total_igv=round(float(total_resumen)*1.18,2)


    context={
        'resumen':resumen,
        'detalles':detalles,
        'resumen_total_igv':resumen_total_igv,
        'cotizacion_id':cotizacion_id,
    }
    
    return render(request, 'cotizacion_export.html', context)
    

@login_required(login_url='/')
def panel_admin(request):
    if request.method == 'POST':
        print(request.POST)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('panel_admin')  # Redirige al usuario a la página de login o donde desees
    else:
        form = UserCreationForm()
    context={
        
    }
    return render(request, 'panel_admin.html', context)

def register(request):
    if request.method == 'POST':
        print(request.POST)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('panel_admin')  # Redirige al usuario a la página de login o donde desees
    else:
        form = UserCreationForm()
    return redirect('panel_admin')

    #return render(request, 'registration/register.html', {'form': form})


@login_required(login_url='/')
def admin_cotizaciones(request):
    cotizaciones=ResumenCotizacion.objects.all().order_by('-fecha')
    context={
        'cotizaciones':cotizaciones,
    }
    return render(request, 'admin_cotizaciones.html', context)

@login_required(login_url='/')
def panel_admin(request):
    context={}
    return render(request, 'panel_admin.html', context)

def get_diametros(request):
    roller_name = request.GET.get('roller_name')
    rollers = Roller.objects.filter(nombre=roller_name)
    diametros = Diametro.objects.filter(roller__in=rollers).distinct()
    diametro_list = [{'id': diametro.id, 'descripcion': diametro.descripcion} for diametro in diametros]
    return JsonResponse(diametro_list, safe=False)

def get_roller_id(request):
    roller_name = request.GET.get('roller_name')
    diametro_id = request.GET.get('diametro_id')
    try:
        rollers = Roller.objects.filter(nombre=roller_name,diametro_id=diametro_id).first()
        #diametros = Diametro.objects.filter(roller__in=rollers).distinct()
        roller_id = [{'id': rollers.id} ]
        print(f"Roller id:{roller_id}")
        return JsonResponse(roller_id, safe=False)
    except Exception as e:
        print(e)

def get_max_dimensions(request):
    roller_id = request.GET.get('roller_id')
    if roller_id:
        try:
            precios = Precio.objects.filter(roller_id=roller_id)
            total=len(precios)
            print(f"total de registros:{total}")
            max_ancho = precios.aggregate(Max('ancho_final'))['ancho_final__max']
            max_alto = precios.aggregate(Max('alto_final'))['alto_final__max']
            print(f"max_ancho:{max_ancho}")
            print(f"max_alto:{max_alto}")
            if max_alto is None:
                max_alto = 1
            if max_ancho is None:
                max_ancho = 1
            return JsonResponse({'max_ancho': max_ancho, 'max_alto': max_alto ,'total':total})
        except Exception as e:
            print(e)
            return JsonResponse({'max_ancho': 1, 'max_alto': 1})

    return JsonResponse({'max_ancho': 1, 'max_alto': 1})




def render_pdf_view(request,resumen_id):
    resumen = get_object_or_404(ResumenCotizacion, id=resumen_id)    
    detalles = DetalleCotizacion.objects.filter(resumen_cotizacion=resumen)
    total_resumen=0
    for item in detalles:
        total_item=0
        cantidad=item.cantidad
        print(f"cantidad:{cantidad}")
        precio_motor=0
        if(item.motor_id is not None):
            precio_motor = Motor.objects.get(id=item.motor_id).precio
        print(f"motor:{precio_motor}")
        precio_cenefa=0
        if(item.cenefa_id is not None):
            cenefa=Cenefa.objects.get(id=item.cenefa_id)
            precio_cenefa = cenefa.precio * (item.ancho)/1000
            print(f"cenefa:{cenefa.precio}")
            print(f"ancho:{item.ancho}")
            print(f"total cenefa:{precio_cenefa}")
        precio_control=0
        if(item.control_id is not None):
            precio_control = Control.objects.get(id=item.control_id).precio
        print(f"cont:{precio_control}")
        precio_gateway=0
        if(item.gateway_id is not None):
            precio_gateway = Gateway.objects.get(id=item.gateway_id).precio
        print(f"gat:{precio_gateway}")

        precio_roller=roller_price(item.roller,item.ancho,item.alto)
        print(f"roller:{precio_roller}")

        
        precio_instalacion=item.costo_instalacion_motor+item.costo_instalacion_cenefa+item.costo_instalacion_roller
        print(f"i-roller:{item.costo_instalacion_roller}")
        print(f"i-cen:{item.costo_instalacion_cenefa}")
        print(f"i-mot:{item.costo_instalacion_motor}")
        print(f"INST:{precio_instalacion}")
        total_item=(precio_motor*cantidad)+(precio_cenefa*cantidad)+(precio_control*cantidad)+(precio_gateway*cantidad)+precio_instalacion+(precio_roller*cantidad)
    
        print(f"total item:{total_item}")
        item.total=total_item
        item.save()
        total_resumen+=total_item

    resumen.total= round(total_resumen, 2)
    cotizacion_id=str(resumen.id).zfill(4)
    resumen.cotizacion_id=cotizacion_id
    resumen.save()
    resumen_total_igv=round(float(total_resumen)*1.18,2)

    image_path=os.path.join(settings.STATIC_URL  , 'images', 'deslizza2.jpeg')
    cliente=resumen.cliente.nombre
    titulo=f"Cotización {resumen.id}"
    # image_path=image_path.replace('\\','/')
    # print(image_path)
    # Datos que quieres pasar a la plantilla

    context={
        'title': titulo,
        'resumen':resumen,
        'detalles':detalles,
        'resumen_total_igv':resumen_total_igv,
        'cotizacion_id':cotizacion_id,
        'image_path':image_path ,
        'cliente':cliente,
    }
   
    
    template_path = 'test_cotizacion.html'

    template = get_template(template_path)
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, link_callback=link_callback)
    if not pdf.err:
        pdf=result.getvalue()
    else:
        pdf=None
    if pdf:    
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"cotizacion_{cotizacion_id}.pdf"
        content = f"inline; filename={filename}"
        download = request.GET.get("download")
        if download:
            content = f"attachment; filename={filename}"
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Error Generando PDF", status=400)
    
    

