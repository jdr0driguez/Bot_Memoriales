# archivo: api_modelos.py
from dataclasses import dataclass
from typing import Union
import sys
import os

# Aadir el directorio padre al path para importar logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger import setup_logger

# Configurar logger especfico para este mdulo
logger = setup_logger("APIModelos")

@dataclass
class Elemento:
    IdExpediente: int
    Expediente: str
    IdTipoProceso: int
    IdPlantilla: int
    SubEtapaInicialId: int
    CorreoRemitente: str
    CorreoCopia: str
    CorreoPass: str
    
    def __post_init__(self):
        logger.debug(f" Elemento creado: Expediente={self.Expediente}, ID={self.IdExpediente}, Tipo={self.IdTipoProceso}")


@dataclass
class ApiResponse:
    Success: bool
    CodeResult: int
    Message: str
    Element: Union[Elemento, list[Elemento]]
    
    def __post_init__(self):
        if self.Success:
            logger.debug(f" API Response exitosa: Code={self.CodeResult}, Elementos={len(self.Element) if isinstance(self.Element, list) else 1}")
        else:
            logger.warning(f" API Response con error: Code={self.CodeResult}, Mensaje={self.Message}")

@dataclass
class ResultadoTransaccion:
    expediente: str
    exito: bool
    mensaje: str
    
    def __post_init__(self):
        if self.exito:
            logger.info(f" Transaccin exitosa para expediente {self.expediente}: {self.mensaje}")
        else:
            logger.error(f" Transaccin fallida para expediente {self.expediente}: {self.mensaje}")

