from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from .models import Usuario
from .forms import RegistroPacienteForm, InicioSesionForm

@method_decorator([csrf_protect, never_cache], name='dispatch')
class RegistroPacienteView(CreateView):
    """
    Vista para registro de nuevos pacientes
    """
    model = Usuario
    form_class = RegistroPacienteForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('usuarios:registro_exitoso')
    
    def dispatch(self, request, *args, **kwargs):
        # Redirigir usuarios autenticados según su tipo
        if request.user.is_authenticated:
            if request.user.es_administrador() or request.user.es_recepcion():
                return redirect('administracion:dashboard')
            elif request.user.es_doctor():
                return redirect('doctores:gestionar_horarios')
            else:
                return redirect('usuarios:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """Procesar formulario válido"""
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Registro exitoso. Ya puedes iniciar sesión con tu cuenta.'
        )
        return response
    
    def form_invalid(self, form):
        """Procesar formulario inválido"""
        messages.error(
            self.request,
            'Por favor corrige los errores en el formulario.'
        )
        return super().form_invalid(form)


@csrf_protect
@never_cache
def inicio_sesion_view(request):
    """
    Vista para inicio de sesión
    """
    if request.user.is_authenticated:
        # Redirigir según el tipo de usuario si ya está autenticado
        if request.user.es_administrador() or request.user.es_recepcion():
            return redirect('administracion:dashboard')
        elif request.user.es_doctor():
            return redirect('doctores:gestionar_horarios')
        else:
            return redirect('usuarios:dashboard')
    
    if request.method == 'POST':
        form = InicioSesionForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Configurar duración de sesión si "recordarme" está marcado
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)  # Cerrar al cerrar navegador
            
            messages.success(request, f'¡Bienvenido, {user.get_full_name()}!')
            
            # Redirigir según el tipo de usuario
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            
            # Redirigir según el tipo de usuario
            if user.es_administrador():
                return redirect('administracion:dashboard')
            elif user.es_doctor():
                return redirect('doctores:gestionar_horarios')
            elif user.es_recepcion():
                return redirect('administracion:dashboard')  # Recepción también usa el dashboard admin
            else:  # Paciente
                return redirect('usuarios:dashboard')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = InicioSesionForm()
    
    return render(request, 'usuarios/login.html', {'form': form})


@login_required
def cerrar_sesion_view(request):
    """
    Vista para cerrar sesión
    """
    user_name = request.user.get_full_name()
    logout(request)
    messages.success(request, f'Hasta luego, {user_name}. Has cerrado sesión correctamente.')
    return redirect('usuarios:login')


def registro_exitoso_view(request):
    """
    Vista que se muestra después del registro exitoso
    """
    return render(request, 'usuarios/registro_exitoso.html')


@login_required
def dashboard_view(request):
    """
    Vista del dashboard principal según el tipo de usuario
    """
    user = request.user
    
    context = {
        'user': user,
        'tipo_usuario': user.get_tipo_usuario_display(),
    }
    
    # Redirigir según el tipo de usuario
    if user.es_paciente():
        return render(request, 'usuarios/dashboard_paciente.html', context)
    elif user.es_doctor():
        # Los doctores van a su gestión de horarios
        return redirect('doctores:gestionar_horarios')
    elif user.es_recepcion():
        # Recepción va al dashboard de administración
        return redirect('administracion:dashboard')
    elif user.es_administrador():
        # Administradores van al dashboard de administración
        return redirect('administracion:dashboard')
    else:
        return render(request, 'usuarios/dashboard_general.html', context)


def home_view(request):
    """
    Vista de la página de inicio
    """
    if request.user.is_authenticated:
        # Redirigir según el tipo de usuario
        if request.user.es_administrador() or request.user.es_recepcion():
            return redirect('administracion:dashboard')
        elif request.user.es_doctor():
            return redirect('doctores:gestionar_horarios')
        else:
            return redirect('usuarios:dashboard')
    
    return render(request, 'usuarios/home.html')
