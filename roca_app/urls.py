from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='home'),

    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('crear_producto/', views.crear_producto, name='crear_producto'),
    path('cotizaciones/', views.cotizaciones, name='cotizaciones'),
    path('register/', views.register, name='register'),

    path('dashboard/', views.dashboard_redirect, name='dashboard'),

    # init generar cotizacion
    path('panel_usuario/', views.panel_usuario, name='panel_usuario'),
    # agrega items cotizacion
    path('usuario_producto/<int:cliente_id>/<int:resumen_id>/', views.usuario_producto, name='usuario_producto'),
    # export pdf
    path('cotizacion_export/<int:resumen_id>', views.cotizacion_export, name='cotizacion_export'),
    #admin
    path('panel_admin/', views.panel_admin, name='panel_admin'),
    path('admin_cotizaciones/', views.admin_cotizaciones, name='admin_cotizaciones'),

    #path('cotizacion_export/', views.cotizacion_export, name='cotizacion_export'),
    path('get_diametros/', views.get_diametros, name='get_diametros'),
    path('get_roller_id/', views.get_roller_id, name='get_roller_id'),
    path('get_max_dimensions/', views.get_max_dimensions, name='get_max_dimensions'),
    path('generate-pdf/<int:resumen_id>', views.render_pdf_view, name='generate_pdf'),
]