from typing import List, Dict, Tuple, Optional
from collections import Counter
from datetime import date, timedelta
from libro import Libro
from usuario import Usuario
from prestamo import Prestamo


class EstadisticaService:
    """Servicio para cálculos estadísticos"""
    
    @staticmethod
    def libros_mas_prestados(prestamos: List[Prestamo], top_n: int = 5) -> List[Tuple[str, int]]:
        """Devuelve los ISBN de los libros más prestados"""
        contador = Counter(p.libro.isbn for p in prestamos)
        return contador.most_common(top_n)
    
    @staticmethod
    def usuarios_mas_activos(prestamos: List[Prestamo], usuarios: Dict[int, Usuario], top_n: int = 5) -> List[Tuple[Usuario, int]]:
        """Devuelve los usuarios con más préstamos"""
        contador = Counter(p.usuario.id for p in prestamos)
        
        resultados = []
        for usuario_id, count in contador.most_common(top_n):
            if usuario_id in usuarios:
                resultados.append((usuarios[usuario_id], count))
        
        return resultados
    
    @staticmethod
    def calcular_media_prestamos_por_usuario(prestamos: List[Prestamo], total_usuarios: int) -> float:
        """Calcula la media de préstamos por usuario"""
        if total_usuarios == 0:
            return 0.0
        return len(prestamos) / total_usuarios
    
    @staticmethod
    def prestamos_vencidos(prestamos_activos: List[Prestamo], fecha_actual: date) -> List[Prestamo]:
        """Devuelve los préstamos activos que están vencidos"""
        return [p for p in prestamos_activos if p.esta_vencido(fecha_actual)]
    
    @staticmethod
    def multas_pendientes(prestamos_activos: List[Prestamo], fecha_actual: date) -> Dict[Usuario, float]:
        """Calcula las multas pendientes por usuario"""
        multas = {}
        for prestamo in prestamos_activos:
            if prestamo.esta_vencido(fecha_actual):
                multa = prestamo.calcular_multa(fecha_actual)
                if multa > 0:
                    usuario = prestamo.usuario
                    multas[usuario] = multas.get(usuario, 0) + multa
        return multas
    
    @staticmethod
    def disponibilidad_libros(libros: Dict[str, Libro], isbns_prestados: set) -> Dict[str, bool]:
        """Devuelve diccionario con disponibilidad de cada libro"""
        return {isbn: isbn not in isbns_prestados for isbn in libros}
    
    @staticmethod
    def resumen_biblioteca(libros: Dict[str, Libro], usuarios: Dict[int, Usuario], prestamos: List[Prestamo], fecha_actual: date) -> Dict:
        """Genera un resumen completo de la biblioteca"""
        prestamos_activos = [p for p in prestamos if p.esta_activo()]
        isbns_prestados = {p.libro.isbn for p in prestamos_activos}
        
        return {
            'total_libros': len(libros),
            'total_usuarios': len(usuarios),
            'total_prestamos': len(prestamos),
            'prestamos_activos': len(prestamos_activos),
            'libros_disponibles': len([isbn for isbn in libros if isbn not in isbns_prestados]),
            'libros_prestados': len(isbns_prestados),
            'prestamos_vencidos': len(EstadisticaService.prestamos_vencidos(prestamos_activos, fecha_actual)),
            'multas_totales': sum(EstadisticaService.multas_pendientes(prestamos_activos, fecha_actual).values())
        }