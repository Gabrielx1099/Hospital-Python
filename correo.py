from flask_mail import Message


def enviar_correo_confirmacion(app, mail, cita, asunto=None):
    """Envía correo HTML de confirmación al paciente. Retorna True si se envió."""
    if not app.config.get('MAIL_USERNAME') or not app.config.get('MAIL_PASSWORD'):
        app.logger.warning('Correo no configurado: faltan MAIL_USERNAME o MAIL_PASSWORD')
        return False

    paciente = cita.paciente
    medico = cita.medico
    especialidad = cita.especialidad

    if not asunto:
        asunto = f'Confirmación de cita — {especialidad.nombre}'

    html = f"""
    <html><body style="font-family:Arial,sans-serif;color:#1e293b;">
    <h2 style="color:#1a4b8c;">Hospital Carlos Lanfranco La Hoz</h2>
    <p>Estimado/a <strong>{paciente.nombre} {paciente.apellido}</strong>,</p>
    <p>Le informamos los detalles de su cita médica:</p>
    <table style="border-collapse:collapse;margin:16px 0;">
      <tr><td style="padding:6px 12px;font-weight:bold;">Especialidad:</td><td>{especialidad.nombre}</td></tr>
      <tr><td style="padding:6px 12px;font-weight:bold;">Médico:</td><td>Dr. {medico.nombre} {medico.apellido}</td></tr>
      <tr><td style="padding:6px 12px;font-weight:bold;">Fecha:</td><td>{cita.fecha.strftime('%d/%m/%Y')}</td></tr>
      <tr><td style="padding:6px 12px;font-weight:bold;">Hora:</td><td>{cita.hora}</td></tr>
      <tr><td style="padding:6px 12px;font-weight:bold;">Estado:</td><td>{cita.estado.capitalize()}</td></tr>
    </table>
    <p style="color:#64748b;font-size:0.9em;">Este es un mensaje automático. Por favor no responda a este correo.</p>
    </body></html>
    """

    msg = Message(
        subject=asunto,
        recipients=[paciente.email],
        html=html
    )

    try:
        mail.send(msg)
        return True
    except Exception as e:
        app.logger.error('Error al enviar correo de confirmación: %s', e)
        return False
