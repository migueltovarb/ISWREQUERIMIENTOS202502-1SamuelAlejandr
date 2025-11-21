from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime

Usuario = get_user_model()

class Especialidad(models.Model):
    """
    Modelo para las especialidades médicas
    """
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre de la Especialidad'
    )
    
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción'
    )
    
    activa = models.BooleanField(
        default=True,
        verbose_name='Especialidad Activa'
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    
    class Meta:
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Doctor(models.Model):
    """
    Modelo para los doctores del sistema
    """
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo_usuario': 'doctor'},
        verbose_name='Usuario'
    )
    
    especialidad = models.ForeignKey(
        Especialidad,
        on_delete=models.PROTECT,
        verbose_name='Especialidad'
    )
    
    numero_licencia = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Número de Licencia Médica'
    )
    
    telefono_consultorio = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Teléfono del Consultorio'
    )
    
    consultorio = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Número/Nombre del Consultorio'
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Doctor Activo'
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de Actualización'
    )
    
    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctores'
        ordering = ['usuario__first_name', 'usuario__last_name']
    
    def __str__(self):
        return f"Dr. {self.usuario.get_full_name()} - {self.especialidad.nombre}"
    
    def get_nombre_completo(self):
        """Retorna el nombre completo del doctor"""
        return self.usuario.get_full_name()
    
    def save(self, *args, **kwargs):
        """
        Método save personalizado para asegurar que el usuario sea de tipo doctor
        """
        if self.usuario.tipo_usuario != 'doctor':
            self.usuario.tipo_usuario = 'doctor'
            self.usuario.save()
        
        super().save(*args, **kwargs)

class HorarioAtencion(models.Model):
    """
    Modelo para los horarios regulares de atención de los doctores
    """
    DIAS_SEMANA = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='horarios_atencion',
        verbose_name='Doctor'
    )
    
    dia_semana = models.IntegerField(
        choices=DIAS_SEMANA,
        verbose_name='Día de la Semana'
    )
    
    hora_inicio = models.TimeField(
        verbose_name='Hora de Inicio'
    )
    
    hora_fin = models.TimeField(
        verbose_name='Hora de Fin'
    )
    
    duracion_cita = models.IntegerField(
        default=30,
        verbose_name='Duración de Cita (minutos)',
        help_text='Duración estándar de cada cita en minutos'
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Horario Activo'
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    
    class Meta:
        verbose_name = 'Horario de Atención'
        verbose_name_plural = 'Horarios de Atención'
        unique_together = ['doctor', 'dia_semana']
        ordering = ['doctor', 'dia_semana', 'hora_inicio']
    
    def clean(self):
        """Validaciones personalizadas"""
        # Solo validar si ambas horas están presentes
        if self.hora_inicio and self.hora_fin:
            if self.hora_inicio >= self.hora_fin:
                raise ValidationError('La hora de inicio debe ser anterior a la hora de fin.')
        
        # Solo validar duración si está presente
        if self.duracion_cita is not None and self.duracion_cita <= 0:
            raise ValidationError('La duración de la cita debe ser mayor a 0 minutos.')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.doctor} - {self.get_dia_semana_display()}: {self.hora_inicio} - {self.hora_fin}"

class ExcepcionHorario(models.Model):
    """
    Modelo para excepciones o bloqueos en los horarios de los doctores
    """
    TIPO_EXCEPCION_CHOICES = [
        ('vacaciones', 'Vacaciones'),
        ('licencia', 'Licencia Médica'),
        ('reunion', 'Reunión'),
        ('capacitacion', 'Capacitación'),
        ('personal', 'Asunto Personal'),
        ('otro', 'Otro'),
    ]
    
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='excepciones_horario',
        verbose_name='Doctor'
    )
    
    fecha_inicio = models.DateTimeField(
        verbose_name='Fecha y Hora de Inicio'
    )
    
    fecha_fin = models.DateTimeField(
        verbose_name='Fecha y Hora de Fin'
    )
    
    tipo_excepcion = models.CharField(
        max_length=20,
        choices=TIPO_EXCEPCION_CHOICES,
        default='otro',
        verbose_name='Tipo de Excepción'
    )
    
    motivo = models.TextField(
        verbose_name='Motivo/Descripción'
    )
    
    todo_el_dia = models.BooleanField(
        default=False,
        verbose_name='Todo el Día',
        help_text='Marcar si la excepción es para todo el día'
    )
    
    notificado = models.BooleanField(
        default=False,
        verbose_name='Pacientes Notificados',
        help_text='Indica si ya se notificó a los pacientes afectados'
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    
    creado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Creado por'
    )
    
    class Meta:
        verbose_name = 'Excepción de Horario'
        verbose_name_plural = 'Excepciones de Horario'
        ordering = ['-fecha_inicio']
    
    def clean(self):
        """Validaciones personalizadas"""
        # Solo validar si ambas fechas están presentes
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_inicio >= self.fecha_fin:
                raise ValidationError('La fecha de inicio debe ser anterior a la fecha de fin.')
        
        # Solo validar fecha pasada si fecha_inicio está presente
        if self.fecha_inicio and self.fecha_inicio < timezone.now():
            raise ValidationError('No se pueden crear excepciones para fechas pasadas.')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.doctor} - {self.get_tipo_excepcion_display()}: {self.fecha_inicio.strftime('%d/%m/%Y')}"
    
    def esta_activa(self):
        """Verifica si la excepción está actualmente activa"""
        ahora = timezone.now()
        return self.fecha_inicio <= ahora <= self.fecha_fin
