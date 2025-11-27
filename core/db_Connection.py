# db_connection.py
import os
import pyodbc
from contextlib import contextmanager
from typing import Iterator
import sys

# Aadir el directorio padre al path para importar logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger import setup_logger

# Configurar logger especfico para este mdulo
logger = setup_logger("DBConnection")

@contextmanager
def get_db_connection() -> Iterator[pyodbc.Connection]:
    """
    Lee la configuracin de conexin desde variables de entorno
    ( defaults) y abre/ciERRA la conexin automticamente.
    """
    server = os.getenv('DB_SERVER', '10.155.1.15')
    database = os.getenv('DB_NAME', 'ROCKET_PRIME')
    user = os.getenv('DB_USER', 'Dev_JuanR')
    
    logger.debug(f" Configurando conexin a BD: {server}/{database} con usuario: {user}")
    
    conn_str = (
        f"DRIVER={{SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={os.getenv('DB_PASSWORD', '+d3Ve10w4-867d*')};"
        f"TrustServerCertificate=yes;"
    )
    
    conn = None
    try:
        logger.debug(" Estableciendo conexin a la base de datos")
        conn = pyodbc.connect(conn_str)
        logger.debug(" Conexin a base de datos establecida exitosamente")
        yield conn
    except Exception as e:
        logger.error(f" Error al conectar a la base de datos: {e}")
        raise
    finally:
        if conn is not None:
            logger.debug(" Cerrando conexin a la base de datos")
            conn.close()
