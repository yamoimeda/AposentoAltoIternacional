import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#4F46E5")) # Indigo
            self.drawString(40, 762, "EL APOSENTO ALTO INTERNACIONAL")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B")) # Slate 500
            self.drawString(205, 762, "•  Manual y Guía de Uso del Portal Web")
            
            # Subtle top border line
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.75)
            self.line(40, 755, 572, 755)
            self.restoreState()

        # Footer (all pages)
        self.saveState()
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(40, 42, 572, 42)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(40, 30, "El Aposento Alto Internacional © 2026 — Plataforma Oficial")
        
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(572, 30, page_str)
        self.restoreState()


def create_colored_card(title, content_paras, bg_color="#F8FAFC", border_color="#E2E8F0", title_color="#1E293B"):
    elems = []
    if title:
        title_p = Paragraph(f"<b>{title}</b>", ParagraphStyle(
            'CardTitle',
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor(title_color)
        ))
        elems.append(title_p)
        elems.append(Spacer(1, 4))
    
    for p in content_paras:
        if isinstance(p, str):
            elems.append(Paragraph(p, ParagraphStyle(
                'CardText',
                fontName='Helvetica',
                fontSize=9,
                leading=13,
                textColor=colors.HexColor("#334155")
            )))
        else:
            elems.append(p)
        elems.append(Spacer(1, 3))
    
    # Remove last spacer
    if elems:
        elems.pop()

    t = Table([[elems]], colWidths=[532])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_color)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(border_color)),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    return t


