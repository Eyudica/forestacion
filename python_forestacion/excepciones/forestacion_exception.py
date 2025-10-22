class ForestacionException(Exception):
    """Excepción base para el sistema forestal."""
    
    def __init__(self, mensaje_usuario: str, mensaje_tecnico: str, causa=None):
        self._mensaje_usuario = mensaje_usuario
        self._mensaje_tecnico = mensaje_tecnico
        self._causa = causa
        super().__init__(self._mensaje_tecnico)
    
    def get_user_message(self) -> str:
        """Mensaje amigable para el usuario."""
        return self._mensaje_usuario
    
    def get_technical_message(self) -> str:
        """Mensaje técnico detallado."""
        return self._mensaje_tecnico
    
    def get_full_message(self) -> str:
        """Mensaje completo combinado."""
        msg = f"{self._mensaje_usuario}\nDetalle técnico: {self._mensaje_tecnico}"
        if self._causa:
            msg += f"\nCausa: {str(self._causa)}"
        return msg