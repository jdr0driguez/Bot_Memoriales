# test_limpieza_archivos.py
import unittest
import tempfile
import os
from pathlib import Path
import sys

# Añadir el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.processing_service import _limpiar_archivo_local


class TestLimpiezaArchivos(unittest.TestCase):
    """
    Tests para verificar la funcionalidad de limpieza automática de archivos.
    """

    def test_limpiar_archivo_existente(self):
        """Test: Eliminar un archivo que existe."""
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
            temp_file.write(b"contenido de prueba")
        
        # Verificar que el archivo existe
        self.assertTrue(Path(temp_path).exists())
        
        # Limpiar archivo
        _limpiar_archivo_local(temp_path)
        
        # Verificar que el archivo fue eliminado
        self.assertFalse(Path(temp_path).exists())

    def test_limpiar_archivo_inexistente(self):
        """Test: Intentar eliminar un archivo que no existe (no debe fallar)."""
        archivo_inexistente = "/ruta/inexistente/archivo.pdf"
        
        # No debe lanzar excepción
        try:
            _limpiar_archivo_local(archivo_inexistente)
            resultado = True
        except Exception:
            resultado = False
        
        self.assertTrue(resultado, "La función debe manejar archivos inexistentes sin fallar")

    def test_limpiar_archivo_vacio(self):
        """Test: Pasar None o string vacío (no debe fallar)."""
        # No debe lanzar excepción con None
        try:
            _limpiar_archivo_local(None)
            _limpiar_archivo_local("")
            _limpiar_archivo_local("   ")
            resultado = True
        except Exception:
            resultado = False
        
        self.assertTrue(resultado, "La función debe manejar valores vacíos sin fallar")

    def test_limpiar_directorio(self):
        """Test: Intentar eliminar un directorio (no debe eliminarlo)."""
        # Crear directorio temporal
        with tempfile.TemporaryDirectory() as temp_dir:
            # Intentar "limpiar" el directorio
            _limpiar_archivo_local(temp_dir)
            
            # El directorio debe seguir existiendo
            self.assertTrue(Path(temp_dir).exists())


if __name__ == "__main__":
    unittest.main()
