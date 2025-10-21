import time
from datetime import date, timedelta

from python_forestacion.servicios.terrenos.tierra_service import TierraService
from python_forestacion.servicios.terrenos.plantacion_service import PlantacionService
from python_forestacion.servicios.terrenos.registro_forestal_service import RegistroForestalService
from python_forestacion.servicios.personal.trabajador_service import TrabajadorService
from python_forestacion.servicios.negocio.fincas_service import FincasService
from python_forestacion.servicios.cultivos.cultivo_service_registry import CultivoServiceRegistry

from python_forestacion.entidades.terrenos.registro_forestal import RegistroForestal
from python_forestacion.entidades.personal.trabajador import Trabajador
from python_forestacion.entidades.personal.tarea import Tarea
from python_forestacion.entidades.personal.apto_medico import AptoMedico
from python_forestacion.entidades.personal.herramienta import Herramienta
from python_forestacion.entidades.cultivos.pino import Pino
from python_forestacion.entidades.cultivos.olivo import Olivo

from python_forestacion.riego.sensores.temperatura_reader_task import TemperaturaReaderTask
from python_forestacion.riego.sensores.humedad_reader_task import HumedadReaderTask
from python_forestacion.riego.control.control_riego_task import ControlRiegoTask

from python_forestacion.excepciones.forestacion_exception import ForestacionException


def imprimir_separador(titulo: str = "", ancho: int = 70):
    """Imprime un separador visual."""
    if titulo:
        print(f"\n{'-'*ancho}")
        print(f"  {titulo}")
        print(f"{'-'*ancho}")
    else:
        print("="*ancho)


