from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model

from doctores.models import Doctor, Especialidad, HorarioAtencion, ExcepcionHorario
# from citas.models import Cita  # Se descomentará cuando se implemente

Usuario = get_user_model()

def es_administrador(user):
    """Verifica si el usuario es administrador"""
    return user.is_authenticated and user.es_administrador()

@login_required
@user_passes_test(es_administrador)
def dashboard_admin(request):
    """
    Dashboard principal para administradores
    """
    # Estadísticas generales
    total_doctores = Doctor.objects.filter(activo=True).count()
    total_especialidades = Especialidad.objects.filter(activa=True).count()
    total_usuarios = Usuario.objects.filter(is_active=True).count()
    
    # Doctores sin horarios configurados
    doctores_sin_horarios = Doctor.objects.filter(
        activo=True,
        horarios_atencion__isnull=True
    ).distinct().count()
    
    # Excepciones activas hoy
    hoy = timezone.now().date()
    excepciones_hoy = ExcepcionHorario.objects.filter(
        fecha_inicio__date__lte=hoy,
        fecha_fin__date__gte=hoy
    ).count()
    
    # Doctores por especialidad
    doctores_por_especialidad = Especialidad.objects.filter(
        activa=True
    ).annotate(
        total_doctores=Count('doctor', filter=Q(doctor__activo=True))
    ).order_by('-total_doctores')
    
    # Últimos doctores registrados
    ultimos_doctores = Doctor.objects.filter(
        activo=True
    ).select_related('usuario', 'especialidad').order_by('-fecha_creacion')[:5]
    
    # Excepciones próximas (próximos 7 días)
    fecha_limite = timezone.now() + timedelta(days=7)
    excepciones_proximas = ExcepcionHorario.objects.filter(
        fecha_inicio__gte=timezone.now(),
        fecha_inicio__lte=fecha_limite
    ).select_related('doctor', 'doctor__usuario').order_by('fecha_inicio')[:5]
    
    # Usuarios por tipo
    usuarios_por_tipo = {
        'administradores': Usuario.objects.filter(tipo_usuario='administrador', is_active=True).count(),
        'doctores': Usuario.objects.filter(tipo_usuario='doctor', is_active=True).count(),
        'recepcion': Usuario.objects.filter(tipo_usuario='recepcion', is_active=True).count(),
        'pacientes': Usuario.objects.filter(tipo_usuario='paciente', is_active=True).count(),
    }
    
    # TODO: Cuando se implemente el modelo Cita, agregar estas estadísticas:
    # - Total de citas del día
    # - Citas pendientes
    # - Citas por estado
    # - Gráfico de citas por mes
    
    context = {
        'total_doctores': total_doctores,
        'total_especialidades': total_especialidades,
        'total_usuarios': total_usuarios,
        'doctores_sin_horarios': doctores_sin_horarios,
        'excepciones_hoy': excepciones_hoy,
        'doctores_por_especialidad': doctores_por_especialidad,
        'ultimos_doctores': ultimos_doctores,
        'excepciones_proximas': excepciones_proximas,
        'usuarios_por_tipo': usuarios_por_tipo,
    }
    
    return render(request, 'administracion/dashboard.html', context)

@login_required
@user_passes_test(es_administrador)
def gestion_usuarios(request):
    """
    Vista para gestionar usuarios del sistema
    """
    usuarios = Usuario.objects.filter(is_active=True).order_by('-date_joined')
    
    # Filtros
    tipo_usuario = request.GET.get('tipo', '')
    busqueda = request.GET.get('busqueda', '')
    
    if tipo_usuario:
        usuarios = usuarios.filter(tipo_usuario=tipo_usuario)
    
    if busqueda:
        usuarios = usuarios.filter(
            Q(first_name__icontains=busqueda) |
            Q(last_name__icontains=busqueda) |
            Q(email__icontains=busqueda)
        )
    
    context = {
        'usuarios': usuarios,
        'tipo_seleccionado': tipo_usuario,
        'busqueda': busqueda,
        'tipos_usuario': Usuario.TIPO_USUARIO_CHOICES,
    }
    
    return render(request, 'administracion/gestion_usuarios.html', context)

@login_required
@user_passes_test(es_administrador)
def estadisticas(request):
    """
    Vista para mostrar estadísticas detalladas del sistema
    """
    # Estadísticas por mes (últimos 6 meses)
    fecha_inicio = timezone.now() - timedelta(days=180)
    
    # Doctores registrados por mes
    doctores_por_mes = []
    for i in range(6):
        fecha = timezone.now() - timedelta(days=30*i)
        inicio_mes = fecha.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if i == 0:
            fin_mes = timezone.now()
        else:
            fin_mes = inicio_mes.replace(month=inicio_mes.month+1) if inicio_mes.month < 12 else inicio_mes.replace(year=inicio_mes.year+1, month=1)
        
        count = Doctor.objects.filter(
            fecha_creacion__gte=inicio_mes,
            fecha_creacion__lt=fin_mes
        ).count()
        
        doctores_por_mes.append({
            'mes': inicio_mes.strftime('%B %Y'),
            'count': count
        })
    
    doctores_por_mes.reverse()
    
    # Horarios por día de la semana
    horarios_por_dia = []
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    
    for i, dia in enumerate(dias_semana):
        count = HorarioAtencion.objects.filter(dia_semana=i, activo=True).count()
        horarios_por_dia.append({
            'dia': dia,
            'count': count
        })
    
    context = {
        'doctores_por_mes': doctores_por_mes,
        'horarios_por_dia': horarios_por_dia,
    }
    
    return render(request, 'administracion/estadisticas.html', context)
