import base64
import hashlib
from Crypto.Cipher import AES
import sys
import os

# Aadir el directorio padre al path para importar logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger import setup_logger

# Configurar logger especfico para este mdulo
logger = setup_logger("DecryptCSharp")

def decrypt_aes_csharp(encrypted_b64: str, key_value: str) -> str:
    """
    Desencripta el texto cifrado con el mismo mtodo que tu Encrypt/Decrypt en C#:
      1) SHA-512 sobre key_value  password_bytes
      2) PBKDF2-HMAC-SHA512 (salt=[1,2,3,4,5,6,7,8], iter=1000)  48 bytes
         - primeros 32 bytes = AES key (256 bits)
         - siguientes 16 bytes = AES IV (128 bits)
      3) AES-CBC + PKCS7 padding
    """
    logger.debug(" Iniciando proceso de desencriptacin AES")
    
    try:
        # 1) Base64  bytes cifrados
        logger.debug(" Decodificando texto cifrado desde Base64")
        cipher_bytes = base64.b64decode(encrypted_b64)
        
        # 2) SHA-512 de la Key
        logger.debug(" Generando hash SHA-512 de la clave")
        password_bytes = hashlib.sha512(key_value.encode('utf-8')).digest()
        
        # 3) Derivar key+iv con PBKDF2-HMAC-SHA512
        logger.debug(" Derivando clave e IV con PBKDF2-HMAC-SHA512")
        salt = bytes([1, 2, 3, 4, 5, 6, 7, 8])
        derived = hashlib.pbkdf2_hmac(
            'sha512',
            password_bytes,
            salt,
            1000,
            dklen=48
        )
        key = derived[:32]
        iv  = derived[32:48]
        
        # 4) AES-CBC decrypt
        logger.debug(" Aplicando desencriptacin AES-CBC")
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded = cipher.decrypt(cipher_bytes)
        
        # 5) Quitar padding PKCS7
        logger.debug(" Removiendo padding PKCS7")
        pad_len = padded[-1]
        if not 1 <= pad_len <= AES.block_size:
            logger.error(f" Padding invlido ({pad_len})")
            raise ValueError(f"Padding invlido ({pad_len})")
        plaintext = padded[:-pad_len]
        
        logger.debug(" Desencriptacin completada exitosamente")
        return plaintext.decode('utf-8')
        
    except Exception as e:
        logger.error(f" Error durante la desencriptacin: {e}")
        raise


if __name__ == '__main__':
    logger.info(" Ejecutando prueba de desencriptacin")
    ejemplo = "GJNZHDycfmk6C7Ubv/EHUg=="
    key     = "3NcR1p+¡OnP4s$W0rDN@m3k3yV@lv3C0mP4NYC|B3RG3$+!0NM0DVL0|CB4CK3NDW3B"
    resultado = decrypt_aes_csharp(ejemplo, key)
    logger.info(f" Texto desencriptado: {resultado}")
