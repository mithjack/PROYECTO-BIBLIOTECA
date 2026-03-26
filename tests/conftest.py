import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from biblioteca import Biblioteca


@pytest.fixture(autouse=True)
def limpiar_singleton():
    """Limpia la instancia Singleton antes y después de cada test"""
    # Guardar la instancia original si existe
    instancia_original = getattr(Biblioteca, '_instancia', None)
    
    # Resetear la instancia
    Biblioteca._instancia = None
    
    yield
    
    # Restaurar la instancia original después del test (opcional)
    # Biblioteca._instancia = instancia_original
    # Mejor dejar None para evitar interferencias
    Biblioteca._instancia = None