from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Doctor, Especialidad, HorarioAtencion, ExcepcionHorario
from datetime import datetime, timedelta

Usuario = get_user_model()

class CrearDoctorForm(forms.ModelForm):
    """
    Formulario para crear un nuevo doctor desde el panel de administración
    """
    # Campos del usuario
    email = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    first_name = forms.CharField(
        label='Nombre',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    last_name = forms.CharField(
        label='Apellido',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Mínimo 8 caracteres'
    )
    
    password_confirm = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    telefono = forms.CharField(
        label='Teléfono Personal',
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Doctor
        fields = ['especialidad', 'numero_licencia', 'telefono_consultorio', 'consultorio']
        widgets = {
            'especialidad': forms.Select(attrs={'class': 'form-control'}),
            'numero_licencia': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_consultorio': forms.TextInput(attrs={'class': 'form-control'}),
            'consultorio': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_email(self):
        """Validar que el email no esté en uso"""
        email = self.cleaned_data['email']
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError('Ya existe un usuario con este correo electrónico.')
        return email
    
    def clean_numero_licencia(self):
        """Validar que el número de licencia no esté en uso"""
        numero_licencia = self.cleaned_data['numero_licencia']
        if Doctor.objects.filter(numero_licencia=numero_licencia).exists():
            raise ValidationError('Ya existe un doctor con este número de licencia.')
        return numero_licencia
    
    def clean(self):
        """Validaciones adicionales"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm:
            if password != password_confirm:
                raise ValidationError('Las contraseñas no coinciden.')
            
            if len(password) < 8:
                raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
        
        return cleaned_data
    
    def save(self, commit=True):
        """Crear el usuario y el doctor"""
        # Crear el usuario primero
        usuario = Usuario.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            password=self.cleaned_data['password'],
            telefono=self.cleaned_data.get('telefono', ''),
            tipo_usuario='doctor'
        )
        
        # Crear el doctor
        doctor = super().save(commit=False)
        doctor.usuario = usuario
        
        if commit:
            doctor.save()
        
        return doctor

class EditarDoctorForm(forms.ModelForm):
    """
    Formulario para editar información de un doctor existente
    """
    # Campos del usuario que se pueden editar
    first_name = forms.CharField(
        label='Nombre',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    last_name = forms.CharField(
        label='Apellido',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    telefono = forms.CharField(
        label='Teléfono Personal',
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Doctor
        fields = ['especialidad', 'numero_licencia', 'telefono_consultorio', 'consultorio', 'activo']
        widgets = {
            'especialidad': forms.Select(attrs={'class': 'form-control'}),
            'numero_licencia': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_consultorio': forms.TextInput(attrs={'class': 'form-control'}),
            'consultorio': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.usuario:
            self.fields['first_name'].initial = self.instance.usuario.first_name
            self.fields['last_name'].initial = self.instance.usuario.last_name
            self.fields['telefono'].initial = self.instance.usuario.telefono
    
    def save(self, commit=True):
        """Actualizar tanto el doctor como el usuario"""
        doctor = super().save(commit=False)
        
        # Actualizar datos del usuario
        if doctor.usuario:
            doctor.usuario.first_name = self.cleaned_data['first_name']
            doctor.usuario.last_name = self.cleaned_data['last_name']
            doctor.usuario.telefono = self.cleaned_data.get('telefono', '')
            
            if commit:
                doctor.usuario.save()
        
        if commit:
            doctor.save()
        
        return doctor

class HorarioAtencionForm(forms.ModelForm):
    """
    Formulario para gestionar horarios de atención de doctores
    """
    class Meta:
        model = HorarioAtencion
        fields = ['dia_semana', 'hora_inicio', 'hora_fin', 'duracion_cita', 'activo']
        widgets = {
            'dia_semana': forms.Select(attrs={'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'duracion_cita': forms.NumberInput(attrs={'class': 'form-control', 'min': '15', 'max': '120'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean(self):
        """Validaciones personalizadas"""
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        duracion_cita = cleaned_data.get('duracion_cita')
        
        if hora_inicio and hora_fin:
            if hora_inicio >= hora_fin:
                raise ValidationError('La hora de inicio debe ser anterior a la hora de fin.')
        
        if duracion_cita and duracion_cita <= 0:
            raise ValidationError('La duración de la cita debe ser mayor a 0 minutos.')
        
        return cleaned_data

class ExcepcionHorarioForm(forms.ModelForm):
    """
    Formulario para registrar excepciones en los horarios de doctores
    """
    class Meta:
        model = ExcepcionHorario
        fields = ['fecha_inicio', 'fecha_fin', 'tipo_excepcion', 'motivo', 'todo_el_dia']
        widgets = {
            'fecha_inicio': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'fecha_fin': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'tipo_excepcion': forms.Select(attrs={'class': 'form-control'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'todo_el_dia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean(self):
        """Validaciones personalizadas"""
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin:
            if fecha_inicio >= fecha_fin:
                raise ValidationError('La fecha de inicio debe ser anterior a la fecha de fin.')
            
            if fecha_inicio < timezone.now():
                raise ValidationError('No se pueden crear excepciones para fechas pasadas.')
        
        return cleaned_data

class FiltroCalendarioForm(forms.Form):
    """
    Formulario para filtrar el calendario de citas
    """
    fecha = forms.DateField(
        label='Fecha',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        initial=timezone.now().date()
    )
    
    doctor = forms.ModelChoiceField(
        label='Doctor',
        queryset=Doctor.objects.filter(activo=True),
        required=False,
        empty_label='Todos los doctores',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Si el usuario es doctor, solo mostrar su propio perfil
        if user and hasattr(user, 'doctor'):
            self.fields['doctor'].queryset = Doctor.objects.filter(id=user.doctor.id)
            self.fields['doctor'].initial = user.doctor
            self.fields['doctor'].widget.attrs['readonly'] = True 

class ConsultaDisponibilidadForm(forms.Form):
    """
    Formulario para consultar disponibilidad de doctores (HU0001)
    """
    fecha_inicio = forms.DateField(
        label='Fecha de Inicio',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        help_text='Selecciona la fecha desde la cual quieres consultar disponibilidad'
    )
    
    fecha_fin = forms.DateField(
        label='Fecha de Fin',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        help_text='Selecciona la fecha hasta la cual quieres consultar disponibilidad'
    )
    
    especialidad = forms.ModelChoiceField(
        label='Especialidad',
        queryset=Especialidad.objects.filter(activa=True),
        required=False,
        empty_label='Todas las especialidades',
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Filtra por especialidad médica'
    )
    
    doctor = forms.ModelChoiceField(
        label='Doctor Específico',
        queryset=Doctor.objects.filter(activo=True),
        required=False,
        empty_label='Todos los doctores',
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Selecciona un doctor específico (opcional)'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer fecha mínima como hoy
        today = timezone.now().date()
        self.fields['fecha_inicio'].widget.attrs['min'] = today.strftime('%Y-%m-%d')
        self.fields['fecha_fin'].widget.attrs['min'] = today.strftime('%Y-%m-%d')
        
        # Valores por defecto
        if not self.data:
            self.fields['fecha_inicio'].initial = today
            self.fields['fecha_fin'].initial = today + timedelta(days=7)
    
    def clean(self):
        """Validaciones personalizadas"""
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin:
            # Validar que las fechas no sean en el pasado
            today = timezone.now().date()
            if fecha_inicio < today:
                raise ValidationError('La fecha de inicio no puede ser anterior a hoy.')
            
            if fecha_fin < today:
                raise ValidationError('La fecha de fin no puede ser anterior a hoy.')
            
            # Validar que fecha_inicio <= fecha_fin
            if fecha_inicio > fecha_fin:
                raise ValidationError('La fecha de inicio debe ser anterior o igual a la fecha de fin.')
            
            # Validar que el rango no sea mayor a 30 días
            if (fecha_fin - fecha_inicio).days > 30:
                raise ValidationError('El rango de fechas no puede ser mayor a 30 días.')
        
        return cleaned_data 