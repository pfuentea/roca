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


    path('panel_usuario/', views.panel_usuario, name='panel_usuario'),
    path('usuario_producto/', views.usuario_producto, name='usuario_producto'),
    path('cotizacion_export/', views.cotizacion_export, name='cotizacion_export'),

    path('panel_admin/', views.panel_admin, name='panel_admin'),
    path('admin_cotizaciones/', views.admin_cotizaciones, name='admin_cotizaciones'),
    path('cotizacion_export/', views.cotizacion_export, name='cotizacion_export'),

]