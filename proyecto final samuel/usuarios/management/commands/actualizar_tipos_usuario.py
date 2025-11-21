from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class Command(BaseCommand):
    help = 'Actualizar tipos de usuario para usuarios existentes'
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('=== Actualizando tipos de usuario ===\n')
        )
        
        # Actualizar superusuarios a administradores
        superusuarios = Usuario.objects.filter(
            is_superuser=True,
            tipo_usuario='paciente'
        )
        
        count_super = 0
        for usuario in superusuarios:
            usuario.tipo_usuario = 'administrador'
            usuario.save()
            count_super += 1
            self.stdout.write(
                f'✅ {usuario.email} actualizado a Administrador'
            )
        
        # Actualizar staff (no superusuarios) a recepción
        staff_users = Usuario.objects.filter(
            is_staff=True,
            is_superuser=False,
            tipo_usuario='paciente'
        )
        
        count_staff = 0
        for usuario in staff_users:
            usuario.tipo_usuario = 'recepcion'
            usuario.save()
            count_staff += 1
            self.stdout.write(
                f'✅ {usuario.email} actualizado a Personal de Recepción'
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Resumen:\n'
                f'   - Administradores actualizados: {count_super}\n'
                f'   - Personal de recepción actualizado: {count_staff}\n'
                f'   - Total usuarios actualizados: {count_super + count_staff}\n'
            )
        ) 