import mysql.connector

# Prueba de conexión
try:
    conn = mysql.connector.connect(
        host='intra.org.mx',
        user='u530819723_raulacademiapp',
        password='2!fkYgD&',
        database='u530819723_Academiapp'
    )
    
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    print("✅ Conexión exitosa a MySQL!")
    print(f"\nTablas encontradas: {len(tables)}")
    for table in tables:
        print(f"  - {table[0]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error de conexión: {e}")
