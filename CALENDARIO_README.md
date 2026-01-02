# 📅 Módulo de Calendario - Documentación para Nueva App

## Resumen
Este módulo fue desarrollado para gestionar el calendario de clases y talleres de los diplomados. Ha sido removido de la app principal ACADEMIAPP para ser implementado como una aplicación independiente.

---

## 🗄️ Estructura de Base de Datos

### Tabla: `calendario`
```sql
CREATE TABLE IF NOT EXISTS calendario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    diplomado_clave TEXT NOT NULL,
    tipo TEXT NOT NULL,
    modulo INTEGER NOT NULL,
    FOREIGN KEY (diplomado_clave) REFERENCES diplomados(clave)
);
```

**Campos:**
- `id`: Identificador único del evento
- `fecha`: Fecha del evento (formato: YYYY-MM-DD)
- `diplomado_clave`: Clave del diplomado (ej: TCC-8VA-P)
- `tipo`: Tipo de evento ("Clase" o "Mesa de trabajo")
- `modulo`: Número de módulo (1, 2, 3, etc.)

---

## 🔧 Funciones de Base de Datos Necesarias

### 1. Agregar Evento
```python
def add_evento_calendario(self, fecha, diplomado_clave, tipo, modulo):
    query = "INSERT INTO calendario (fecha, diplomado_clave, tipo, modulo) VALUES (?, ?, ?, ?)"
    self.cursor.execute(query, (fecha, diplomado_clave, tipo, modulo))
    self.conn.commit()
    return True
```

### 2. Obtener Todos los Eventos
```python
def get_eventos_calendario(self):
    query = "SELECT * FROM calendario ORDER BY fecha DESC"
    self.cursor.execute(query)
    return self.cursor.fetchall()
```

### 3. Obtener Eventos por Mes
```python
def get_eventos_mes(self, año, mes):
    query = """
    SELECT * FROM calendario 
    WHERE strftime('%Y', fecha) = ? AND strftime('%m', fecha) = ?
    ORDER BY fecha
    """
    self.cursor.execute(query, (str(año), f'{mes:02d}'))
    return self.cursor.fetchall()
```

### 4. Actualizar Evento
```python
def update_evento_calendario(self, id, fecha, diplomado_clave, tipo, modulo):
    query = """
    UPDATE calendario 
    SET fecha = ?, diplomado_clave = ?, tipo = ?, modulo = ?
    WHERE id = ?
    """
    self.cursor.execute(query, (fecha, diplomado_clave, tipo, modulo, id))
    self.conn.commit()
    return True
```

### 5. Eliminar Evento
```python
def delete_evento_calendario(self, id):
    query = "DELETE FROM calendario WHERE id = ?"
    self.cursor.execute(query, (id,))
    self.conn.commit()
    return True
```

---

## 🎨 Interfaz de Usuario (3 Pestañas)

### Pestaña 1: Vista de Calendario 📅
**Funcionalidades:**
- **4 Filtros principales:**
  - Año (año anterior, actual, siguiente)
  - Mes (Todos, Enero-Diciembre)
  - Diplomado (Todos o filtrar por diplomado específico)
  - Tipo (Todos, Clase, Mesa de trabajo)

- **Estadísticas rápidas:**
  - Total de eventos
  - Total de clases
  - Total de mesas de trabajo

- **Visualización:**
  - Eventos agrupados por fecha
  - Expandables con día de la semana
  - Muestra: Diplomado, Tipo, Módulo, ID

- **Gráfico:**
  - Distribución de eventos por diplomado (gráfico de barras)

### Pestaña 2: Agregar Evento ➕
**Formulario con:**
- Fecha del evento (date_input)
- Diplomado (selectbox con lista de diplomados)
- Tipo de evento (radio: Clase / Mesa de trabajo)
- Módulo (number_input)
- Botón "Guardar Evento"

### Pestaña 3: Gestionar Eventos 📋
**Funcionalidades:**
- **Búsqueda avanzada:**
  - Filtros: Mes, Año, Diplomado
  - Tabla con todos los eventos filtrados

- **Acciones:**
  - **Editar:** Cargar evento por ID y modificar sus datos
  - **Eliminar:** Eliminar evento por ID

- **Descarga:**
  - Botón para descargar calendario en CSV

---

## 📦 Dependencias

```python
import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px
```

---

## 🎯 Características Implementadas

### Filtro "Todos" en Mes
Cuando se selecciona "Todos" en el filtro de mes, muestra todos los eventos del año seleccionado.

### Códigos de Días de Semana
```python
dia_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"][fecha_obj.weekday()]
```

### Formato de Fecha para Display
```python
fecha_obj.strftime('%d de %B de %Y')  # Ej: 29 de Diciembre de 2025
```

---

## 🔗 Relación con Diplomados

El calendario está vinculado a la tabla `diplomados` mediante la columna `diplomado_clave`. 

**Asegúrate de tener acceso a:**
```python
db.get_all_diplomados()  # Retorna lista de diplomados para los selectores
```

**Formato esperado del retorno:**
```python
[(id, nombre, clave, modalidad, fecha_inicio, fecha_fin, mensualidades, total_alumnos), ...]
```

---

## 💡 Notas de Implementación

1. **Validación:** Asegúrate de que `diplomado_clave` no sea None antes de guardar
2. **Rerun:** Usa `st.rerun()` después de agregar/editar/eliminar para refrescar la vista
3. **Session State:** Utiliza `st.session_state.evento_edit` para mantener el evento en edición
4. **Keys únicos:** Usa keys en widgets dentro de tabs para evitar conflictos (ej: `key="cal_año"`)

---

## 🚀 Para Implementar en Nueva App

### Paso 1: Crear la base de datos
- Crear tabla `calendario` con el schema proporcionado
- Implementar las 5 funciones de base de datos

### Paso 2: Importar dependencias
- Streamlit
- Pandas
- Plotly Express
- datetime

### Paso 3: Copiar el código UI
El código completo de las 3 pestañas está en el archivo original antes de ser eliminado.

### Paso 4: Conectar con diplomados
- Asegúrate de tener acceso a la lista de diplomados
- Puedes compartir la misma base de datos o hacer una conexión externa

---

## 📊 Datos de Ejemplo

```python
# Ejemplo de evento
{
    'id': 1,
    'fecha': '2025-12-30',
    'diplomado_clave': 'TCC-8VA-P',
    'tipo': 'Clase',
    'modulo': 3
}
```

---

## ✅ Checklist de Implementación

- [ ] Crear tabla calendario en DB
- [ ] Implementar las 5 funciones CRUD
- [ ] Crear interfaz con 3 pestañas
- [ ] Implementar filtros (Año, Mes, Diplomado, Tipo)
- [ ] Agregar estadísticas y métricas
- [ ] Implementar gráfico de distribución
- [ ] Agregar funcionalidad de edición
- [ ] Agregar funcionalidad de eliminación
- [ ] Implementar descarga a CSV
- [ ] Probar con datos reales

---

## 🎨 Estilo CSS (Opcional)

Si quieres mantener el mismo estilo de la app principal:

```css
.main-header {
    font-size: 2rem;
    font-weight: bold;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 20px;
}
```

---

**Fecha de Documentación:** 29 de Diciembre de 2025  
**Autor:** Sistema AcademiApp  
**Versión:** 1.0