def build_tutorial_pdf(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=50,
        bottomMargin=55
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=colors.HexColor("#0F172A"),
        alignment=0
    )
    
    style_cover_subtitle = ParagraphStyle(
        'CoverSubtitle',
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#4F46E5"),
        alignment=0
    )

    style_h1 = ParagraphStyle(
        'Header1',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#1E1B4B"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'Header2',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#3730A3"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )

    style_bullet = ParagraphStyle(
        'Bullet',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#334155"),
        leftIndent=15,
        spaceAfter=3
    )

    style_tip = ParagraphStyle(
        'TipText',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#1E3A8A")
    )

    story = []

    # =========================================================================
    # PORTADA / ENCABEZADO PRINCIPAL
    # =========================================================================
    
    # Header badge & title block
    badge_table = Table([[
        Paragraph("<b>GUÍA OFICIAL • TUTORIAL PASO A PASO</b>", ParagraphStyle(
            'Badge', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.HexColor("#4338CA")
        ))
    ]], colWidths=[200])
    badge_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EEF2FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#C7D2FE")),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ]))
    
    story.append(badge_table)
    story.append(Spacer(1, 8))
    story.append(Paragraph("Manual de Usuario de la Aplicación", style_cover_title))
    story.append(Spacer(1, 3))
    story.append(Paragraph("El Aposento Alto Internacional — Todo lo que necesitas saber de forma sencilla", style_cover_subtitle))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#4F46E5"), spaceAfter=12))

    # Bienvenida amigable
    intro_card = create_colored_card(
        "👋 ¡Bienvenido a nuestra plataforma web!",
        [
            "Esta guía práctica ha sido diseñada pensando en ti. Con un lenguaje claro, sencillo y directo, aprenderás a sacarle el máximo provecho a la plataforma de <b>El Aposento Alto Internacional</b>.",
            "Ya sea que quieras <b>inscribirte a una conferencia o retiro</b>, <b>descargar tu pase de entrada QR</b>, <b>conocer nuestras actividades</b> o <b>gestionar eventos como administrador</b>, aquí encontrarás el paso a paso detallado."
        ],
        bg_color="#F8FAFC",
        border_color="#CBD5E1",
        title_color="#0F172A"
    )
    story.append(intro_card)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECCIÓN 1: ESTRUCTURA Y NAVEGACIÓN
    # =========================================================================
    story.append(Paragraph("1. ¿Qué puedes hacer en la aplicación?", style_h1))
    story.append(Paragraph(
        "La web está organizada para que encuentres todo en pocos clics, tanto desde tu computadora como desde tu teléfono celular:",
        style_body
    ))

    # Tabla resumen de secciones
    sections_data = [
        [
            Paragraph("<b>Sección</b>", ParagraphStyle('TH1', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white)),
            Paragraph("<b>¿Para qué sirve?</b>", ParagraphStyle('TH2', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white)),
            Paragraph("<b>¿Quién la usa?</b>", ParagraphStyle('TH3', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white))
        ],
        [
            Paragraph("<b>Inicio</b>", ParagraphStyle('TB1', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor("#1E293B"))),
            Paragraph("Conoce las próximas actividades destacadas, horarios e información general de la iglesia.", ParagraphStyle('TB2', fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor("#475569"))),
            Paragraph("Todos los visitantes", ParagraphStyle('TB3', fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor("#4F46E5")))
        ],
        [
            Paragraph("<b>Eventos</b>", ParagraphStyle('TB1', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor("#1E293B"))),
            Paragraph("Explora el catálogo de conferencias, retiros y talleres disponibles con fechas, costos y cupos.", ParagraphStyle('TB2', fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor("#475569"))),
            Paragraph("Miembros e invitados", ParagraphStyle('TB3', fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor("#4F46E5")))
        ],
        [
            Paragraph("<b>Inscripción</b>", ParagraphStyle('TB1', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor("#1E293B"))),
            Paragraph("Regístrate en un evento, añade a tus acompañantes y sube tu comprobante de pago con validación inteligente.", ParagraphStyle('TB2', fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor("#475569"))),
            Paragraph("Asistentes a eventos", ParagraphStyle('TB3', fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor("#4F46E5")))
        ],
        [
            Paragraph("<b>Verificar Inscripción</b>", ParagraphStyle('TB1', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor("#1E293B"))),
            Paragraph("Consulta el estado de tu pago, revisa tus datos y descarga tu <b>Boleto Digital con Código QR</b>.", ParagraphStyle('TB2', fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor("#475569"))),
            Paragraph("Registrados", ParagraphStyle('TB3', fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor("#4F46E5")))
        ],
        [
            Paragraph("<b>Nosotros / Contacto</b>", ParagraphStyle('TB1', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor("#1E293B"))),
            Paragraph("Conoce la visión pastoral, sedes, números telefónicos y enlace directo a WhatsApp.", ParagraphStyle('TB2', fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor("#475569"))),
            Paragraph("Todos los usuarios", ParagraphStyle('TB3', fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor("#4F46E5")))
        ],
        [
            Paragraph("<b>Panel Administrativo</b>", ParagraphStyle('TB1', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor("#1E293B"))),
            Paragraph("Crea eventos, aprueba pagos, revisa comprobantes bancarios y realiza el control de asistencia.", ParagraphStyle('TB2', fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor("#475569"))),
            Paragraph("Líderes autorizados", ParagraphStyle('TB3', fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor("#DC2626")))
        ]
    ]

    t_sections = Table(sections_data, colWidths=[110, 312, 110])
    t_sections.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E1B4B")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_sections)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECCIÓN 2: GUÍA PASO A PASO PARA EL ASISTENTE
    # =========================================================================
    story.append(PageBreak())
    
    story.append(Paragraph("2. Guía Paso a Paso: ¿Cómo Inscribirte a un Evento?", style_h1))
    story.append(Paragraph(
        "Inscribirte a una actividad especial (retiro, conferencia o taller) toma menos de 3 minutos. Sigue estos sencillos pasos:",
        style_body
    ))
    story.append(Spacer(1, 4))

    # Pasos numerados con cajas estilizadas
    steps = [
        (
            "Paso 1: Elige tu Evento",
            "#4F46E5",
            [
                "1. En el menú superior, haz clic en la pestaña <b>Eventos</b>.",
                "2. Verás las tarjetas con los eventos disponibles. Haz clic en el botón <b>Ver Detalle</b> o <b>Inscribirme</b> del evento al que deseas asistir.",
                "3. Revisa la fecha, hora, lugar y el costo por persona."
            ]
        ),
        (
            "Paso 2: Completa tus Datos Personales",
            "#059669",
            [
                "1. Ingresa tu <b>Nombre completo</b>, <b>Correo electrónico</b> y <b>Número de WhatsApp</b>.",
                "2. Si vas acompañado de familiares o amigos, puedes seleccionar la <b>cantidad de cupos</b> y registrar sus nombres para que queden asegurados bajo tu misma reserva.",
                "3. El sistema calculará automáticamente el monto total a pagar."
            ]
        ),
        (
            "Paso 3: Realiza el Pago y Sube tu Comprobante",
            "#D97706",
            [
                "1. En pantalla verás los métodos de pago oficiales habilitados (por ejemplo: <b>Yape, Plin o Transferencia Bancaria</b> con sus números y titulares).",
                "2. Realiza el pago desde tu aplicación bancaria o billetera digital.",
                "3. Toma una captura de pantalla clara del comprobante y súbela en el botón <b>Seleccionar comprobante / Tomar foto</b>.",
                "4. <i>¡Novedad Inteligente!</i> La plataforma cuenta con lectura automática (OCR) que verificará que la imagen sea legible y detectará el monto y la fecha para acelerar tu confirmación.",
                "5. Haz clic en <b>Confirmar y Enviar Inscripción</b>."
            ]
        ),
        (
            "Paso 4: Guarda tu Código de Registro y tu Pase QR",
            "#7C3AED",
            [
                "1. Al finalizar, la pantalla te mostrará un mensaje de felicitaciones con tu <b>Código de Inscripción único</b> (ejemplo: <code>INS-84920</code>).",
                "2. Tu inscripción entrará en estado <b>En Revisión / Pendiente</b> mientras el equipo valida el depósito.",
                "3. Una vez aprobada, tendrás disponible tu <b>Boleto Digital con Código QR</b>, el cual puedes descargar o guardar en tu celular para presentarlo el día del evento."
            ]
        )
    ]

    for title, color_code, bullets in steps:
        step_box = create_colored_card(
            title,
            bullets,
            bg_color="#F8FAFC",
            border_color="#E2E8F0",
            title_color=color_code
        )
        story.append(step_box)
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 6))
    
    # Tips útiles
    tip_card = create_colored_card(
        "💡 Consejos para que tu inscripción sea aprobada al instante:",
        [
            "• <b>Comprobante nítido:</b> Asegúrate de que la captura muestre claramente el número de operación, la fecha y el importe exacto.",
            "• <b>Guarda tu comprobante original:</b> Guarda la imagen en tu galería de fotos por si necesitas consultarla después.",
            "• <b>Verifica tu número de WhatsApp:</b> Te servirá para consultar tu pase y recibir notificaciones."
        ],
        bg_color="#ECFDF5",
        border_color="#A7F3D0",
        title_color="#065F46"
    )
    story.append(tip_card)

    # =========================================================================
    # SECCIÓN 3: CÓMO CONSULTAR Y DESCARGAR TU BOLETO
    # =========================================================================
    story.append(Spacer(1, 14))
    story.append(Paragraph("3. ¿Cómo consultar tu inscripción y descargar tu Boleto QR?", style_h1))
    story.append(Paragraph(
        "Si ya te inscribiste y quieres ver si tu pago fue aprobado o necesitas volver a descargar tu boleto digital, sigue estos pasos:",
        style_body
    ))

    verify_points = [
        "1. Haz clic en el botón o enlace <b>Verificar Inscripción</b> en la barra superior o en el pie de página.",
        "2. Elige el <b>Evento</b> en el que te registraste.",
        "3. Ingresa tu <b>Correo electrónico</b>, <b>Número de Teléfono</b> o tu <b>Código de Inscripción</b>.",
        "4. Haz clic en <b>Buscar mi Inscripción</b>.",
        "5. El sistema te mostrará tu ficha con el estado actual (<i>Pendiente, Confirmado o Asistió</i>).",
        "6. Cuando esté <b>Confirmado</b>, podrás ver tu <b>Código QR</b> y presionar el botón <b>Descargar Boleto</b>."
    ]

    story.append(create_colored_card(
        "🎟️ Pasos para obtener tu Boleto Digital en cualquier momento",
        verify_points,
        bg_color="#EEF2FF",
        border_color="#C7D2FE",
        title_color="#3730A3"
    ))

    # =========================================================================
    # SECCIÓN 4: GUÍA PARA EL ADMINISTRADOR Y LÍDERES
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("4. Guía para Administradores y Equipo de Trabajo", style_h1))
    story.append(Paragraph(
        "El portal cuenta con un <b>Panel Administrativo moderno y seguro</b> para que los líderes organicen eventos, auditen ingresos y controlen el aforo en tiempo real.",
        style_body
    ))
    story.append(Spacer(1, 6))

    admin_features = [
        (
            "🔑 1. Acceso Seguro al Sistema",
            "#1E293B",
            [
                "• Ingresa a través de la ruta protegida <code>/admin-login</code>.",
                "• Utiliza tu correo y contraseña asignados por la administración.",
                "• Las sesiones cuentan con protección de autenticación Firebase para resguardar la privacidad de los asistentes."
            ]
        ),
        (
            "📅 2. Gestión Integral de Eventos (Crear, Editar y Publicar)",
            "#4F46E5",
            [
                "• En la pestaña <b>Eventos</b>, puedes crear nuevas actividades con su título, descripción, fecha, hora y ubicación.",
                "• <b>Configuración Financiera:</b> Define el precio por cupo y los datos de cuentas bancarias (Yape/Plin/Cuentas BCP, BBVA, Interbank).",
                "• <b>Límites de Aforo:</b> Establece un número máximo de cupos. El sistema bloqueará nuevas inscripciones automáticamente cuando se agoten.",
                "• <b>Estado:</b> Puedes activar o pausar un evento en cualquier momento con un solo interruptor."
            ]
        ),
        (
            "📋 3. Revisión y Aprobación de Inscripciones",
            "#059669",
            [
                "• En la sección <b>Inscripciones</b>, puedes ver la lista completa organizada por cada evento.",
                "• <b>Visor de Comprobantes:</b> Haz clic sobre el comprobante para verlo en tamaño completo, verificar el número de operación y compararlo con tus extractos.",
                "• <b>Acciones Rápidas:</b> Con un clic puedes cambiar el estado a <b>Aprobado</b> o <b>Rechazado</b> (agregando un motivo si el comprobante no coincide).",
                "• <b>Filtros y Búsqueda:</b> Encuentra inscripciones por nombre, teléfono o estado de pago al instante."
            ]
        ),
        (
            "📱 4. Control de Asistencia y Check-in el Día del Evento",
            "#7C3AED",
            [
                "• Al momento del ingreso de las personas al auditorio, el equipo de recepción puede escanear el <b>Código QR</b> del asistente o buscarlo por su nombre.",
                "• El sistema marcará la asistencia en tiempo real evitando que un mismo boleto sea utilizado dos veces.",
                "• Consulta las estadísticas de asistencia en vivo (porcentaje de asistencia vs inscritos)."
            ]
        )
    ]

    for title, color_code, bullets in admin_features:
        card = create_colored_card(
            title,
            bullets,
            bg_color="#F8FAFC",
            border_color="#E2E8F0",
            title_color=color_code
        )
        story.append(card)
        story.append(Spacer(1, 6))

    # =========================================================================
    # SECCIÓN 5: PREGUNTAS FRECUENTES (FAQ)
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("5. Preguntas Frecuentes (FAQ)", style_h1))
    story.append(Spacer(1, 4))

    faq_items = [
        (
            "❓ ¿Qué hago si me equivoqué al subir la foto del comprobante?",
            "No te preocupes. Puedes comunicarte directamente al WhatsApp de soporte de la iglesia indicando tu nombre y código de registro, o el administrador podrá solicitarte que envíes la captura correcta para actualizar tu ficha."
        ),
        (
            "❓ ¿Puedo pagar por varias personas en una sola transferencia?",
            "¡Sí! Al momento de inscribirte, selecciona el número total de cupos (ej. 3 personas). El sistema calculará el monto total. Haces una única transferencia por ese total, subes el comprobante y listo."
        ),
        (
            "❓ ¿Es obligatorio imprimir el boleto con código QR?",
            "No es obligatorio imprimirlo en papel. Puedes mostrar el código QR directamente desde la pantalla de tu teléfono celular al ingresar al evento."
        ),
        (
            "❓ ¿La aplicación funciona bien en teléfonos móviles?",
            "Sí, la plataforma es 100% responsiva y está optimizada para que cargue con gran velocidad y comodidad en cualquier celular Android o iPhone."
        )
    ]

    for q, a in faq_items:
        faq_card = create_colored_card(
            q,
            [a],
            bg_color="#FFFFFF",
            border_color="#E2E8F0",
            title_color="#1E293B"
        )
        story.append(faq_card)
        story.append(Spacer(1, 5))

    # =========================================================================
    # CIERRE Y CANALES DE SOPORTE
    # =========================================================================
    story.append(Spacer(1, 10))
    support_box = create_colored_card(
        "⛪ ¿Necesitas ayuda o tienes alguna duda adicional?",
        [
            "Si necesitas asistencia personalizada, puedes escribirnos a través del botón de <b>Contacto</b> de la página web o visitar nuestras reuniones presenciales.",
            "<i>«Porque donde están dos o tres congregados en mi nombre, allí estoy yo en medio de ellos.» — Mateo 18:20</i>"
        ],
        bg_color="#F1F5F9",
        border_color="#CBD5E1",
        title_color="#334155"
    )
    story.append(support_box)

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {output_path}")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "docs/Manual_Usuario_Aposento_Alto.pdf"
    build_tutorial_pdf(out)
