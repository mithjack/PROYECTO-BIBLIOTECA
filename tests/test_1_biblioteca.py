# tests/test_1_biblioteca.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from datetime import date
import biblioteca as bib_module
from biblioteca import Biblioteca
from libro import Libro
from usuario import Usuario


@pytest.fixture(autouse=True)
def limpiar_singleton():
    """Limpia la instancia Singleton antes de cada test"""
    # Resetear la instancia Singleton
    Biblioteca._instancia = None
    yield
    # Limpiar después del test también
    Biblioteca._instancia = None


@pytest.fixture
def biblioteca_vacia():
    """Crea una biblioteca vacía con plugins cargados"""
    b = Biblioteca()
    b.cargar_plugins()
    return b


@pytest.fixture
def biblioteca_con_datos():
    """Crea una biblioteca con datos precargados"""
    b = Biblioteca()
    b.cargar_plugins()
    
    # Libros
    b.registrar_libro(Libro("111", "Python Basics", "John Doe"))
    b.registrar_libro(Libro("222", "Advanced Python", "Jane Smith"))
    b.registrar_libro(Libro("333", "Data Science", "Alan Turing"))
    
    # Usuarios
    b.registrar_usuario(Usuario(1, "Ana", 2))
    b.registrar_usuario(Usuario(2, "Luis", 1))
    b.registrar_usuario(Usuario(3, "Marta", 3))
    
    return b


@pytest.fixture
def biblioteca_con_prestamos(biblioteca_con_datos):
    """Crea una biblioteca con préstamos activos"""
    b = biblioteca_con_datos
    
    # Realizar préstamos
    b.prestar_libro("111", 1, date(2025, 3, 1))
    b.prestar_libro("222", 2, date(2025, 3, 1))
    
    return b


# ============ TESTS DE SINGLETON ============

def test_singleton_pattern():
    """Verifica que Biblioteca implementa correctamente el patrón Singleton"""
    b1 = Biblioteca()
    b2 = Biblioteca()
    assert b1 is b2
    assert id(b1) == id(b2)


# ============ TESTS DE LIBROS ============

def test_registrar_libro(biblioteca_vacia):
    """Test de registro de libro"""
    libro = Libro("123", "Test Book", "Test Author")
    biblioteca_vacia.registrar_libro(libro)
    
    assert "123" in biblioteca_vacia.libros
    assert biblioteca_vacia.libros["123"] == libro


def test_registrar_libro_duplicado_sobrescribe(biblioteca_con_datos):
    """Test que sobrescribe libro existente"""
    libro_nuevo = Libro("111", "Nuevo Titulo", "Nuevo Autor")
    biblioteca_con_datos.registrar_libro(libro_nuevo)
    
    assert biblioteca_con_datos.libros["111"].titulo == "Nuevo Titulo"
    assert biblioteca_con_datos.libros["111"].autor == "Nuevo Autor"


def test_comprobar_isbn_existente(biblioteca_con_datos):
    """Test de comprobación de ISBN existente"""
    assert biblioteca_con_datos.comprobar_isbn("111") == True
    assert biblioteca_con_datos.comprobar_isbn("999") == False


def test_buscar_libro_por_titulo(biblioteca_con_datos):
    """Test de búsqueda de libro por título"""
    resultados = biblioteca_con_datos.buscar_libro("Python")
    assert len(resultados) == 2
    assert all("Python" in r.titulo for r in resultados)


def test_buscar_libro_por_autor(biblioteca_con_datos):
    """Test de búsqueda de libro por autor"""
    resultados = biblioteca_con_datos.buscar_libro("Jane")
    assert len(resultados) == 1
    assert resultados[0].autor == "Jane Smith"


def test_buscar_libro_no_existente(biblioteca_con_datos):
    """Test de búsqueda sin resultados"""
    resultados = biblioteca_con_datos.buscar_libro("Inexistente")
    assert len(resultados) == 0


# ============ TESTS DE USUARIOS ============

def test_registrar_usuario(biblioteca_vacia):
    """Test de registro de usuario"""
    usuario = Usuario(1, "Carlos", 3)
    resultado = biblioteca_vacia.registrar_usuario(usuario)
    
    assert resultado == True
    assert 1 in biblioteca_vacia.usuarios
    assert biblioteca_vacia.usuarios[1] == usuario


