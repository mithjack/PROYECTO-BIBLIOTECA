class EstadisticasMixin:

    def total_libros(self):
        return f"La biblioteca tiene {len(self._libros)} libros en ella"

    def total_usuarios(self):
        return f"La biblioteca tiene {len(self._usuarios) } usuarios registrados"

    def total_prestamos(self):
        return f"La biblioteca tiene {len(self._prestamos) } libros prestados"