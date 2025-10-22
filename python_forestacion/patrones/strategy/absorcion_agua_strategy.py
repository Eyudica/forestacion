
from abc import ABC, abstractmethod
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from python_forestacion.entidades.cultivos.cultivo import Cultivo


class AbsorcionAguaStrategy(ABC):
    """Estrategia para calcular absorción de agua."""
    
    @abstractmethod
    def calcular_absorcion(
        self,
        fecha: date,
        temperatura: float,
        humedad: float,
        cultivo: 'Cultivo'
    ) -> int:
        """
        Calcula litros de agua absorbidos.
        
        Args:
            fecha: Fecha actual
            temperatura: Temperatura ambiente
            humedad: Humedad relativa
            cultivo: Cultivo que absorbe
            
        Returns:
            Litros de agua absorbidos
        """
        pass