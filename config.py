# Configuración de la base de datos MySQL

# Para desarrollo local, usa MySQL local
# Para producción (Streamlit Cloud), usa MySQL remoto
import os

# Detectar entorno: Streamlit Cloud tiene estas variables
IS_PRODUCTION = (
    os.getenv('STREAMLIT_SHARING_MODE') is not None or
    os.getenv('STREAMLIT_SERVER_HEADLESS') == 'true'
)

# DESACTIVA ESTO PARA DESARROLLO LOCAL SIN MYSQL
FORCE_PRODUCTION = True  # Cambia a False si instalas MySQL local

if IS_PRODUCTION or FORCE_PRODUCTION:
    # MySQL Remoto (Streamlit Cloud)
    MYSQL_CONFIG = {
        'host': 'intra.org.mx',
        'user': 'u530819723_raulacademiapp',
        'password': '2!fkYgD&',
        'database': 'u530819723_Academiapp'
    }
else:
    # MySQL Local (Desarrollo)
    MYSQL_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'academiapp'
    }
