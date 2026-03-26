# tests/test_3_usuario_avanzado.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import date
import pytest
from usuario import Usuario


@pytest.fixture
def usuario_basico():
    return Usuario(1, "Ana", max_prestamos=2)


def test_usuario_basico():
    usuario = Usuario(1, "Ana", max_prestamos=2)
    assert usuario.id == 1
    assert usuario.nombre == "Ana"
    assert usuario.max_prestamos == 2


def test_limite_prestamos_positivo():
    with pytest.raises(ValueError, match="positivo"):
        Usuario(1, "Ana", max_prestamos=0)


def test_usuario_no_gestiona_prestamos():
    usuario = Usuario(1, "Ana")
    assert not hasattr(usuario, "prestamos")
    assert not hasattr(usuario, "prestar")


def test_creacion_usuario_con_valores_validos():
    """Test de creación con valores válidos"""
    usuario = Usuario(5, "María", 3)
    assert usuario.id == 5
    assert usuario.nombre == "María"
    assert usuario.max_prestamos == 3


def test_creacion_usuario_max_prestamos_por_defecto():
    """Test que max_prestamos por defecto es 1"""
    usuario = Usuario(1, "Ana")
    assert usuario.max_prestamos == 1


def test_max_prestamos_no_puede_ser_cero():
    """Test que max_prestamos no puede ser 0"""
    with pytest.raises(ValueError, match="positivo"):
        Usuario(1, "Ana", max_prestamos=0)


def test_max_prestamos_no_puede_ser_negativo():
    """Test que max_prestamos no puede ser negativo"""
    with pytest.raises(ValueError, match="positivo"):
        Usuario(1, "Ana", max_prestamos=-5)


def test_str_representation(usuario_basico):
    """Test del método __str__"""
    assert str(usuario_basico) == "ID: 1 | Ana — 2 prestamos maximos"


def test_nombre_setter(usuario_basico):
    """Test del setter de nombre"""
    usuario_basico.nombre = "Ana María"
    assert usuario_basico.nombre == "Ana María"


def test_nombre_setter_tipo_incorrecto(usuario_basico):
    """Test que el setter de nombre rechaza tipos incorrectos"""
    with pytest.raises(TypeError, match="Nombre debe ser una cadena de texto"):
        usuario_basico.nombre = 123


def test_max_prestamos_setter(usuario_basico):
    """Test del setter de max_prestamos"""
    usuario_basico.max_prestamos = 5
    assert usuario_basico.max_prestamos == 5


def test_max_prestamos_setter_tipo_incorrecto(usuario_basico):
    """Test que el setter de max_prestamos rechaza tipos incorrectos"""
    with pytest.raises(TypeError, match="max_prestamos debe ser int"):
        usuario_basico.max_prestamos = "cinco"


def test_id_inmutable(usuario_basico):
    """Test que el ID no puede modificarse después de creado"""
    with pytest.raises(AttributeError):
        usuario_basico.id = 99


def test_call_method():
    """Test del método __call__ para préstamo directo"""
    from unittest.mock import Mock
    
    mock_biblioteca = Mock()
    mock_biblioteca.prestar_libro.return_value = "Préstamo creado"
    
    usuario = Usuario(1, "Ana", 2)
    resultado = usuario(mock_biblioteca, "123", date(2025, 3, 1), dias_maximos=7)
    
    mock_biblioteca.prestar_libro.assert_called_once_with(
        isbn="123",
        usuario_id=1,
        fecha=date(2025, 3, 1),
        dias_maximos=7
    )
    assert resultado == "Préstamo creado"


def test_call_method_con_dias_por_defecto():
    """Test del método __call__ con días por defecto"""
    from unittest.mock import Mock
    
    mock_biblioteca = Mock()
    mock_biblioteca.prestar_libro.return_value = "Préstamo creado"
    
    usuario = Usuario(1, "Ana", 2)
    resultado = usuario(mock_biblioteca, "123", date(2025, 3, 1))
    
    mock_biblioteca.prestar_libro.assert_called_once_with(
        isbn="123",
        usuario_id=1,
        fecha=date(2025, 3, 1),
        dias_maximos=7
    )
    assert resultado == "Préstamo creado"


def test_usuario_no_tiene_atributo_prestamos(usuario_basico):
    """Test que el usuario no gestiona préstamos directamente"""
    assert not hasattr(usuario_basico, "prestamos")
    assert not hasattr(usuario_basico, "prestar")
    assert not hasattr(usuario_basico, "prestamos_activos")