from django.urls import path
from . import views

app_name = 'doctores'

urlpatterns = [
    # URLs para administradores - Gestión de doctores (HU0011)
    path('', views.lista_doctores, name='lista_doctores'),
    path('crear/', views.crear_doctor, name='crear_doctor'),
    path('<int:doctor_id>/editar/', views.editar_doctor, name='editar_doctor'),
    path('<int:doctor_id>/eliminar/', views.eliminar_doctor, name='eliminar_doctor'),
    
    # URLs para doctores - Gestión de horarios (HU0007)
    path('horarios/', views.gestionar_horarios, name='gestionar_horarios'),
    path('horarios/<int:horario_id>/editar/', views.editar_horario, name='editar_horario'),
    path('horarios/<int:horario_id>/eliminar/', views.eliminar_horario, name='eliminar_horario'),
    
    # URLs para doctores - Gestión de excepciones (HU0008)
    path('excepciones/', views.gestionar_excepciones, name='gestionar_excepciones'),
    path('excepciones/<int:excepcion_id>/eliminar/', views.eliminar_excepcion, name='eliminar_excepcion'),
    
    # URLs para calendario (HU0012)
    path('calendario/', views.calendario_citas, name='calendario_citas'),
    
    # URLs para consulta de disponibilidad (HU0001)
    path('disponibilidad/', views.consultar_disponibilidad, name='consultar_disponibilidad'),
    
    # URLs AJAX
    path('api/<int:doctor_id>/horarios/', views.obtener_horarios_doctor, name='obtener_horarios_doctor'),
    path('api/<int:doctor_id>/excepciones/', views.obtener_excepciones_doctor, name='obtener_excepciones_doctor'),
] 