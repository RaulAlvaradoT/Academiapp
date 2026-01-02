import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from database import DatabaseManager
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="AcademiApp",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SISTEMA DE AUTENTICACIÓN
# ============================================================================
# Contraseña de acceso
PASSWORD = "2!fkYgD&"

# Inicializar estado de sesión
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Verificar autenticación
if not st.session_state.authenticated:
    st.markdown('<p style="font-size: 2.5rem; font-weight: bold; color: #1f77b4; text-align: center;">AcademiApp</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("🔒 Acceso al Sistema")
        password_input = st.text_input("Ingresa la contraseña:", type="password", key="password_input")
        
        if st.button("Ingresar", use_container_width=True):
            if password_input == PASSWORD:
                st.session_state.authenticated = True
                st.success("✅ Acceso concedido")
                st.rerun()
            else:
                st.error("❌ Contraseña incorrecta")
    
    st.stop()

# ============================================================================
# APLICACIÓN PRINCIPAL
# ============================================================================

# Inicializar base de datos
db = DatabaseManager()

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar - Navegación
st.sidebar.title("AcademiApp")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navegación",
    ["🏠 Dashboard", "📚 Diplomados", "👥 Alumnos", "💰 Pagos", "💸 Gastos", "📊 Reportes"]
)

st.sidebar.markdown("---")
st.sidebar.info(f"📅 {datetime.now().strftime('%d/%m/%Y')}")

# Botón de cerrar sesión
if st.sidebar.button("🚪 Cerrar Sesión"):
    st.session_state.authenticated = False
    st.rerun()

# ============================================================================
# 🏠 DASHBOARD
# ============================================================================
if menu == "🏠 Dashboard":
    st.markdown('<p class="main-header">Dashboard - Resumen General</p>', unsafe_allow_html=True)
    
    # Obtener datos para métricas
    total_alumnos = db.get_total_alumnos()
    alumnos_activos = db.get_alumnos_activos()
    total_diplomados = db.get_total_diplomados()
    ingresos_mes = db.get_ingresos_mes_actual()
    gastos_mes = db.get_gastos_mes_actual()
    
    # Métricas principales
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📚 Total Diplomados", total_diplomados)
    with col2:
        st.metric("👥 Total Alumnos", total_alumnos)
    with col3:
        st.metric("✅ Alumnos Activos", alumnos_activos)
    with col4:
        st.metric("💰 Ingresos (Mes)", f"${ingresos_mes:,.2f}")
    with col5:
        st.metric("💸 Gastos (Mes)", f"${gastos_mes:,.2f}")
    
    st.markdown("---")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Alumnos por Diplomado")
        alumnos_por_diplomado = db.get_alumnos_por_diplomado()
        if alumnos_por_diplomado:
            df = pd.DataFrame(alumnos_por_diplomado, columns=['Diplomado', 'Total'])
            fig = px.bar(df, x='Diplomado', y='Total', color='Total', 
                        color_continuous_scale='Blues')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos de alumnos por diplomado")
    
    with col2:
        st.subheader("💵 Ingresos vs Gastos (6 meses)")
        ingresos_gastos = db.get_ingresos_gastos_6_meses()
        if ingresos_gastos:
            df = pd.DataFrame(ingresos_gastos, columns=['Mes', 'Ingresos', 'Gastos'])
            fig = go.Figure()
            fig.add_trace(go.Bar(x=df['Mes'], y=df['Ingresos'], name='Ingresos', marker_color='green'))
            fig.add_trace(go.Bar(x=df['Mes'], y=df['Gastos'], name='Gastos', marker_color='red'))
            fig.update_layout(barmode='group')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos de ingresos y gastos")
    


