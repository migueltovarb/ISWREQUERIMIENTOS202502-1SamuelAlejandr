from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Especialidad, Doctor, HorarioAtencion, ExcepcionHorario

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activa', 'cantidad_doctores', 'fecha_creacion']
    list_filter = ['activa', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    ordering = ['nombre']
    
    def cantidad_doctores(self, obj):
        """Muestra la cantidad de doctores activos en esta especialidad"""
        count = obj.doctor_set.filter(activo=True).count()
        return f"{count} doctor{'es' if count != 1 else ''}"
    cantidad_doctores.short_description = 'Doctores Activos'

class HorarioAtencionInline(admin.TabularInline):
    model = HorarioAtencion
    extra = 0
    fields = ['dia_semana', 'hora_inicio', 'hora_fin', 'duracion_cita', 'activo']
    ordering = ['dia_semana']

class ExcepcionHorarioInline(admin.TabularInline):
    model = ExcepcionHorario
    extra = 0
    fields = ['fecha_inicio', 'fecha_fin', 'tipo_excepcion', 'motivo', 'todo_el_dia']
    readonly_fields = ['fecha_creacion', 'creado_por']
    ordering = ['-fecha_inicio']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = [
        'get_nombre_completo', 'especialidad', 'numero_licencia', 
        'consultorio', 'activo', 'tiene_horarios', 'fecha_creacion'
    ]
    list_filter = ['especialidad', 'activo', 'fecha_creacion']
    search_fields = [
        'usuario__first_name', 'usuario__last_name', 'usuario__email',
        'numero_licencia', 'especialidad__nombre'
    ]
    ordering = ['usuario__first_name', 'usuario__last_name']
    
    fieldsets = (
        ('Información del Doctor', {
            'fields': ('usuario', 'especialidad', 'numero_licencia')
        }),
        ('Información del Consultorio', {
            'fields': ('consultorio', 'telefono_consultorio')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )
    
    inlines = [HorarioAtencionInline, ExcepcionHorarioInline]
    
    def get_nombre_completo(self, obj):
        """Muestra el nombre completo del doctor"""
        return obj.get_nombre_completo()
    get_nombre_completo.short_description = 'Nombre Completo'
    get_nombre_completo.admin_order_field = 'usuario__first_name'
    
    def tiene_horarios(self, obj):
        """Indica si el doctor tiene horarios configurados"""
        count = obj.horarios_atencion.filter(activo=True).count()
        if count > 0:
            return format_html(
                '<span style="color: green;">✓ {} día{}</span>',
                count,
                's' if count != 1 else ''
            )
        else:
            return format_html('<span style="color: red;">✗ Sin horarios</span>')
    tiene_horarios.short_description = 'Horarios Configurados'
    
    def save_model(self, request, obj, form, change):
        """Personalizar el guardado para asegurar el tipo de usuario"""
        if obj.usuario.tipo_usuario != 'doctor':
            obj.usuario.tipo_usuario = 'doctor'
            obj.usuario.save()
        super().save_model(request, obj, form, change)

@admin.register(HorarioAtencion)
class HorarioAtencionAdmin(admin.ModelAdmin):
    list_display = [
        'doctor', 'get_dia_semana_display', 'hora_inicio', 'hora_fin', 
        'duracion_cita', 'activo'
    ]
    list_filter = ['dia_semana', 'activo', 'doctor__especialidad']
    search_fields = ['doctor__usuario__first_name', 'doctor__usuario__last_name']
    ordering = ['doctor', 'dia_semana', 'hora_inicio']
    
    fieldsets = (
        ('Doctor y Día', {
            'fields': ('doctor', 'dia_semana')
        }),
        ('Horario', {
            'fields': ('hora_inicio', 'hora_fin', 'duracion_cita')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )

@admin.register(ExcepcionHorario)
class ExcepcionHorarioAdmin(admin.ModelAdmin):
    list_display = [
        'doctor', 'tipo_excepcion', 'fecha_inicio', 'fecha_fin', 
        'todo_el_dia', 'notificado', 'esta_activa_display'
    ]
    list_filter = ['tipo_excepcion', 'todo_el_dia', 'notificado', 'fecha_inicio']
    search_fields = ['doctor__usuario__first_name', 'doctor__usuario__last_name', 'motivo']
    ordering = ['-fecha_inicio']
    
    fieldsets = (
        ('Doctor y Tipo', {
            'fields': ('doctor', 'tipo_excepcion')
        }),
        ('Fechas y Horarios', {
            'fields': ('fecha_inicio', 'fecha_fin', 'todo_el_dia')
        }),
        ('Descripción', {
            'fields': ('motivo',)
        }),
        ('Estado', {
            'fields': ('notificado',)
        }),
        ('Auditoría', {
            'fields': ('creado_por',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['fecha_creacion']
    
    def esta_activa_display(self, obj):
        """Muestra si la excepción está actualmente activa"""
        if obj.esta_activa():
            return format_html('<span style="color: orange;">🔴 Activa</span>')
        else:
            return format_html('<span style="color: green;">✓ Inactiva</span>')
    esta_activa_display.short_description = 'Estado Actual'
    
    def save_model(self, request, obj, form, change):
        """Asignar el usuario que crea la excepción"""
        if not change:  # Solo en creación
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)