def test_registrar_usuario_duplicado_sin_reemplazo(biblioteca_con_datos):
    """Test que no reemplaza usuario si no se confirma"""
    usuario_nuevo = Usuario(1, "Nuevo", 5)
    resultado = biblioteca_con_datos.registrar_usuario(usuario_nuevo, confirmar_reemplazo=False)
    
    assert resultado == False
    assert biblioteca_con_datos.usuarios[1].nombre == "Ana"


# ============ TESTS DE PRÉSTAMOS ============

def test_prestar_libro_correcto(biblioteca_con_datos):
    """Test de préstamo correcto"""
    prestamo = biblioteca_con_datos.prestar_libro("333", 1, date(2025, 3, 10))
    
    assert prestamo.esta_activo() == True
    assert len(biblioteca_con_datos.prestamos_activos()) == 1


def test_prestar_libro_no_existente(biblioteca_con_datos):
    """Test de préstamo de libro no existente"""
    with pytest.raises(ValueError, match="no está registrado"):
        biblioteca_con_datos.prestar_libro("999", 1, date(2025, 3, 10))


def test_prestar_libro_usuario_no_existente(biblioteca_con_datos):
    """Test de préstamo con usuario no existente"""
    with pytest.raises(ValueError, match="no está registrado"):
        biblioteca_con_datos.prestar_libro("111", 99, date(2025, 3, 10))


def test_prestar_libro_ya_prestado(biblioteca_con_prestamos):
    """Test de préstamo de libro ya prestado"""
    with pytest.raises(RuntimeError, match="ya está prestado"):
        biblioteca_con_prestamos.prestar_libro("111", 2, date(2025, 3, 5))


def test_prestar_libro_supera_limite_usuario(biblioteca_con_datos):
    """Test de usuario que supera límite de préstamos"""
    # Usuario 2 tiene límite 1
    biblioteca_con_datos.prestar_libro("111", 2, date(2025, 3, 1))
    
    # Segundo préstamo debería fallar
    with pytest.raises(RuntimeError, match="supera límite"):
        biblioteca_con_datos.prestar_libro("222", 2, date(2025, 3, 2))


def test_devolver_libro_correcto(biblioteca_con_prestamos):
    """Test de devolución correcta"""
    prestamo = biblioteca_con_prestamos.devolver_libro("111", date(2025, 3, 8))
    
    assert prestamo.esta_activo() == False
    assert prestamo._devolucion == date(2025, 3, 8)


def test_devolver_libro_no_prestado(biblioteca_con_datos):
    """Test de devolución de libro no prestado"""
    with pytest.raises(RuntimeError, match="no tiene préstamo activo"):
        biblioteca_con_datos.devolver_libro("111", date(2025, 3, 8))


def test_prestamos_activos(biblioteca_con_prestamos):
    """Test de obtener préstamos activos"""
    activos = biblioteca_con_prestamos.prestamos_activos()
    assert len(activos) == 2
    assert all(p.esta_activo() for p in activos)


def test_isbns_prestados(biblioteca_con_prestamos):
    """Test de obtener ISBNs de libros prestados"""
    isbns = biblioteca_con_prestamos.isbns_prestados()
    assert isbns == {"111", "222"}


def test_menu_libros_disponibles(biblioteca_con_prestamos):
    """Test de libros disponibles (no prestados)"""
    disponibles = biblioteca_con_prestamos.menu_libros_disponibles()
    assert "333" in disponibles
    assert "111" not in disponibles
    assert "222" not in disponibles


# ============ TESTS DE ITERACIÓN Y ACCESO ============

def test_iteracion_libros(biblioteca_con_datos):
    """Test que la biblioteca es iterable"""
    libros_iterados = list(biblioteca_con_datos)
    assert len(libros_iterados) == 3
    assert "111" in libros_iterados
    assert "222" in libros_iterados
    assert "333" in libros_iterados


def test_acceso_por_indice(biblioteca_con_datos):
    """Test de acceso por índice (__getitem__)"""
    libro = biblioteca_con_datos["111"]
    assert libro.titulo == "Python Basics"


def test_operador_suma(biblioteca_vacia):
    """Test del operador + para añadir libros"""
    libro = Libro("999", "Nuevo Libro", "Autor")
    biblioteca_vacia + libro
    
    assert "999" in biblioteca_vacia.libros


