from django.urls import path
from . import views

app_name = 'administracion'

urlpatterns = [
    # Dashboard principal
    path('dashboard/', views.dashboard_admin, name='dashboard'),
    
    # Gestión de usuarios
    path('usuarios/', views.gestion_usuarios, name='gestion_usuarios'),
    
    # Estadísticas
    path('estadisticas/', views.estadisticas, name='estadisticas'),
] 