def main():
    """Función principal con demostración completa."""
    
    print("="*70)
    print("         SISTEMA DE GESTION FORESTAL - PATRONES DE DISENO")
    print("="*70)
    
    # ========================================================================
    # 1. PATRON SINGLETON
    # ========================================================================
    imprimir_separador("PATRON SINGLETON: Inicializando servicios")
    
    registry1 = CultivoServiceRegistry.get_instance()
    registry2 = CultivoServiceRegistry.get_instance()
    
    if registry1 is registry2:
        print("[OK] Todos los servicios comparten la misma instancia del Registry")
    
    # ========================================================================
    # 2. CREACION DE INFRAESTRUCTURA
    # ========================================================================
    imprimir_separador("Creando infraestructura")
    
    tierra_service = TierraService()
    plantacion_service = PlantacionService()
    trabajador_service = TrabajadorService()
    registro_service = RegistroForestalService()
    fincas_service = FincasService()
    
    print("1. Creando tierra con plantacion...")
    terreno = tierra_service.crear_tierra_con_plantacion(
        id_padron_catastral=123456,
        superficie=10000.0,  # 10,000 m2
        domicilio="Ruta 40 Km 1080, Agrelo, Mendoza",
        nombre_plantacion="Finca del Madero"
    )
    
    plantacion = terreno.get_finca()
    print(f"[OK] Tierra creada: Padron {terreno.get_id_padron()}")
    print(f"[OK] Plantacion '{plantacion.get_nombre()}' con {plantacion.get_superficie_total()}m2")
    
    # ========================================================================
    # 3. PATRON FACTORY METHOD
    # ========================================================================
    imprimir_separador("PATRON FACTORY METHOD: Plantando cultivos")
    
    try:
        print("\n2. Plantando cultivos usando Factory Method...")
        plantacion_service.plantar(plantacion, "Pino", 50)
        plantacion_service.plantar(plantacion, "Olivo", 30)
        plantacion_service.plantar(plantacion, "Lechuga", 100)
        plantacion_service.plantar(plantacion, "Zanahoria", 150)
        
        plantacion_service.mostrar_estado(plantacion)
        
    except ForestacionException as e:
        print(f"[ERROR] {e.get_full_message()}")
    
    # ========================================================================
    # 4. GESTION DE PERSONAL
    # ========================================================================
    imprimir_separador("Gestion de Personal")
    
    print("\n3. Creando trabajadores con certificacion medica...")
    
    apto_juan = AptoMedico(
        fecha_emision=date.today() - timedelta(days=30),
        observaciones="Apto para trabajos agricolas"
    )
    
    tarea1 = Tarea(1, "Mantenimiento de pinos", date.today())
    tarea2 = Tarea(2, "Riego manual de hortalizas", date.today())
    
    trabajador1 = Trabajador(
        dni=12345678,
        nombre="Juan Perez",
        tareas=[tarea1, tarea2],
        apto_medico=apto_juan
    )
    
    trabajador2 = Trabajador(
        dni=87654321,
        nombre="Maria Gomez",
        tareas=[],
        apto_medico=None  # Sin apto medico
    )
    
    plantacion.add_trabajador(trabajador1)
    plantacion.add_trabajador(trabajador2)
    
    herramienta = Herramienta(
        id_herramienta=1,
        nombre="Pala de jardineria",
        certificacion_hs=True
    )
    
    print(f"[OK] Trabajador: {trabajador1.get_nombre()} - Apto medico: SI")
    print(f"[OK] Trabajador: {trabajador2.get_nombre()} - Apto medico: NO")
    
    # Trabajar
    print("\n4. Ejecutando tareas...")
    trabajador_service.trabajar(trabajador1, date.today(), herramienta)
    trabajador_service.trabajar(trabajador2, date.today(), herramienta)
    
    # ========================================================================
    # 5. PATRON STRATEGY + Riego Manual
    # ========================================================================
    imprimir_separador("PATRON STRATEGY: Riego manual (absorcion diferenciada)")
    
    try:
        print("\n5. Regando plantacion manualmente...")
        plantacion_service.regar(plantacion)
        
    except ForestacionException as e:
        print(f"[ERROR] {e.get_full_message()}")
    
    # ========================================================================
    # 6. PATRON OBSERVER + Sistema de Riego Automatizado
    # ========================================================================
    imprimir_separador("PATRON OBSERVER: Sistema de riego automatizado")
    
    print("\n6. Iniciando sensores y controlador de riego...")
    
    # Crear sensores (Observable)
    tarea_temp = TemperaturaReaderTask()
    tarea_hum = HumedadReaderTask()
    
    # Crear controlador (Observer)
    tarea_control = ControlRiegoTask(
        tarea_temp,
        tarea_hum,
        plantacion,
        plantacion_service
    )
    
    # Iniciar threads daemon
    tarea_temp.start()
    tarea_hum.start()
    tarea_control.start()
    
    print("[OK] Sensores y control iniciados")
    print("[INFO] Sistema funcionando durante 15 segundos...")
    
    # Dejar funcionar el sistema
    time.sleep(15)
    
    # Detener sistema
    print("\n[INFO] Deteniendo sistema de riego...")
    tarea_temp.detener()
    tarea_hum.detener()
    tarea_control.detener()
    
    # Esperar a que terminen
    tarea_temp.join(timeout=2)
    tarea_hum.join(timeout=2)
    tarea_control.join(timeout=2)
    
    # ========================================================================
    # 7. COSECHA CON GENERICS
    # ========================================================================
    imprimir_separador("Cosecha con Paquetes Genericos")
    
    print("\n7. Cosechando por tipo...")
    
    paquete_pinos = fincas_service.cosechar_por_tipo(plantacion, Pino)
    paquete_olivos = fincas_service.cosechar_por_tipo(plantacion, Olivo)
    
    fincas_service.mostrar_paquete(paquete_pinos, "Pino")
    fincas_service.mostrar_paquete(paquete_olivos, "Olivo")
    
    # ========================================================================
    # 8. FUMIGACION
    # ========================================================================
    print("\n8. Fumigando plantacion...")
    plantacion_service.fumigar(plantacion, "Fungicida Organico XYZ")
    
    # ========================================================================
    # 9. PERSISTENCIA
    # ========================================================================
    imprimir_separador("Persistencia con Pickle")
    
    print("\n9. Creando registro forestal...")
    registro = RegistroForestal(
        id_padron=terreno.get_id_padron(),
        tierra=terreno,
        plantacion=plantacion,
        propietario="Juan Perez",
        avaluo=50309233.55
    )
    
    print("\n10. Persistiendo registro en disco...")
    try:
        registro_service.persistir(registro)
        print("[OK] Registro guardado exitosamente")
    except ForestacionException as e:
        print(f"[ERROR] {e.get_full_message()}")
    
    print("\n11. Recuperando registro desde disco...")
    try:
        registro_leido = RegistroForestalService.leer_registro("Juan Perez")
        registro_service.mostrar_datos(registro_leido)
        print("[OK] Registro recuperado exitosamente")
    except ForestacionException as e:
        print(f"[ERROR] {e.get_full_message()}")
    
    # ========================================================================
    # RESUMEN FINAL
    # ========================================================================
    imprimir_separador()
    print("              EJEMPLO COMPLETADO EXITOSAMENTE")
    imprimir_separador()
    print("  [OK] SINGLETON   - CultivoServiceRegistry (instancia unica)")
    print("  [OK] FACTORY     - Creacion de 4 tipos de cultivos")
    print("  [OK] OBSERVER    - Sistema de sensores y eventos")
    print("  [OK] STRATEGY    - Algoritmos de absorcion de agua")
    print("  [OK] REGISTRY    - Dispatch polimorfico sin isinstance")
    print("  [OK] GENERICS    - Paquetes tipo-seguros")
    print("  [OK] THREADS     - Sensores y control concurrente")
    print("  [OK] PERSISTENCIA- Guardado y recuperacion con Pickle")
    imprimir_separador()
    print("\n[INFO] Revise el archivo: data/Juan Perez.dat")
    print("[INFO] Sistema finalizado correctamente\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n[ERROR FATAL] {e}")
        import traceback
        traceback.print_exc()