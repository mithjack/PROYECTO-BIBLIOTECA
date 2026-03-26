# tests/test_5_libro_avanzado.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from libro import Libro


def test_creacion_libro_basica():
    libro = Libro("123", "Titulo", "Autor")
    assert libro.isbn == "123"
    assert libro.titulo == "Titulo"
    assert libro.autor == "Autor"


def test_isbn_obligatorio():
    with pytest.raises(ValueError):
        Libro("", "Titulo", "Autor")


def test_libro_no_tiene_estado_prestamo():
    libro = Libro("123", "Titulo", "Autor")
    assert not hasattr(libro, "prestado")
    assert not hasattr(libro, "esta_prestado")


def test_creacion_libro_con_datos_validos():
    """Test de creación con datos válidos"""
    libro = Libro("978-3-16-148410-0", "Clean Code", "Robert Martin")
    assert libro.isbn == "978-3-16-148410-0"
    assert libro.titulo == "Clean Code"
    assert libro.autor == "Robert Martin"


def test_str_representation():
    """Test del método __str__"""
    libro = Libro("123", "Python Crash Course", "Eric Matthes")
    assert str(libro) == "ISBN: 123 | Python Crash Course — Eric Matthes"


def test_repr_representation():
    """Test del método __repr__"""
    libro = Libro("123", "Python Crash Course", "Eric Matthes")
    expected = "Libro (isbn='123', titulo='Python Crash Course', autor='Eric Matthes')"
    assert repr(libro) == expected


def test_eq_mismo_isbn():
    """Test de igualdad por ISBN"""
    libro1 = Libro("123", "Titulo A", "Autor A")
    libro2 = Libro("123", "Titulo B", "Autor B")
    assert libro1 == libro2


def test_eq_distinto_isbn():
    """Test de desigualdad por ISBN"""
    libro1 = Libro("123", "Titulo A", "Autor A")
    libro2 = Libro("456", "Titulo A", "Autor A")
    assert libro1 != libro2


def test_hash_mismo_isbn():
    """Test que el hash depende solo del ISBN"""
    libro1 = Libro("123", "Titulo A", "Autor A")
    libro2 = Libro("123", "Titulo B", "Autor B")
    assert hash(libro1) == hash(libro2)


def test_isbn_inmutable():
    """Test que ISBN no puede modificarse después de creado"""
    libro = Libro("123", "Titulo", "Autor")
    with pytest.raises(AttributeError):
        libro.isbn = "456"


def test_titulo_setter():
    """Test del setter de título"""
    libro = Libro("123", "Titulo Original", "Autor")
    libro.titulo = "Nuevo Titulo"
    assert libro.titulo == "Nuevo Titulo"


def test_titulo_setter_tipo_incorrecto():
    """Test que el setter de título rechaza tipos incorrectos"""
    libro = Libro("123", "Titulo", "Autor")
    with pytest.raises(TypeError, match="Título debe ser una cadena de texto"):
        libro.titulo = 123


def test_autor_setter():
    """Test del setter de autor"""
    libro = Libro("123", "Titulo", "Autor Original")
    libro.autor = "Nuevo Autor"
    assert libro.autor == "Nuevo Autor"


def test_autor_setter_tipo_incorrecto():
    """Test que el setter de autor rechaza tipos incorrectos"""
    libro = Libro("123", "Titulo", "Autor")
    with pytest.raises(TypeError, match="Autor debe ser una cadena de texto"):
        libro.autor = 123


def test_titulo_setter_rechaza_tipos_incorrectos():
    """Test que el setter de título rechaza tipos incorrectos"""
    libro = Libro("123", "Titulo", "Autor")
    
    with pytest.raises(TypeError):
        libro.titulo = None
    
    with pytest.raises(TypeError):
        libro.titulo = [1, 2, 3]


def test_isbn_no_puede_ser_vacio():
    """Test que ISBN no puede ser vacío"""
    with pytest.raises(ValueError):
        Libro("", "Titulo", "Autor")