# ============ TESTS DE EXPORTACIÓN ============

def test_exportar_json(biblioteca_con_datos, tmp_path, monkeypatch):
    """Test de exportación a JSON"""
    import json
    import os
    import biblioteca as bib_module
    
    original_db_dir = bib_module.DB_DIR
    
    try:
        monkeypatch.setattr(bib_module, 'DB_DIR', str(tmp_path))
        
        biblioteca_con_datos.exportar_json(oculto=True)
        
        json_file = os.path.join(str(tmp_path), "biblioteca.json")
        assert os.path.exists(json_file)
        
        with open(json_file, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        assert len(datos["libros"]) == 3
        assert len(datos["usuarios"]) == 3
        # El primer libro puede variar, verificamos que existe "111"
        isbns = [l["isbn"] for l in datos["libros"]]
        assert "111" in isbns
        
    finally:
        monkeypatch.setattr(bib_module, 'DB_DIR', original_db_dir)


def test_exportar_csv(biblioteca_con_datos, tmp_path, monkeypatch):
    """Test de exportación a CSV"""
    import csv
    import os
    import biblioteca as bib_module
    
    original_db_dir = bib_module.DB_DIR
    
    try:
        monkeypatch.setattr(bib_module, 'DB_DIR', str(tmp_path))
        
        biblioteca_con_datos.exportar_csv(oculto=True)
        
        libros_csv = os.path.join(str(tmp_path), "libros.csv")
        usuarios_csv = os.path.join(str(tmp_path), "usuarios.csv")
        
        assert os.path.exists(libros_csv)
        assert os.path.exists(usuarios_csv)
        
        with open(libros_csv, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            # Header + 3 libros
            assert len(rows) == 4
            
    finally:
        monkeypatch.setattr(bib_module, 'DB_DIR', original_db_dir)


# ============ TESTS DE PLUGINS ============

def test_cargar_plugins(biblioteca_vacia):
    """Test de carga de plugins"""
    assert hasattr(biblioteca_vacia, 'limpiar_pantalla')
    assert hasattr(biblioteca_vacia, 'pausa')
    assert hasattr(biblioteca_vacia, 'menu_seleccionar')


def test_total_libros_plugin(biblioteca_con_datos):
    """Test del plugin total_libros"""
    assert biblioteca_con_datos.total_libros() == "La biblioteca tiene 3 libros en ella"


def test_total_usuarios_plugin(biblioteca_con_datos):
    """Test del plugin total_usuarios"""
    assert biblioteca_con_datos.total_usuarios() == "La biblioteca tiene 3 usuarios registrados"


def test_total_prestamos_plugin(biblioteca_con_prestamos):
    """Test del plugin total_prestamos"""
    assert biblioteca_con_prestamos.total_prestamos() == "La biblioteca tiene 2 libros prestados"


# ============ TESTS DE CASOS LÍMITE ============

def test_prestamo_con_dias_negativos(biblioteca_con_datos):
    """Test de préstamo con días máximos negativos"""
    with pytest.raises(ValueError, match="positivos"):
        biblioteca_con_datos.prestar_libro("111", 1, date(2025, 3, 1), dias_maximos=-5)


def test_prestamo_sin_libros_disponibles(biblioteca_con_prestamos):
    """Test cuando no hay libros disponibles"""
    # Prestar el último libro disponible
    biblioteca_con_prestamos.prestar_libro("333", 3, date(2025, 3, 10))
    
    disponibles = biblioteca_con_prestamos.menu_libros_disponibles()
    assert len(disponibles) == 0


def test_usuario_con_prestamo_maximo(biblioteca_con_datos):
    """Test que usuario respeta límite de préstamos"""
    # Ana (ID 1) tiene límite 2
    biblioteca_con_datos.prestar_libro("111", 1, date(2025, 3, 1))
    biblioteca_con_datos.prestar_libro("222", 1, date(2025, 3, 2))
    
    # Debería tener 2 préstamos activos
    prestamos_usuario = [p for p in biblioteca_con_datos.prestamos_activos() if p.usuario.id == 1]
    assert len(prestamos_usuario) == 2
    
    # Tercer préstamo debería fallar
    with pytest.raises(RuntimeError):
        biblioteca_con_datos.prestar_libro("333", 1, date(2025, 3, 3))