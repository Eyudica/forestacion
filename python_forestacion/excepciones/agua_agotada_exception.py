from python_forestacion.excepciones.forestacion_exception import ForestacionException
from python_forestacion.excepciones.mensajes_exception import MensajesException


class AguaAgotadaException(ForestacionException):
    """Excepción lanzada cuando el agua disponible es insuficiente."""
    
    def __init__(self, agua_disponible: int, agua_requerida: int):
        self._agua_disponible = agua_disponible
        self._agua_requerida = agua_requerida
        
        super().__init__(
            MensajesException.AGUA_AGOTADA_USUARIO,
            f"{MensajesException.AGUA_AGOTADA_TECNICO}: "
            f"disponible={agua_disponible}L, requerida={agua_requerida}L"
        )
    
    def get_agua_disponible(self) -> int:
        return self._agua_disponible
    
    def get_agua_requerida(self) -> int:
        return self._agua_requerida

