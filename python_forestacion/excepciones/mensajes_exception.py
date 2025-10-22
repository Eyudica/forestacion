class MensajesException:
    """Mensajes de error del sistema."""
    
    # Superficie
    SUPERFICIE_INSUFICIENTE_USUARIO = "No hay suficiente superficie disponible para plantar"
    SUPERFICIE_INSUFICIENTE_TECNICO = "Superficie requerida excede disponible"
    
    # Agua
    AGUA_AGOTADA_USUARIO = "El agua de la plantación se ha agotado"
    AGUA_AGOTADA_TECNICO = "Agua disponible insuficiente para operación de riego"
    
    # Persistencia
    PERSISTENCIA_ERROR_USUARIO = "Error al guardar o recuperar datos"
    PERSISTENCIA_ERROR_TECNICO = "Fallo en operación de persistencia con Pickle"
