import threading
import time
import random
from python_forestacion.patrones.observer.observable import Observable
from python_forestacion.constantes import (
    INTERVALO_SENSOR_TEMPERATURA,
    TEMP_MIN,
    TEMP_MAX
)


class TemperaturaReaderTask(threading.Thread, Observable[float]):
    """Thread que lee temperatura y notifica a observadores."""
    
    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        Observable.__init__(self)
        self._detenido = threading.Event()
    
    def run(self) -> None:
        """Loop principal del sensor."""
        print("[SENSOR] Temperatura iniciado")
        
        while not self._detenido.is_set():
            temperatura = self._leer_temperatura()
            self.notificar_observadores(temperatura)
            time.sleep(INTERVALO_SENSOR_TEMPERATURA)
        
        print("[SENSOR] Temperatura detenido")
    
    def _leer_temperatura(self) -> float:
        """Simula lectura de sensor."""
        return round(random.uniform(TEMP_MIN, TEMP_MAX), 1)
    
    def detener(self) -> None:
        """Detiene el thread gracefully."""
        self._detenido.set()