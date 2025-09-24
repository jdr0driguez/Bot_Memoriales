# repository.py
from typing import Optional, Tuple
from pyodbc import Connection
import sys
import os

# Aadir el directorio padre al path para importar logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger import setup_logger

# Configurar logger especfico para este mdulo
logger = setup_logger("Repository")

def fetch_campos_especificos(
    conn: Connection, 
    expediente: str
) -> Optional[Tuple[int, str, float]]:
    """
    Recupera los valores de columnaX, columnaY y columnaZ para un expediente dado.
    Devuelve (valorX, valorY, valorZ) o None si no existe el expediente.
    Ajusta los tipos de retorno segn el esquema real.
    """
    logger.debug(f"Consultando campos especficos para expediente: {expediente}")
    
    sql = """
    SELECT TOP (1)
    [DEMANDADO1_NOMBRE],
    [DEMANDADO1_DOCUMENTO],
    [DEMANDADO2_NOMBRE],
    [DEMANDADO2_DOCUMENTO],
    [DEMANDADO3_NOMBRE],
    [DEMANDADO3_DOCUMENTO],
    [DEMANDADO4_NOMBRE],
    [DEMANDADO4_DOCUMENTO],
    [RADICADO_LARGO]
  FROM [ROCKET_PRIME].[dbo].[INFORME_JURIDICO]
 WHERE ID_EXPEDIENTE = ?
"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql, expediente)
        row = cursor.fetchone()
        
        if not row:
            logger.warning(f"No se encontraron datos para expediente: {expediente}")
            return None

        # Puedes acceder por ndice o por nombre si lo prefieres:
        nomDemandado1 = row[0]           
        docDemandado1 = row[1]           
        nomDemandado2 = row[2]           
        docDemandado2 = row[3]
        nomDemandado3 = row[4]           
        docDemandado3 = row[5]
        nomDemandado4 = row[6]          
        docDemandado4 = row[7]
        numRadicadoLargo = row[8] 
        
        logger.debug(f"Datos recuperados para expediente {expediente}: Demandado1={nomDemandado1}, Doc={docDemandado1}")
        return nomDemandado1, docDemandado1, nomDemandado2, docDemandado2, nomDemandado3, docDemandado3, nomDemandado4, docDemandado4, numRadicadoLargo
        
    except Exception as e:
        logger.error(f"Error consultando campos especficos para expediente {expediente}: {e}")
        return None

def fetch_correo_juzgado(
    conn: Connection, 
    expediente: str
) -> Optional[Tuple[int, str, float]]:
    """
    Recupera los valores de columnaX, columnaY y columnaZ para un expediente dado.
    Devuelve (valorX, valorY, valorZ) o None si no existe el expediente.
    Ajusta los tipos de retorno segn el esquema real.
    """
    logger.debug(f" Consultando correo del juzgado para expediente: {expediente}")
    
    sql = """
    SELECT TOP (1) APLI_JUZGADOS.correoElectronico
    FROM   APLI_JUZGADOS INNER JOIN
             APLI_JUZGADO_EXPEDIENTES ON APLI_JUZGADOS.idJuzgado = APLI_JUZGADO_EXPEDIENTES.juzgadoId
    WHERE APLI_JUZGADO_EXPEDIENTES.expedienteId = ?
"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql, expediente)
        row = cursor.fetchone()
        
        if not row:
            logger.warning(f" No se encontr correo del juzgado para expediente: {expediente}")
            return None

        # Puedes acceder por ndice o por nombre si lo prefieres:
        correoJuzgado = row[0]                   
        logger.debug(f" Correo del juzgado encontrado para expediente {expediente}: {correoJuzgado}")
        return correoJuzgado
        
    except Exception as e:
        logger.error(f" Error consultando correo del juzgado para expediente {expediente}: {e}")
        return None

