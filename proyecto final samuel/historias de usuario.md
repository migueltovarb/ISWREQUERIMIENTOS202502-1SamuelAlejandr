| Identificador               | HU0010                                                    |
|-----------------------------|-----------------------------------------------------------|
| **Título**                  | Inicio de sesión                                           |
| **Narrativa**               | Como usuario (paciente, recepción, doctor o administrador) deseo iniciar sesión con mi correo y contraseña para acceder a mis funcionalidades. |
| **Criterios de aceptación** | <ol><li>El usuario ingresa correo electrónico y contraseña en el formulario de inicio de sesión.</li><li>El sistema valida las credenciales contra la base de datos de Django.</li><li>Si las credenciales son válidas, se crea la sesión de usuario y se redirige a la página de inicio según el rol.</li><li>Si las credenciales son inválidas, se muestra un mensaje de error “Correo o contraseña incorrectos”.</li><li>El formulario incluye protección CSRF y límite de intentos para evitar ataques de fuerza bruta.</li></ol> |


| Identificador               | HU0009                                                    |
|-----------------------------|-----------------------------------------------------------|
| **Título**                  | Registro de cuenta de paciente                              |
| **Narrativa**               | Como paciente deseo crear una cuenta con mi nombre, correo y contraseña para poder agendar citas y recibir recordatorios. |
| **Criterios de aceptación** | <ol><li>El paciente debe ingresar nombre completo, correo electrónico y contraseña.</li><li>La contraseña debe cumplir con criterios de longitud y complejidad (mínimo 8 caracteres, incluir letra y número).</li><li>El sistema verifica que el correo no esté registrado previamente.</li><li>Al registrarse correctamente, se envía un correo de verificación y la cuenta queda activa tras confirmar el enlace.</li><li>Si hay campos inválidos o correo duplicado, el sistema muestra mensajes de error adecuados.</li></ol> |


| Identificador               | HU0011                                                    |
|-----------------------------|-----------------------------------------------------------|
| **Título**                  | Gestionar perfiles de doctores                              |
| **Narrativa**               | Como administrador deseo crear, editar y eliminar perfiles de doctores para mantener actualizada la información de la plantilla médica. |
| **Criterios de aceptación** | <ol><li>El administrador puede crear un nuevo perfil de doctor ingresando nombre, especialidad y horarios regulares.</li><li>Se pueden editar datos existentes: nombre, especialidad, horarios y excepciones.</li><li>El administrador puede eliminar un perfil de doctor si no tiene citas confirmadas futuras.</li><li>Si el doctor tiene citas futuras, el sistema muestra un mensaje indicando que primero se deben reprogramar o cancelar dichas citas.</li><li>El administrador puede listar todos los doctores con filtros (especialidad, nombre).</li></ol> |

| Identificador               | HU0007                                                    |
|-----------------------------|-----------------------------------------------------------|
| **Título**                  | Definir horarios de atención regulares                     |
| **Narrativa**               | Como doctor o administrador deseo configurar mi horario de atención semanal para que los pacientes puedan ver las franjas disponibles. |
| **Criterios de aceptación** | <ol><li>El usuario (doctor o admin) ingresa hora de inicio y hora de fin para cada día de la semana.</li><li>Se valida que la hora de inicio sea anterior a la de fin y que no existan solapamientos dentro del mismo día.</li><li>Se define la duración estándar de la cita (por defecto 30 minutos, configurable).</li><li>El sistema guarda el horario y lo utiliza para calcular franjas libres al consultar disponibilidad.</li><li>Si hay solapamientos o datos inválidos, el sistema muestra mensajes de validación apropiados.</li></ol> |

| Identificador               | HU0008                                                    |
|-----------------------------|-----------------------------------------------------------|
| **Título**                  | Registrar excepciones o bloqueos de horario                |
| **Narrativa**               | Como doctor o administrador deseo registrar días de descanso, vacaciones o reuniones para bloquear franjas y evitar que se agenden citas en esos periodos. |
| **Criterios de aceptación** | <ol><li>El usuario selecciona rango de fechas y motivo de la excepción (vacaciones, reunión, licencia, etc.).</li><li>El sistema verifica si existen citas confirmadas en esas franjas bloqueadas.</li><li>Si hay citas afectadas, el sistema notifica al doctor y al paciente con al menos 72 horas de antelación y ofrece franjas alternativas.</li><li>Las franjas bloqueadas se marcan como **No disponible** en la vista de calendario de disponibilidad.</li><li>Si no hay citas afectadas, el sistema bloquea directamente las franjas en el calendario.</li></ol> |

| Identificador               | HU0012                                                    |
|-----------------------------|-----------------------------------------------------------|
| **Título**                  | Visualizar calendario de citas para personal de recepción y doctores |
| **Narrativa**               | Como personal de recepción o doctor deseo ver el calendario diario de citas para conocer las citas agendadas y su estado. |
| **Criterios de aceptación** | <ol><li>El usuario accede al módulo de calendario y ve las franjas horarias del día con estado **Disponible**, **Ocupado** o **No disponible** según corresponda.</li><li>Las citas confirmadas aparecen con nombre del paciente, hora y estado de la cita.</li><li>El personal de recepción puede filtrar por doctor; el doctor ve solo su propio calendario.</li><li>Al hacer clic en una cita, se abre un detalle modal con información del paciente y opciones para cancelar o modificar (según permisos).</li></ol> |

| Identificador               | HU0001                                                    |
|-----------------------------|-----------------------------------------------------------|
| **Título**                  | Consultar disponibilidad de doctores                      |
| **Narrativa**               | Como paciente o personal de recepción deseo consultar la disponibilidad de doctores en un rango de fechas y horas para identificar franjas libres y agendar citas. |
| **Criterios de aceptación** | <ol><li>El usuario debe poder ingresar rango de fecha y hora de inicio y fin.</li><li>Las fechas/horas ingresadas no pueden ser anteriores al momento actual.</li><li>Al enviar la consulta, el sistema combina el horario regular del doctor, excepciones/bloqueos y citas confirmadas, y muestra las franjas disponibles.</li><li>Para cada franja disponible, se muestra: nombre del doctor (con especialidad), fecha, hora y estado de la franja.</li><li>Si no existen franjas libres en el rango especificado, el sistema muestra un mensaje indicando “No hay disponibilidad en el rango seleccionado”.</li></ol> |