from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')


class Observer(Generic[T], ABC):
    """Interfaz para observadores que reciben eventos tipo T."""
    
    @abstractmethod
    def actualizar(self, evento: T) -> None:
        """
        Recibe notificación de un evento.
        
        Args:
            evento: Dato del evento (tipo genérico T)
        """
        pass
