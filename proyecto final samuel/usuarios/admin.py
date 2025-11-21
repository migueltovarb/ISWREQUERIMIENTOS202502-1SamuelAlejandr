from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Configuración del admin para el modelo Usuario personalizado
    """
    
    # Campos que se muestran en la lista
    list_display = (
        'email', 'first_name', 'last_name', 'tipo_usuario', 
        'is_active', 'date_joined'
    )
    
    # Campos por los que se puede filtrar
    list_filter = (
        'tipo_usuario', 'is_active', 'is_staff', 'date_joined'
    )
    
    # Campos por los que se puede buscar
    search_fields = ('email', 'first_name', 'last_name', 'username')
    
    # Ordenamiento por defecto
    ordering = ('-date_joined',)
    
    # Configuración de los fieldsets para el formulario de edición
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'email', 'telefono', 'fecha_nacimiento', 'direccion')
        }),
        ('Configuración de Usuario', {
            'fields': ('tipo_usuario',)
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Fechas Importantes', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    # Configuración para agregar nuevo usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'tipo_usuario', 'password1', 'password2'),
        }),
    )
    
    # Campos de solo lectura
    readonly_fields = ('date_joined', 'last_login')
    
    # Acciones personalizadas
    actions = ['desactivar_usuarios', 'activar_usuarios']
    
    def desactivar_usuarios(self, request, queryset):
        """Acción para desactivar usuarios seleccionados"""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated} usuario(s) han sido desactivados.'
        )
    desactivar_usuarios.short_description = "Desactivar usuarios seleccionados"
    
    def activar_usuarios(self, request, queryset):
        """Acción para activar usuarios seleccionados"""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f'{updated} usuario(s) han sido activados.'
        )
    activar_usuarios.short_description = "Activar usuarios seleccionados"
