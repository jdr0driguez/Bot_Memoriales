import paramiko
import os
import sys

# Aadir el directorio padre al path para importar logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger import setup_logger

from config import HOST, PORT, USERNAME, PASSWORD

# Configurar logger especfico para este mdulo
logger = setup_logger("SFTPDownload")

def descargar_archivo_sftp(nombre_archivo: str) -> str:
    """
    Descarga un archivo desde el servidor SFTP, dado el nombre del archivo PDF.

    Parmetros:
        nombre_archivo (str): Nombre del archivo con extensin (ej: '29923_29052025092837.pdf')

    Retorna:
        str: Ruta local del archivo descargado si tuvo xito.
        None: Si ocurre un error o no se encuentra el archivo.
    """
    logger.info(f" Iniciando descarga SFTP del archivo: {nombre_archivo}")
    
    remote_path = f"/FilesRocket/documento-generados/{nombre_archivo}"
    local_path = os.path.join(os.getcwd(), nombre_archivo)
    
    logger.debug(f" Ruta remota: {remote_path}")
    logger.debug(f" Ruta local: {local_path}")

    try:
        logger.debug(f" Conectando al servidor SFTP: {HOST}:{PORT}")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=HOST, port=PORT, username=USERNAME, password=PASSWORD)

        logger.debug(" Conexin SSH exitosa. Estableciendo canal SFTP...")
        sftp = ssh.open_sftp()

        logger.debug(f" Verificando existencia del archivo: {remote_path}")
        sftp.stat(remote_path)

        logger.info(f" Descargando archivo a: {local_path}")
        sftp.get(remote_path, local_path)

        logger.info(" Descarga completada correctamente.")

        sftp.close()
        ssh.close()
        logger.debug(" Conexiones SFTP y SSH cerradas")

        return local_path

    except FileNotFoundError:
        logger.error(f" El archivo '{nombre_archivo}' no fue encontrado en la ubicacin remota: {remote_path}")
    except Exception as e:
        logger.error(f" Error durante la conexin o transferencia SFTP: {e}")
    
    return None
