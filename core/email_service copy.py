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

# Aadir el directorio padre al path para importar logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger import setup_logger

# Configurar logger especfico para este mdulo
logger = setup_logger("EmailService")

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
    attachment_path: Optional[str] = None   # <- ahora es opcional
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

    # Creamos un multipart/mixed para adjuntos y contenido
    msg = MIMEMultipart('mixed')
    msg["From"] = user
    msg["Subject"] = subject

    # Procesar destinatarios
    to_list = [addr.strip() for addr in to.split(",") if addr.strip()]
    msg["To"] = ", ".join(to_list)
    recipients = to_list.copy()
    cc_list = []
    if cc:
        cc_list = [addr.strip() for addr in cc.split(",") if addr.strip()]
        msg["Cc"] = ", ".join(cc_list)
        recipients += cc_list
    
    logger.debug(f" Destinatarios: To={to_list}, Cc={cc_list if cc else 'None'}")

    if cuerpoCorreo:
        logger.debug(" Agregando cuerpo del correo HTML")
        alternative = MIMEMultipart('alternative')
        alternative.attach(MIMEText("Este mensaje necesita un cliente que soporte HTML.", 'plain'))
        alternative.attach(MIMEText(cuerpoCorreo, 'html'))
        msg.attach(alternative)

    # Adjuntar archivo solo si attachment_path fue pasado
    if attachment_path:
        path = Path(attachment_path)
        if not path.exists() or not path.is_file():
            logger.error(f" No existe el archivo para adjuntar: {attachment_path}")
            raise FileNotFoundError(f"No existe el archivo para adjuntar: {attachment_path}")

        logger.debug(f" Adjuntando archivo: {path.name}")
        with path.open("rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{path.name}"')
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
            f" Correo enviado exitosamente vía {smtp_server} para {expediente}  To={to_list}, "
            f"Cc={cc}, Attachment={'Ninguno' if not attachment_path else Path(attachment_path).name}"
        )
    except Exception as e:
        logger.error(f" Error al enviar correo para {expediente}: {e}")
        raise