from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser
    para manejar diferentes tipos de usuarios en el sistema
    """
    
    TIPO_USUARIO_CHOICES = [
        ('paciente', 'Paciente'),
        ('recepcion', 'Personal de Recepción'),
        ('doctor', 'Doctor'),
        ('administrador', 'Administrador'),
    ]
    
    # Campos adicionales
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO_CHOICES,
        default='paciente',
        verbose_name='Tipo de Usuario'
    )
    
    telefono = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Teléfono'
    )
    
    fecha_nacimiento = models.DateField(
        blank=True,
        null=True,
        verbose_name='Fecha de Nacimiento'
    )
    
    direccion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Dirección'
    )
    
    # Campos de auditoría
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de Actualización'
    )
    
    # Hacer que el email sea requerido y único
    email = models.EmailField(
        unique=True,
        verbose_name='Correo Electrónico'
    )
    
    # Usar email como campo de autenticación en lugar de username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'usuarios_usuario'
    
    def save(self, *args, **kwargs):
        """
        Método save personalizado para asignar automáticamente
        el tipo de usuario correcto según los permisos
        """
        # Si es superusuario, asignar tipo administrador
        if self.is_superuser and self.tipo_usuario == 'paciente':
            self.tipo_usuario = 'administrador'
        
        # Si es staff pero no superusuario y es paciente, asignar recepción
        elif self.is_staff and not self.is_superuser and self.tipo_usuario == 'paciente':
            self.tipo_usuario = 'recepcion'
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        """Retorna el nombre completo del usuario"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def es_paciente(self):
        """Verifica si el usuario es un paciente"""
        return self.tipo_usuario == 'paciente'
    
    def es_doctor(self):
        """Verifica si el usuario es un doctor"""
        return self.tipo_usuario == 'doctor'
    
    def es_recepcion(self):
        """Verifica si el usuario es personal de recepción"""
        return self.tipo_usuario == 'recepcion'
    
    def es_administrador(self):
        """Verifica si el usuario es administrador"""
        return self.tipo_usuario == 'administrador'
