# usuario.py
from plugins.mixins import Validable, ValidadoresComunes


class Usuario(Validable, ValidadoresComunes):
    """Clase que representa un usuario de la biblioteca"""
    
    def __init__(self, id: int, nombre: str, max_prestamos: int = 1):
        """
        Inicializa un nuevo usuario.
        
        INPUT:
            id (int): Identificador único del usuario
            nombre (str): Nombre del usuario
            max_prestamos (int): Máximo de préstamos permitidos (default: 1)
        RAISE:
            ValueError: Si max_prestamos es <= 0
        """
        self._id = id
        self._nombre = None
        self._max_prestamos = None
        
        self.nombre = nombre
        self.max_prestamos = max_prestamos

    def __str__(self):
        return f"ID: {self.id} | {self.nombre} — {self.max_prestamos} prestamos maximos"
    
    def __call__(self, biblioteca, isbn, fecha, dias_maximos=7):
        """
        Permite al usuario realizar un préstamo directamente.
        """
        return biblioteca.prestar_libro(
            isbn=isbn,
            usuario_id=self.id,
            fecha=fecha,
            dias_maximos=dias_maximos
        )
    
    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, value):
        raise AttributeError("ID no se puede modificar después de la creación")
    
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, nombre: str) -> None:
        self._nombre = nombre
    
    @staticmethod
    def validate_nombre(value):
        """Validador para el nombre"""
        Usuario.validar_no_vacio(value, "Nombre")
    
    @property
    def max_prestamos(self) -> int:
        return self._max_prestamos

    @max_prestamos.setter
    def max_prestamos(self, max_prestamos: int) -> None:
        self._max_prestamos = max_prestamos
    
    @staticmethod
    def validate_max_prestamos(value):
        """Validador para max_prestamos"""
        # Primero validar tipo
        if not isinstance(value, int):
            raise TypeError(f"max_prestamos debe ser int, got {type(value).__name__}")
        # Luego validar que sea positivo
        if value <= 0:
            raise ValueError("max_prestamos debe ser positivo")