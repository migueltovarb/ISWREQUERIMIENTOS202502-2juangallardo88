# 🚀 GUÍA DE INICIO RÁPIDO

## ¡Tu aplicación de reclamos está lista!

### Paso 1: Iniciar el Servidor
```bash
cd "c:\Users\juan gallardo\Desktop\Django"
python manage.py runserver
```

Deberías ver:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Paso 2: Acceder a la Aplicación
- **URL**: http://127.0.0.1:8000/
- **Panel Admin**: http://127.0.0.1:8000/admin/

### Paso 3: Credenciales de Prueba

#### 👨‍💼 Administrador
```
Usuario: admin
Contraseña: admin123
```

#### 👨‍💻 Empleados (Staff)
```
Usuario: empleado1/empleado2/empleado3
Contraseña: empleado123
```

#### 👤 Clientes
```
Usuario: cliente1/cliente2/cliente3
Contraseña: cliente123
```

---

## 📝 Flujo de Prueba Rápido (5 minutos)

### 1️⃣ REGISTRAR RECLAMO SIN LOGIN (1 min)
```
1. Haz clic en "📝 Registrar Reclamo"
2. Completa el formulario:
   - Nombre: Tu Nombre
   - Email: tu@email.com
   - Zona: Tu Barrio
   - Descripción: Mi problema...
   - Prioridad: Normal
3. Haz clic en "Registrar Reclamo"
4. ✅ Recibirás un número de reclamo
```

### 2️⃣ BUSCAR TU RECLAMO (30 seg)
```
1. Haz clic en "🔍 Buscar Reclamo"
2. Ingresa el número que recibiste
3. Haz clic en "Buscar"
4. ✅ Ver detalles del reclamo
```

### 3️⃣ CREAR CUENTA Y VER TUS RECLAMOS (2 min)
```
1. Haz clic en "✍️ Registrarse"
2. Crea una cuenta:
   - Usuario: miusuario
   - Email: mi@email.com
   - Contraseña: MiPassword123
3. Inicia sesión
4. Haz clic en "📝 Registrar Reclamo"
5. Completa otro reclamo
6. Haz clic en tu usuario → "Mis Reclamos"
7. ✅ Ver todos tus reclamos asociados
```

### 4️⃣ PANEL DE ADMINISTRADOR (1.5 min)
```
1. Cierra sesión
2. Ve al login
3. Inicia sesión como: admin / admin123
4. Haz clic en tu usuario → "Panel Admin"
5. ✅ Ver todos los reclamos en tabla
6. Prueba filtros:
   - Por estado
   - Por zona
   - Por fechas
7. Haz clic en ✏️ para cambiar estado
8. Selecciona "En proceso"
9. ✅ El historial se actualiza automáticamente
```

### 5️⃣ GENERAR REPORTES (30 seg)
```
1. Como admin, haz clic en "Reportes"
2. Aplica filtros si deseas
3. Haz clic en "Descargar CSV"
4. ✅ Se descarga archivo con datos
5. Haz clic en "Descargar PDF"
6. ✅ Se descarga reporte formateado
```

### 6️⃣ VER PREGUNTAS FRECUENTES (15 seg)
```
1. Haz clic en "❓ Ayuda"
2. Lee las preguntas frecuentes
3. ✅ 10 FAQs precargadas disponibles
```

---

## 🎯 Verificación de Funcionalidades

Marca cada una conforme las pruebes:

### Funciones de Cliente
- [ ] Registrar reclamo sin login
- [ ] Recibir número de confirmación
- [ ] Buscar reclamo por número
- [ ] Ver estado del reclamo
- [ ] Crear cuenta
- [ ] Ver mis reclamos
- [ ] Ver detalles con historial

### Funciones de Admin
- [ ] Ver todos los reclamos
- [ ] Filtrar por estado
- [ ] Filtrar por zona
- [ ] Filtrar por fechas
- [ ] Cambiar estado
- [ ] Asignar a empleado
- [ ] Ver historial de cambios
- [ ] Ver actividades
- [ ] Descargar CSV
- [ ] Descargar PDF
- [ ] Gestionar FAQs

---

## 🐛 Solucionar Problemas

### "No se abre la página"
```
✓ Verifica que el servidor esté corriendo
✓ Usa exactamente: http://127.0.0.1:8000/
✓ No uses localhost (puede no funcionar)
```

### "Error en base de datos"
```
✓ Ejecuta: python manage.py migrate
✓ Ejecuta: python manage.py load_faqs
```

### "No puedo crear usuario"
```
✓ El usuario no debe existir ya
✓ Usa caracteres válidos en nombre
✓ Contraseña debe tener 8+ caracteres
```

### "No puedo descargar PDF"
```
✓ Verifica que reportlab esté instalado
✓ Ejecuta: pip install reportlab
```

---

## 📞 Información Importante

### Ubicación de Archivos
```
Aplicación: c:\Users\juan gallardo\Desktop\Django
Base de datos: db.sqlite3 (en la carpeta raíz)
Media/evidencias: media/ (se crea automáticamente)
```

### Documentación
```
README.md - Información general
TESTING_GUIDE.md - Guía detallada de pruebas
IMPLEMENTATION_SUMMARY.md - Resumen técnico
```

### Crear Datos de Prueba
```bash
python create_demo_data.py
```

---

## ✨ Próximos Pasos

Después de validar la aplicación:

1. **Configurar Email Real**
   - Edita settings.py
   - Configura SMTP
   - Las notificaciones se enviarán

2. **Integrar SMS**
   - Registrate en Twilio
   - Actualiza views.py
   - SMS se enviará en reclamos urgentes

3. **Hacer Backup**
   ```bash
   python manage.py dumpdata > backup.json
   ```

4. **Producción**
   - Cambia DEBUG = False en settings.py
   - Configura ALLOWED_HOSTS
   - Usa servidor profesional (Gunicorn)
   - Configura base de datos (PostgreSQL)

---

## 🎓 Aprende Más

### Estructura del Proyecto
```
Django/
├── manage.py              # Comandos Django
├── db.sqlite3            # Base de datos
├── requirements.txt      # Dependencias
├── create_demo_data.py   # Crear datos
├── README.md             # Información
├── reclamos_project/     # Configuración
│   ├── settings.py       # Configuración principal
│   ├── urls.py          # URLs del proyecto
│   └── wsgi.py
└── claims/              # Aplicación principal
    ├── models.py        # 5 modelos
    ├── views.py         # 20+ vistas
    ├── forms.py         # 5 formularios
    ├── urls.py          # 24 rutas
    ├── admin.py         # Admin config
    └── templates/       # 15 plantillas HTML
```

### Comandos Útiles
```bash
# Ver migraciones
python manage.py showmigrations

# Revertir migración
python manage.py migrate claims 0000

# Shell interactivo
python manage.py shell

# Crear datos
python create_demo_data.py

# Cargar FAQs
python manage.py load_faqs
```

---

## 🎊 ¡Listo para Comenzar!

Tu aplicación de reclamos incluye:
- ✅ 24 requerimientos implementados
- ✅ 5 modelos de datos
- ✅ 20+ vistas
- ✅ 15 plantillas HTML
- ✅ Sistema de auditoría
- ✅ Reportes exportables
- ✅ 10 FAQs precargadas
- ✅ Usuarios de prueba

**¡Disfruta usando tu sistema de reclamos!** 🚀

---

**Versión**: 1.0  
**Fecha**: 21 de Noviembre de 2025  
**Estado**: ✅ Producción Lista
