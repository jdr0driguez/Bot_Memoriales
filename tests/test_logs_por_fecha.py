# test_logs_por_fecha.py
import unittest
import tempfile
import os
import sys
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import shutil

# Añadir el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestLogsPorFecha(unittest.TestCase):
    """
    Tests para verificar la organización de logs por carpetas de fecha.
    """

    def setUp(self):
        """Configurar entorno de test."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_logs_base_dir = None

    def tearDown(self):
        """Limpiar después de cada test."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        
        # Limpiar módulos importados
        modules_to_clean = ['logger']
        for module in modules_to_clean:
            if module in sys.modules:
                del sys.modules[module]

    def test_formato_fecha_carpeta(self):
        """Test: Verificar formato de fecha DDMMAAAA."""
        with patch('logger.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 9, 24, 10, 30, 0)
            mock_datetime.strftime = datetime.strftime
            
            from logger import _get_fecha_carpeta
            
            fecha = _get_fecha_carpeta()
            self.assertEqual(fecha, "24092025")

    def test_get_log_dir_for_date(self):
        """Test: Verificar generación de directorio para fecha específica."""
        with patch('logger.LOGS_BASE_DIR', self.temp_dir):
            from logger import _get_log_dir_for_date
            
            log_dir = _get_log_dir_for_date("24092025")
            expected_path = os.path.join(self.temp_dir, "24092025")
            
            self.assertEqual(log_dir, expected_path)

    def test_ensure_log_dir_exists(self):
        """Test: Verificar creación de directorio de logs."""
        from logger import _ensure_log_dir_exists
        
        test_dir = os.path.join(self.temp_dir, "24092025")
        self.assertFalse(os.path.exists(test_dir))
        
        _ensure_log_dir_exists(test_dir)
        self.assertTrue(os.path.exists(test_dir))

    def test_get_carpetas_logs_antiguas(self):
        """Test: Identificar carpetas de logs antiguas."""
        with patch('logger.LOGS_BASE_DIR', self.temp_dir):
            # Crear carpetas de diferentes fechas
            fecha_hoy = datetime.now()
            fecha_ayer = fecha_hoy - timedelta(days=1)
            fecha_hace_8_dias = fecha_hoy - timedelta(days=8)
            fecha_hace_15_dias = fecha_hoy - timedelta(days=15)
            
            carpeta_hoy = fecha_hoy.strftime("%d%m%Y")
            carpeta_ayer = fecha_ayer.strftime("%d%m%Y")
            carpeta_8_dias = fecha_hace_8_dias.strftime("%d%m%Y")
            carpeta_15_dias = fecha_hace_15_dias.strftime("%d%m%Y")
            
            # Crear las carpetas
            for carpeta in [carpeta_hoy, carpeta_ayer, carpeta_8_dias, carpeta_15_dias]:
                os.makedirs(os.path.join(self.temp_dir, carpeta))
            
            # También crear una carpeta con formato incorrecto
            os.makedirs(os.path.join(self.temp_dir, "invalid_format"))
            
            from logger import _get_carpetas_logs_antiguas
            
            # Mantener 7 días
            carpetas_antiguas = _get_carpetas_logs_antiguas(7)
            
            # Solo la carpeta de hace 8 y 15 días deberían estar marcadas para eliminación
            carpetas_nombres = [os.path.basename(path) for path in carpetas_antiguas]
            
            self.assertIn(carpeta_8_dias, carpetas_nombres)
            self.assertIn(carpeta_15_dias, carpetas_nombres)
            self.assertNotIn(carpeta_hoy, carpetas_nombres)
            self.assertNotIn(carpeta_ayer, carpetas_nombres)
            self.assertNotIn("invalid_format", carpetas_nombres)

    def test_get_carpetas_logs_antiguas_sin_limpieza(self):
        """Test: No limpiar cuando días_mantener es 0."""
        from logger import _get_carpetas_logs_antiguas
        
        carpetas_antiguas = _get_carpetas_logs_antiguas(0)
        self.assertEqual(len(carpetas_antiguas), 0)

    def test_limpiar_logs_antiguos_deshabilitado(self):
        """Test: No limpiar cuando está deshabilitado en config."""
        with patch('logger.ENABLE_AUTO_CLEANUP_LOGS', False):
            with patch('logger.DIAS_LOGS_MANTENER', 7):
                from logger import _limpiar_logs_antiguos
                
                # No debería hacer nada
                _limpiar_logs_antiguos()  # No debe lanzar excepción

    def test_formato_fecha_invalido(self):
        """Test: Ignorar carpetas con formato de fecha inválido."""
        with patch('logger.LOGS_BASE_DIR', self.temp_dir):
            # Crear carpetas con formatos inválidos
            carpetas_invalidas = ["invalid", "12345678", "abcd1234", "1234abcd", ""]
            
            for carpeta in carpetas_invalidas:
                if carpeta:  # No crear carpeta vacía
                    os.makedirs(os.path.join(self.temp_dir, carpeta))
            
            from logger import _get_carpetas_logs_antiguas
            
            carpetas_antiguas = _get_carpetas_logs_antiguas(1)
            
            # No debería encontrar ninguna carpeta válida para eliminar
            self.assertEqual(len(carpetas_antiguas), 0)


if __name__ == "__main__":
    unittest.main()
