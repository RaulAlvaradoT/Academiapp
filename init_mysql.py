import mysql.connector
from config import MYSQL_CONFIG

print("🔧 Inicializando base de datos MySQL...")

try:
    # Conectar a MySQL
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()
    
    print("✅ Conexión exitosa a MySQL")
    
    # Crear tabla diplomados
    print("\n📚 Creando tabla diplomados...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diplomados (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            clave VARCHAR(50) UNIQUE NOT NULL,
            modalidad VARCHAR(50) NOT NULL,
            fecha_inicio DATE NOT NULL,
            fecha_fin DATE NOT NULL,
            num_mensualidades INT NOT NULL,
            alumnos_inscritos INT DEFAULT 0,
            status VARCHAR(50) DEFAULT 'Activo'
        )
    ''')
    
    # Crear tabla alumnos
    print("👥 Creando tabla alumnos...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alumnos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            matricula VARCHAR(50) NOT NULL,
            nombre_completo VARCHAR(255) NOT NULL,
            status VARCHAR(50) NOT NULL,
            diplomado_id INT,
            diplomado_clave VARCHAR(50) NOT NULL,
            telefono VARCHAR(50) NOT NULL,
            correo VARCHAR(255) NOT NULL,
            fecha_inscripcion DATE NOT NULL,
            pago_inscripcion DECIMAL(10,2) NOT NULL,
            mensualidad DECIMAL(10,2) NOT NULL,
            num_mensualidades INT NOT NULL,
            total_diplomado DECIMAL(10,2) NOT NULL,
            curp VARCHAR(50) NOT NULL,
            fecha_baja DATE,
            motivo_baja TEXT,
            FOREIGN KEY (diplomado_id) REFERENCES diplomados(id)
        )
    ''')
    
    # Crear tabla pagos
    print("💰 Creando tabla pagos...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pagos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            alumno_id INT NOT NULL,
            num_mensualidad INT NOT NULL,
            monto DECIMAL(10,2) NOT NULL,
            fecha_pago DATE NOT NULL,
            metodo_pago VARCHAR(50) NOT NULL,
            FOREIGN KEY (alumno_id) REFERENCES alumnos(id)
        )
    ''')
    
    # Crear tabla gastos
    print("💸 Creando tabla gastos...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fecha DATE NOT NULL,
            concepto VARCHAR(255) NOT NULL,
            monto DECIMAL(10,2) NOT NULL
        )
    ''')
    
    # Crear tabla calendario
    print("📅 Creando tabla calendario...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calendario (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fecha DATE NOT NULL,
            diplomado_clave VARCHAR(50) NOT NULL,
            tipo VARCHAR(50) NOT NULL,
            modulo INT NOT NULL,
            FOREIGN KEY (diplomado_clave) REFERENCES diplomados(clave)
        )
    ''')
    
    conn.commit()
    
    # Verificar tablas creadas
    print("\n✅ Tablas creadas exitosamente:")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    for table in tables:
        print(f"  ✓ {table[0]}")
    
    cursor.close()
    conn.close()
    
    print("\n🎉 Base de datos MySQL inicializada correctamente!")
    print("\n💡 Ahora puedes:")
    print("  1. Cambiar USE_MYSQL = True en config.py")
    print("  2. Ejecutar la app con: py -m streamlit run app.py")
    print("  3. O migrar datos desde SQLite con: py migrate_to_mysql.py")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n⚠️  Verifica:")
    print("  - Que las credenciales en config.py sean correctas")
    print("  - Que el servidor MySQL esté accesible desde tu red")