def fetch_campos_idDemandado(
    conn: Connection, 
    idDemandado: str
) -> Optional[Tuple[int, str, float]]:
    """
    Recupera los valores de columnaX, columnaY y columnaZ para un expediente dado.
    Devuelve (valorX, valorY, valorZ) o None si no existe el expediente.
    Ajusta los tipos de retorno segn el esquema real.
    """
    logger.debug(f" Consultando IdDemandado para documento: {idDemandado}")
    
    sql = """
    SELECT TOP (1) [idDemandado]
  FROM [ROCKET_PRIME].[dbo].[APLI_DEMANDADOS]
  WHERE numeroDocumentoDemandado = ? ;
"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql, idDemandado)
        row = cursor.fetchone()
        
        if not row:
            logger.warning(f" No se encontr IdDemandado para documento: {idDemandado}")
            return None

        # Puedes acceder por ndice o por nombre si lo prefieres:
        DemandadoId = row[0]                   
        logger.debug(f" IdDemandado encontrado para documento {idDemandado}: {DemandadoId}")
        return DemandadoId
        
    except Exception as e:
        logger.error(f" Error consultando IdDemandado para documento {idDemandado}: {e}")
        return None

def fetch_nombre_plantilla(
    conn: Connection, 
    IdPlantilla: str
) -> Optional[Tuple[int, str, float]]:
    """
    Recupera los valores de columnaX, columnaY y columnaZ para un expediente dado.
    Devuelve (valorX, valorY, valorZ) o None si no existe el expediente.
    Ajusta los tipos de retorno segn el esquema real.
    """
    logger.debug(f" Consultando nombre de plantilla para ID: {IdPlantilla}")
    
    sql = """
    SELECT TOP (1) [nombrePlantilla]
    FROM [ROCKET_PRIME].[dbo].[BOFF_DOC_PLANTILLAS]
    WHERE idPlantilla = ?;
"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql, IdPlantilla)
        row = cursor.fetchone()
        
        if not row:
            logger.warning(f" No se encontr nombre de plantilla para ID: {IdPlantilla}")
            return None

        # Puedes acceder por ndice o por nombre si lo prefieres:
        nomPlantilla = row[0]           
        logger.debug(f" Nombre de plantilla encontrado para ID {IdPlantilla}: {nomPlantilla}")
        return nomPlantilla
        
    except Exception as e:
        logger.error(f" Error consultando nombre de plantilla para ID {IdPlantilla}: {e}")
        return None

def fetch_plantilla_correo(
    conn: Connection, 
    idPlantilla: str,
    idExpediente: str
) -> Optional[Tuple[int, str, float]]:
    """
    Recupera los valores de columnaX, columnaY y columnaZ para un expediente dado.
    Devuelve (valorX, valorY, valorZ) o None si no existe el expediente.
    Ajusta los tipos de retorno segn el esquema real.
    """
    logger.debug(f" Consultando correo de plantilla para ID de plantilla: {idPlantilla} y expediente: {idExpediente}")
    
    sql = """
    SELECT TOP (1) [correoPlantilla]
    FROM [ROCKET_PRIME].[dbo].[APLI_EXPEDIENTES_PLANTILLA]
    WHERE plantillaId = ? AND expedienteId = ?
"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql, idPlantilla, idExpediente)
        row = cursor.fetchone()
        
        if not row:
            logger.warning(f" No se encontr correo de plantilla para ID de plantilla: {idPlantilla} y expediente: {idExpediente}")
            return None

        # Puedes acceder por ndice o por nombre si lo prefieres:
        plantillaCorreo = row[0]                   
        logger.debug(f" Correo de plantilla encontrado para ID de plantilla {idPlantilla} y expediente {idExpediente}")
        return plantillaCorreo
        
    except Exception as e:
        logger.error(f" Error consultando correo de plantilla para ID de plantilla {idPlantilla} y expediente {idExpediente}: {e}")
        return None

def fetch_idDemandado(
        conn: Connection, 
        idPlantilla: str, 
        idExpediente: str) -> Optional[int]:
    """
    Recupera los valores de columnaX, columnaY y columnaZ para un expediente dado.
    Devuelve (valorX, valorY, valorZ) o None si no existe el expediente.
    Ajusta los tipos de retorno segn el esquema real.
    """
    logger.debug(f" Consultando idDemandado para ID de plantilla: {idPlantilla} y expediente: {idExpediente}")
    
    sql = """
    SELECT TOP (1) [demandadoId]
    FROM [ROCKET_PRIME].[dbo].[APLI_EXP_DOCUMENTOS]
    WHERE expedienteId = ? and plantillaId = ? and tipoExpDocumentoId = 1;
