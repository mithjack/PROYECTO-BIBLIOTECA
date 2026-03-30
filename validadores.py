class ValidarLibroMeta(type):
    """Metaclase simple para validar Libro"""
    
    def __new__(mcs, name, bases, namespace):
        atributos_requeridos = ['isbn', 'titulo', 'autor']
        for attr in atributos_requeridos:
            if attr not in namespace:
                raise TypeError(f"❌ a Libro le falta el atributo: '{attr}'")
        
        # Validar __init__
        if '__init__' not in namespace:
            raise TypeError("❌ Configura __init__ en Libro")
        
        # Validar __str__
        if '__str__' not in namespace:
            print("⚠️ Recomendable implementar __str__ en Libro")
        
        print(f"✅ Clase {name} validada correctamente")
        
        return super().__new__(mcs, name, bases, namespace)