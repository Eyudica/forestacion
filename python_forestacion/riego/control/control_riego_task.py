import threading
import time
from typing import TYPE_CHECKING

from python_forestacion.patrones.observer.observer import Observer
from python_forestacion.constantes import (
    INTERVALO_CONTROL_RIEGO,
    TEMP_MIN_RIEGO,
    TEMP_MAX_RIEGO,
    HUMEDAD_MAX_RIEGO
)

if TYPE_CHECKING:
    from python_forestacion.entidades.terrenos.plantacion import Plantacion
    from python_forestacion.servicios.terrenos.plantacion_service import PlantacionService
    from python_forestacion.riego.sensores.temperatura_reader_task import TemperaturaReaderTask
    from python_forestacion.riego.sensores.humedad_reader_task import HumedadReaderTask


class ControlRiegoTask(threading.Thread, Observer[float]):
    """
    Controlador de riego automático.
    Observa sensores y riega cuando se cumplen condiciones.
    """
    
    def __init__(self, 
                 sensor_temperatura: 'TemperaturaReaderTask',
                 sensor_humedad: 'HumedadReaderTask',
                 plantacion: 'Plantacion',
                 plantacion_service: 'PlantacionService'):
        threading.Thread.__init__(self, daemon=True)
        
        self._plantacion = plantacion
        self._plantacion_service = plantacion_service
        
        self._ultima_temperatura = None
        self._ultima_humedad = None
        self._detenido = threading.Event()
        
        # Suscribirse a sensores (Observer pattern)
        sensor_temperatura.agregar_observador(self)
        sensor_humedad.agregar_observador(self)
    
    def actualizar(self, evento: float) -> None:
        """
        Recibe eventos de sensores (Observer pattern).
        
        Args:
            evento: Lectura del sensor (temperatura o humedad)
        """
        # Identificar tipo de evento por rango aproximado
        if -30 <= evento <= 60:  # Rango de temperatura
            self._ultima_temperatura = evento
        else:  # Rango de humedad (0-100)
            self._ultima_humedad = evento
    
    def run(self) -> None:
        """Loop principal del controlador."""
        print("[CONTROL] Riego automatico iniciado")
        
        while not self._detenido.is_set():
            if self._debe_regar():
                self._ejecutar_riego()
            
            time.sleep(INTERVALO_CONTROL_RIEGO)
        
        print("[CONTROL] Riego automatico detenido")
    
    def _debe_regar(self) -> bool:
        """
        Evalúa si se deben cumplir condiciones de riego.
        
        Condiciones:
        - Temperatura entre TEMP_MIN_RIEGO y TEMP_MAX_RIEGO
        - Humedad menor a HUMEDAD_MAX_RIEGO
        
        Returns:
            True si debe regar
        """
        if self._ultima_temperatura is None or self._ultima_humedad is None:
            return False
        
        temp_ok = TEMP_MIN_RIEGO <= self._ultima_temperatura <= TEMP_MAX_RIEGO
        humedad_ok = self._ultima_humedad < HUMEDAD_MAX_RIEGO
        
        return temp_ok and humedad_ok
    
    def _ejecutar_riego(self) -> None:
        """Ejecuta el riego de la plantación."""
        try:
            print(f"\n[RIEGO AUTO] T={self._ultima_temperatura}C, "
                  f"H={self._ultima_humedad}% -> REGANDO")
            self._plantacion_service.regar(self._plantacion)
        except Exception as e:
            print(f"[ERROR] Fallo en riego automatico: {e}")
    
    def detener(self) -> None:
        """Detiene el thread gracefully."""
        self._detenido.set()

