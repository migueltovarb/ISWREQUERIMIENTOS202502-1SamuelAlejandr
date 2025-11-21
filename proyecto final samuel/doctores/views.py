from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from datetime import datetime, timedelta

from .models import Doctor, Especialidad, HorarioAtencion, ExcepcionHorario
from .forms import (
    CrearDoctorForm, EditarDoctorForm, HorarioAtencionForm, 
    ExcepcionHorarioForm, FiltroCalendarioForm, ConsultaDisponibilidadForm
)

def es_administrador(user):
    """Verifica si el usuario es administrador"""
    return user.is_authenticated and user.es_administrador()

def es_doctor_o_admin(user):
    """Verifica si el usuario es doctor o administrador"""
    return user.is_authenticated and (user.es_doctor() or user.es_administrador())

def es_staff_o_admin(user):
    """Verifica si el usuario es staff (recepción) o administrador"""
    return user.is_authenticated and (user.es_recepcion() or user.es_administrador())

# ==================== VISTAS PARA ADMINISTRADORES ====================

@login_required
@user_passes_test(es_administrador)
def lista_doctores(request):
    """
    HU0011: Lista todos los doctores para administradores
    """
    doctores = Doctor.objects.select_related('usuario', 'especialidad').all()
    
    # Filtros de búsqueda
    busqueda = request.GET.get('busqueda', '')
    especialidad_id = request.GET.get('especialidad', '')
    activo = request.GET.get('activo', '')
    
    if busqueda:
        doctores = doctores.filter(
            Q(usuario__first_name__icontains=busqueda) |
            Q(usuario__last_name__icontains=busqueda) |
            Q(usuario__email__icontains=busqueda) |
            Q(numero_licencia__icontains=busqueda)
        )
    
    if especialidad_id:
        doctores = doctores.filter(especialidad_id=especialidad_id)
    
    if activo:
        doctores = doctores.filter(activo=activo == 'true')
    
    # Paginación
    paginator = Paginator(doctores, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    especialidades = Especialidad.objects.filter(activa=True)
    
    context = {
        'page_obj': page_obj,
        'especialidades': especialidades,
        'busqueda': busqueda,
        'especialidad_seleccionada': especialidad_id,
        'activo_seleccionado': activo,
    }
    
    return render(request, 'doctores/lista_doctores.html', context)

@login_required
@user_passes_test(es_administrador)
def crear_doctor(request):
    """
    HU0011: Crear un nuevo doctor
    """
    if request.method == 'POST':
        form = CrearDoctorForm(request.POST)
        if form.is_valid():
            try:
                doctor = form.save()
                messages.success(
                    request, 
                    f'Doctor {doctor.get_nombre_completo()} creado exitosamente.'
                )
                return redirect('doctores:lista_doctores')
            except Exception as e:
                messages.error(request, f'Error al crear el doctor: {str(e)}')
    else:
        form = CrearDoctorForm()
    
    return render(request, 'doctores/crear_doctor.html', {'form': form})

@login_required
@user_passes_test(es_administrador)
def editar_doctor(request, doctor_id):
    """
    HU0011: Editar información de un doctor existente
    """
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    if request.method == 'POST':
        form = EditarDoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            try:
                doctor = form.save()
                messages.success(
                    request, 
                    f'Doctor {doctor.get_nombre_completo()} actualizado exitosamente.'
                )
                return redirect('doctores:lista_doctores')
            except Exception as e:
                messages.error(request, f'Error al actualizar el doctor: {str(e)}')
    else:
        form = EditarDoctorForm(instance=doctor)
    
    context = {
        'form': form,
        'doctor': doctor,
    }
    
    return render(request, 'doctores/editar_doctor.html', context)

@login_required
@user_passes_test(es_administrador)
def eliminar_doctor(request, doctor_id):
    """
    HU0011: Eliminar un doctor (solo si no tiene citas futuras)
    """
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    # TODO: Verificar si tiene citas futuras cuando se implemente el modelo Cita
    # Por ahora solo desactivamos
    
    if request.method == 'POST':
        try:
            doctor.activo = False
            doctor.save()
            messages.success(
                request, 
                f'Doctor {doctor.get_nombre_completo()} desactivado exitosamente.'
            )
        except Exception as e:
            messages.error(request, f'Error al desactivar el doctor: {str(e)}')
        
        return redirect('doctores:lista_doctores')
    
    context = {
        'doctor': doctor,
    }
    
    return render(request, 'doctores/confirmar_eliminar_doctor.html', context)

# ==================== VISTAS PARA DOCTORES ====================

@login_required
@user_passes_test(es_doctor_o_admin)
def gestionar_horarios(request):
    """
    HU0007: Gestionar horarios de atención del doctor
    """
    # Obtener el doctor actual
    if request.user.es_doctor():
        doctor = get_object_or_404(Doctor, usuario=request.user)
    else:
        # Si es admin, puede gestionar horarios de cualquier doctor
        doctor_id = request.GET.get('doctor_id')
        if doctor_id:
            doctor = get_object_or_404(Doctor, id=doctor_id)
        else:
            # Si no se especifica doctor_id, redirigir a la lista de doctores
            messages.info(request, 'Selecciona un doctor para gestionar sus horarios.')
            return redirect('doctores:lista_doctores')
    
    horarios = HorarioAtencion.objects.filter(doctor=doctor).order_by('dia_semana')
    
    if request.method == 'POST':
        form = HorarioAtencionForm(request.POST)
        if form.is_valid():
            horario = form.save(commit=False)
            horario.doctor = doctor
            try:
                horario.save()
                messages.success(request, 'Horario agregado exitosamente.')
                if request.user.es_administrador():
                    return redirect(f'{request.path}?doctor_id={doctor.id}')
                else:
                    return redirect('doctores:gestionar_horarios')
            except Exception as e:
                messages.error(request, f'Error al guardar el horario: {str(e)}')
    else:
        form = HorarioAtencionForm()
    
    context = {
        'doctor': doctor,
        'horarios': horarios,
        'form': form,
    }
    
    return render(request, 'doctores/gestionar_horarios.html', context)

@login_required
@user_passes_test(es_doctor_o_admin)
def editar_horario(request, horario_id):
    """
    HU0007: Editar un horario específico
    """
    horario = get_object_or_404(HorarioAtencion, id=horario_id)
    
    # Verificar permisos
    if request.user.es_doctor() and horario.doctor.usuario != request.user:
        messages.error(request, 'No tienes permisos para editar este horario.')
        return redirect('doctores:gestionar_horarios')
    
    if request.method == 'POST':
        form = HorarioAtencionForm(request.POST, instance=horario)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Horario actualizado exitosamente.')
                
                # Redirigir según el tipo de usuario
                if request.user.es_administrador():
                    url = reverse('doctores:gestionar_horarios') + f'?doctor_id={horario.doctor.id}'
                    return HttpResponseRedirect(url)
                else:
                    return redirect('doctores:gestionar_horarios')
            except Exception as e:
                messages.error(request, f'Error al actualizar el horario: {str(e)}')
    else:
        form = HorarioAtencionForm(instance=horario)
    
    context = {
        'form': form,
        'horario': horario,
    }
    
    return render(request, 'doctores/editar_horario.html', context)

@login_required
@user_passes_test(es_doctor_o_admin)
def eliminar_horario(request, horario_id):
    """
    HU0007: Eliminar un horario
    """
    horario = get_object_or_404(HorarioAtencion, id=horario_id)
    
    # Verificar permisos
    if request.user.es_doctor() and horario.doctor.usuario != request.user:
        messages.error(request, 'No tienes permisos para eliminar este horario.')
        return redirect('doctores:gestionar_horarios')
    
    if request.method == 'POST':
        try:
            doctor_id = horario.doctor.id
            horario.delete()
            messages.success(request, 'Horario eliminado exitosamente.')
            
            # Redirigir según el tipo de usuario
            if request.user.es_administrador():
                url = reverse('doctores:gestionar_horarios') + f'?doctor_id={doctor_id}'
                return HttpResponseRedirect(url)
            else:
                return redirect('doctores:gestionar_horarios')
        except Exception as e:
            messages.error(request, f'Error al eliminar el horario: {str(e)}')
        
        return redirect('doctores:gestionar_horarios')
    
    context = {
        'horario': horario,
    }
    
    return render(request, 'doctores/confirmar_eliminar_horario.html', context)

@login_required
@user_passes_test(es_doctor_o_admin)
def gestionar_excepciones(request):
    """
    HU0008: Gestionar excepciones de horario
    """
    # Obtener el doctor actual
    if request.user.es_doctor():
        doctor = get_object_or_404(Doctor, usuario=request.user)
    else:
        # Si es admin, puede gestionar excepciones de cualquier doctor
        doctor_id = request.GET.get('doctor_id')
        if doctor_id:
            doctor = get_object_or_404(Doctor, id=doctor_id)
        else:
            # Si no se especifica doctor_id, redirigir a la lista de doctores
            messages.info(request, 'Selecciona un doctor para gestionar sus excepciones.')
            return redirect('doctores:lista_doctores')
    
    excepciones = ExcepcionHorario.objects.filter(
        doctor=doctor,
        fecha_fin__gte=timezone.now()
    ).order_by('fecha_inicio')
    
    if request.method == 'POST':
        form = ExcepcionHorarioForm(request.POST)
        if form.is_valid():
            excepcion = form.save(commit=False)
            excepcion.doctor = doctor
            excepcion.creado_por = request.user
            try:
                excepcion.save()
                messages.success(request, 'Excepción de horario registrada exitosamente.')
                if request.user.es_administrador():
                    return redirect(f'{request.path}?doctor_id={doctor.id}')
                else:
                    return redirect('doctores:gestionar_excepciones')
            except Exception as e:
                messages.error(request, f'Error al registrar la excepción: {str(e)}')
    else:
        form = ExcepcionHorarioForm()
    
    context = {
        'doctor': doctor,
        'excepciones': excepciones,
        'form': form,
    }
    
    return render(request, 'doctores/gestionar_excepciones.html', context)

@login_required
@user_passes_test(es_doctor_o_admin)
def eliminar_excepcion(request, excepcion_id):
    """
    HU0008: Eliminar una excepción de horario
    """
    excepcion = get_object_or_404(ExcepcionHorario, id=excepcion_id)
    
    # Verificar permisos
    if request.user.es_doctor() and excepcion.doctor.usuario != request.user:
        messages.error(request, 'No tienes permisos para eliminar esta excepción.')
        return redirect('doctores:gestionar_excepciones')
    
    if request.method == 'POST':
        try:
            doctor_id = excepcion.doctor.id
            excepcion.delete()
            messages.success(request, 'Excepción eliminada exitosamente.')
            
            # Redirigir según el tipo de usuario
            if request.user.es_administrador():
                url = reverse('doctores:gestionar_excepciones') + f'?doctor_id={doctor_id}'
                return HttpResponseRedirect(url)
            else:
                return redirect('doctores:gestionar_excepciones')
        except Exception as e:
            messages.error(request, f'Error al eliminar la excepción: {str(e)}')
    
    context = {
        'excepcion': excepcion,
    }
    
    return render(request, 'doctores/confirmar_eliminar_excepcion.html', context)

# ==================== VISTAS PARA CALENDARIO ====================

@login_required
@user_passes_test(es_staff_o_admin)
def calendario_citas(request):
    """
    HU0012: Visualizar calendario de citas
    """
    form = FiltroCalendarioForm(request.GET or None, user=request.user)
    
    fecha_seleccionada = timezone.now().date()
    doctor_seleccionado = None
    
    if form.is_valid():
        fecha_seleccionada = form.cleaned_data['fecha']
        doctor_seleccionado = form.cleaned_data.get('doctor')
    
    # Obtener doctores según el tipo de usuario
    if request.user.es_doctor():
        doctores = Doctor.objects.filter(usuario=request.user, activo=True)
        doctor_seleccionado = doctores.first()
    elif doctor_seleccionado:
        doctores = [doctor_seleccionado]
    else:
        doctores = Doctor.objects.filter(activo=True)
    
    # Generar franjas horarias para la fecha seleccionada
    franjas_por_doctor = {}
    
    for doctor in doctores:
        franjas_por_doctor[doctor] = generar_franjas_dia(doctor, fecha_seleccionada)
    
    context = {
        'form': form,
        'fecha_seleccionada': fecha_seleccionada,
        'doctor_seleccionado': doctor_seleccionado,
        'franjas_por_doctor': franjas_por_doctor,
    }
    
    return render(request, 'doctores/calendario_citas.html', context)

def consultar_disponibilidad(request):
    """
    HU0001: Consultar disponibilidad de doctores
    Vista pública para que pacientes y recepción consulten disponibilidad
    """
    form = ConsultaDisponibilidadForm(request.GET or None)
    doctores_disponibilidad = {}
    fecha_inicio = None
    fecha_fin = None
    
    if form.is_valid():
        fecha_inicio = form.cleaned_data['fecha_inicio']
        fecha_fin = form.cleaned_data['fecha_fin']
        especialidad = form.cleaned_data.get('especialidad')
        doctor_especifico = form.cleaned_data.get('doctor')
        
        # Filtrar doctores según criterios
        doctores = Doctor.objects.filter(activo=True)
        
        if especialidad:
            doctores = doctores.filter(especialidad=especialidad)
        
        if doctor_especifico:
            doctores = doctores.filter(id=doctor_especifico.id)
        
        # Generar disponibilidad para el rango de fechas
        fecha_actual = fecha_inicio
        while fecha_actual <= fecha_fin:
            for doctor in doctores:
                if doctor not in doctores_disponibilidad:
                    doctores_disponibilidad[doctor] = {}
                
                franjas = generar_franjas_dia(doctor, fecha_actual)
                # Solo incluir franjas disponibles
                franjas_disponibles = [f for f in franjas if f['estado'] == 'disponible']
                
                if franjas_disponibles:
                    doctores_disponibilidad[doctor][fecha_actual] = franjas_disponibles
            
            fecha_actual += timedelta(days=1)
    
    context = {
        'form': form,
        'doctores_disponibilidad': doctores_disponibilidad,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'hay_resultados': bool(doctores_disponibilidad),
    }
    
    return render(request, 'doctores/consultar_disponibilidad.html', context)

def generar_franjas_dia(doctor, fecha):
    """
    Genera las franjas horarias para un doctor en una fecha específica
    """
    dia_semana = fecha.weekday()  # 0=Lunes, 6=Domingo
    
    # Obtener horario del doctor para ese día
    try:
        horario = HorarioAtencion.objects.get(
            doctor=doctor,
            dia_semana=dia_semana,
            activo=True
        )
    except HorarioAtencion.DoesNotExist:
        return []
    
    # Generar franjas cada X minutos según la duración de cita
    franjas = []
    hora_actual = datetime.combine(fecha, horario.hora_inicio)
    hora_fin = datetime.combine(fecha, horario.hora_fin)
    
    while hora_actual < hora_fin:
        # Verificar si hay excepción en esta franja
        hay_excepcion = ExcepcionHorario.objects.filter(
            doctor=doctor,
            fecha_inicio__lte=hora_actual,
            fecha_fin__gt=hora_actual
        ).exists()
        
        # TODO: Verificar si hay cita confirmada en esta franja
        # cuando se implemente el modelo Cita
        hay_cita = False
        
        estado = 'no_disponible' if hay_excepcion else ('ocupado' if hay_cita else 'disponible')
        
        franjas.append({
            'hora': hora_actual.time(),
            'estado': estado,
            'paciente': None,  # TODO: Obtener paciente cuando se implemente
        })
        
        hora_actual += timedelta(minutes=horario.duracion_cita)
    
    return franjas

# ==================== VISTAS AJAX ====================

@login_required
def obtener_horarios_doctor(request, doctor_id):
    """
    Vista AJAX para obtener horarios de un doctor específico
    """
    doctor = get_object_or_404(Doctor, id=doctor_id)
    horarios = HorarioAtencion.objects.filter(doctor=doctor, activo=True)
    
    data = []
    for horario in horarios:
        data.append({
            'dia_semana': horario.dia_semana,
            'dia_nombre': horario.get_dia_semana_display(),
            'hora_inicio': horario.hora_inicio.strftime('%H:%M'),
            'hora_fin': horario.hora_fin.strftime('%H:%M'),
            'duracion_cita': horario.duracion_cita,
        })
    
    return JsonResponse({'horarios': data})

@login_required
def obtener_excepciones_doctor(request, doctor_id):
    """
    Vista AJAX para obtener excepciones de un doctor específico
    """
    doctor = get_object_or_404(Doctor, id=doctor_id)
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    excepciones = ExcepcionHorario.objects.filter(doctor=doctor)
    
    if fecha_inicio:
        excepciones = excepciones.filter(fecha_fin__gte=fecha_inicio)
    if fecha_fin:
        excepciones = excepciones.filter(fecha_inicio__lte=fecha_fin)
    
    data = []
    for excepcion in excepciones:
        data.append({
            'id': excepcion.id,
            'fecha_inicio': excepcion.fecha_inicio.isoformat(),
            'fecha_fin': excepcion.fecha_fin.isoformat(),
            'tipo': excepcion.get_tipo_excepcion_display(),
            'motivo': excepcion.motivo,
            'todo_el_dia': excepcion.todo_el_dia,
        })
    
    return JsonResponse({'excepciones': data})
