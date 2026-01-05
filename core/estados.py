from enum import IntEnum

class EstadoStagingExpedienteMemoriales(IntEnum):
    PENDIENTE = 0
    PROCESANDO_JOB = 1
    FINALIZADO_JOB = 2
    PROCESANDO_BOT = 3
    FINALIZADO_P2 = 4
    ERROR = 5