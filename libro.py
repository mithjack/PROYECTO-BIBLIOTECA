# libro.py
from plugins.mixins import Validable, ValidadoresComunes


class Libro(Validable, ValidadoresComunes):
    """
    Clase que representa un libro en la biblioteca.
    """

    def __init__(self, isbn, titulo, autor):
        """
        Inicializa un nuevo libro.
        
        INPUT:
            isbn (str): ISBN del libro (obligatorio)
            titulo (str): Título del libro
            autor (str): Autor del libro
        RAISE:
            ValueError: Si el ISBN está vacío o título/autor inválidos
        """
        # ISBN no tiene validador porque es inmutable
        if not isbn or isbn == "":
            raise ValueError("No has introducido ISBN")
        
        self._isbn = isbn
        self._titulo = None
        self._autor = None
        
        self.titulo = titulo  # Se valida automáticamente
        self.autor = autor    # Se valida automáticamente

    def __str__(self):
        return f"ISBN: {self.isbn} | {self.titulo} — {self.autor}"

    def __repr__(self) -> str:
        return f"Libro (isbn='{self.isbn}', titulo='{self.titulo}', autor='{self.autor}')"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Libro):
            return NotImplemented
        return self.isbn == other.isbn

    def __hash__(self) -> int:
        return hash(self.isbn)
    
    @property
    def isbn(self) -> str:
        return self._isbn
    
    @isbn.setter
    def isbn(self, value):
        raise AttributeError("ISBN no se puede modificar después de la creación")
    
    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, titulo):
        self._titulo = titulo
    
    @staticmethod
    def validate_titulo(value):
        """Validador para el título"""
        # Esto lanzará TypeError si no es string, y ValueError si está vacío
        Libro.validar_no_vacio(value, "Título")
    
    @property
    def autor(self) -> str:
        return self._autor

    @autor.setter
    def autor(self, autor):
        self._autor = autor
    
    @staticmethod
    def validate_autor(value):
        """Validador para el autor"""
        Libro.validar_no_vacio(value, "Autor")