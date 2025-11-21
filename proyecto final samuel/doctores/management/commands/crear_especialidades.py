from django.core.management.base import BaseCommand
from doctores.models import Especialidad

class Command(BaseCommand):
    help = 'Crear especialidades médicas básicas para el sistema'
    
    def handle(self, *args, **options):
        especialidades = [
            {
                'nombre': 'Medicina General',
                'descripcion': 'Atención médica general y preventiva'
            },
            {
                'nombre': 'Cardiología',
                'descripcion': 'Especialidad médica que se ocupa del corazón y sistema cardiovascular'
            },
            {
                'nombre': 'Dermatología',
                'descripcion': 'Especialidad médica que se ocupa de la piel y sus enfermedades'
            },
            {
                'nombre': 'Pediatría',
                'descripcion': 'Especialidad médica que se ocupa de la salud de niños y adolescentes'
            },
            {
                'nombre': 'Ginecología',
                'descripcion': 'Especialidad médica que se ocupa de la salud del aparato reproductor femenino'
            },
            {
                'nombre': 'Traumatología',
                'descripcion': 'Especialidad médica que se ocupa de lesiones del sistema musculoesquelético'
            },
            {
                'nombre': 'Oftalmología',
                'descripcion': 'Especialidad médica que se ocupa de los ojos y la visión'
            },
            {
                'nombre': 'Otorrinolaringología',
                'descripcion': 'Especialidad médica que se ocupa de oído, nariz y garganta'
            },
            {
                'nombre': 'Neurología',
                'descripcion': 'Especialidad médica que se ocupa del sistema nervioso'
            },
            {
                'nombre': 'Psiquiatría',
                'descripcion': 'Especialidad médica que se ocupa de la salud mental'
            },
            {
                'nombre': 'Endocrinología',
                'descripcion': 'Especialidad médica que se ocupa del sistema endocrino y hormonas'
            },
            {
                'nombre': 'Gastroenterología',
                'descripcion': 'Especialidad médica que se ocupa del sistema digestivo'
            },
        ]
        
        self.stdout.write(
            self.style.SUCCESS('=== Creando Especialidades Médicas ===\n')
        )
        
        creadas = 0
        existentes = 0
        
        for esp_data in especialidades:
            especialidad, created = Especialidad.objects.get_or_create(
                nombre=esp_data['nombre'],
                defaults={
                    'descripcion': esp_data['descripcion'],
                    'activa': True
                }
            )
            
            if created:
                creadas += 1
                self.stdout.write(
                    f'✅ Creada: {especialidad.nombre}'
                )
            else:
                existentes += 1
                self.stdout.write(
                    f'ℹ️  Ya existe: {especialidad.nombre}'
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Resumen:\n'
                f'   - Especialidades creadas: {creadas}\n'
                f'   - Especialidades existentes: {existentes}\n'
                f'   - Total especialidades: {creadas + existentes}\n'
            )
        ) 