# Sistema de Reclamos - Django

Una aplicación completa de gestión de reclamos con funcionalidades para clientes y administradores.

## Características Implementadas

### Para Clientes (RF1-RF10)
- ✅ **RF1**: Registrar reclamos sin necesidad de login
- ✅ **RF2**: Asociación automática si tienes cuenta
- ✅ **RF3**: Campos requeridos: nombre completo, número de pedido, contacto, descripción
- ✅ **RF4**: Adjuntar fotos/capturas como evidencia
- ✅ **RF5**: Marcar como urgente o normal
- ✅ **RF6**: Asociar a zona/barrio de la ciudad
- ✅ **RF7**: Consultar estado del reclamo (pendiente, en proceso, resuelto, cerrado)
- ✅ **RF8**: Notificaciones por email cuando cambia el estado
- ✅ **RF9**: Notificaciones dentro de la app (simuladas)
- ✅ **RF10**: SMS adicional para reclamos urgentes (integración preparada)

### Para Administradores (RF11-RF24)
- ✅ **RF11**: Panel administrativo con todos los reclamos
- ✅ **RF12**: Filtrar por estado, fecha, prioridad o zona
- ✅ **RF13**: Cambiar estado de reclamos
- ✅ **RF14**: Historial de cambios con auditoría
- ✅ **RF15**: Clientes ven historial de sus reclamos
- ✅ **RF16**: Generar reportes por zonas, fechas, prioridades
- ✅ **RF17**: Exportar a CSV y PDF
- ✅ **RF18**: Asignar reclamos a empleados
- ✅ **RF19**: Validación de campos obligatorios
- ✅ **RF20**: Mensaje de confirmación con número de reclamo
- ✅ **RF21**: Buscar por número de reclamo o número de pedido
- ✅ **RF22**: Control de permisos (solo admin puede editar/eliminar)
- ✅ **RF23**: Registro de actividades de administradores
- ✅ **RF24**: Sección de preguntas frecuentes (FAQs)

## Instalación

### 1. Requisitos Previos
```bash
Python 3.10+
pip
virtualenv (opcional pero recomendado)
```

### 2. Configurar el Entorno Virtual
```bash
python -m venv venv
.\venv\Scripts\activate  # En Windows
source venv/bin/activate  # En macOS/Linux
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

Si no tienes `requirements.txt`, instala:
```bash
pip install django reportlab python-dateutil
```

### 4. Migraciones de Base de Datos
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Cargar FAQs Iniciales
```bash
python manage.py load_faqs
```

### 6. Crear Superusuario (Admin)
```bash
python manage.py createsuperuser
```

### 7. Iniciar el Servidor
```bash
python manage.py runserver
```

Luego accede a `http://127.0.0.1:8000/`

## Uso

### Para Clientes
1. **Registrar Reclamo**: Ve a "Registrar Reclamo" sin necesidad de login
2. **Buscar Reclamo**: Usa "Buscar Reclamo" con el número o número de pedido
3. **Ver Mis Reclamos**: Si tienes cuenta, inicia sesión para ver tu historial

### Para Administradores
1. **Acceder al Panel**: Inicia sesión con usuario admin y accede a "Panel Admin"
2. **Ver Reclamos**: Lista completa con filtros
3. **Actualizar Estado**: Haz clic en el lápiz para cambiar estado y asignar
4. **Generar Reportes**: Ve a "Reportes" para exportar en CSV o PDF
5. **Ver Actividades**: Panel de auditoría de cambios realizados
6. **Gestionar FAQs**: Agregar, editar o eliminar preguntas frecuentes

## Estructura de Base de Datos

### Modelos Principales
- **Claim**: Almacena reclamos
- **ClaimHistory**: Historial de cambios de estado
- **Notification**: Notificaciones enviadas
- **AdminActivity**: Registro de actividades del admin
- **FAQ**: Preguntas frecuentes

## URLs Disponibles

```
/                           - Inicio
/registrar/                 - Registrar reclamo
/buscar/                    - Buscar reclamo
/reclamo/<id>/              - Detalle del reclamo (privado)
/reclamo-publico/<id>/      - Detalle del reclamo (público)
/mis-reclamos/              - Mis reclamos (requiere login)
/faqs/                      - Preguntas frecuentes
/login/                     - Iniciar sesión
/logout/                    - Cerrar sesión
/register/                  - Crear cuenta

ADMIN:
/admin/lista/               - Panel de reclamos
/admin/actualizar-estado/   - Actualizar estado
/admin/reportes/            - Generar reportes
/admin/actividades/         - Ver actividades
/admin/faqs/                - Gestionar FAQs
```

## Configuración de Email (Opcional)

Para habilitar notificaciones por email, actualiza `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu_email@gmail.com'
EMAIL_HOST_PASSWORD = 'tu_contraseña'
```

## Notas Técnicas

- Los campos email y teléfono se detectan automáticamente en el formulario
- Los reclamos urgentes pueden tener integración SMS (preparada)
- Las notificaciones se guardan en la base de datos para auditoría
- El sistema respeta los permisos de Django (staff/superuser)

## Soporte

Para reportar errores o sugerencias, contacta a soporte@reclamos.com

---

Versión: 1.0  
Última actualización: 2025
