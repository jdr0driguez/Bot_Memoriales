import smtplib
import logging
from pathlib import Path
from typing import Optional
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import email.encoders as encoders
import sys
import os
import re
import unicodedata
import mimetypes

# Añadir el directorio padre al path para importar logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger import setup_logger

# Configurar logger específico para este módulo
logger = setup_logger("EmailService")


# ---------- Utilidades de normalización para adjuntos ----------
def _strip_diacritics(text: str) -> str:
    """Quita tildes/diacríticos (ñ -> n, ü -> u, etc.)."""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in nfkd if not unicodedata.combining(ch))


def _sanitize_for_email_filename(text: str) -> str:
    """
    Versión conservadora para encabezados de email:
    - permite letras, números, -, _, ., ( )
    - convierte espacios a _
    - contrae múltiples _ y elimina extremos
    """
    text = text.replace(" ", "_")
    text = re.sub(r"[^A-Za-z0-9_.()\-]", "_", text)
    text = re.sub(r"_+", "_", text).strip("._ ")
    return text or "archivo"


def _normalize_email_filename(filename: str) -> str:
    """
    Normaliza un nombre de archivo para usar en headers MIME:
    - quita diacríticos/emoji
    - conserva extensión (si existe)
    - deja solo ASCII seguro para evitar 'no name' / '.bin'
    """
    stem, ext = os.path.splitext(filename)
    stem = _strip_diacritics(stem)
    ext  = _strip_diacritics(ext)
    safe_stem = _sanitize_for_email_filename(stem)
    safe_ext  = _sanitize_for_email_filename(ext)
    # asegurar que la "extensión" siga teniendo punto si existe
    if safe_ext and not safe_ext.startswith("."):
        safe_ext = "." + safe_ext
    return (safe_stem or "archivo") + (safe_ext if safe_ext else "")


def _guess_mime(path: Path) -> tuple[str, str]:
    """
    Detecta el MIME type del archivo; fallback a application/octet-stream.
    """
    ctype, _enc = mimetypes.guess_type(str(path))
    if not ctype:
        return "application", "octet-stream"
    maintype, subtype = ctype.split("/", 1)
    return maintype, subtype
# ---------------------------------------------------------------


def send_email_with_attachment(
    expediente: str,
    docDemandado: str,
    nomDemandado: str,
    radicado: str,
    nomPlantilla: str,
    mailFrom: str,
    passFrom: str,
    to: str,
    cc: Optional[str],
    cuerpoCorreo: Optional[str],
    attachment_path: Optional[str] = None,   # <- opcional
    bcc: Optional[str] = None   # <- copia oculta
) -> None:
    logger.info(f" Iniciando envío de correo para expediente: {expediente}")

    if not expediente:
        logger.error(" El campo 'expediente' no puede estar vacío")
        raise ValueError("El campo 'expediente' no puede estar vacío")

    provider = expediente[0].upper()
    if provider == "L":
        smtp_server, smtp_port = "smtp.gmail.com", 587
        user, password = mailFrom, passFrom
        logger.debug(f" Configurando Gmail SMTP: {smtp_server}:{smtp_port}")
    elif provider == "A":
        smtp_server, smtp_port = "smtp.office365.com", 587
        user, password = mailFrom, passFrom
        logger.debug(f" Configurando Office365 SMTP: {smtp_server}:{smtp_port}")
    else:
        logger.error(f" Proveedor no reconocido: {provider}")
        raise ValueError("Proveedor no reconocido: expediente debe empezar por 'L' o 'A'")

    if not user or not password:
        logger.error(f" Credenciales de {provider!r} no configuradas")
        raise RuntimeError(f"Credenciales de {provider!r} no configuradas en variables de entorno")

    subject = f"{docDemandado}_{nomDemandado}_{radicado}_{nomPlantilla}"
    logger.debug(f" Asunto del correo: {subject}")

    # multipart/mixed para adjuntos + contenido
    msg = MIMEMultipart('mixed')
    msg["From"] = user
    msg["Subject"] = subject

    # Destinatarios
    to_list = [addr.strip() for addr in to.split(",") if addr.strip()]
    msg["To"] = ", ".join(to_list)
    recipients = to_list.copy()
    cc_list = []
    if cc:
        cc_list = [addr.strip() for addr in cc.split(",") if addr.strip()]
        msg["Cc"] = ", ".join(cc_list)
        recipients += cc_list
    
    # Copia oculta (BCC) - se agregan a recipients pero NO al header
    bcc_list = []
    if bcc:
        bcc_list = [addr.strip() for addr in bcc.split(";") if addr.strip()]
        recipients += bcc_list

    logger.debug(
        f" Destinatarios: To={to_list}, Cc={cc_list if cc else 'None'}, "
        f"Bcc={bcc_list if bcc else 'None'}"
    )

    if cuerpoCorreo:
        logger.debug(" Agregando cuerpo del correo HTML")
        alternative = MIMEMultipart('alternative')
        alternative.attach(MIMEText("Este mensaje necesita un cliente que soporte HTML.", 'plain'))
        alternative.attach(MIMEText(cuerpoCorreo, 'html'))
        msg.attach(alternative)

    # Adjuntar archivo (normalizando SOLO el nombre que viaja en el correo)
    if attachment_path:
        path = Path(attachment_path)
        if not path.exists() or not path.is_file():
            logger.error(f" No existe el archivo para adjuntar: {attachment_path}")
            raise FileNotFoundError(f"No existe el archivo para adjuntar: {attachment_path}")

        # Nombre seguro para el header MIME (ASCII, sin tildes/ñ)
        original_name = path.name
        safe_name = _normalize_email_filename(original_name)
        logger.debug(f" Adjuntando archivo: original='{original_name}' -> enviado como='{safe_name}'")

        maintype, subtype = _guess_mime(path)
        with path.open("rb") as f:
            part = MIMEBase(maintype, subtype)
            part.set_payload(f.read())

        encoders.encode_base64(part)

        # Header Content-Disposition con nombre normalizado (seguro)
        # Si prefieres enviar UTF-8 RFC2231 (y no normalizar), reemplaza safe_name por:
        #   ("utf-8", "", original_name)
        part.add_header("Content-Disposition", "attachment", filename=safe_name)

        # También incluimos el "name" en Content-Type por compatibilidad con algunos clientes
        part.set_param("name", safe_name, header="Content-Type")

        msg.attach(part)
    else:
        logger.info(" Enviando correo SIN adjunto")

    # Envío
    try:
        logger.info(f" Conectando a {smtp_server}:{smtp_port}")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()
            logger.debug(" Autenticando con el servidor SMTP")
            server.login(user, password)
            logger.debug(" Enviando correo")
            server.sendmail(user, recipients, msg.as_string())

        logger.info(
            f" Correo enviado exitosamente vía {smtp_server} para {expediente}  "
            f"To={to_list}, Cc={cc}, Bcc={bcc if bcc else 'None'}, "
            f"Attachment={'Ninguno' if not attachment_path else Path(attachment_path).name}"
        )
    except Exception as e:
        logger.error(f" Error al enviar correo para {expediente}: {e}")
        raise
