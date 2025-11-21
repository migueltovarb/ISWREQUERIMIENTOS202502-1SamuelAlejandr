from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Página de inicio
    path('', views.home_view, name='home'),
    
    # Autenticación
    path('login/', views.inicio_sesion_view, name='login'),
    path('logout/', views.cerrar_sesion_view, name='logout'),
    
    # Registro
    path('registro/', views.RegistroPacienteView.as_view(), name='registro'),
    path('registro/exitoso/', views.registro_exitoso_view, name='registro_exitoso'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
] 