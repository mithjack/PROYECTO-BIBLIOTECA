# plugins/mixins.py
"""
Módulo que proporciona metaclases y mixins para validación automática de atributos.
"""


class ValidatorMeta(type):
    """
    Metaclase que recolecta métodos de validación estáticos y los almacena.
    
    Los métodos de validación deben tener el formato: validate_nombre_campo
    """
    
    def __new__(mcs, name, bases, attrs):
        validators = {}
        
        # Buscar todos los métodos que comienzan con 'validate_'
        for attr_name, attr_value in attrs.items():
            if attr_name.startswith('validate_'):
                field_name = attr_name.replace('validate_', '')
                validators[field_name] = attr_value
        
        # Almacenar los validadores en la clase
        attrs['_validators'] = validators
        
        return super().__new__(mcs, name, bases, attrs)


class Validable(metaclass=ValidatorMeta):
    """
    Clase base que proporciona validación automática de atributos.
    """
    
    def __setattr__(self, name, value):
        """
        Sobrescribe el setter de atributos para aplicar validadores.
        """
        # Aplicar validador si existe
        if hasattr(self, '_validators') and name in self._validators:
            self._validators[name](value)
        
        super().__setattr__(name, value)
    
    def validar_todos(self):
        """
        Valida todos los atributos actuales.
        """
        for name, validator in self._validators.items():
            if hasattr(self, name):
                validator(getattr(self, name))


class ValidadoresComunes:
    """
    Mixin con validadores comunes reutilizables.
    """
    
    @staticmethod
    def validar_no_vacio(valor, campo: str = "Campo") -> None:
        """
        Valida que un string no esté vacío.
        Solo aplica si el valor es string.
        
        INPUT:
            valor: Valor a validar
            campo (str): Nombre del campo para el mensaje de error
        RAISE:
            TypeError: Si el valor no es string
            ValueError: Si el valor está vacío
        """
        # Primero validar tipo
        if not isinstance(valor, str):
            raise TypeError(f"{campo} debe ser una cadena de texto, got {type(valor).__name__}")
        
        # Luego validar que no esté vacío
        if not valor or not valor.strip():
            raise ValueError(f"{campo} no puede estar vacío")
    
    @staticmethod
    def validar_tipo(valor, tipo_esperado, campo: str) -> None:
        """
        Valida que un valor sea del tipo esperado.
        
        INPUT:
            valor: Valor a validar
            tipo_esperado (type): Tipo esperado
            campo (str): Nombre del campo para el mensaje de error
        RAISE:
            TypeError: Si el tipo no es el esperado
        """
        if not isinstance(valor, tipo_esperado):
            raise TypeError(f"{campo} debe ser {tipo_esperado.__name__}, "
                          f"got {type(valor).__name__}")
    
    @staticmethod
    def validar_positivo(valor, campo: str) -> None:
        """
        Valida que un número sea positivo.
        
        INPUT:
            valor (int/float): Valor a validar
            campo (str): Nombre del campo para el mensaje de error
        RAISE:
            TypeError: Si no es número
            ValueError: Si el valor no es positivo
        """
        if not isinstance(valor, (int, float)):
            raise TypeError(f"{campo} debe ser un número, got {type(valor).__name__}")
        
        if valor <= 0:
            raise ValueError(f"{campo} debe ser positivo")
    
    @staticmethod
    def validar_rango(valor, minimo, maximo, campo: str) -> None:
        """
        Valida que un número esté dentro de un rango.
        
        INPUT:
            valor (int/float): Valor a validar
            minimo (int/float): Valor mínimo
            maximo (int/float): Valor máximo
            campo (str): Nombre del campo para el mensaje de error
        RAISE:
            ValueError: Si el valor está fuera del rango
        """
        if valor < minimo or valor > maximo:
            raise ValueError(f"{campo} debe estar entre {minimo} y {maximo}")