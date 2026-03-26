from datetime import date, timedelta

class Prestamo:

    MULTA_DIARIA = 0.25

    def __init__(self, libro, usuario, fecha_alquiler:date, dias_maximos:int = 7):
        if dias_maximos <= 0:
            raise ValueError("Los dias maximos de alquiler tienen que ser positivos")
        self.libro = libro
        self.usuario = usuario
        self._fecha_alquiler = fecha_alquiler
        self._dias_maximos = dias_maximos
        self._devolucion = None

    def __str__(self):
        estado = ("alquiler activo" if self.esta_activo()else f"devuelto el: {self._devolucion}")
        return (
            f"Libro '{self.libro.titulo}' (ISBN: {self.libro.isbn}) "
            f"al usuario '{self.usuario.nombre}' (ID: {self.usuario.id}) "
            f"el dia: {self._fecha_alquiler}, "
            f"durante: {self._dias_maximos} dias, "
            f"{estado}"
        )
    
    def esta_activo(self)->bool:
        return self._devolucion is None
    
    def esta_vencido(self, fecha_alquiler:date)->bool:
        devolucion = self._fecha_alquiler + timedelta(days=self._dias_maximos)
        return fecha_alquiler > devolucion 

    def devolver(self, fecha_alquiler: date) -> None:
        if not self.esta_activo():
            raise RuntimeError("No hay que devolverlo")
        self._devolucion = fecha_alquiler
        return self

    def calcular_multa(self, fecha_alquiler):
        devolucion = self._fecha_alquiler + timedelta(days=self._dias_maximos)
        dias_excedidos = (fecha_alquiler - devolucion).days
        return 0 if fecha_alquiler <= devolucion else dias_excedidos * self.MULTA_DIARIA