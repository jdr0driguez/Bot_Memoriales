# archivo: API_Modelos.py
from dataclasses import dataclass
from typing import Union, List
import sys
import os

# Añadir el directorio padre al path para importar logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger import setup_logger

logger = setup_logger("APIModelos")


@dataclass
class Elemento:
    ImportId: int
    Correlativo: int

    IdExpediente: int
    Expediente: str
    IdTipoProceso: int
    IdPlantilla: int
    SubEtapaInicialId: int

    CorreoRemitente: str
    CorreoCopia: str
    CorreoPass: str
    CorreoCopiaOculta: str

    def __post_init__(self):
        logger.debug(
            f"Elemento creado: ImportId={self.ImportId}, Correlativo={self.Correlativo}, "
            f"Expediente={self.Expediente}, ID={self.IdExpediente}, Tipo={self.IdTipoProceso}"
        )


@dataclass
class ApiResponse:
    Success: bool
    CodeResult: int
    Message: str
    Element: List[Elemento]

    def __post_init__(self):
        if self.Success:
            logger.debug(f"API Response exitosa: Code={self.CodeResult}, Elementos={len(self.Element)}")
        else:
            logger.warning(f"API Response con error: Code={self.CodeResult}, Mensaje={self.Message}")


@dataclass
class ResultadoTransaccion:
    expediente: str
    exito: bool
    mensaje: str

    def __post_init__(self):
        if self.exito:
            logger.info(f"Transacción exitosa para expediente {self.expediente}: {self.mensaje}")
        else:
            logger.error(f"Transacción fallida para expediente {self.expediente}: {self.mensaje}")
