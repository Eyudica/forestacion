from python_forestacion.excepciones.forestacion_exception import ForestacionException
from python_forestacion.excepciones.mensajes_exception import MensajesException


class PersistenciaException(ForestacionException):
    """Excepción lanzada en errores de persistencia."""
    
    def __init__(self, operacion: str, causa=None):
        super().__init__(
            MensajesException.PERSISTENCIA_ERROR_USUARIO,
            f"{MensajesException.PERSISTENCIA_ERROR_TECNICO} en operación: {operacion}",
            causa
        )

