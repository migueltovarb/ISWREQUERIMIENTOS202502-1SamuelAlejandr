from django.core.management.base import BaseCommand
from django.core.management import CommandError
from django.contrib.auth import get_user_model
from django.db import IntegrityError
import getpass

Usuario = get_user_model()

class Command(BaseCommand):
    help = 'Crear un superusuario administrador para AgendaMédica'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Correo electrónico del administrador',
        )
        parser.add_argument(
            '--nombre',
            type=str,
            help='Nombre del administrador',
        )
        parser.add_argument(
            '--apellido',
            type=str,
            help='Apellido del administrador',
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Contraseña del administrador (no recomendado por seguridad)',
        )
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('=== Crear Administrador de AgendaMédica ===\n')
        )
        
        # Obtener email
        email = options.get('email')
        if not email:
            email = input('Correo electrónico: ')
        
        if not email:
            raise CommandError('El correo electrónico es requerido.')
        
        # Verificar si ya existe un usuario con ese email
        if Usuario.objects.filter(email=email).exists():
            raise CommandError(f'Ya existe un usuario con el email: {email}')
        
        # Obtener nombre
        nombre = options.get('nombre')
        if not nombre:
            nombre = input('Nombre: ')
        
        if not nombre:
            raise CommandError('El nombre es requerido.')
        
        # Obtener apellido
        apellido = options.get('apellido')
        if not apellido:
            apellido = input('Apellido: ')
        
        if not apellido:
            raise CommandError('El apellido es requerido.')
        
        # Obtener contraseña
        password = options.get('password')
        if not password:
            password = getpass.getpass('Contraseña: ')
            password_confirm = getpass.getpass('Confirmar contraseña: ')
            
            if password != password_confirm:
                raise CommandError('Las contraseñas no coinciden.')
        
        if not password:
            raise CommandError('La contraseña es requerida.')
        
        # Validar longitud de contraseña
        if len(password) < 8:
            raise CommandError('La contraseña debe tener al menos 8 caracteres.')
        
        try:
            # Crear el superusuario administrador
            usuario = Usuario.objects.create_user(
                username=email,  # Usar email como username
                email=email,
                first_name=nombre,
                last_name=apellido,
                password=password,
                is_staff=True,
                is_superuser=True,
                tipo_usuario='administrador'  # Asignar explícitamente
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✅ Administrador creado exitosamente:\n'
                    f'   Email: {usuario.email}\n'
                    f'   Nombre: {usuario.get_full_name()}\n'
                    f'   Tipo: {usuario.get_tipo_usuario_display()}\n'
                    f'   Superusuario: Sí\n'
                    f'   Staff: Sí\n'
                )
            )
            
            self.stdout.write(
                self.style.WARNING(
                    f'\n⚠️  Recuerda:\n'
                    f'   - Puedes acceder al admin en: http://127.0.0.1:8000/admin/\n'
                    f'   - También puedes iniciar sesión en: http://127.0.0.1:8000/login/\n'
                )
            )
            
        except IntegrityError:
            raise CommandError(f'Error: Ya existe un usuario con el email {email}')
        except Exception as e:
            raise CommandError(f'Error al crear el administrador: {str(e)}') 