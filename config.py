# Configuración de la base de datos

# Cambia esto a True para usar MySQL, False para SQLite local
USE_MYSQL = False  # SOLO cambiar a True cuando despliegues en Streamlit Cloud o servidor web

# Configuración MySQL (para producción)
MYSQL_CONFIG = {
    'host': 'intra.org.mx',
    'user': 'u530819723_raulacademiapp',
    'password': '2!fkYgD&',
    'database': 'u530819723_Academiapp'
}

# Configuración SQLite (para desarrollo local)
SQLITE_DB = 'academiapp.db'
