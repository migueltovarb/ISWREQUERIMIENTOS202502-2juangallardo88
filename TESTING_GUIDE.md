# Guía de Pruebas - Sistema de Reclamos

## Pruebas Rápidas para Verificar Funcionalidad

### 1. PRUEBA SIN AUTENTICACIÓN (RF1, RF3, RF4, RF5, RF6, RF19, RF20)

**Objetivo**: Verificar que cualquiera puede registrar un reclamo

**Pasos**:
1. Ve a `http://127.0.0.1:8000/`
2. Haz clic en "Registrar Reclamo"
3. Completa el formulario:
   - Nombre completo: "Juan Pérez"
   - Correo o Teléfono: "juan@example.com"
   - Número de pedido: "PED-12345"
   - Zona: "Centro"
   - Descripción: "El producto llegó dañado"
   - Prioridad: "Normal"
   - Evidencia: (Opcional, adjunta una imagen)
4. Haz clic en "Registrar Reclamo"

**Resultado Esperado**: 
- ✅ Ver mensaje: "¡Reclamo registrado correctamente! Tu número de reclamo es: R-XXXXXXXX"
- ✅ Ser redirigido a página con número de reclamo
- ✅ Poder ver el estado: "Pendiente"

---

### 2. PRUEBA DE BÚSQUEDA (RF21)

**Objetivo**: Buscar reclamo por número

**Pasos**:
1. Ve a "Buscar Reclamo"
2. Ingresa el número que recibiste (ej: R-ABC12345)
3. Haz clic en "Buscar"
4. También intenta con número de pedido

**Resultado Esperado**:
- ✅ Ver reclamo en los resultados
- ✅ Poder acceder a los detalles

---

### 3. PRUEBA DE REGISTRO DE USUARIO (RF2)

**Objetivo**: Verificar asociación automática de reclamos

**Pasos**:
1. Ve a "Registrarse"
2. Crea una cuenta:
   - Usuario: "testuser"
   - Email: "test@example.com"
   - Contraseña: "Test1234"
3. Inicia sesión
4. Registra un nuevo reclamo

**Resultado Esperado**:
- ✅ El reclamo se asocia automáticamente a tu usuario
- ✅ En "Mis Reclamos" ver este reclamo

---

### 4. PRUEBA PANEL DE ADMINISTRADOR (RF11, RF12, RF13, RF14)

**Objetivo**: Verificar funcionalidades admin

**Pasos**:
1. Crea un superusuario si no lo tienes:
   ```bash
   python manage.py createsuperuser
   ```

2. Inicia sesión con el admin
3. Ve a "Panel Admin"
4. Prueba filtros:
   - Filtrar por estado
   - Filtrar por prioridad
   - Filtrar por zona
   - Filtrar por fechas
5. Haz clic en el lápiz ✏️ para editar un reclamo
6. Cambia el estado a "En proceso"
7. Asigna a un usuario

**Resultado Esperado**:
- ✅ Los filtros funcionan correctamente
- ✅ El estado cambia
- ✅ Se muestra el historial de cambios
- ✅ Se registra la actividad

---

### 5. PRUEBA DE REPORTES (RF16, RF17)

**Objetivo**: Generar y exportar reportes

**Pasos**:
1. Como admin, ve a "Reportes"
2. Aplica filtros si lo deseas
3. Haz clic en "Descargar CSV"
4. Haz clic en "Descargar PDF"

**Resultado Esperado**:
- ✅ Se descarga un archivo CSV
- ✅ Se descarga un archivo PDF
- ✅ Los datos están correctos en ambos formatos

---

### 6. PRUEBA DE FAQs (RF24)

**Objetivo**: Verificar sección de ayuda

**Pasos**:
1. Ve a "Ayuda" en el menú
2. Lee las preguntas frecuentes
3. Como admin, ve a "Gestionar FAQs"
4. Haz clic en "Agregar FAQ"
5. Crea una nueva pregunta

**Resultado Esperado**:
- ✅ Las FAQs se muestran correctamente
- ✅ Puedes agregar nuevas FAQs
- ✅ Puedes editar y eliminar FAQs

---

### 7. PRUEBA DE AUDITORÍA (RF23)

**Objetivo**: Ver registro de actividades

**Pasos**:
1. Como admin, ve a "Actividades"
2. Deberías ver todas las acciones realizadas

**Resultado Esperado**:
- ✅ Ver todas las actividades del admin
- ✅ Incluir cambios de estado, creación de reclamos, etc.

---

### 8. PRUEBA DE VALIDACIONES (RF19)

**Objetivo**: Verificar validaciones de formulario

**Pasos**:
1. Ve a "Registrar Reclamo"
2. Intenta dejar campos en blanco
3. Ingresa descripción muy corta (menos de 10 caracteres)
4. Ingresa zona muy corta

**Resultado Esperado**:
- ✅ Ver mensajes de error claros
- ✅ El formulario no se envía
- ✅ Se señalan los campos con problemas

---

## Checklist Final

- [ ] RF1: Registrar sin login
- [ ] RF2: Asociación automática de cuenta
- [ ] RF3: Todos los datos requeridos
- [ ] RF4: Adjuntar evidencia
- [ ] RF5: Marcar como urgente/normal
- [ ] RF6: Asociar a zona
- [ ] RF7: Consultar estado
- [ ] RF8-RF10: Notificaciones (guardadas en BD)
- [ ] RF11-RF13: Panel admin con filtros y cambio de estado
- [ ] RF14: Historial con auditoría
- [ ] RF15: Clientes ven su historial
- [ ] RF16-RF17: Reportes y exportación
- [ ] RF18: Asignación a empleados
- [ ] RF19: Validaciones
- [ ] RF20: Confirmación con número
- [ ] RF21: Búsqueda
- [ ] RF22: Control de permisos
- [ ] RF23: Registro de actividades
- [ ] RF24: FAQs

---

## Errores Comunes y Soluciones

### Error: "No matching URL pattern"
- Verifica que estés usando URLs correctas
- Recarga la página del servidor

### Error: "Relation does not exist"
- Ejecuta: `python manage.py migrate`

### Error: Notificaciones no se envían por email
- Configura EMAIL_BACKEND en settings.py
- Por defecto se guardan en la base de datos

### Error: No puedo descargar PDF
- Verifica que reportlab esté instalado: `pip install reportlab`

---

## Contacto y Soporte

Para soporte técnico:
📧 soporte@reclamos.com
📱 +1 234 567 890
