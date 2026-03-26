# servicios/prestamo_service.py
from datetime import date, timedelta
from typing import List, Optional, TYPE_CHECKING
from prestamo import Prestamo
from libro import Libro
from usuario import Usuario

if TYPE_CHECKING:
    from biblioteca import Biblioteca


class PrestamoService:
    """Servicio para gestionar la lógica de préstamos"""
    
    @staticmethod
    def puede_prestar(usuario: Usuario, prestamos_activos: List[Prestamo]) -> bool:
        """Verifica si un usuario puede realizar un nuevo préstamo"""
        prestamos_usuario = sum(1 for p in prestamos_activos if p.usuario.id == usuario.id)
        return prestamos_usuario < usuario.max_prestamos
    
    @staticmethod
    def calcular_fecha_devolucion(fecha_prestamo: date, dias_maximos: int) -> date:
        """Calcula la fecha límite de devolución"""
        return fecha_prestamo + timedelta(days=dias_maximos)
    
    @staticmethod
    def esta_disponible(libro: Libro, prestamos_activos: List[Prestamo]) -> bool:
        """Verifica si un libro está disponible para préstamo"""
        return not any(p.libro.isbn == libro.isbn and p.esta_activo() 
                      for p in prestamos_activos)
    
    @staticmethod
    def obtener_prestamo_activo(isbn: str, prestamos: List[Prestamo]) -> Optional[Prestamo]:
        """Obtiene el préstamo activo de un libro si existe"""
        for p in prestamos:
            if p.libro.isbn == isbn and p.esta_activo():
                return p
        return None
    
    @staticmethod
    def contar_prestamos_usuario(usuario_id: int, prestamos: List[Prestamo]) -> int:
        """Cuenta los préstamos activos de un usuario"""
        return sum(1 for p in prestamos if p.usuario.id == usuario_id and p.esta_activo())
    
    @staticmethod
    def validar_prestamo(biblioteca: 'Biblioteca', isbn: str, usuario_id: int) -> None:
        """
        Valida que se pueda realizar un préstamo
        Raises: ValueError, RuntimeError
        """
        # Validar libro existe
        if isbn not in biblioteca.libros:
            raise ValueError(f"El libro con isbn: {isbn} no está registrado")
        
        # Validar usuario existe
        if usuario_id not in biblioteca.usuarios:
            raise ValueError(f"El usuario con ID: {usuario_id} no está registrado")
        
        # Obtener préstamos activos
        prestamos_activos = biblioteca.prestamos_activos()
        
        # Validar libro no está prestado
        for p in prestamos_activos:
            if p.libro.isbn == isbn and p.esta_activo():
                raise RuntimeError(f"El libro {isbn} ya está prestado")
        
        # Validar límite de préstamos del usuario
        usuario = biblioteca.usuarios[usuario_id]
        prestamos_usuario = PrestamoService.contar_prestamos_usuario(usuario_id, prestamos_activos)
        
        if prestamos_usuario >= usuario.max_prestamos:
            raise RuntimeError(f"Usuario {usuario_id} supera límite de préstamos")