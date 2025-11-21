## 2.1 Perspectiva del Producto
La _AgendaMédica_ es un producto nuevo, diseñado como un sistema independiente y autoconclusivo. No forma parte de una familia de productos existente, ni es una actualización o reemplazo de otro sistema previo.

Este producto tiene como objetivo cubrir de manera integral el proceso de:
- Consulta de disponibilidad de doctores.
- Creación, modificación y cancelación de citas médicas.
- Gestión de horarios de atención de los doctores.
- Envío de recordatorios automáticos (correo electrónico y/o SMS) tanto a pacientes como a médicos.

Funciona como una solución completa, sin depender de la integración con otros sistemas externos, más allá de los necesarios para:
- Envío de correos de confirmación, recordatorios y notificaciones.
- Envío de SMS (opcional) para recordatorios urgentes o confirmaciones rápidas.

A continuación, se presenta un diagrama de alto nivel que ilustra los principales componentes del sistema y sus interacciones:  
![image](https://github.com/user-attachments/assets/ec15fca8-93f0-4fc9-9572-e55c863c5983)

---

## 2.2 Funciones del Producto

![leider uml](https://github.com/user-attachments/assets/04ddce82-68ee-4379-b2ae-afdca1cf40fb)

### **1. Gestión de Disponibilidad de Doctores**
- **Consulta de disponibilidad por rango de fechas y horas**  
  - Permitir a los pacientes o personal de recepción ingresar rango de fecha y hora para consultar franjas libres de cada doctor.  
  - Validar que las fechas/horas ingresadas no sean anteriores al momento actual.
- **Listado de franjas disponibles**  
  - Para cada franja horaria marcada como **Libres** dentro del horario de atención del doctor, mostrar:
    - Nombre del doctor (especialidad asociada).  
    - Fecha y hora de la franja disponible.  
    - Estado de la franja: **Disponible** (libre) o **Ocupada** (ya asignada o bloqueada).
- **Cálculo dinámico de franjas**  
  - Al consultar disponibilidad, combinar:
    - Horario regular de atención configurado del doctor.  
    - Excepciones o bloqueos de horario (licencias, vacaciones, reuniones).  
    - Citas ya confirmadas (para evitar solapamientos).

---

### **2. Gestión de Citas**
- **Creación de cita**  
  - El usuario (paciente) deberá completar:
    - Identificación del paciente (nombre completo, correo electrónico y/o teléfono).  
    - Doctor seleccionado.  
    - Fecha y hora de la cita (una franja marcada como **Disponible**).  
  - Validaciones antes de confirmar:
    - La fecha/hora solicitadas estén dentro del horario de atención predefinido del doctor.  
    - No exista otra cita confirmada o pendiente para ese mismo doctor en la misma franja.  
    - La fecha/hora no sean anteriores al momento actual.  
  - Si hay conflicto o dato inválido, se mostrará un mensaje de error indicando el motivo concreto.
- **Generación de ID de cita único**  
  - Al confirmar la cita satisfactoriamente:
    - El sistema generará un **ID de cita único**.  
    - El estado inicial de la cita será **Confirmada**.
- **Envío de confirmación**  
  - El sistema enviará al paciente (correo y/o SMS) un mensaje que incluya:
    - Número o código único de la cita.  
    - Nombre del doctor y especialidad.  
    - Fecha y hora de la cita.  
    - Ubicación o sala de la clínica (si aplica).  

---

### **3. Modificación de Citas**
- **Permitir modificación de cita existente**  
  - El paciente, a través del enlace único, podrá solicitar modificación de fecha y/o hora de la cita.  
- **Condiciones para modificar**  
  - La cita debe estar en estado **Confirmada**.  
  - Debe faltar más de 24 horas para la fecha y hora originalmente programadas.  
- **Proceso de modificación**  
  - Al solicitar la modificación, se desplegarán las nuevas franjas disponibles del doctor en el rango deseado.  
  - El paciente seleccionará la nueva franja; el sistema verificará:
    - Que la nueva fecha/hora esté dentro del horario de atención del doctor.  
    - Que no exista otra cita confirmada en ese mismo doctor para esa franja.  
  - Si la nueva franja cumple condiciones, se actualizará la cita (mismo ID) y se mantendrá el estado **Confirmada**.
- **Notificaciones tras modificación**  
  - Se enviará un correo o SMS de confirmación al paciente con los nuevos datos.  
  - Se notificará al doctor sobre el cambio de horario (incluyendo datos previos y nuevos).
- **Errores de modificación**  
  - Si la cita no existe, ya está cancelada o no cumple el plazo de 24 horas, el sistema mostrará un mensaje de error específico.

---

### **4. Cancelación de Citas**
- **Permitir cancelación de cita**  
  - El paciente podrá cancelar una cita en estado **Confirmada** a través del enlace único.
- **Condiciones para cancelar**  
  - Debe faltar más de 12 horas para la fecha y hora programadas de la cita.  
  - Si la solicitud se hace con menos de 12 horas de anticipación, se mostrará un mensaje indicando que no es posible cancelar en ese plazo.
- **Proceso de cancelación**  
  - Al confirmar la cancelación, el sistema:
    - Cambiará el estado de la cita a **Cancelada**.  
    - Liberará la franja horaria del doctor (quedará marcada como **Disponible** nuevamente).  
- **Notificaciones tras cancelación**  
  - Se enviará un correo o SMS al paciente indicando que la cita ha sido cancelada.  
  - Se enviará una notificación al doctor informando de la cancelación y liberación de la franja.
- **Errores de cancelación**  
  - Si la cita no existe, ya está cancelada o no cumple el plazo de 12 horas, se mostrará un mensaje de error apropiado.

---

### **5. Envío de Recordatorios**
- **Generar y programar recordatorios automáticos**  
  - El sistema enviará recordatorios al paciente (correo y/o SMS) recordando la cita programada.
- **Tiempos de envío de recordatorios al paciente**  
  - Un recordatorio 24 horas antes de la cita.  
  - Un recordatorio 1 hora antes de la cita.
- **Contenido de los recordatorios**  
  - Nombre del paciente.  
  - Nombre del doctor y especialidad.  
  - Fecha y hora de la cita.  
  - Ubicación o sala de la clínica.  
- **Omisión de recordatorios tras cancelación**  
  - Si el paciente cancela la cita antes del envío de un recordatorio, el sistema omitirá los envíos posteriores.
- **Recordatorios internos para el doctor**  
  - Envío de aviso al doctor 2 horas antes de cada cita agendada.  
  - Envío de lista de pacientes del día siguiente (la noche anterior).

---

### **6. Gestión de Horarios de Disponibilidad de Doctores**
- **Definir horarios de atención regulares**  
  - El sistema permitirá a cada doctor (o al administrador de la clínica) configurar sus horarios de atención semanales, indicando para cada día:
    - Hora de inicio de atención (ej: 08:00).  
    - Hora de fin de atención (ej: 17:00).  
    - Duración estándar de cada cita (por defecto 30 minutos, configurable).
  - Validar que la hora de inicio sea anterior a la hora de fin y que no existan solapamientos dentro de ese horario.
- **Registrar excepciones o bloqueos de horario**  
  - El sistema permitirá a los doctores (o al administrador) registrar:
    - Días de descanso o vacaciones.  
    - Permisos o licencias médicas.  
    - Reuniones internas o actividades administrativas.
  - Al registrar una excepción, verificar si existen citas confirmadas en la franja bloqueada; de haber citas:
    - Notificar al doctor y al paciente con al menos 72 horas de antelación para reprogramar.  
    - Ofrecer al paciente franjas alternativas disponibles.
- **Mostrar disponibilidad en calendario**  
  - Al consultar la disponibilidad para agendar o modificar una cita, el sistema calculará las franjas libres considerando:
    - Horarios regulares de atención del doctor.  
    - Excepciones/ausencias registradas.  
    - Citas ya confirmadas en otras franjas.
  - En la vista de calendario:
    - Las franjas ocupadas se marcarán como **Ocupado**.  
    - Las franjas bloqueadas (excepciones) como **No disponible**.  
    - Las franjas libres como **Disponible**.

---

### **7. Autenticación y Cuentas**
- **Registro de cuenta de paciente**  
  - Los pacientes deben crear una cuenta con nombre, correo electrónico y contraseña antes de poder agendar citas.  
  - La contraseña deberá cumplir con criterios mínimos de seguridad (longitud, complejidad).
- **Inicio de sesión**  
  - Los usuarios (pacientes, personal de recepción, doctores, administradores) deberán autenticarse con correo electrónico y contraseña para acceder a sus respectivas funcionalidades:
    - Pacientes: agendar, modificar, cancelar citas; consultar historial; recibir recordatorios.  
    - Personal de recepción: gestionar citas de pacientes, confirmar/cancelar manualmente, acceder al calendario de doctores.  
    - Doctores: gestionar su horario, ver lista de pacientes, recibir notificaciones internas.  
    - Administradores: acceso completo a la configuración del sistema.  
  - Si se introducen credenciales inválidas, el sistema mostrará un mensaje de error.

---

### **8. Administración (Back-Office)**
- **Gestión de doctores** (solo personal autorizado)  
  - CRUD de perfiles de doctor (crear, editar, eliminar, listar).  
  - Definir atributos: nombre, especialidad, horario de atención regular, excepciones.
- **Gestión de citas**  
  - Visualizar todas las citas con filtros (fecha, estado, paciente, doctor).  
  - Modificar manualmente el estado de la cita (por ejemplo, marcar como **Confirmada**, **Cancelada** o **En curso**) en casos especiales.
- **Informes y métricas**  
  - Carga diaria/mensual de citas por doctor.  
  - Historial de cancelaciones y reprogramaciones.  
  - Reportes de tiempo de consulta (por ejemplo, cumplimiento de franjas, tardanzas).  
  - Estadísticas de cancelaciones tardías (menos de 12 horas) y modificaciones (menos de 24 horas).

---

## 2.3 Clases de Usuario y Características

El sistema _AgendaMédica_ está diseñado para ser utilizado por cuatro clases principales de usuarios, con diferentes privilegios y características:

### **1. Pacientes (Usuarios Externos)**
- **Frecuencia de uso**: Moderada a alta.  
- **Funciones utilizadas**:  
  - Registro y autenticación de cuenta.  
  - Consulta de disponibilidad de doctores.  
  - Creación, modificación y cancelación de citas.  
  - Recepción de recordatorios.  
  - Consulta de historial de citas y notificaciones.  
- **Nivel técnico**: Bajo a medio.  
- **Privilegios**:  
  - Acceso a su propio perfil y a la gestión completa de sus citas.  
  - No puede ver ni modificar información de otros pacientes o doctores.

---

### **2. Personal de Recepción (Usuarios Internos)**
- **Frecuencia de uso**: Alta.  
- **Funciones utilizadas**:  
  - Autenticación en el sistema.  
  - Consulta y gestión de citas de pacientes (confirmar, cancelar, reasignar).  
  - Verificación y registro manual de datos cuando el paciente no pueda hacerlo en línea.  
  - Asistencia en la modificación de citas si el paciente lo solicita por teléfono o presencialmente.  
- **Nivel técnico**: Medio.  
- **Privilegios**:  
  - Acceso a todas las citas del día y a la información básica de los pacientes para atención inmediata.  
  - No puede modificar horarios regulares de los doctores ni crear cuentas de administrador.

---

### **3. Doctores (Usuarios Internos)**
- **Frecuencia de uso**: Moderada.  
- **Funciones utilizadas**:  
  - Autenticación en el sistema.  
  - Visualización de su propio calendario de citas.  
  - Registro de excepciones o bloqueos de horario (vacaciones, permisos, reuniones).  
  - Consulta de lista de pacientes del día siguiente.  
  - Recepción de recordatorios internos (2 horas antes de cada cita).  
- **Nivel técnico**: Medio.  
- **Privilegios**:  
  - Acceso a su perfil, horario y citas asignadas.  
  - No puede ver el historial de citas de otros doctores ni modificar información de pacientes.

---

### **4. Administrador (Usuario Interno con Privilegios Ampliados)**
- **Frecuencia de uso**: Alta.  
- **Funciones utilizadas**:  
  - Todas las funciones del Personal de Recepción y de los Doctores.  
  - Creación, edición y eliminación de cuentas de Personal de Recepción y Doctores.  
  - Configuración y mantenimiento de la base de datos de doctores y horarios.  
  - Generación de informes y métricas globales del sistema.  
- **Nivel técnico**: Medio-alto.  
- **Privilegios**:  
  - Acceso completo a la configuración del sistema: gestión de doctores, citas, usuarios internos e informes.

### Resumen de Clases de Usuario

| **Clase de Usuario**       | **Frecuencia de Uso** | **Funciones Principales**                                                                                                 | **Nivel Técnico** | **Privilegios**                                                                                  |
|----------------------------|-----------------------|---------------------------------------------------------------------------------------------------------------------------|-------------------|--------------------------------------------------------------------------------------------------|
| **Pacientes (Externos)**   | Moderada a Alta       | Registro y gestión de citas, consulta de disponibilidad, modificación y cancelación, recepción de recordatorios           | Bajo a Medio      | Acceso completo a su propio perfil y citas; no puede ver ni modificar la información de otros. |
| **Personal de Recepción**  | Alta                  | Gestión diaria de citas, confirmación/cancelación, asistencia a pacientes, consulta de calendario de doctores            | Medio             | Acceso a citas del día y datos básicos de pacientes; no puede gestionar horarios de doctores.  |
| **Doctores (Internos)**    | Moderada              | Visualización de su calendario, registro de excepciones de horario, consulta de lista de pacientes, recepción de recordatorios internos | Medio             | Acceso a su perfil, horario y citas asignadas; no puede modificar datos de otros usuarios.    |
| **Administrador (Interno)**| Alta                  | Gestión de usuarios internos, configuración de horarios de doctores, generación de informes, supervisión de todo el sistema| Medio-Alto        | Acceso completo a doctores, citas, usuarios internos e informes.                                |

---

## 2.5 Restricciones de Diseño e Implementación
- **Arquitectura**:  
  Basada en el patrón **Modelo-Vista-Template (MVT)** de **Django**, expuesta mediante vistas y API RESTful para facilitar futuras integraciones móviles o de terceros.
- **Lenguaje y Framework**:  
  Backend y lógica de negocio implementados con **Python** y **Django** (incluyendo **Django REST Framework** para APIs internas).  
  Frontend utilizando **Django Templates** y, de ser necesario, **AJAX** para interacciones dinámicas (consulta de disponibilidad sin recarga completa).
- **Base de datos**:  
  **SQLite** (archivo local) para prototipado y despliegue inicial; migraciones posteriores a **PostgreSQL** o **MySQL** en entornos de producción.
- **Autenticación y autorización**:  
  Gestionadas con el sistema de **auth** de Django (usuarios, grupos y permisos).  
  Sesiones seguras y contraseñas cifradas según estándares de Django.  
  Roles definidos: Paciente, Personal de Recepción, Doctor, Administrador.
- **Envío de correos y SMS**:  
  Integración con el backend de correos de Django (`EMAIL_BACKEND`) para confirmaciones, notificaciones de check-in/check-out y recordatorios.  
  Opcional: servicio externo o biblioteca para envío de SMS (Twilio, Nexmo, etc.).
- **Validaciones**:  
  Formularios de Django (`ModelForm` y `Form`) para validación en servidor; validación adicional en frontend con JavaScript para experiencia de usuario.
- **Seguridad**:  
  - Uso de **HTTPS** obligatorio en todo el sitio.  
  - Control de acceso basado en permisos de Django (rol Paciente, Recepción, Doctor, Administrador).  
  - Protección CSRF nativa de Django en formularios.  
  - Tasa límite de solicitudes para evitar ataques de fuerza bruta en login.
- **Escalabilidad**:  
  - Diseñado con separación clara entre lógica de negocio y presentación para facilitar futura migración a microservicios o integración con aplicaciones móviles.

---

## 2.6 Documentación para el Usuario
- **Tutoriales en línea**:  
  Videos y guías paso a paso para:
  - Registro de cuenta y autenticación.  
  - Búsqueda de disponibilidad de doctores y creación de cita.  
  - Modificación y cancelación de cita.  
  - Proceso de envío y recepción de recordatorios.  
  - Ingreso al calendario personal (para doctores y recepción).
- **Soporte en línea**:  
  - Chat integrado en la aplicación web para resolver dudas inmediatas.  
  - Sistema de tickets vía correo electrónico para incidencias más complejas.
- **Manuales de usuario (PDF)**:  
  - **Paciente**: registro, reserva, modificación, cancelación y recepción de recordatorios.  
  - **Personal de Recepción**: búsqueda y gestión de citas diarias, confirmaciones y atención en mostrador.  
  - **Doctor**: configuración de horarios, registro de ausencias, consulta de agenda diaria.  
  - **Administrador**: creación y gestión de usuarios internos, configuración de horarios generales, generación de informes y métricas.

---

## 2.7 Supuestos y Dependencias

### Supuestos
- Pacientes y personal con acceso a Internet y conocimientos básicos de uso web.  
- Doctores con acceso a un dispositivo (computadora/tableta) para consultar sus horarios.  
- Entorno de servidor compatible con Python 3.x, Django y SQLite (para pruebas iniciales).  
- Cuenta SMTP activa y configurada en Django para el envío de correos.  
- Servicio externo (o biblioteca) disponible para envío de SMS si se desea esta funcionalidad.

### Dependencias
- **Django** (>= 3.2) y librerías oficiales:  
  - **Django REST Framework** (si se proyecta exponer API).  
  - **django-crontab** o similar para programar tareas de envío de recordatorios.  
- **SQLite** para prototipado; migración a **PostgreSQL** o **MySQL** en producción.  
- **Biblioteca/servicio de envío de SMS** (opcional): Twilio, Nexmo, o similar, debidamente configurado.  
- **JavaScript** moderno (ECMAScript 6+) para validaciones y AJAX en el frontend.  
- **Servidor web** (Gunicorn, uWSGI) y **Nginx** (o equivalente) para despliegue en producción.  
- **Certificado SSL/TLS** válido para habilitar HTTPS obligatorio.  
- (Opcional) **Docker** para contenedorización y despliegues reproducibles.
