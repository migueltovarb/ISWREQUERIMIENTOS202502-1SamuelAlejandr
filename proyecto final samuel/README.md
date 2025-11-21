# AgendaMédica

Sistema integral de gestión de citas médicas desarrollado con Django.

## Descripción

AgendaMédica es un sistema web que permite la gestión completa de citas médicas, incluyendo:

- Consulta de disponibilidad de doctores
- Creación, modificación y cancelación de citas
- Gestión de horarios de atención
- Envío de recordatorios automáticos por correo electrónico y SMS
- Administración de usuarios (pacientes, doctores, recepción, administradores)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/agenda-medica.git
cd agenda-medica
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Unix o MacOS:
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Aplicar migraciones:
```bash
python manage.py migrate
```

5. Crear superusuario administrador:
```bash
python manage.py crear_admin
```

## Comandos Personalizados

El proyecto incluye comandos personalizados para la gestión de usuarios y datos iniciales:

### Crear Administrador
```bash
python manage.py crear_admin
```
Este comando interactivo permite crear un superusuario administrador con todos los permisos necesarios. También acepta argumentos opcionales:
```bash
python manage.py crear_admin --email=admin@ejemplo.com --nombre=Admin --apellido=Sistema --password=contraseña
```

### Actualizar Tipos de Usuario
```bash
python manage.py actualizar_tipos_usuario
```
Este comando actualiza automáticamente los tipos de usuario para usuarios existentes:
- Convierte superusuarios a tipo 'administrador'
- Convierte usuarios staff (no superusuarios) a tipo 'recepcion'

### Crear Especialidades Médicas
```bash
python manage.py crear_especialidades
```
Este comando crea las especialidades médicas básicas en el sistema:
- Medicina General, Cardiología, Dermatología, Pediatría
- Ginecología, Traumatología, Oftalmología, Otorrinolaringología
- Neurología, Psiquiatría, Endocrinología, Gastroenterología

### Configuración Inicial Completa
Para configurar el sistema desde cero, ejecuta los comandos en este orden:
```bash
python manage.py migrate
python manage.py crear_especialidades
python manage.py crear_admin
```

## Estructura del Proyecto

El proyecto está organizado en las siguientes aplicaciones Django:

- **usuarios**: Gestión de autenticación y diferentes tipos de usuarios
- **doctores**: Gestión de doctores, especialidades y horarios de atención
- **citas**: Gestión completa del ciclo de vida de las citas médicas
- **notificaciones**: Sistema de envío de recordatorios y notificaciones
- **administracion**: Funciones de back-office e informes

## Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd agenda_medica
```

2. Crear y activar el entorno virtual:
```bash
python -m venv venv

# En Windows
.\venv\Scripts\Activate.ps1

# En Linux/Mac
source venv/bin/activate
```

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

4. Realizar las migraciones de la base de datos:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Crear un superusuario:
```bash
python manage.py createsuperuser
```

6. Ejecutar el servidor de desarrollo:
```bash
python manage.py runserver
```

El sistema estará disponible en `http://127.0.0.1:8000/`

## Tecnologías Utilizadas

- **Backend**: Django 5.2.1, Django REST Framework
- **Base de datos**: SQLite (desarrollo), PostgreSQL/MySQL (producción)
- **Frontend**: Django Templates, JavaScript
- **Tareas programadas**: django-crontab
- **Notificaciones**: Django Email Backend, Twilio (SMS opcional)

## Características Principales

### Tipos de Usuario

1. **Pacientes**: Pueden agendar, modificar y cancelar sus citas
2. **Personal de Recepción**: Gestión diaria de citas y atención al cliente
3. **Doctores**: Gestión de horarios y consulta de agenda
4. **Administradores**: Acceso completo al sistema y generación de reportes

### Funcionalidades

- ✅ Consulta de disponibilidad de doctores
- ✅ Gestión completa de citas (CRUD)
- ✅ Sistema de recordatorios automáticos
- ✅ Gestión de horarios y excepciones
- ✅ Autenticación y autorización por roles
- ✅ Panel de administración
- ✅ API REST para futuras integraciones

## Estado del Proyecto

🚧 **En desarrollo** - Estructura base creada, pendiente implementación de lógica de negocio.

## Contribución

Este proyecto está en desarrollo activo. Para contribuir:

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## Licencia

[Especificar licencia del proyecto]

## Contacto

[Información de contacto del desarrollador/equipo] 