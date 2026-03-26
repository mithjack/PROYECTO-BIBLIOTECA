"""
Servicio para gestionar múltiples bibliotecas (Singleton por nombre)
"""
from biblioteca import Biblioteca


class BibliotecaManager:
    """
    Gestor de múltiples bibliotecas.
    Cada biblioteca tiene un nombre único y se almacena como instancia.
    """
    _bibliotecas = {}  # Diccionario con nombre: instancia
    _biblioteca_actual = None  # Nombre de la biblioteca activa
    
    @classmethod
    def crear_biblioteca(cls, nombre: str) -> Biblioteca:
        """
        Crea una nueva biblioteca con el nombre especificado.
        
        INPUT:
            nombre (str): Nombre único de la biblioteca
        OUTPUT:
            Biblioteca: Instancia de la biblioteca creada
        RAISE:
            ValueError: Si ya existe una biblioteca con ese nombre
        """
        if nombre in cls._bibliotecas:
            raise ValueError(f"Ya existe una biblioteca con el nombre '{nombre}'")
        
        # Crear nueva instancia
        biblioteca = Biblioteca()
        cls._bibliotecas[nombre] = biblioteca
        
        # Si es la primera, establecer como actual
        if cls._biblioteca_actual is None:
            cls._biblioteca_actual = nombre
        
        print(f"✅ Biblioteca '{nombre}' creada correctamente.")
        return biblioteca
    
    @classmethod
    def cambiar_biblioteca(cls, nombre: str) -> Biblioteca:
        """
        Cambia a la biblioteca especificada.
        
        INPUT:
            nombre (str): Nombre de la biblioteca
        OUTPUT:
            Biblioteca: Instancia de la biblioteca seleccionada
        RAISE:
            ValueError: Si no existe la biblioteca
        """
        if nombre not in cls._bibliotecas:
            raise ValueError(f"No existe la biblioteca '{nombre}'")
        
        cls._biblioteca_actual = nombre
        print(f"📚 Cambiado a biblioteca '{nombre}'")
        return cls._bibliotecas[nombre]
    
    @classmethod
    def obtener_biblioteca_actual(cls) -> Biblioteca:
        """
        Obtiene la biblioteca actualmente activa.
        
        OUTPUT:
            Biblioteca: Instancia de la biblioteca actual
        RAISE:
            RuntimeError: Si no hay biblioteca activa
        """
        if cls._biblioteca_actual is None:
            raise RuntimeError("No hay ninguna biblioteca activa")
        return cls._bibliotecas[cls._biblioteca_actual]
    
    @classmethod
    def listar_bibliotecas(cls) -> list:
        """
        Lista todas las bibliotecas creadas.
        
        OUTPUT:
            list: Lista de nombres de bibliotecas
        """
        return list(cls._bibliotecas.keys())
    
    @classmethod
    def eliminar_biblioteca(cls, nombre: str) -> bool:
        """
        Elimina una biblioteca.
        
        INPUT:
            nombre (str): Nombre de la biblioteca a eliminar
        OUTPUT:
            bool: True si se eliminó correctamente
        RAISE:
            ValueError: Si no existe la biblioteca o es la única
        """
        if nombre not in cls._bibliotecas:
            raise ValueError(f"No existe la biblioteca '{nombre}'")
        
        if len(cls._bibliotecas) == 1:
            raise ValueError("No se puede eliminar la única biblioteca")
        
        # Si eliminamos la actual, cambiar a otra
        if cls._biblioteca_actual == nombre:
            # Cambiar a la primera disponible
            nueva = next(n for n in cls._bibliotecas.keys() if n != nombre)
            cls.cambiar_biblioteca(nueva)
        
        del cls._bibliotecas[nombre]
        print(f"🗑️ Biblioteca '{nombre}' eliminada.")
        return True
    
    @classmethod
    def existe_biblioteca(cls, nombre: str) -> bool:
        """
        Verifica si existe una biblioteca.
        
        INPUT:
            nombre (str): Nombre de la biblioteca
        OUTPUT:
            bool: True si existe
        """
        return nombre in cls._bibliotecas