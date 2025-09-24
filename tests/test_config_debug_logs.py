# test_config_debug_logs.py
import unittest
import logging
import tempfile
import os
import sys
from unittest.mock import patch

# Añadir el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestConfigDebugLogs(unittest.TestCase):
    """
    Tests para verificar la configuración de logs DEBUG.
    """

    def setUp(self):
        """Limpiar loggers antes de cada test."""
        # Limpiar todos los handlers de loggers existentes
        for logger_name in list(logging.Logger.manager.loggerDict.keys()):
            logger = logging.getLogger(logger_name)
            logger.handlers.clear()
            logger.setLevel(logging.NOTSET)
        
        # Limpiar el logger raíz también
        root_logger = logging.getLogger()
        root_logger.handlers.clear()

    def test_debug_habilitado(self):
        """Test: DEBUG habilitado debe permitir logs DEBUG."""
        with patch('config.ENABLE_DEBUG_LOGS', True):
            with patch('config.MIN_LOG_LEVEL_WHEN_DEBUG_OFF', 'INFO'):
                # Reimportar logger para aplicar la configuración
                if 'logger' in sys.modules:
                    del sys.modules['logger']
                from logger import setup_logger
                
                test_logger = setup_logger("test_debug_on")
                
                # Verificar que el nivel es DEBUG
                self.assertEqual(test_logger.level, logging.DEBUG)
                self.assertTrue(test_logger.isEnabledFor(logging.DEBUG))

    def test_debug_deshabilitado_info(self):
        """Test: DEBUG deshabilitado con nivel INFO."""
        with patch('config.ENABLE_DEBUG_LOGS', False):
            with patch('config.MIN_LOG_LEVEL_WHEN_DEBUG_OFF', 'INFO'):
                # Reimportar logger para aplicar la configuración
                if 'logger' in sys.modules:
                    del sys.modules['logger']
                from logger import setup_logger
                
                test_logger = setup_logger("test_debug_off_info")
                
                # Verificar que el nivel es INFO
                self.assertEqual(test_logger.level, logging.INFO)
                self.assertFalse(test_logger.isEnabledFor(logging.DEBUG))
                self.assertTrue(test_logger.isEnabledFor(logging.INFO))

    def test_debug_deshabilitado_warning(self):
        """Test: DEBUG deshabilitado con nivel WARNING."""
        with patch('config.ENABLE_DEBUG_LOGS', False):
            with patch('config.MIN_LOG_LEVEL_WHEN_DEBUG_OFF', 'WARNING'):
                # Reimportar logger para aplicar la configuración
                if 'logger' in sys.modules:
                    del sys.modules['logger']
                from logger import setup_logger
                
                test_logger = setup_logger("test_debug_off_warning")
                
                # Verificar que el nivel es WARNING
                self.assertEqual(test_logger.level, logging.WARNING)
                self.assertFalse(test_logger.isEnabledFor(logging.DEBUG))
                self.assertFalse(test_logger.isEnabledFor(logging.INFO))
                self.assertTrue(test_logger.isEnabledFor(logging.WARNING))

    def test_debug_deshabilitado_error(self):
        """Test: DEBUG deshabilitado con nivel ERROR."""
        with patch('config.ENABLE_DEBUG_LOGS', False):
            with patch('config.MIN_LOG_LEVEL_WHEN_DEBUG_OFF', 'ERROR'):
                # Reimportar logger para aplicar la configuración
                if 'logger' in sys.modules:
                    del sys.modules['logger']
                from logger import setup_logger
                
                test_logger = setup_logger("test_debug_off_error")
                
                # Verificar que el nivel es ERROR
                self.assertEqual(test_logger.level, logging.ERROR)
                self.assertFalse(test_logger.isEnabledFor(logging.DEBUG))
                self.assertFalse(test_logger.isEnabledFor(logging.INFO))
                self.assertFalse(test_logger.isEnabledFor(logging.WARNING))
                self.assertTrue(test_logger.isEnabledFor(logging.ERROR))

    def test_config_inexistente(self):
        """Test: Comportamiento cuando no existe config.py."""
        # Simular que no existe config.py
        with patch.dict('sys.modules', {'config': None}):
            if 'logger' in sys.modules:
                del sys.modules['logger']
            
            # Debería usar valores por defecto
            from logger import setup_logger
            test_logger = setup_logger("test_no_config")
            
            # Por defecto debería ser DEBUG habilitado
            self.assertEqual(test_logger.level, logging.DEBUG)

    def tearDown(self):
        """Limpiar después de cada test."""
        # Limpiar módulos importados para evitar interferencias
        modules_to_clean = ['logger']
        for module in modules_to_clean:
            if module in sys.modules:
                del sys.modules[module]


if __name__ == "__main__":
    unittest.main()
