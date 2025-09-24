# test_validacion_correo_juzgado.py
import unittest
import sys
import os

# Añadir el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.processing_service import _validar_email


class TestValidacionCorreoJuzgado(unittest.TestCase):
    """
    Tests para verificar la validación de correos del juzgado.
    """

    def test_emails_validos(self):
        """Test: Emails con formato válido."""
        emails_validos = [
            "juzgado@ejemplo.com",
            "test.email@domain.co",
            "usuario+tag@dominio.org",
            "correo123@test-domain.com",
            "admin@sub.domain.gov.co"
        ]
        
        for email in emails_validos:
            with self.subTest(email=email):
                self.assertTrue(_validar_email(email), f"Email válido rechazado: {email}")

    def test_emails_invalidos(self):
        """Test: Emails con formato inválido."""
        emails_invalidos = [
            "NO ESPECIFICADO",
            "null",
            "NONE",
            "",
            "   ",
            "email_sin_arroba.com",
            "@dominio.com",
            "usuario@",
            "usuario@dominio",
            "usuario@.com",
            "usuario@dominio.",
            "usuario espacios@dominio.com",
            None
        ]
        
        for email in emails_invalidos:
            with self.subTest(email=email):
                self.assertFalse(_validar_email(email), f"Email inválido aceptado: {email}")

    def test_emails_con_espacios(self):
        """Test: Emails válidos con espacios al inicio/final."""
        emails_con_espacios = [
            "  correo@dominio.com  ",
            "\tjuzgado@ejemplo.org\n",
            " admin@test.co "
        ]
        
        for email in emails_con_espacios:
            with self.subTest(email=email):
                self.assertTrue(_validar_email(email), f"Email válido con espacios rechazado: '{email}'")

    def test_casos_especiales(self):
        """Test: Casos especiales que deben ser rechazados."""
        casos_especiales = [
            "NO ESPECIFICADO",
            "no especificado",
            "NULL",
            "null",
            "NONE",
            "none",
            123,  # Número
            [],   # Lista vacía
            {}    # Diccionario vacío
        ]
        
        for caso in casos_especiales:
            with self.subTest(caso=caso):
                self.assertFalse(_validar_email(caso), f"Caso especial aceptado incorrectamente: {caso}")


if __name__ == "__main__":
    unittest.main()
