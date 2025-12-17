import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional

class DatabaseManager:
    def __init__(self, db_name='academiapp.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Crear conexión a la base de datos"""
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        """Inicializar todas las tablas de la base de datos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de Diplomados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS diplomados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                clave TEXT UNIQUE NOT NULL,
                modalidad TEXT NOT NULL,
                fecha_inicio TEXT NOT NULL,
                fecha_fin TEXT NOT NULL,
                num_mensualidades INTEGER NOT NULL,
                alumnos_inscritos INTEGER DEFAULT 0
            )
        ''')
        
        # Tabla de Alumnos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alumnos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricula TEXT NOT NULL,
                nombre_completo TEXT NOT NULL,
                status TEXT NOT NULL,
                diplomado_id INTEGER,
                diplomado_clave TEXT NOT NULL,
                telefono TEXT NOT NULL,
                correo TEXT NOT NULL,
                fecha_inscripcion TEXT NOT NULL,
                pago_inscripcion REAL NOT NULL,
                mensualidad REAL NOT NULL,
                num_mensualidades INTEGER NOT NULL,
                total_diplomado REAL NOT NULL,
                curp TEXT NOT NULL,
                FOREIGN KEY (diplomado_id) REFERENCES diplomados(id)
            )
        ''')
        
        # Tabla de Pagos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pagos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alumno_id INTEGER NOT NULL,
                num_mensualidad INTEGER NOT NULL,
                monto REAL NOT NULL,
                fecha_pago TEXT NOT NULL,
                metodo_pago TEXT NOT NULL,
                FOREIGN KEY (alumno_id) REFERENCES alumnos(id)
            )
        ''')
        
        # Tabla de Gastos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gastos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                concepto TEXT NOT NULL,
                monto REAL NOT NULL
            )
        ''')
        
        conn.commit()
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
            cursor.execute('''
                INSERT INTO diplomados (nombre, clave, modalidad, fecha_inicio, fecha_fin, num_mensualidades)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nombre, clave, modalidad, fecha_inicio, fecha_fin, num_mensualidades))
            conn.commit()
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
        conn.close()
        return diplomados
    
    def update_diplomado(self, id: int, nombre: str, clave: str, modalidad: str,
                        fecha_inicio: str, fecha_fin: str, num_mensualidades: int) -> bool:
        """Actualizar un diplomado"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE diplomados 
                SET nombre=?, clave=?, modalidad=?, fecha_inicio=?, fecha_fin=?, num_mensualidades=?
                WHERE id=?
            ''', (nombre, clave, modalidad, fecha_inicio, fecha_fin, num_mensualidades, id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al actualizar diplomado: {e}")
            return False
    
    def delete_diplomado(self, id: int) -> bool:
        """Eliminar un diplomado (solo si no tiene alumnos)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Verificar si tiene alumnos
            cursor.execute('SELECT COUNT(*) FROM alumnos WHERE diplomado_id=?', (id,))
            count = cursor.fetchone()[0]
            
            if count > 0:
                conn.close()
                return False
            
            cursor.execute('DELETE FROM diplomados WHERE id=?', (id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al eliminar diplomado: {e}")
            return False
    
    def update_alumnos_inscritos(self, diplomado_id: int):
        """Actualizar el contador de alumnos inscritos en un diplomado"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE diplomados 
            SET alumnos_inscritos = (
                SELECT COUNT(*) FROM alumnos WHERE diplomado_id=?
            )
            WHERE id=?
        ''', (diplomado_id, diplomado_id))
        conn.commit()
        conn.close()
    
    # ========================================================================
    # FUNCIONES PARA ALUMNOS
    # ========================================================================
    
    def add_alumno(self, matricula: str, nombre_completo: str, status: str,
                  diplomado_clave: str, telefono: str, correo: str, fecha_inscripcion: str,
                  pago_inscripcion: float, mensualidad: float, num_mensualidades: int,
                  total_diplomado: float, curp: str) -> bool:
        """Agregar un nuevo alumno"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Obtener el ID del diplomado por su clave
            cursor.execute('SELECT id FROM diplomados WHERE clave=?', (diplomado_clave,))
            diplomado_id = cursor.fetchone()
            
            if not diplomado_id:
                conn.close()
                return False
            
            cursor.execute('''
                INSERT INTO alumnos (matricula, nombre_completo, status, diplomado_id, diplomado_clave,
                                   telefono, correo, fecha_inscripcion, pago_inscripcion, mensualidad,
                                   num_mensualidades, total_diplomado, curp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (matricula, nombre_completo, status, diplomado_id[0], diplomado_clave, telefono, correo,
                 fecha_inscripcion, pago_inscripcion, mensualidad, num_mensualidades, total_diplomado, curp))
            conn.commit()
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
        
        query = 'SELECT * FROM alumnos WHERE 1=1'
        params = []
        
        if nombre:
            query += ' AND nombre_completo LIKE ?'
            params.append(f'%{nombre}%')
        
        if matricula:
            query += ' AND matricula LIKE ?'
            params.append(f'%{matricula}%')
        
        if diplomado and diplomado != "Todos":
            # Extraer la clave entre paréntesis
            clave = diplomado.split('(')[1].strip(')')
            query += ' AND diplomado_clave=?'
            params.append(clave)
        
        query += ' ORDER BY nombre_completo'
        
        cursor.execute(query, params)
        alumnos = cursor.fetchall()
        conn.close()
        return alumnos
    
    def get_alumno_por_matricula(self, matricula: str) -> Optional[Tuple]:
        """Obtener un alumno por su matrícula"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM alumnos WHERE matricula=?', (matricula,))
        alumno = cursor.fetchone()
        conn.close()
        return alumno
    
    def update_alumno(self, id: int, matricula: str, nombre: str, status: str,
                     diplomado_clave: str, telefono: str, correo: str,
                     fecha_inscripcion: str, pago_inscripcion: float,
                     mensualidad: float, curp: str) -> bool:
        """Actualizar un alumno"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Obtener el ID del diplomado
            cursor.execute('SELECT id FROM diplomados WHERE clave=?', (diplomado_clave,))
            diplomado_id = cursor.fetchone()
            
            if not diplomado_id:
                conn.close()
                return False
            
            cursor.execute('''
                UPDATE alumnos 
                SET matricula=?, nombre_completo=?, status=?, diplomado_id=?, diplomado_clave=?,
                    telefono=?, correo=?, fecha_inscripcion=?, pago_inscripcion=?, mensualidad=?, curp=?
                WHERE id=?
            ''', (matricula, nombre, status, diplomado_id[0], diplomado_clave, telefono, correo,
                 fecha_inscripcion, pago_inscripcion, mensualidad, curp, id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al actualizar alumno: {e}")
            return False
    
    def delete_alumno(self, id: int) -> bool:
        """Eliminar un alumno"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Primero eliminar sus pagos
            cursor.execute('DELETE FROM pagos WHERE alumno_id=?', (id,))
            
            # Luego eliminar el alumno
            cursor.execute('DELETE FROM alumnos WHERE id=?', (id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al eliminar alumno: {e}")
            return False
    
    def get_alumnos_por_diplomado_clave(self, clave: str) -> List[Tuple]:
        """Obtener todos los alumnos de un diplomado específico"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, matricula, nombre_completo, mensualidad 
            FROM alumnos 
            WHERE diplomado_clave=? AND status='Activo'
            ORDER BY nombre_completo
        ''', (clave,))
        alumnos = cursor.fetchall()
        conn.close()
        return alumnos
    
    # ========================================================================
    # FUNCIONES PARA PAGOS
    # ========================================================================
    
    def add_pago(self, alumno_id: int, num_mensualidad: int, monto: float,
                fecha_pago: str, metodo_pago: str) -> bool:
        """Registrar un nuevo pago"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO pagos (alumno_id, num_mensualidad, monto, fecha_pago, metodo_pago)
                VALUES (?, ?, ?, ?, ?)
            ''', (alumno_id, num_mensualidad, monto, fecha_pago, metodo_pago))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al registrar pago: {e}")
            return False
    
    def verificar_pago_mensualidad(self, alumno_id: int, num_mensualidad: int) -> bool:
        """Verificar si un alumno ya pagó una mensualidad específica"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM pagos 
            WHERE alumno_id=? AND num_mensualidad=?
        ''', (alumno_id, num_mensualidad))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    
    def get_detalle_pago(self, alumno_id: int, num_mensualidad: int) -> Optional[Tuple]:
        """Obtener detalles de un pago específico"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT monto, fecha_pago, metodo_pago 
            FROM pagos 
            WHERE alumno_id=? AND num_mensualidad=?
        ''', (alumno_id, num_mensualidad))
        pago = cursor.fetchone()
        conn.close()
        return pago
    
    def get_pagos_alumno(self, alumno_id: int) -> List[Tuple]:
        """Obtener todos los pagos de un alumno"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT num_mensualidad, monto, fecha_pago, metodo_pago 
            FROM pagos 
            WHERE alumno_id=?
            ORDER BY num_mensualidad
        ''', (alumno_id,))
        pagos = cursor.fetchall()
        conn.close()
        return pagos
    
    def get_pagos_filtrados(self, fecha_inicio: str, fecha_fin: str, 
                           diplomado_clave: str = None) -> List[Tuple]:
        """Obtener pagos con filtros de fecha y diplomado"""
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
        conn.close()
        return pagos
    
    def get_reporte_pagos_diplomado(self, diplomado_clave: str, fecha_inicio: str, 
                                   fecha_fin: str) -> List[Tuple]:
        """Obtener reporte de pagos por diplomado"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.matricula, a.nombre_completo, p.num_mensualidad, p.monto, 
                   p.fecha_pago, p.metodo_pago
            FROM pagos p
            JOIN alumnos a ON p.alumno_id = a.id
            WHERE a.diplomado_clave=? AND p.fecha_pago BETWEEN ? AND ?
            ORDER BY a.nombre_completo, p.num_mensualidad
        ''', (diplomado_clave, fecha_inicio, fecha_fin))
        pagos = cursor.fetchall()
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
            cursor.execute('''
                INSERT INTO gastos (fecha, concepto, monto)
                VALUES (?, ?, ?)
            ''', (fecha, concepto, monto))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al registrar gasto: {e}")
            return False
    
    def get_gastos_filtrados(self, fecha_inicio: str, fecha_fin: str) -> List[Tuple]:
        """Obtener gastos filtrados por fecha"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM gastos 
            WHERE fecha BETWEEN ? AND ?
            ORDER BY fecha DESC
        ''', (fecha_inicio, fecha_fin))
        gastos = cursor.fetchall()
        conn.close()
        return gastos
    
    def delete_gasto(self, id: int) -> bool:
        """Eliminar un gasto"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM gastos WHERE id=?', (id,))
            conn.commit()
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
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM alumnos')
        total = cursor.fetchone()[0]
        conn.close()
        return total
    
    def get_alumnos_activos(self) -> int:
        """Obtener total de alumnos activos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM alumnos WHERE status='Activo'")
        total = cursor.fetchone()[0]
        conn.close()
        return total
    
    def get_total_diplomados(self) -> int:
        """Obtener total de diplomados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM diplomados')
        total = cursor.fetchone()[0]
        conn.close()
        return total
    
    def get_ingresos_mes_actual(self) -> float:
        """Obtener ingresos del mes actual"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        fecha_actual = datetime.now()
        primer_dia = fecha_actual.replace(day=1).strftime('%Y-%m-%d')
        ultimo_dia = fecha_actual.strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT COALESCE(SUM(monto), 0) FROM pagos 
            WHERE fecha_pago BETWEEN ? AND ?
        ''', (primer_dia, ultimo_dia))
        total = cursor.fetchone()[0]
        conn.close()
        return total
    
    def get_gastos_mes_actual(self) -> float:
        """Obtener gastos del mes actual"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        fecha_actual = datetime.now()
        primer_dia = fecha_actual.replace(day=1).strftime('%Y-%m-%d')
        ultimo_dia = fecha_actual.strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT COALESCE(SUM(monto), 0) FROM gastos 
            WHERE fecha BETWEEN ? AND ?
        ''', (primer_dia, ultimo_dia))
        total = cursor.fetchone()[0]
        conn.close()
        return total
    
    def get_alumnos_por_diplomado(self) -> List[Tuple]:
        """Obtener conteo de alumnos por diplomado"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT diplomado_clave, COUNT(*) 
            FROM alumnos 
            WHERE status='Activo'
            GROUP BY diplomado_clave
        ''')
        datos = cursor.fetchall()
        conn.close()
        return datos
    
    def get_ingresos_gastos_6_meses(self) -> List[Tuple]:
        """Obtener ingresos y gastos de los últimos 6 meses"""
        from datetime import timedelta
        
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
            cursor.execute('''
                SELECT COALESCE(SUM(monto), 0) FROM pagos 
                WHERE fecha_pago BETWEEN ? AND ?
            ''', (primer_dia, ultimo_dia))
            ingresos = cursor.fetchone()[0]
            
            # Obtener gastos
            cursor.execute('''
                SELECT COALESCE(SUM(monto), 0) FROM gastos 
                WHERE fecha BETWEEN ? AND ?
            ''', (primer_dia, ultimo_dia))
            gastos = cursor.fetchone()[0]
            
            # Nombre del mes
            nombres_meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                           'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
            nombre_mes = nombres_meses[mes - 1]
            
            meses.append((nombre_mes, ingresos, gastos))
        
        conn.close()
        return meses
    
    def get_alumnos_con_adeudos(self) -> List[Tuple]:
        """Obtener alumnos que tienen adeudos"""
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
        conn.close()
        return alumnos
