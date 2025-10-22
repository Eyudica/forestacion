import threading
import time
import random
from python_forestacion.patrones.observer.observable import Observable
from python_forestacion.constantes import (
    INTERVALO_SENSOR_HUMEDAD,
    HUMEDAD_MIN,
    HUMEDAD_MAX
)


class HumedadReaderTask(threading.Thread, Observable[float]):
    """Thread que lee humedad y notifica a observadores."""
    
    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        Observable.__init__(self)
        self._detenido = threading.Event()
    
    def run(self) -> None:
        """Loop principal del sensor."""
        print("[SENSOR] Humedad iniciado")
        
        while not self._detenido.is_set():
            humedad = self._leer_humedad()
            self.notificar_observadores(humedad)
            time.sleep(INTERVALO_SENSOR_HUMEDAD)
        
        print("[SENSOR] Humedad detenido")
    
    def _leer_humedad(self) -> float:
        """Simula lectura de sensor."""
        return round(random.uniform(HUMEDAD_MIN, HUMEDAD_MAX), 1)
    
    def detener(self) -> None:
        """Detiene el thread gracefully."""
        self._detenido.set()