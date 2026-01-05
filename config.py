# Configuración de la base de datos MySQL

# IMPORTANTE: Crea una base de datos MySQL gratuita con acceso remoto en:
# - FreeSQLDatabase.com (gratis, sin tarjeta)
# - Railway.app (gratis con GitHub)
# - Aiven.io (gratis 1GB)
# 
# Tu hosting actual (srv1266.hstgr.io) bloquea puerto 3306 para conexiones externas

import os

# MySQL Remoto (funciona desde cualquier lugar)
MYSQL_CONFIG = {
    'host': 'srv1266.hstgr.io',  # Intentar con DNS
    'port': 3306,
    'user': 'u530819723_raulacademiapp',
    'password': '2!fkYgD&',
    'database': 'u530819723_Academiapp',
    'connect_timeout': 30,
    'autocommit': True,
    'raise_on_warnings': False
}