# ============================================================================
# 📚 GESTIÓN DE DIPLOMADOS
# ============================================================================
elif menu == "📚 Diplomados":
    st.markdown('<p class="main-header">Gestión de Diplomados</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 Diplomados Activos", "📦 Diplomados Archivados", "➕ Agregar Diplomado"])
    
    with tab1:
        diplomados = db.get_diplomados_filtrados('Activo')
        
        if diplomados:
            st.subheader("Diplomados Activos")
            
            for dip in diplomados:
                with st.expander(f"📚 {dip[1]} - {dip[2]}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Clave:** {dip[2]}")
                        st.write(f"**Modalidad:** {dip[3]}")
                        st.write(f"**Inicio:** {dip[4]} | **Fin:** {dip[5]}")
                        st.write(f"**Mensualidades:** {dip[6]}")
                        st.write(f"**Alumnos inscritos:** {dip[7]}")
                    
                    with col2:
                        if st.button("✏️ Editar", key=f"edit_dip_{dip[0]}"):
                            st.session_state.editing_diplomado = dip[0]
                        if st.button("📦 Archivar", key=f"arch_dip_{dip[0]}"):
                            if db.archivar_diplomado(dip[0]):
                                st.success("Diplomado archivado")
                                st.rerun()
                            else:
                                st.error("Error al archivar")
                        if st.button("🗑️ Eliminar", key=f"del_dip_{dip[0]}"):
                            if db.delete_diplomado(dip[0]):
                                st.success("Diplomado eliminado")
                                st.rerun()
                            else:
                                st.error("No se puede eliminar (tiene alumnos)")
                    
                    # Modo edición
                    if st.session_state.get('editing_diplomado') == dip[0]:
                        st.markdown("---")
                        st.subheader("Editar Diplomado")
                        
                        with st.form(f"edit_form_{dip[0]}"):
                            nombre = st.text_input("Nombre", value=dip[1])
                            clave = st.text_input("Clave", value=dip[2])
                            modalidad = st.selectbox("Modalidad", 
                                                    ["Presencial", "Virtual", "Híbrida"],
                                                    index=["Presencial", "Virtual", "Híbrida"].index(dip[3]))
                            fecha_inicio = st.date_input("Fecha Inicio", value=datetime.strptime(dip[4], '%Y-%m-%d'))
                            fecha_fin = st.date_input("Fecha Fin", value=datetime.strptime(dip[5], '%Y-%m-%d'))
                            mensualidades = st.number_input("Mensualidades", value=dip[6], min_value=1)
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button("💾 Guardar cambios"):
                                    db.update_diplomado(dip[0], nombre, clave, modalidad, 
                                                       fecha_inicio.strftime('%Y-%m-%d'),
                                                       fecha_fin.strftime('%Y-%m-%d'), mensualidades)
                                    del st.session_state.editing_diplomado
                                    st.success("Diplomado actualizado")
                                    st.rerun()
                            with col2:
                                if st.form_submit_button("❌ Cancelar"):
                                    del st.session_state.editing_diplomado
                                    st.rerun()
        else:
            st.info("No hay diplomados activos")
    
    with tab2:
        diplomados_archivados = db.get_diplomados_filtrados('Archivado')
        
        if diplomados_archivados:
            st.subheader("Diplomados Archivados")
            
            for dip in diplomados_archivados:
                with st.expander(f"📦 {dip[1]} - {dip[2]}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Clave:** {dip[2]}")
                        st.write(f"**Modalidad:** {dip[3]}")
                        st.write(f"**Inicio:** {dip[4]} | **Fin:** {dip[5]}")
                        st.write(f"**Mensualidades:** {dip[6]}")
                        st.write(f"**Alumnos inscritos:** {dip[7]}")
                    
                    with col2:
                        if st.button("🔄 Reactivar", key=f"react_dip_{dip[0]}"):
                            if db.reactivar_diplomado(dip[0]):
                                st.success("Diplomado reactivado")
                                st.rerun()
                            else:
                                st.error("Error al reactivar")
        else:
            st.info("No hay diplomados archivados")
    
    with tab3:
        st.subheader("Registrar Nuevo Diplomado")
        
        with st.form("nuevo_diplomado"):
            nombre = st.text_input("Nombre del Diplomado *")
            clave = st.text_input("Clave (ej: TCC-8VA-P) *")
            modalidad = st.selectbox("Modalidad *", ["Presencial", "Virtual", "Híbrida"])
            
            col1, col2 = st.columns(2)
            with col1:
                fecha_inicio = st.date_input("Fecha de Inicio *")
            with col2:
                fecha_fin = st.date_input("Fecha de Finalización *")
            
            mensualidades = st.number_input("Número de Mensualidades *", min_value=1, value=10)
            
            submitted = st.form_submit_button("➕ Registrar Diplomado")
            
            if submitted:
                if not nombre or not clave:
                    st.error("Por favor completa todos los campos obligatorios")
                else:
                    if db.add_diplomado(nombre, clave, modalidad, 
                                       fecha_inicio.strftime('%Y-%m-%d'),
                                       fecha_fin.strftime('%Y-%m-%d'), mensualidades):
                        st.success("✅ Diplomado registrado exitosamente")
                        st.rerun()
                    else:
                        st.error("Error al registrar diplomado")

# ============================================================================
# 👥 GESTIÓN DE ALUMNOS
# ============================================================================
elif menu == "👥 Alumnos":
    st.markdown('<p class="main-header">Gestión de Alumnos</p>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📋 Lista de Alumnos", "➕ Agregar Alumno"])
    
    with tab1:
        st.subheader("Buscar Alumnos")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            filtro_nombre = st.text_input("🔍 Buscar por nombre")
        with col2:
            filtro_matricula = st.text_input("🔍 Buscar por matrícula")
        with col3:
            diplomados = db.get_all_diplomados()
            opciones_dip = ["Todos"] + [f"{d[1]} ({d[2]})" for d in diplomados]
            filtro_diplomado = st.selectbox("Filtrar por diplomado", opciones_dip)
        
        # Obtener alumnos
        alumnos = db.get_alumnos_filtrados(filtro_nombre, filtro_matricula, 
                                          None if filtro_diplomado == "Todos" else filtro_diplomado)
        
        if alumnos:
            st.write(f"**Total de registros encontrados:** {len(alumnos)}")
            
            for alumno in alumnos:
                with st.expander(f"👤 {alumno[2]} - {alumno[1]} ({alumno[5]})"):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.write(f"**Matrícula:** {alumno[1]}")
                        st.write(f"**Nombre:** {alumno[2]}")
                        st.write(f"**CURP:** {alumno[13]}")
                        st.write(f"**Teléfono:** {alumno[6]}")
                        st.write(f"**Correo:** {alumno[7]}")
                    
                    with col2:
                        st.write(f"**Status:** {alumno[3]}")
                        st.write(f"**Diplomado:** {alumno[5]}")
                        st.write(f"**Inscripción:** {alumno[8]}")
                        st.write(f"**Pago Inscripción:** ${alumno[9]:,.2f}")
                        st.write(f"**Mensualidad:** ${alumno[10]:,.2f}")
                        
                        # Mostrar información de baja si aplica
                        if alumno[3] == "Baja" and len(alumno) > 14:
                            if alumno[14]:  # fecha_baja
                                st.write(f"**Fecha de Baja:** {alumno[14]}")
                            if len(alumno) > 15 and alumno[15]:  # motivo_baja
                                st.write(f"**Motivo:** {alumno[15]}")
                    
                    with col3:
                        if st.button("✏️ Editar", key=f"edit_al_{alumno[0]}"):
                            st.session_state.editing_alumno = alumno[0]
                        if st.button("🗑️ Eliminar", key=f"del_al_{alumno[0]}"):
                            if db.delete_alumno(alumno[0]):
                                st.success("Alumno eliminado")
                                st.rerun()
                    
                    # Ver pagos
                    pagos = db.get_pagos_alumno(alumno[0])
                    if pagos:
                        st.markdown("**Historial de Pagos:**")
                        df_pagos = pd.DataFrame(pagos, 
                                              columns=['Mensualidad', 'Monto', 'Fecha', 'Método'])
                        st.dataframe(df_pagos, use_container_width=True)
                    
                    # Modo edición
                    if st.session_state.get('editing_alumno') == alumno[0]:
                        st.markdown("---")
                        with st.form(f"edit_alumno_{alumno[0]}"):
                            st.subheader("Editar Alumno")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                matricula = st.text_input("Matrícula", value=alumno[1])
                                nombre = st.text_input("Nombre Completo", value=alumno[2])
                                curp = st.text_input("CURP", value=alumno[13], max_chars=18)
                                telefono = st.text_input("Teléfono", value=alumno[6], max_chars=10)
                                correo = st.text_input("Correo", value=alumno[7])
                            
                            with col2:
                                status = st.selectbox("Status", 
                                    ["Activo", "Baja", "Baja temporal", "Prospecto"],
                                    index=["Activo", "Baja", "Baja temporal", "Prospecto"].index(alumno[3]))
                                
                                # Si el status es Baja, mostrar campos adicionales
                                fecha_baja = None
                                motivo_baja = None
                                if status == "Baja":
                                    st.markdown("**Información de Baja:**")
                                    fecha_baja_val = alumno[14] if len(alumno) > 14 and alumno[14] else datetime.now().strftime('%Y-%m-%d')
                                    fecha_baja = st.date_input("Fecha de Baja", 
                                        value=datetime.strptime(fecha_baja_val, '%Y-%m-%d') if fecha_baja_val else datetime.now())
                                    motivo_baja = st.text_area("Motivo de Baja", 
                                        value=alumno[15] if len(alumno) > 15 and alumno[15] else "")
                                
                                dips = db.get_all_diplomados()
                                dip_options = [f"{d[2]}" for d in dips]
                                diplomado = st.selectbox("Diplomado Activo", dip_options,
                                    index=dip_options.index(alumno[5]) if alumno[5] in dip_options else 0)
                                
                                fecha_insc = st.date_input("Fecha Inscripción", 
                                    value=datetime.strptime(alumno[8], '%Y-%m-%d'))
                                pago_insc = st.number_input("Pago Inscripción", value=float(alumno[9]), min_value=0.0)
                                mensualidad = st.number_input("Mensualidad", value=float(alumno[10]), min_value=0.0)
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button("💾 Guardar"):
                                    # Validaciones
                                    if len(curp) != 18:
                                        st.error("CURP debe tener 18 caracteres")
                                    elif len(telefono) != 10:
                                        st.error("Teléfono debe tener 10 dígitos")
                                    elif '@' not in correo:
                                        st.error("Correo debe contener @")
                                    elif len(matricula) != 10:
                                        st.error("Matrícula debe tener 10 dígitos")
                                    elif status == "Baja" and not motivo_baja:
                                        st.error("Debes especificar el motivo de baja")
                                    else:
                                        fecha_baja_str = fecha_baja.strftime('%Y-%m-%d') if fecha_baja and status == "Baja" else None
                                        motivo_baja_str = motivo_baja if status == "Baja" else None
                                        
                                        db.update_alumno(alumno[0], matricula, nombre, status, 
                                                       diplomado, telefono, correo,
                                                       fecha_insc.strftime('%Y-%m-%d'),
                                                       pago_insc, mensualidad, curp,
                                                       fecha_baja_str, motivo_baja_str)
                                        del st.session_state.editing_alumno
                                        st.success("Alumno actualizado")
                                        st.rerun()
                            with col2:
                                if st.form_submit_button("❌ Cancelar"):
                                    del st.session_state.editing_alumno
                                    st.rerun()
        else:
            st.info("No se encontraron alumnos")
    
    with tab2:
        st.subheader("Registrar Nuevo Alumno")
        
        with st.form("nuevo_alumno"):
            col1, col2 = st.columns(2)
            
            with col1:
                nombre_completo = st.text_input("Nombre *")
                status = st.selectbox("Status *", ["Activo", "Baja", "Baja temporal", "Prospecto"])
                
                diplomados = db.get_all_diplomados()
                if diplomados:
                    opciones = [f"{d[2]}" for d in diplomados]
                    diplomado_activo = st.selectbox("Diplomado Activo *", opciones)
                else:
                    st.warning("⚠️ Primero debes registrar diplomados")
                    diplomado_activo = None
                
                matricula = st.text_input("Matrícula (10 dígitos)", max_chars=10)
                curp = st.text_input("CURP (18 caracteres) *", max_chars=18)
                telefono = st.text_input("Teléfono (10 dígitos) *", max_chars=10)
            
            with col2:
                correo = st.text_input("Correo Electrónico *")
                fecha_inscripcion = st.date_input("Fecha de Inscripción *")
                pago_inscripcion = st.number_input("Inscripción *", min_value=0.0, step=100.0)
                mensualidad = st.number_input("Mensualidad *", min_value=0.0, step=100.0)
                
                # Calcular y mostrar total diplomado
                if diplomados and diplomado_activo:
                    dip_seleccionado = next(d for d in diplomados if d[2] == diplomado_activo)
                    num_mensualidades = dip_seleccionado[6]
                    total_calculado = pago_inscripcion + (mensualidad * num_mensualidades)
                    st.info(f"**Total Diplomado:** ${total_calculado:,.2f}")
            
            submitted = st.form_submit_button("➕ Registrar Alumno")
            
            if submitted:
                # Validaciones
                if not all([nombre_completo, curp, telefono, correo, diplomado_activo]):
                    st.error("Por favor completa todos los campos obligatorios")
                elif matricula and len(matricula) != 10:
                    st.error("La matrícula debe tener exactamente 10 dígitos (o dejarla vacía)")
                elif len(curp) != 18:
                    st.error("El CURP debe tener exactamente 18 caracteres")
                elif len(telefono) != 10:
                    st.error("El teléfono debe tener exactamente 10 dígitos")
                elif '@' not in correo:
                    st.error("El correo debe contener @")
                else:
                    # Si matrícula está vacía, generar una temporal
                    if not matricula:
                        matricula = f"TEMP{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    
                    # Obtener número de mensualidades del diplomado
                    dip_seleccionado = next(d for d in diplomados if d[2] == diplomado_activo)
                    num_mensualidades = dip_seleccionado[6]
                    total = pago_inscripcion + (mensualidad * num_mensualidades)
                    
                    if db.add_alumno(matricula, nombre_completo, status, diplomado_activo, 
                                   telefono, correo, fecha_inscripcion.strftime('%Y-%m-%d'),
                                   pago_inscripcion, mensualidad, num_mensualidades, total, curp):
                        st.success("✅ Alumno registrado exitosamente")
                        # Actualizar contador de alumnos en diplomado
                        db.update_alumnos_inscritos(dip_seleccionado[0])
                        st.rerun()
                    else:
                        st.error("Error al registrar alumno")

# ============================================================================
# 💰 REGISTRO DE PAGOS
# ============================================================================
elif menu == "💰 Pagos":
    st.markdown('<p class="main-header">Registro de Pagos</p>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["➕ Registrar Pago", "📋 Historial de Pagos"])
    
    with tab1:
        st.subheader("Registrar Nuevo Pago")
        
        # Selección de diplomado
        diplomados = db.get_all_diplomados()
        if not diplomados:
            st.warning("⚠️ No hay diplomados registrados")
        else:
            opciones_dip = [f"{d[1]} ({d[2]})" for d in diplomados]
            diplomado_sel = st.selectbox("Selecciona el Diplomado", opciones_dip)
            
            # Extraer clave del diplomado
            clave_dip = diplomado_sel.split('(')[1].strip(')')
            
            # Obtener alumnos del diplomado
            alumnos = db.get_alumnos_por_diplomado_clave(clave_dip)
            
            if not alumnos:
                st.info("No hay alumnos en este diplomado")
            else:
                # Número de mensualidad
                mensualidad_num = st.number_input("Número de Mensualidad", min_value=1, value=1)
                
                st.markdown("---")
                st.subheader(f"Registrar pagos - Mensualidad #{mensualidad_num}")
                
                # Formulario para cada alumno
                for alumno in alumnos:
                    alumno_id, matricula, nombre, mensualidad_monto = alumno[0], alumno[1], alumno[2], alumno[3]
                    
                    # Verificar si ya pagó esta mensualidad
                    ya_pago = db.verificar_pago_mensualidad(alumno_id, mensualidad_num)
                    
                    with st.expander(f"{'✅' if ya_pago else '⏳'} {nombre} - {matricula}"):
                        if ya_pago:
                            st.success(f"✅ Mensualidad #{mensualidad_num} ya registrada")
                            # Mostrar detalles del pago
                            pago_info = db.get_detalle_pago(alumno_id, mensualidad_num)
                            if pago_info:
                                st.write(f"**Monto:** ${pago_info[0]:,.2f}")
                                st.write(f"**Fecha:** {pago_info[1]}")
                                st.write(f"**Método:** {pago_info[2]}")
                        else:
                            with st.form(f"pago_{alumno_id}_{mensualidad_num}"):
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    st.write(f"**Mensualidad:** ${mensualidad_monto:,.2f}")
                                    monto = st.number_input("Monto pagado", 
                                                           value=float(mensualidad_monto), 
                                                           min_value=0.0, key=f"monto_{alumno_id}")
                                
                                with col2:
                                    fecha_pago = st.date_input("Fecha de pago", 
                                                              key=f"fecha_{alumno_id}")
                                
                                with col3:
                                    metodo = st.selectbox("Método de pago",
                                                         ["Transferencia", "Efectivo", "Depósito", "Enlace"],
                                                         key=f"metodo_{alumno_id}")
                                
                                if st.form_submit_button("💾 Registrar Pago"):
                                    if db.add_pago(alumno_id, mensualidad_num, monto, 
                                                  fecha_pago.strftime('%Y-%m-%d'), metodo):
                                        st.success(f"✅ Pago registrado para {nombre}")
                                        st.rerun()
                                    else:
                                        st.error("Error al registrar pago")
    
    with tab2:
        st.subheader("Historial de Pagos")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            fecha_inicio = st.date_input("Desde", value=datetime.now().replace(day=1))
        with col2:
            fecha_fin = st.date_input("Hasta", value=datetime.now())
        with col3:
            diplomados = db.get_all_diplomados()
            opciones = ["Todos"] + [d[2] for d in diplomados]
            filtro_dip = st.selectbox("Diplomado", opciones)
        
        if st.button("🔍 Buscar"):
            pagos = db.get_pagos_filtrados(fecha_inicio.strftime('%Y-%m-%d'),
                                          fecha_fin.strftime('%Y-%m-%d'),
                                          None if filtro_dip == "Todos" else filtro_dip)
            
            if pagos:
                df = pd.DataFrame(pagos, 
                                columns=['Matrícula', 'Nombre', 'Diplomado', 'Mensualidad', 
                                        'Monto', 'Fecha', 'Método'])
                st.dataframe(df, use_container_width=True)
                
                total = sum([p[4] for p in pagos])
                st.success(f"**Total recaudado:** ${total:,.2f}")
            else:
                st.info("No se encontraron pagos en el periodo seleccionado")

# ============================================================================
# 💸 REGISTRO DE GASTOS
# ============================================================================
elif menu == "💸 Gastos":
    st.markdown('<p class="main-header">Registro de Gastos</p>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["➕ Registrar Gasto", "📋 Historial de Gastos"])
    
    with tab1:
        st.subheader("Registrar Nuevo Gasto")
        
        with st.form("nuevo_gasto"):
            fecha = st.date_input("Fecha del Gasto *")
            concepto = st.text_input("Concepto *", placeholder="Ej: Papelería, Renta, Servicios...")
            monto = st.number_input("Monto *", min_value=0.0, step=10.0)
            
            submitted = st.form_submit_button("💾 Registrar Gasto")
            
            if submitted:
                if not concepto:
                    st.error("El concepto es obligatorio")
                elif monto <= 0:
                    st.error("El monto debe ser mayor a 0")
                else:
                    if db.add_gasto(fecha.strftime('%Y-%m-%d'), concepto, monto):
                        st.success("✅ Gasto registrado exitosamente")
                        st.rerun()
                    else:
                        st.error("Error al registrar gasto")
    
    with tab2:
        st.subheader("Historial de Gastos")
        
        col1, col2 = st.columns(2)
        with col1:
            fecha_inicio = st.date_input("Desde", value=datetime.now().replace(day=1), key="gasto_inicio")
        with col2:
            fecha_fin = st.date_input("Hasta", value=datetime.now(), key="gasto_fin")
        
        if st.button("🔍 Buscar Gastos"):
            gastos = db.get_gastos_filtrados(fecha_inicio.strftime('%Y-%m-%d'),
                                           fecha_fin.strftime('%Y-%m-%d'))
            
            if gastos:
                df = pd.DataFrame(gastos, columns=['ID', 'Fecha', 'Concepto', 'Monto'])
                
                # Botones de editar/eliminar
                for idx, gasto in enumerate(gastos):
                    col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 1, 1])
                    with col1:
                        st.write(gasto[1])  # Fecha
                    with col2:
                        st.write(gasto[2])  # Concepto
                    with col3:
                        st.write(f"${gasto[3]:,.2f}")  # Monto
                    with col4:
                        if st.button("✏️", key=f"edit_gasto_{gasto[0]}"):
                            st.session_state.editing_gasto = gasto[0]
                    with col5:
                        if st.button("🗑️", key=f"del_gasto_{gasto[0]}"):
                            if db.delete_gasto(gasto[0]):
                                st.success("Gasto eliminado")
                                st.rerun()
                
                st.markdown("---")
                total = sum([g[3] for g in gastos])
                st.error(f"**Total de gastos:** ${total:,.2f}")
            else:
                st.info("No se encontraron gastos en el periodo seleccionado")

# ============================================================================
# 📊 REPORTES
# ============================================================================
if menu == "📊 Reportes":
    st.markdown('<p class="main-header">Reportes y Análisis</p>', unsafe_allow_html=True)
    
    tipo_reporte = st.selectbox("Selecciona el tipo de reporte",
                               ["Pagos por Diplomado", "Pagos por Alumno", "Pagos por Periodo",
                                "Estado de Cuenta por Alumno", "Resumen Financiero"])
    
    st.markdown("---")
    
    if tipo_reporte == "Pagos por Diplomado":
        st.subheader("📚 Reporte de Pagos por Diplomado")
        
        diplomados = db.get_all_diplomados()
        if diplomados:
            opciones = [f"{d[1]} ({d[2]})" for d in diplomados]
            dip_sel = st.selectbox("Selecciona Diplomado", opciones)
            clave = dip_sel.split('(')[1].strip(')')
            
            col1, col2 = st.columns(2)
            with col1:
                fecha_inicio = st.date_input("Desde", key="rep1_inicio")
            with col2:
                fecha_fin = st.date_input("Hasta", key="rep1_fin")
            
            if st.button("Generar Reporte"):
                pagos = db.get_reporte_pagos_diplomado(clave, 
                                                      fecha_inicio.strftime('%Y-%m-%d'),
                                                      fecha_fin.strftime('%Y-%m-%d'))
                if pagos:
                    df = pd.DataFrame(pagos, 
                                    columns=['Matrícula', 'Nombre', 'Mensualidad', 'Monto', 'Fecha', 'Método'])
                    st.dataframe(df, use_container_width=True)
                    
                    total = sum([p[3] for p in pagos])
                    st.success(f"**Total recaudado:** ${total:,.2f}")
                    
                    # Botón para descargar
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Descargar CSV", csv, 
                                     f"reporte_{clave}_{datetime.now().strftime('%Y%m%d')}.csv",
                                     "text/csv")
                else:
                    st.info("No hay pagos en el periodo seleccionado")
    
    elif tipo_reporte == "Pagos por Alumno":
        st.subheader("👤 Reporte de Pagos por Alumno")
        
        matricula = st.text_input("Ingresa la Matrícula del Alumno")
        
        if matricula and st.button("Generar Reporte"):
            alumno_info = db.get_alumno_por_matricula(matricula)
            
            if alumno_info:
                st.write(f"**Nombre:** {alumno_info[2]}")
                st.write(f"**Diplomado:** {alumno_info[5]}")
                st.write(f"**Status:** {alumno_info[3]}")
                
                st.markdown("---")
                
                pagos = db.get_pagos_alumno(alumno_info[0])
                if pagos:
                    df = pd.DataFrame(pagos, columns=['Mensualidad', 'Monto', 'Fecha', 'Método'])
                    st.dataframe(df, use_container_width=True)
                    
                    total_pagado = sum([p[1] for p in pagos])
                    total_esperado = alumno_info[9] + (alumno_info[10] * alumno_info[11])
                    adeudo = total_esperado - total_pagado
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Pagado", f"${total_pagado:,.2f}")
                    with col2:
                        st.metric("Total Esperado", f"${total_esperado:,.2f}")
                    with col3:
                        st.metric("Adeudo", f"${adeudo:,.2f}", 
                                delta=f"{'-' if adeudo < 0 else ''}${abs(adeudo):,.2f}")
                else:
                    st.warning("No hay pagos registrados para este alumno")
            else:
                st.error("Matrícula no encontrada")
    
    elif tipo_reporte == "Pagos por Periodo":
        st.subheader("📅 Reporte de Pagos por Periodo")
        
        col1, col2 = st.columns(2)
        with col1:
            fecha_inicio = st.date_input("Desde", key="rep3_inicio")
        with col2:
            fecha_fin = st.date_input("Hasta", key="rep3_fin")
        
        if st.button("Generar Reporte", key="btn_rep3"):
            pagos = db.get_pagos_filtrados(fecha_inicio.strftime('%Y-%m-%d'),
                                          fecha_fin.strftime('%Y-%m-%d'), None)
            
            if pagos:
                df = pd.DataFrame(pagos, 
                                columns=['Matrícula', 'Nombre', 'Diplomado', 'Mensualidad', 
                                        'Monto', 'Fecha', 'Método'])
                st.dataframe(df, use_container_width=True)
                
                # Resumen por método de pago
                st.subheader("Resumen por Método de Pago")
                metodos = {}
                for p in pagos:
                    metodo = p[6]
                    if metodo not in metodos:
                        metodos[metodo] = 0
                    metodos[metodo] += p[4]
                
                col1, col2, col3, col4 = st.columns(4)
                cols = [col1, col2, col3, col4]
                for idx, (metodo, total) in enumerate(metodos.items()):
                    with cols[idx % 4]:
                        st.metric(metodo, f"${total:,.2f}")
                
                total_general = sum([p[4] for p in pagos])
                st.success(f"**Total del periodo:** ${total_general:,.2f}")
                
                # Descargar
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Descargar CSV", csv, 
                                 f"reporte_periodo_{datetime.now().strftime('%Y%m%d')}.csv",
                                 "text/csv")
            else:
                st.info("No hay pagos en el periodo seleccionado")
    
    elif tipo_reporte == "Estado de Cuenta por Alumno":
        st.subheader("📄 Estado de Cuenta Detallado")
        
        matricula = st.text_input("Matrícula del Alumno", key="estado_cuenta_mat")
        
        if matricula and st.button("Generar Estado de Cuenta"):
            alumno = db.get_alumno_por_matricula(matricula)
            
            if alumno:
                st.markdown("### Información del Alumno")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Nombre:** {alumno[2]}")
                    st.write(f"**Matrícula:** {alumno[1]}")
                    st.write(f"**CURP:** {alumno[13]}")
                with col2:
                    st.write(f"**Diplomado:** {alumno[5]}")
                    st.write(f"**Status:** {alumno[3]}")
                    st.write(f"**Inscripción:** {alumno[8]}")
                
                st.markdown("---")
                st.markdown("### Detalle de Pagos")
                
                # Información de pagos esperados
                num_mensualidades = alumno[11]
                monto_mensualidad = alumno[10]
                pago_inscripcion = alumno[9]
                
                # Pagos realizados
                pagos = db.get_pagos_alumno(alumno[0])
                mensualidades_pagadas = [p[0] for p in pagos] if pagos else []
                
                # Tabla de mensualidades
                data = []
                for i in range(1, num_mensualidades + 1):
                    if i in mensualidades_pagadas:
                        pago = next(p for p in pagos if p[0] == i)
                        data.append({
                            'Mensualidad': i,
                            'Esperado': monto_mensualidad,
                            'Pagado': pago[1],
                            'Fecha': pago[2],
                            'Método': pago[3],
                            'Status': '✅ Pagado'
                        })
                    else:
                        data.append({
                            'Mensualidad': i,
                            'Esperado': monto_mensualidad,
                            'Pagado': 0,
                            'Fecha': '-',
                            'Método': '-',
                            'Status': '⏳ Pendiente'
                        })
                
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)
                
                # Resumen financiero
                st.markdown("---")
                st.markdown("### Resumen Financiero")
                
                total_esperado = pago_inscripcion + (monto_mensualidad * num_mensualidades)
                total_pagado = pago_inscripcion + sum([p[1] for p in pagos]) if pagos else pago_inscripcion
                adeudo = total_esperado - total_pagado
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Inscripción", f"${pago_inscripcion:,.2f}")
                with col2:
                    st.metric("Total Pagado", f"${total_pagado:,.2f}")
                with col3:
                    st.metric("Total Esperado", f"${total_esperado:,.2f}")
                with col4:
                    if adeudo > 0:
                        st.metric("Adeudo", f"${adeudo:,.2f}", delta="Pendiente", delta_color="inverse")
                    else:
                        st.metric("Adeudo", "$0.00", delta="Al corriente", delta_color="normal")
            else:
                st.error("Matrícula no encontrada")
    
    elif tipo_reporte == "Resumen Financiero":
        st.subheader("💰 Resumen Financiero General")
        
        col1, col2 = st.columns(2)
        with col1:
            fecha_inicio = st.date_input("Desde", key="resumen_inicio")
        with col2:
            fecha_fin = st.date_input("Hasta", key="resumen_fin")
        
        if st.button("Generar Resumen"):
            # Ingresos
            pagos = db.get_pagos_filtrados(fecha_inicio.strftime('%Y-%m-%d'),
                                          fecha_fin.strftime('%Y-%m-%d'), None)
            total_ingresos = sum([p[4] for p in pagos]) if pagos else 0
            
            # Gastos
            gastos = db.get_gastos_filtrados(fecha_inicio.strftime('%Y-%m-%d'),
                                            fecha_fin.strftime('%Y-%m-%d'))
            total_gastos = sum([g[3] for g in gastos]) if gastos else 0
            
            # Balance
            balance = total_ingresos - total_gastos
            
            # Métricas
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("💰 Total Ingresos", f"${total_ingresos:,.2f}")
            with col2:
                st.metric("💸 Total Gastos", f"${total_gastos:,.2f}")
            with col3:
                st.metric("📊 Balance", f"${balance:,.2f}",
                         delta=f"{'Positivo' if balance > 0 else 'Negativo'}")
            
            st.markdown("---")
            
            # Gráfico
            if pagos or gastos:
                fig = go.Figure()
                fig.add_trace(go.Bar(x=['Ingresos', 'Gastos'], 
                                   y=[total_ingresos, total_gastos],
                                   marker_color=['green', 'red']))
                fig.update_layout(title="Ingresos vs Gastos", 
                                yaxis_title="Monto (MXN)")
                st.plotly_chart(fig, use_container_width=True)
            
            # Detalles
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("💰 Detalle de Ingresos")
                if pagos:
                    # Agrupar por diplomado
                    ingresos_dip = {}
                    for p in pagos:
                        dip = p[2]
                        if dip not in ingresos_dip:
                            ingresos_dip[dip] = 0
                        ingresos_dip[dip] += p[4]
                    
                    for dip, monto in ingresos_dip.items():
                        st.write(f"**{dip}:** ${monto:,.2f}")
                else:
                    st.info("Sin ingresos en el periodo")
            
            with col2:
                st.subheader("💸 Detalle de Gastos")
                if gastos:
                    for g in gastos:
                        st.write(f"**{g[2]}:** ${g[3]:,.2f} ({g[1]})")
                else:
                    st.info("Sin gastos en el periodo")

# Footer
st.sidebar.markdown("---")