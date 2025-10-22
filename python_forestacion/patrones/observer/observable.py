from abc import ABC
from typing import Generic, TypeVar, List
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from python_forestacion.patrones.observer.observer import Observer

T = TypeVar('T')


class Observable(Generic[T], ABC):
    """Clase base para objetos observables que emiten eventos tipo T."""
    
    def __init__(self):
        self._observadores: List['Observer[T]'] = []
    
    def agregar_observador(self, observador: 'Observer[T]') -> None:
        """Agrega un observador a la lista."""
        if observador not in self._observadores:
            self._observadores.append(observador)
    
    def remover_observador(self, observador: 'Observer[T]') -> None:
        """Remueve un observador de la lista."""
        if observador in self._observadores:
            self._observadores.remove(observador)
    
    def notificar_observadores(self, evento: T) -> None:
        """Notifica a todos los observadores con el evento."""
        for observador in self._observadores:
            observador.actualizar(evento)