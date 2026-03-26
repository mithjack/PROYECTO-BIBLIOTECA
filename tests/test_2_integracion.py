# tests/test_2_integracion.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import date
import pytest
from biblioteca import Biblioteca
from libro import Libro
from usuario import Usuario
from prestamo import Prestamo


@pytest.fixture
def sistema_completo():
    """Crea un sistema completo con múltiples libros y usuarios"""
    b = Biblioteca()
    b.cargar_plugins()
    
    # Libros
    libros = [
        ("001", "El Quijote", "Cervantes"),
        ("002", "Cien años de soledad", "García Márquez"),
        ("003", "1984", "Orwell"),
        ("004", "El principito", "Saint-Exupéry"),
        ("005", "La sombra del viento", "Zafón"),
    ]
    
    for isbn, titulo, autor in libros:
        b.registrar_libro(Libro(isbn, titulo, autor))
    
    # Usuarios
    usuarios = [
        (1, "Ana", 2),
        (2, "Luis", 3),
        (3, "Marta", 1),
        (4, "Carlos", 2),
    ]
    
    for id, nombre, max_prest in usuarios:
        b.registrar_usuario(Usuario(id, nombre, max_prest))
    
    return b


@pytest.fixture
def sistema_con_prestamos(sistema_completo):
    """Crea un sistema con préstamos activos"""
    b = sistema_completo
    
    # Realizar algunos préstamos
    b.prestar_libro("001", 1, date(2025, 3, 1))
    b.prestar_libro("002", 2, date(2025, 3, 1))
    
    return b


def test_flujo_completo_prestamo_devolucion(sistema_completo):
    """Test del flujo completo: préstamo → devolución"""
    # Prestar libro
    prestamo = sistema_completo.prestar_libro("001", 1, date(2025, 3, 1))
    assert prestamo.esta_activo() is True
    assert len(sistema_completo.prestamos_activos()) == 1
    
    # Verificar que el libro no está disponible
    disponibles = sistema_completo.menu_libros_disponibles()
    assert "001" not in disponibles
    
    # Devolver libro
    prestamo_devuelto = sistema_completo.devolver_libro("001", date(2025, 3, 8))
    assert prestamo_devuelto.esta_activo() is False
    
    # Verificar que el libro está disponible nuevamente
    disponibles = sistema_completo.menu_libros_disponibles()
    assert "001" in disponibles
    assert len(sistema_completo.prestamos_activos()) == 0


def test_usuario_con_multiples_prestamos(sistema_completo):
    """Test que un usuario puede tener múltiples préstamos según su límite"""
    # Ana (ID 1) tiene límite 2
    sistema_completo.prestar_libro("001", 1, date(2025, 3, 1))
    sistema_completo.prestar_libro("002", 1, date(2025, 3, 1))
    
    # Debería tener 2 préstamos activos
    prestamos_usuario = [p for p in sistema_completo.prestamos_activos() if p.usuario.id == 1]
    assert len(prestamos_usuario) == 2
    
    # Intentar un tercero debería fallar
    with pytest.raises(RuntimeError):
        sistema_completo.prestar_libro("003", 1, date(2025, 3, 2))


def test_busqueda_y_prestamo(sistema_completo):
    """Test de búsqueda de libro y luego préstamo"""
    # Buscar libro por título
    resultados = sistema_completo.buscar_libro("Quijote")
    assert len(resultados) == 1
    libro = resultados[0]
    
    # Prestar el libro encontrado
    prestamo = sistema_completo.prestar_libro(libro.isbn, 2, date(2025, 3, 1))
    assert prestamo.esta_activo() is True
    assert libro.isbn in sistema_completo.isbns_prestados()


def test_mismo_libro_no_prestable_dos_veces(sistema_completo):
    """Test que el mismo libro no se puede prestar dos veces"""
    # Primer préstamo
    sistema_completo.prestar_libro("001", 1, date(2025, 3, 1))
    
    # Segundo préstamo del mismo libro a otro usuario
    with pytest.raises(RuntimeError, match="ya está prestado"):
        sistema_completo.prestar_libro("001", 2, date(2025, 3, 2))


def test_usuario_puede_prestar_despues_de_devolver(sistema_completo):
    """Test que un usuario puede prestar de nuevo después de devolver"""
    # Prestar
    sistema_completo.prestar_libro("001", 3, date(2025, 3, 1))
    
    # Devolver
    sistema_completo.devolver_libro("001", date(2025, 3, 5))
    
    # Prestar otro libro
    prestamo = sistema_completo.prestar_libro("002", 3, date(2025, 3, 6))
    assert prestamo.esta_activo() is True


def test_exportar_y_cargar_backup(sistema_completo, tmp_path, monkeypatch):
    """Test de exportación y carga de backup"""
    import json
    import os
    import biblioteca as bib_module
    
    original_db_dir = bib_module.DB_DIR
    
    try:
        monkeypatch.setattr(bib_module, 'DB_DIR', str(tmp_path))
        
        # Exportar datos
        sistema_completo.exportar_json(oculto=True)
        sistema_completo.exportar_csv(oculto=True)
        
        # Crear nueva instancia y cargar backup
        nueva_biblioteca = Biblioteca()
        nueva_biblioteca.cargar_plugins()
        resultado = nueva_biblioteca.cargar_backup()
        
        assert resultado is True
        
        # Verificar que los datos se cargaron correctamente
        assert len(nueva_biblioteca.libros) == 5
        assert len(nueva_biblioteca.usuarios) == 4
        
    finally:
        monkeypatch.setattr(bib_module, 'DB_DIR', original_db_dir)


def test_calculo_multas_integracion(sistema_completo):
    """Test integrado de cálculo de multas"""
    # Prestar libro con retraso
    fecha_prestamo = date(2025, 3, 1)
    prestamo = sistema_completo.prestar_libro("001", 1, fecha_prestamo, dias_maximos=7)
    
    # Devolver con retraso
    fecha_devolucion = date(2025, 3, 15)  # 7 días de retraso
    prestamo_devuelto = sistema_completo.devolver_libro("001", fecha_devolucion)
    
    # Calcular multa
    multa = prestamo_devuelto.calcular_multa(fecha_devolucion)
    assert multa == 7 * 0.25  # 7 días * 0.25


def test_singleton_comparte_datos(sistema_completo):
    """Test que el patrón Singleton comparte datos entre instancias"""
    b2 = Biblioteca()
    
    # Ambas instancias deberían tener los mismos datos
    assert len(b2.libros) == len(sistema_completo.libros)
    assert b2.libros.keys() == sistema_completo.libros.keys()
    
    # Modificar desde una instancia afecta a la otra
    b2.registrar_libro(Libro("999", "Nuevo", "Autor"))
    assert "999" in sistema_completo.libros