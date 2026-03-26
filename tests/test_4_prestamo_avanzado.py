# tests/test_prestamo_avanzado.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import date, timedelta
import pytest
from libro import Libro
from usuario import Usuario
from prestamo import Prestamo


@pytest.fixture
def libro():
    return Libro("123", "Python Avanzado", "Autor")


@pytest.fixture
def usuario():
    return Usuario(1, "Carlos", 3)


@pytest.fixture
def prestamo_activo(libro, usuario):
    return Prestamo(libro, usuario, date(2025, 3, 1), dias_maximos=7)


def test_creacion_prestamo_dias_por_defecto(libro, usuario):
    """Test de creación con días por defecto (7)"""
    prestamo = Prestamo(libro, usuario, date(2025, 3, 1))
    assert prestamo._dias_maximos == 7


def test_creacion_prestamo_dias_personalizados(libro, usuario):
    """Test de creación con días personalizados"""
    prestamo = Prestamo(libro, usuario, date(2025, 3, 1), dias_maximos=14)
    assert prestamo._dias_maximos == 14


def test_creacion_prestamo_dias_cero(libro, usuario):
    """Test que rechaza días máximos = 0"""
    with pytest.raises(ValueError, match="positivos"):
        Prestamo(libro, usuario, date(2025, 3, 1), dias_maximos=0)


def test_str_prestamo_activo(prestamo_activo):
    """Test de representación string con préstamo activo"""
    assert "alquiler activo" in str(prestamo_activo)
    assert "Python Avanzado" in str(prestamo_activo)
    assert "Carlos" in str(prestamo_activo)


def test_str_prestamo_devuelto(prestamo_activo):
    """Test de representación string con préstamo devuelto"""
    prestamo_activo.devolver(date(2025, 3, 5))
    assert "devuelto el:" in str(prestamo_activo)
    assert "2025-03-05" in str(prestamo_activo)


def test_esta_activo_inicialmente(prestamo_activo):
    """Test que préstamo está activo al inicio"""
    assert prestamo_activo.esta_activo() is True


def test_esta_activo_despues_devolucion(prestamo_activo):
    """Test que préstamo no está activo después de devolver"""
    prestamo_activo.devolver(date(2025, 3, 5))
    assert prestamo_activo.esta_activo() is False


def test_esta_vencido_dentro_plazo(prestamo_activo):
    """Test que préstamo no está vencido dentro del plazo"""
    fecha_devolucion = date(2025, 3, 5)  # 4 días después
    assert prestamo_activo.esta_vencido(fecha_devolucion) is False


def test_esta_vencido_justo_en_plazo(prestamo_activo):
    """Test que préstamo no está vencido el último día"""
    fecha_devolucion = date(2025, 3, 8)  # 7 días después
    assert prestamo_activo.esta_vencido(fecha_devolucion) is False


def test_esta_vencido_fuera_plazo(prestamo_activo):
    """Test que préstamo está vencido fuera del plazo"""
    fecha_devolucion = date(2025, 3, 9)  # 8 días después (1 día retraso)
    assert prestamo_activo.esta_vencido(fecha_devolucion) is True


def test_calcular_multa_sin_retraso(prestamo_activo):
    """Test multa = 0 cuando no hay retraso"""
    assert prestamo_activo.calcular_multa(date(2025, 3, 5)) == 0


def test_calcular_multa_un_dia_retraso(prestamo_activo):
    """Test multa por 1 día de retraso"""
    assert prestamo_activo.calcular_multa(date(2025, 3, 9)) == 0.25  # 1 día


def test_calcular_multa_varios_dias_retraso(prestamo_activo):
    """Test multa por múltiples días de retraso"""
    assert prestamo_activo.calcular_multa(date(2025, 3, 15)) == 7 * 0.25  # 7 días


def test_devolver_antes_del_plazo(prestamo_activo):
    """Test devolución antes del plazo"""
    fecha_devolucion = date(2025, 3, 4)  # 3 días después
    prestamo_activo.devolver(fecha_devolucion)
    
    assert prestamo_activo.esta_activo() is False
    assert prestamo_activo._devolucion == fecha_devolucion
    assert prestamo_activo.calcular_multa(fecha_devolucion) == 0


def test_devolver_exactamente_el_plazo(prestamo_activo):
    """Test devolución el último día"""
    fecha_devolucion = date(2025, 3, 8)  # 7 días después
    prestamo_activo.devolver(fecha_devolucion)
    
    assert prestamo_activo.esta_activo() is False
    assert prestamo_activo.calcular_multa(fecha_devolucion) == 0


def test_devolver_con_retraso(prestamo_activo):
    """Test devolución con retraso"""
    fecha_devolucion = date(2025, 3, 10)  # 9 días después (2 días retraso)
    prestamo_activo.devolver(fecha_devolucion)
    
    assert prestamo_activo.esta_activo() is False
    assert prestamo_activo.calcular_multa(fecha_devolucion) == 0.50


def test_no_puede_devolver_dos_veces(prestamo_activo):
    """Test que no se puede devolver un libro dos veces"""
    prestamo_activo.devolver(date(2025, 3, 5))
    
    with pytest.raises(RuntimeError, match="No hay que devolverlo"):
        prestamo_activo.devolver(date(2025, 3, 6))


def test_multa_constante_clase():
    """Test que la constante MULTA_DIARIA existe y es correcta"""
    assert hasattr(Prestamo, 'MULTA_DIARIA')
    assert Prestamo.MULTA_DIARIA == 0.25