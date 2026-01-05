import streamlit as st
import pymysql
from datetime import datetime
from typing import List, Tuple, Optional

class DatabaseManager:
    def __init__(self):
        # Obtener configuración desde secrets
        secrets = st.secrets["connections"]["mysql"]
        self.config = {
            'host': secrets['host'],
            'port': secrets['port'],
            'user': secrets['username'],
            'password': secrets['password'],
            'database': secrets['database']
        }
        self.init_database()
    
    def get_connection(self):
        """Crear conexión PyMySQL directa"""
        return pymysql.connect(**self.config)
    
    def get_placeholder(self):
        """Retorna el placeholder para MySQL"""
        return '%s'
    
    def init_database(self):
        """Inicializar todas las tablas de la base de datos MySQL"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tipos de datos MySQL
        pk = "INT AUTO_INCREMENT PRIMARY KEY"
        integer = "INT"
        real = "DECIMAL(10,2)"
        text_type = "TEXT"
        varchar_50 = "VARCHAR(50)"
        varchar_255 = "VARCHAR(255)"
        date_type = "DATE"
        
        # Tabla de Diplomados
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS diplomados (
                id {pk},
                nombre {varchar_255} NOT NULL,
                clave {varchar_50} UNIQUE NOT NULL,
                modalidad {varchar_50} NOT NULL,
                fecha_inicio {date_type} NOT NULL,
                fecha_fin {date_type} NOT NULL,
                num_mensualidades {integer} NOT NULL,
                alumnos_inscritos {integer} DEFAULT 0,
                status {varchar_50} DEFAULT 'Activo'
            )
        ''')
        
        # Agregar columna status si no existe
        try:
            cursor.execute(f"ALTER TABLE diplomados ADD COLUMN status VARCHAR(20) DEFAULT 'Activo'")
            conn.commit()
        except:
            pass
        
        # Tabla de Alumnos
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS alumnos (
                id {pk},
                matricula {varchar_50} NOT NULL,
                nombre_completo {varchar_255} NOT NULL,
                status {varchar_50} NOT NULL,
                diplomado_id {integer},
                diplomado_clave {varchar_50} NOT NULL,
                telefono {varchar_50} NOT NULL,
                correo {varchar_255} NOT NULL,
                fecha_inscripcion {date_type} NOT NULL,
                pago_inscripcion {real} NOT NULL,
                mensualidad {real} NOT NULL,
                num_mensualidades {integer} NOT NULL,
                total_diplomado {real} NOT NULL,
                fecha_baja {date_type},
                motivo_baja {text_type},
                FOREIGN KEY (diplomado_id) REFERENCES diplomados(id)
            )
        ''')
        
        # Agregar columnas si no existen
        try:
            cursor.execute(f"ALTER TABLE alumnos ADD COLUMN fecha_baja {date_type}")
            conn.commit()
        except:
            pass
        try:
            cursor.execute(f"ALTER TABLE alumnos ADD COLUMN motivo_baja {text_type}")
            conn.commit()
        except:
            pass
        
        # Tabla de Pagos
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS pagos (
                id {pk},
                alumno_id {integer} NOT NULL,
                num_mensualidad {integer} NOT NULL,
                monto {real} NOT NULL,
                fecha_pago {date_type} NOT NULL,
                metodo_pago {varchar_50} NOT NULL,
                FOREIGN KEY (alumno_id) REFERENCES alumnos(id)
            )
        ''')
        
        # Tabla de Gastos
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS gastos (
                id {pk},
                fecha {date_type} NOT NULL,
                concepto {varchar_255} NOT NULL,
                monto {real} NOT NULL
            )
        ''')
        
        # Tabla de Calendario
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS calendario (
                id {pk},
                fecha {date_type} NOT NULL,
                diplomado_clave {varchar_50} NOT NULL,
                tipo {varchar_50} NOT NULL,
                modulo {integer} NOT NULL,
                FOREIGN KEY (diplomado_clave) REFERENCES diplomados(clave)
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
    
    # ========================================================================
    # FUNCIONES PARA DIPLOMADOS
    # ========================================================================
    
    def add_diplomado(self, nombre: str, clave: str, modalidad: str, 
                     fecha_inicio: str, fecha_fin: str, num_mensualidades: int) -> bool:
        """Agregar un nuevo diplomado"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            ph = self.get_placeholder()
            cursor.execute(f'''
                INSERT INTO diplomados (nombre, clave, modalidad, fecha_inicio, fecha_fin, num_mensualidades)
                VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph})
            ''', (nombre, clave, modalidad, fecha_inicio, fecha_fin, num_mensualidades))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al agregar diplomado: {e}")
            return False
    
    def get_all_diplomados(self) -> List[Tuple]:
        """Obtener todos los diplomados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM diplomados ORDER BY fecha_inicio DESC')
        diplomados = cursor.fetchall()
        cursor.close()
        conn.close()
        return diplomados
    
    def update_diplomado(self, id: int, nombre: str, clave: str, modalidad: str,
                        fecha_inicio: str, fecha_fin: str, num_mensualidades: int) -> bool:
        """Actualizar un diplomado"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            ph = self.get_placeholder()
            cursor.execute(f'''
                UPDATE diplomados 
                SET nombre={ph}, clave={ph}, modalidad={ph}, fecha_inicio={ph}, fecha_fin={ph}, num_mensualidades={ph}
                WHERE id = {ph}
            ''', (nombre, clave, modalidad, fecha_inicio, fecha_fin, num_mensualidades, id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al actualizar diplomado: {e}")
            return False
    
    def delete_diplomado(self, id: int) -> bool:
        """Eliminar un diplomado (solo si no tiene alumnos)"""
        ph = self.get_placeholder()
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Verificar si tiene alumnos
            cursor.execute(f'SELECT COUNT(*) FROM alumnos WHERE diplomado_id = {ph}', (id,))
            count = cursor.fetchone()[0]
            
            if count > 0:
                cursor.close()
                conn.close()
                return False
            
            cursor.execute(f'DELETE FROM diplomados WHERE id = {ph}', (id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al eliminar diplomado: {e}")
            return False
    
    def archivar_diplomado(self, id: int) -> bool:
        """Archivar un diplomado (cambiar status a Archivado)"""
        ph = self.get_placeholder()
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(f"UPDATE diplomados SET status='Archivado' WHERE id = {ph}", (id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al archivar diplomado: {e}")
            return False
    
    def reactivar_diplomado(self, id: int) -> bool:
        """Reactivar un diplomado archivado (cambiar status a Activo)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE diplomados SET status='Activo' WHERE id = {ph}", (id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al reactivar diplomado: {e}")
            return False
    
    def get_diplomados_filtrados(self, status: str = None) -> List[Tuple]:
        """Obtener diplomados filtrados por status"""
        ph = self.get_placeholder()
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if status:
            cursor.execute(f'SELECT * FROM diplomados WHERE status = {ph} ORDER BY fecha_inicio DESC', (status,))
        else:
            cursor.execute('SELECT * FROM diplomados ORDER BY fecha_inicio DESC')
        
        diplomados = cursor.fetchall()
        cursor.close()
        conn.close()
        return diplomados
    
    def update_alumnos_inscritos(self, diplomado_id: int):
        """Actualizar el contador de alumnos inscritos en un diplomado"""
        ph = self.get_placeholder()
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(f'''
            UPDATE diplomados 
            SET alumnos_inscritos = (
                SELECT COUNT(*) FROM alumnos WHERE diplomado_id = {ph}
            )
            WHERE id = {ph}
        ''', (diplomado_id, diplomado_id))
        conn.commit()
        cursor.close()
        conn.close()
    
    # ========================================================================
    # FUNCIONES PARA ALUMNOS
    # ========================================================================
    
    def add_alumno(self, matricula: str, nombre_completo: str, status: str,
                  diplomado_clave: str, telefono: str, correo: str, fecha_inscripcion: str,
                  pago_inscripcion: float, mensualidad: float, num_mensualidades: int,
                  total_diplomado: float) -> bool:
        """Agregar un nuevo alumno"""
        ph = self.get_placeholder()
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Obtener el ID del diplomado por su clave
            cursor.execute(f'SELECT id FROM diplomados WHERE clave = {ph}', (diplomado_clave,))
            diplomado_id = cursor.fetchone()
            
            if not diplomado_id:
                cursor.close()
                conn.close()
                return False
            
            cursor.execute(f'''
                INSERT INTO alumnos (matricula, nombre_completo, status, diplomado_id, diplomado_clave,
                                   telefono, correo, fecha_inscripcion, pago_inscripcion, mensualidad,
                                   num_mensualidades, total_diplomado)
                VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph})
            ''', (matricula, nombre_completo, status, diplomado_id[0], diplomado_clave, telefono, correo,
                 fecha_inscripcion, pago_inscripcion, mensualidad, num_mensualidades, total_diplomado))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al agregar alumno: {e}")
            return False
    
    def get_alumnos_filtrados(self, nombre: str = None, matricula: str = None, 
                             diplomado: str = None) -> List[Tuple]:
        """Obtener alumnos con filtros opcionales"""
        conn = self.get_connection()
        cursor = conn.cursor()
        ph = self.get_placeholder()
        
        query = 'SELECT * FROM alumnos WHERE 1=1'
        params = []
        
        if nombre:
            query += f' AND nombre_completo LIKE {ph}'
            params.append(f'%{nombre}%')
        
        if matricula:
            query += f' AND matricula LIKE {ph}'
            params.append(f'%{matricula}%')
        
        if diplomado and diplomado != "Todos":
            # Extraer la clave entre paréntesis
            clave = diplomado.split('(')[1].strip(')')
            query += f' AND diplomado_clave = {ph}'
            params.append(clave)
        
        query += ' ORDER BY nombre_completo'
        
        cursor.execute(query, params)
        alumnos = cursor.fetchall()
        cursor.close()
        conn.close()
        return alumnos
    
    def get_alumno_por_matricula(self, matricula: str) -> Optional[Tuple]:
        """Obtener un alumno por su matrícula"""
        ph = self.get_placeholder()
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM alumnos WHERE matricula = {ph}', (matricula,))
        alumno = cursor.fetchone()
        cursor.close()
        conn.close()
        return alumno
    
    def update_alumno(self, id: int, matricula: str, nombre: str, status: str,
                     diplomado_clave: str, telefono: str, correo: str,
                     fecha_inscripcion: str, pago_inscripcion: float,
                     mensualidad: float, fecha_baja: str = None, 
                     motivo_baja: str = None) -> bool:
        """Actualizar un alumno"""
        ph = self.get_placeholder()
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Obtener el ID del diplomado
            cursor.execute(f'SELECT id FROM diplomados WHERE clave = {ph}', (diplomado_clave,))
            diplomado_id = cursor.fetchone()
            
            if not diplomado_id:
                cursor.close()
                conn.close()
                return False
            
            cursor.execute(f'''
                UPDATE alumnos 
                SET matricula={ph}, nombre_completo={ph}, status={ph}, diplomado_id={ph}, diplomado_clave={ph},
                    telefono={ph}, correo={ph}, fecha_inscripcion={ph}, pago_inscripcion={ph}, mensualidad={ph},
                    fecha_baja={ph}, motivo_baja={ph}
                WHERE id = {ph}
            ''', (matricula, nombre, status, diplomado_id[0], diplomado_clave, telefono, correo,
                 fecha_inscripcion, pago_inscripcion, mensualidad, fecha_baja, motivo_baja, id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al actualizar alumno: {e}")
            return False
    
    def registrar_baja_alumno(self, id: int, fecha_baja: str, motivo_baja: str) -> bool:
        """Registrar la baja de un alumno con fecha y motivo"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(f'''
                UPDATE alumnos 
                SET status='Baja', fecha_baja=?, motivo_baja=?
                WHERE id = {ph}
            ''', (fecha_baja, motivo_baja, id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al registrar baja: {e}")
            return False
    
    def delete_alumno(self, id: int) -> bool:
        """Eliminar un alumno"""
        ph = self.get_placeholder()
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Primero eliminar sus pagos
            cursor.execute(f'DELETE FROM pagos WHERE alumno_id = {ph}', (id,))
            
            # Luego eliminar el alumno
            cursor.execute(f'DELETE FROM alumnos WHERE id = {ph}', (id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al eliminar alumno: {e}")
            return False
    
    def get_alumnos_por_diplomado_clave(self, clave: str) -> List[Tuple]:
        """Obtener todos los alumnos de un diplomado específico"""
        ph = self.get_placeholder()
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(f'''
            SELECT id, matricula, nombre_completo, mensualidad 
            FROM alumnos 
            WHERE diplomado_clave = {ph} AND status='Activo'
            ORDER BY nombre_completo
        ''', (clave,))
        alumnos = cursor.fetchall()
        cursor.close()
        conn.close()
        return alumnos
    
    # ========================================================================
    # FUNCIONES PARA PAGOS
    # ========================================================================
    
    def add_pago(self, alumno_id: int, num_mensualidad: int, monto: float,
                fecha_pago: str, metodo_pago: str) -> bool:
        """Registrar un nuevo pago"""
        ph = self.get_placeholder()
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(f'''
                INSERT INTO pagos (alumno_id, num_mensualidad, monto, fecha_pago, metodo_pago)
                VALUES ({ph}, {ph}, {ph}, {ph}, {ph})
            ''', (alumno_id, num_mensualidad, monto, fecha_pago, metodo_pago))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al registrar pago: {e}")
            return False
    
    def verificar_pago_mensualidad(self, alumno_id: int, num_mensualidad: int) -> bool:
        """Verificar si un alumno ya pagó una mensualidad específica"""
        ph = self.get_placeholder()
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(f'''
            SELECT COUNT(*) FROM pagos 
            WHERE alumno_id = {ph} AND num_mensualidad = {ph}
        ''', (alumno_id, num_mensualidad))
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count > 0
    
    def get_detalle_pago(self, alumno_id: int, num_mensualidad: int) -> Optional[Tuple]:
        """Obtener detalles de un pago específico"""
        ph = self.get_placeholder()
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(f'''
            SELECT monto, fecha_pago, metodo_pago 
            FROM pagos 
            WHERE alumno_id = {ph} AND num_mensualidad = {ph}
        ''', (alumno_id, num_mensualidad))
        pago = cursor.fetchone()
        cursor.close()
        conn.close()
        return pago
    
    def get_pagos_alumno(self, alumno_id: int) -> List[Tuple]:
        """Obtener todos los pagos de un alumno"""
        ph = self.get_placeholder()
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(f'''
            SELECT num_mensualidad, monto, fecha_pago, metodo_pago 
            FROM pagos 
            WHERE alumno_id = {ph}
            ORDER BY num_mensualidad
        ''', (alumno_id,))
        pagos = cursor.fetchall()
        cursor.close()
        conn.close()
        return pagos
    
    def get_pagos_filtrados(self, fecha_inicio: str, fecha_fin: str, 
                           diplomado_clave: str = None) -> List[Tuple]:
        """Obtener pagos con filtros de fecha y diplomado"""
        ph = self.get_placeholder()
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT a.matricula, a.nombre_completo, a.diplomado_clave, p.num_mensualidad,
                   p.monto, p.fecha_pago, p.metodo_pago
            FROM pagos p
            JOIN alumnos a ON p.alumno_id = a.id
            WHERE p.fecha_pago BETWEEN ? AND ?
        '''
        params = [fecha_inicio, fecha_fin]
        
        if diplomado_clave:
            query += ' AND a.diplomado_clave=?'
            params.append(diplomado_clave)
        
        query += ' ORDER BY p.fecha_pago DESC'
        
        cursor.execute(query, params)
        pagos = cursor.fetchall()
        cursor.close()
        conn.close()
        return pagos
    
    def get_reporte_pagos_diplomado(self, diplomado_clave: str, fecha_inicio: str, 
                                   fecha_fin: str) -> List[Tuple]:
        """Obtener reporte de pagos por diplomado"""
        ph = self.get_placeholder()
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(f'''
            SELECT a.matricula, a.nombre_completo, p.num_mensualidad, p.monto, 
                   p.fecha_pago, p.metodo_pago
            FROM pagos p
            JOIN alumnos a ON p.alumno_id = a.id
            WHERE a.diplomado_clave={ph} AND p.fecha_pago BETWEEN {ph} AND {ph}
            ORDER BY a.nombre_completo, p.num_mensualidad
        ''', (diplomado_clave, fecha_inicio, fecha_fin))
        pagos = cursor.fetchall()
        cursor.close()
        conn.close()
        return pagos
    
    # ========================================================================
    # FUNCIONES PARA GASTOS
    # ========================================================================
    
    def add_gasto(self, fecha: str, concepto: str, monto: float) -> bool:
        """Registrar un nuevo gasto"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(f'''
                INSERT INTO gastos (fecha, concepto, monto)
                VALUES ({ph}, {ph}, {ph})
            ''', (fecha, concepto, monto))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al registrar gasto: {e}")
            return False
    
    def get_gastos_filtrados(self, fecha_inicio: str, fecha_fin: str) -> List[Tuple]:
        """Obtener gastos filtrados por fecha"""
        ph = self.get_placeholder()
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(f'''
            SELECT * FROM gastos 
            WHERE fecha BETWEEN {ph} AND {ph}
            ORDER BY fecha DESC
        ''', (fecha_inicio, fecha_fin))
        gastos = cursor.fetchall()
        cursor.close()
        conn.close()
        return gastos
    
    def delete_gasto(self, id: int) -> bool:
        """Eliminar un gasto"""
        ph = self.get_placeholder()
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(f'DELETE FROM gastos WHERE id = {ph}', (id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al eliminar gasto: {e}")
            return False
    
    # ========================================================================
    # FUNCIONES PARA DASHBOARD Y ESTADÍSTICAS
    # ========================================================================
    
    def get_total_alumnos(self) -> int:
        """Obtener total de alumnos"""
        ph = self.get_placeholder()
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM alumnos')
        total = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return total
    
    def get_alumnos_activos(self) -> int:
        """Obtener total de alumnos activos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM alumnos WHERE status='Activo'")
        total = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return total
    
    def get_total_diplomados(self) -> int:
        """Obtener total de diplomados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM diplomados')
        total = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return total
    
    def get_ingresos_mes_actual(self) -> float:
        """Obtener ingresos del mes actual"""
        conn = self.get_connection()
        cursor = conn.cursor()
        ph = self.get_placeholder()
        
        fecha_actual = datetime.now()
        primer_dia = fecha_actual.replace(day=1).strftime('%Y-%m-%d')
        ultimo_dia = fecha_actual.strftime('%Y-%m-%d')
        
        cursor.execute(f'''
            SELECT COALESCE(SUM(monto), 0) FROM pagos 
            WHERE fecha_pago BETWEEN {ph} AND {ph}
        ''', (primer_dia, ultimo_dia))
        total = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return total
    
    def get_gastos_mes_actual(self) -> float:
        """Obtener gastos del mes actual"""
        ph = self.get_placeholder()
        conn = self.get_connection()
        cursor = conn.cursor()
        
        fecha_actual = datetime.now()
        primer_dia = fecha_actual.replace(day=1).strftime('%Y-%m-%d')
        ultimo_dia = fecha_actual.strftime('%Y-%m-%d')
        
        cursor.execute(f'''
            SELECT COALESCE(SUM(monto), 0) FROM gastos 
            WHERE fecha BETWEEN {ph} AND {ph}
        ''', (primer_dia, ultimo_dia))
        total = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return total
    
    def get_alumnos_por_diplomado(self) -> List[Tuple]:
        """Obtener conteo de alumnos por diplomado"""
        ph = self.get_placeholder()
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT diplomado_clave, COUNT(*) 
            FROM alumnos 
            WHERE status='Activo'
            GROUP BY diplomado_clave
        ''')
        datos = cursor.fetchall()
        cursor.close()
        conn.close()
        return datos
    
    def get_ingresos_gastos_6_meses(self) -> List[Tuple]:
        """Obtener ingresos y gastos de los últimos 6 meses"""
        from datetime import timedelta
        ph = self.get_placeholder()
        conn = self.get_connection()
        cursor = conn.cursor()
        
        meses = []
        fecha_actual = datetime.now()
        
        for i in range(5, -1, -1):
            # Calcular el primer día del mes
            if fecha_actual.month - i <= 0:
                mes = 12 + (fecha_actual.month - i)
                año = fecha_actual.year - 1
            else:
                mes = fecha_actual.month - i
                año = fecha_actual.year
            
            primer_dia = datetime(año, mes, 1).strftime('%Y-%m-%d')
            
            # Calcular el último día del mes
            if mes == 12:
                ultimo_dia = datetime(año, mes, 31).strftime('%Y-%m-%d')
            else:
                ultimo_dia = (datetime(año, mes + 1, 1) - timedelta(days=1)).strftime('%Y-%m-%d')
            
            # Obtener ingresos
            cursor.execute(f'''
                SELECT COALESCE(SUM(monto), 0) FROM pagos 
                WHERE fecha_pago BETWEEN {ph} AND {ph}
            ''', (primer_dia, ultimo_dia))
            ingresos = cursor.fetchone()[0]
            
            # Obtener gastos
            cursor.execute(f'''
                SELECT COALESCE(SUM(monto), 0) FROM gastos 
                WHERE fecha BETWEEN {ph} AND {ph}
            ''', (primer_dia, ultimo_dia))
            gastos = cursor.fetchone()[0]
            
            # Nombre del mes
            nombres_meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                           'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
            nombre_mes = nombres_meses[mes - 1]
            
            meses.append((nombre_mes, ingresos, gastos))
        
        cursor.close()
        conn.close()
        return meses
    
    def get_alumnos_con_adeudos(self) -> List[Tuple]:
        """Obtener alumnos que tienen adeudos"""
        ph = self.get_placeholder()
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.matricula, a.nombre_completo, a.diplomado_clave,
                   (SELECT COUNT(*) FROM pagos WHERE alumno_id = a.id) as pagadas,
                   a.num_mensualidades,
                   (a.total_diplomado - a.pago_inscripcion - 
                    COALESCE((SELECT SUM(monto) FROM pagos WHERE alumno_id = a.id), 0)) as adeudo
            FROM alumnos a
            WHERE status='Activo' 
            AND (a.total_diplomado - a.pago_inscripcion - 
                 COALESCE((SELECT SUM(monto) FROM pagos WHERE alumno_id = a.id), 0)) > 0
            ORDER BY adeudo DESC
        ''')
        
        alumnos = cursor.fetchall()
        cursor.close()
        conn.close()
        return alumnos
    
    # ========================================================================
    # FUNCIONES PARA CALENDARIO
    # ========================================================================
    
    def add_evento_calendario(self, fecha: str, diplomado_clave: str, tipo: str, modulo: int) -> bool:
        """Agregar un nuevo evento al calendario"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(f'''
                INSERT INTO calendario (fecha, diplomado_clave, tipo, modulo)
                VALUES ({ph}, {ph}, {ph}, {ph})
            ''', (fecha, diplomado_clave, tipo, modulo))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al agregar evento: {e}")
            return False
    
    def get_eventos_calendario(self, fecha_inicio: str = None, fecha_fin: str = None, 
                               diplomado_clave: str = None) -> List[Tuple]:
        """Obtener eventos del calendario con filtros opcionales"""
        ph = self.get_placeholder()
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM calendario WHERE 1=1'
        params = []
        
        if fecha_inicio and fecha_fin:
            query += ' AND fecha BETWEEN ? AND ?'
            params.extend([fecha_inicio, fecha_fin])
        
        if diplomado_clave:
            query += ' AND diplomado_clave = {ph}'
            params.append(diplomado_clave)
        
        query += ' ORDER BY fecha'
        
        cursor.execute(query, params)
        eventos = cursor.fetchall()
        cursor.close()
        conn.close()
        return eventos
    
    def get_eventos_mes(self, año: int, mes: int) -> List[Tuple]:
        """Obtener eventos de un mes específico"""
        from datetime import datetime
        primer_dia = datetime(año, mes, 1).strftime('%Y-%m-%d')
        if mes == 12:
            ultimo_dia = datetime(año, mes, 31).strftime('%Y-%m-%d')
        else:
            from datetime import timedelta
            ultimo_dia = (datetime(año, mes + 1, 1) - timedelta(days=1)).strftime('%Y-%m-%d')
        
        return self.get_eventos_calendario(primer_dia, ultimo_dia)
    
    def update_evento_calendario(self, id: int, fecha: str, diplomado_clave: str, 
                                 tipo: str, modulo: int) -> bool:
        """Actualizar un evento del calendario"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            ph = self.get_placeholder()
            cursor.execute(f'''
                UPDATE calendario 
                SET fecha={ph}, diplomado_clave={ph}, tipo={ph}, modulo={ph}
                WHERE id = {ph}
            ''', (fecha, diplomado_clave, tipo, modulo, id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al actualizar evento: {e}")
            return False
    
    def delete_evento_calendario(self, id: int) -> bool:
        """Eliminar un evento del calendario"""
        ph = self.get_placeholder()
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(f'DELETE FROM calendario WHERE id = {ph}', (id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al eliminar evento: {e}")
            return False