"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (idExpediente, idPlantilla))
        row = cursor.fetchone()
        
        if not row:
            logger.warning(f" No se encontro idDemandado para ID de plantilla: {idPlantilla} y expediente: {idExpediente}")
            return None

        # Puedes acceder por ndice o por nombre si lo prefieres:
        idDemandado = row[0]                   
        logger.debug(f" idDemandado de plantilla encontrado para ID de plantilla {idPlantilla} y expediente {idExpediente}: {idDemandado}")
        return idDemandado
        
    except Exception as e:
        logger.error(f" Error consultando idDemandado de plantilla para ID de plantilla {idPlantilla} y expediente {idExpediente}: {e}")
        return None

def fetch_nomDocumento(
        conn: Connection, 
        idPlantilla: str, 
        idExpediente: str) -> Optional[int]:
    """
    Recupera el valor del nombre del documento a descargar
    """
    logger.debug(f" Consultando nomDocumentoAdjunto para ID de plantilla: {idPlantilla} y expediente: {idExpediente}")
    
    sql = """
    select top (1) nombreDocAdjunto from APLI_EXP_DOCUMENTOS
    where expedienteId = ? AND plantillaId = ?;
"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (idExpediente, idPlantilla))
        row = cursor.fetchone()
        
        if not row:
            logger.warning(f" No se encontro nomDocumentoAdjunto para ID de plantilla: {idPlantilla} y expediente: {idExpediente}")
            return None

        # Puedes acceder por ndice o por nombre si lo prefieres:
        nomDocAdjunto = row[0]                   
        logger.debug(f" nomDocumentoAdjunto de plantilla encontrado para ID de plantilla {idPlantilla} y expediente {idExpediente}: {nomDocAdjunto}")
        return nomDocAdjunto
        
    except Exception as e:
        logger.error(f" Error consultando nomDocumentoAdjunto de plantilla para ID de plantilla {idPlantilla} y expediente {idExpediente}: {e}")
        return None

def fetch_tipoPlantilla(
        conn: Connection, 
        idPlantilla: str,
        idExpediente: str ) -> Optional[int]:
    """
    Obtiene el ID del tipo de plantilla, correo o formato
    """
    logger.debug(f" Consultando TipoPlantilla para ID de plantilla: {idPlantilla} y expediente: {idExpediente}")
    
    sql = """
    SELECT TOP (1) [tipoPlantillaId]
    FROM BOFF_DOC_PLANTILLAS
    WHERE idPlantilla = ?;
"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (idPlantilla))
        row = cursor.fetchone()
        
        if not row:
            logger.warning(f" No se encontro TipoPlantilla para ID de plantilla: {idPlantilla} y expediente: {idExpediente}")
            return None

        # Puedes acceder por ndice o por nombre si lo prefieres:
        idTipoPlantilla = row[0]                   
        logger.debug(f" TipoPlantilla de plantilla encontrado para ID de plantilla {idPlantilla} y expediente {idExpediente}: {idTipoPlantilla}")
        return idTipoPlantilla
        
    except Exception as e:
        logger.error(f" Error consultando TipoPlantilla de plantilla para ID de plantilla {idPlantilla} y expediente {idExpediente}: {e}")
        return None
