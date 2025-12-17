# AcademiApp 🎓

Sistema de Gestión Administrativa para Academia de Psicología

## Características

- 📚 **Gestión de Diplomados**: Registro y administración de diplomados con todas sus características
- 👥 **Gestión de Alumnos**: Control completo de alumnos, con validaciones de matrícula, CURP, teléfono y correo
- 💰 **Registro de Pagos**: Sistema de registro de pagos por mensualidad con múltiples métodos
- 💸 **Control de Gastos**: Registro sencillo de gastos de la academia
- 📊 **Dashboard**: Vista general con métricas y gráficos
- 📄 **Reportes**: Generación de reportes detallados con filtros avanzados

## Instalación Local

1. Clona o descarga este repositorio
2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecuta la aplicación:

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## Estructura de Datos

### Diplomados
- Nombre del diplomado
- Clave (ej: TCC-8VA-P)
- Modalidad (Presencial/Virtual/Híbrida)
- Fechas de inicio y finalización
- Número de mensualidades
- Alumnos inscritos

### Alumnos
- Matrícula (10 dígitos)
- Nombre completo
- CURP (18 caracteres)
- Status (Activo/Baja/Baja temporal/Prospecto)
- Diplomado activo
- Teléfono (10 dígitos)
- Correo electrónico
- Fecha de inscripción
- Pagos (inscripción y mensualidades)

### Pagos
- Alumno y diplomado asociado
- Número de mensualidad
- Monto
- Fecha de pago
- Método de pago (Transferencia/Efectivo/Depósito/Enlace)

### Gastos
- Fecha
- Concepto
- Monto

## Despliegue en Streamlit Cloud

Para usar la aplicación desde cualquier lugar:

1. Sube este proyecto a un repositorio de GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu cuenta de GitHub
4. Selecciona el repositorio y la rama
5. Especifica el archivo principal: `app.py`
6. Haz clic en "Deploy"

Tu aplicación estará disponible en línea con una URL única.

## Uso

### Dashboard
Vista general con métricas de:
- Total de diplomados y alumnos
- Ingresos y gastos del mes
- Gráficos de alumnos por diplomado
- Lista de alumnos con adeudos

### Gestión de Diplomados
- Registra nuevos diplomados con toda la información necesaria
- Edita o elimina diplomados existentes
- Visualiza todos los diplomados activos

### Gestión de Alumnos
- Registra nuevos alumnos con validaciones automáticas
- Busca y filtra alumnos por nombre, matrícula o diplomado
- Edita información de alumnos
- Visualiza historial de pagos por alumno

### Registro de Pagos
- Selecciona el diplomado y número de mensualidad
- Registra pagos de múltiples alumnos a la vez
- Visualiza qué alumnos ya pagaron
- Historial completo de pagos con filtros

### Control de Gastos
- Registro rápido de gastos
- Historial de gastos con filtros por fecha
- Totales automáticos

### Reportes
- Pagos por diplomado
- Pagos por alumno
- Pagos por periodo
- Estado de cuenta detallado
- Resumen financiero con gráficos
- Exportación a CSV

## Base de Datos

La aplicación usa SQLite, una base de datos ligera que se guarda en un archivo local (`academiapp.db`). No requiere instalación de servidor de base de datos.

## Soporte

Para cualquier duda o sugerencia, por favor contacta al administrador de la academia.

---

**AcademiApp v1.0** - Sistema de Gestión Académica
