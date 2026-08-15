import os
import sys
import asyncio
from playwright.async_api import async_playwright
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, HRFlowable
)
from reportlab.pdfgen import canvas

SCREENSHOTS_DIR = "/home/yamoi/Documents/Proyectos/AposentoAltoIternacional/docs/screenshots"

async def capture_all_screenshots():
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Standard desktop viewport
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            device_scale_factor=2
        )
        page = await context.new_page()

        base_url = "https://el-aposento-alto.web.app"
        print(f"Connecting to {base_url}...")

        # 1. Inicio
        try:
            await page.goto(f"{base_url}/", wait_until="domcontentloaded", timeout=15000)
            await page.wait_for_timeout(2500)
            await page.screenshot(path=f"{SCREENSHOTS_DIR}/01_inicio.png", clip={"x": 0, "y": 0, "width": 1280, "height": 720})
            print("Captured 01_inicio.png")
        except Exception as e:
            print(f"Error capturing inicio: {e}")

        # 2. Eventos
        try:
            await page.goto(f"{base_url}/eventos", wait_until="domcontentloaded", timeout=15000)
            await page.wait_for_timeout(2500)
            await page.screenshot(path=f"{SCREENSHOTS_DIR}/02_eventos.png", clip={"x": 0, "y": 0, "width": 1280, "height": 720})
            print("Captured 02_eventos.png")
        except Exception as e:
            print(f"Error capturing eventos: {e}")

        # 3. Verificar Inscripcion
        try:
            await page.goto(f"{base_url}/verificar-inscripcion", wait_until="domcontentloaded", timeout=15000)
            await page.wait_for_timeout(2500)
            await page.screenshot(path=f"{SCREENSHOTS_DIR}/03_verificar.png", clip={"x": 0, "y": 0, "width": 1280, "height": 720})
            print("Captured 03_verificar.png")
        except Exception as e:
            print(f"Error capturing verificar: {e}")

        # 4. Admin Login
        try:
            await page.goto(f"{base_url}/admin-login", wait_until="domcontentloaded", timeout=15000)
            await page.wait_for_timeout(2500)
            await page.screenshot(path=f"{SCREENSHOTS_DIR}/04_admin_login.png", clip={"x": 0, "y": 0, "width": 1280, "height": 720})
            print("Captured 04_admin_login.png")
        except Exception as e:
            print(f"Error capturing admin_login: {e}")

        # 5. Contacto / Nosotros
        try:
            await page.goto(f"{base_url}/contacto", wait_until="domcontentloaded", timeout=15000)
            await page.wait_for_timeout(2500)
            await page.screenshot(path=f"{SCREENSHOTS_DIR}/05_contacto.png", clip={"x": 0, "y": 0, "width": 1280, "height": 720})
            print("Captured 05_contacto.png")
        except Exception as e:
            print(f"Error capturing contacto: {e}")

        await browser.close()
        print("All screenshots successfully captured!")


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
            self.setFillColor(colors.HexColor("#4F46E5"))
            self.drawString(40, 762, "EL APOSENTO ALTO INTERNACIONAL")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(205, 762, "•  Manual Visual Ilustrado del Sistema Web")
            
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.75)
            self.line(40, 755, 572, 755)
            self.restoreState()

        # Footer (all pages)
        self.saveState()
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(40, 40, 572, 40)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(40, 28, "El Aposento Alto Internacional © 2026 — Plataforma Oficial")
        
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(572, 28, page_str)
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


def create_image_frame(img_path, caption_text, width=532, height=220):
    if not os.path.exists(img_path):
        return Paragraph(f"<i>[Imagen no disponible: {os.path.basename(img_path)}]</i>", ParagraphStyle('Missing', fontName='Helvetica-Oblique', fontSize=8, textColor=colors.gray))
    
    img = Image(img_path, width=width, height=height)
    
    caption = Paragraph(
        f"📸 <b>Captura del Sistema:</b> {caption_text}",
        ParagraphStyle(
            'Caption',
            fontName='Helvetica',
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#475569"),
            alignment=1
        )
    )
    
    t = Table([[img], [caption]], colWidths=[width])
    t.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (0,0), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('BACKGROUND', (0,1), (0,1), colors.HexColor("#F8FAFC")),
    ]))
    return t


def build_pdf(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=45,
        bottomMargin=50
    )

    style_cover_title = ParagraphStyle(
        'CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#0F172A")
    )
    
    style_cover_subtitle = ParagraphStyle(
        'CoverSubtitle',
        fontName='Helvetica',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor("#4F46E5")
    )

    style_h1 = ParagraphStyle(
        'Header1',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#1E1B4B"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
        spaceAfter=4
    )

    story = []

    # =========================================================================
    # PÁGINA 1: PORTADA & PÁGINA DE INICIO VISUAL
    # =========================================================================
    badge_table = Table([[
        Paragraph("<b>GUÍA VISUAL ILUSTRADA • TUTORIAL PASO A PASO</b>", ParagraphStyle(
            'Badge', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.HexColor("#4338CA")
        ))
    ]], colWidths=[240])
    badge_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EEF2FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#C7D2FE")),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    
    story.append(badge_table)
    story.append(Spacer(1, 6))
    story.append(Paragraph("Manual de Usuario con Capturas de Pantalla", style_cover_title))
    story.append(Spacer(1, 2))
    story.append(Paragraph("El Aposento Alto Internacional — Conoce y usa la web de forma fácil y rápida", style_cover_subtitle))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#4F46E5"), spaceAfter=8))

    story.append(Paragraph("1. Pantalla Principal y Navegación de la Web", style_h1))
    story.append(Paragraph(
        "Al ingresar a la plataforma, encontrarás una interfaz moderna que te permite explorar las próximas actividades, prédicas y servicios de la congregación.",
        style_body
    ))
    story.append(Spacer(1, 3))

    # Imagen 1: Inicio
    img1_path = f"{SCREENSHOTS_DIR}/01_inicio.png"
    story.append(create_image_frame(img1_path, "Vista principal de la plataforma web con menú de navegación y acceso a eventos.", width=532, height=195))
    story.append(Spacer(1, 6))

    card_menu = create_colored_card(
        "🧭 ¿Cómo desplazarte por la web?",
        [
            "• <b>Inicio:</b> Portada, anuncios principales y accesos rápidos.",
            "• <b>Eventos:</b> Cartelera completa con fechas, precios y cupos.",
            "• <b>Verificar Inscripción:</b> Consulta de pagos y descarga de tu pase QR.",
            "• <b>Nosotros & Contacto:</b> Dirección de nuestras sedes y enlace directo a WhatsApp."
        ],
        bg_color="#F8FAFC",
        border_color="#CBD5E1",
        title_color="#0F172A"
    )
    story.append(card_menu)

    # =========================================================================
    # PÁGINA 2: CATÁLOGO DE EVENTOS & INSCRIPCIÓN
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("2. Explorar Eventos e Inscribirte Paso a Paso", style_h1))
    story.append(Paragraph(
        "En la pestaña <b>Eventos</b> puedes consultar todas las conferencias, talleres y retiros activos. Al hacer clic en <b>Inscribirme</b> o <b>Ver Detalle</b>, accederás al formulario de registro.",
        style_body
    ))
    story.append(Spacer(1, 3))

    # Imagen 2: Eventos
    img2_path = f"{SCREENSHOTS_DIR}/02_eventos.png"
    story.append(create_image_frame(img2_path, "Catálogo de eventos activos con sus tarjetas informativas, fechas y botón de inscripción.", width=532, height=195))
    story.append(Spacer(1, 6))

    steps_card = create_colored_card(
        "📝 Pasos sencillos para completar tu inscripción:",
        [
            "<b>1. Tus Datos:</b> Escribe tu nombre, cédula/DNI, número de WhatsApp y correo electrónico.",
            "<b>2. Cantidad de Cupos:</b> Selecciona cuántas personas asistirán contigo bajo una misma reserva.",
            "<b>3. Pago Móvil / Bancario:</b> Realiza el pago por <b>Yape, Plin o Transferencia</b> al número oficial indicado en pantalla.",
            "<b>4. Comprobante con Validación Inteligente:</b> Sube la foto del comprobante. El sistema verificará automáticamente que sea legible y coincida con el monto total.",
            "<b>5. Código Único:</b> Al enviar, recibirás tu código de registro (ej. <code>INS-9281</code>) para tu seguimiento."
        ],
        bg_color="#ECFDF5",
        border_color="#A7F3D0",
        title_color="#065F46"
    )
    story.append(steps_card)

    # =========================================================================
    # PÁGINA 3: CONSULTAR ESTADO & BOLETO CON CÓDIGO QR
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("3. Verificar tu Pago y Descargar tu Boleto QR", style_h1))
    story.append(Paragraph(
        "La sección <b>Verificar Inscripción</b> te permite consultar en cualquier momento si tu registro ya fue aprobado por los líderes y obtener tu pase digital con código QR para ingresar sin imprimir papel.",
        style_body
    ))
    story.append(Spacer(1, 3))

    # Imagen 3: Verificar
    img3_path = f"{SCREENSHOTS_DIR}/03_verificar.png"
    story.append(create_image_frame(img3_path, "Buscador de inscripción por correo, teléfono o código para generar y descargar el Boleto QR.", width=532, height=195))
    story.append(Spacer(1, 6))

    qr_card = create_colored_card(
        "🎟️ ¿Cómo usar tu Boleto Digital el día del evento?",
        [
            "• <b>Sin papeles:</b> Solo necesitas llevar tu teléfono celular y mostrar el Código QR generado en la entrada.",
            "• <b>Descarga directa:</b> Presiona el botón <b>Descargar Boleto</b> para guardarlo como imagen en tu galería de fotos.",
            "• <b>Múltiples cupos:</b> Si compraste varios boletos para tu familia, el mismo pase contiene la cantidad total de personas reservadas."
        ],
        bg_color="#EEF2FF",
        border_color="#C7D2FE",
        title_color="#3730A3"
    )
    story.append(qr_card)

    # =========================================================================
    # PÁGINA 4: PANEL ADMINISTRATIVO, EDICIÓN & AUDITORÍA
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("4. Panel de Administración y Registro de Ediciones", style_h1))
    story.append(Paragraph(
        "Los líderes y coordinadores acceden al portal mediante una conexión protegida. El sistema cuenta con <b>auditoría de cambios en tiempo real</b>, mostrando en pantalla quién realizó cada edición.",
        style_body
    ))
    story.append(Spacer(1, 3))

    # Imagen 4: Admin Login
    img4_path = f"{SCREENSHOTS_DIR}/04_admin_login.png"
    story.append(create_image_frame(img4_path, "Pantalla de acceso administrativo seguro con opción de recuperación de clave y enlace de retorno.", width=532, height=195))
    story.append(Spacer(1, 6))

    admin_summary = create_colored_card(
        "🛡️ Funciones Administrativas y Trazabilidad:",
        [
            "• <b>Creación y Edición de Eventos:</b> Configura títulos, afiches, fechas, cupos y precios.",
            "• <b>¿Quién editó cada registro?</b> Tanto en el formulario de edición de inscripciones como en el de publicaciones, una barra superior indica: <i>'Última edición por: admin@... el DD/MM/AAAA'</i> y <i>'Editando como: tu-correo'</i>.",
            "• <b>Aprobación de Comprobantes:</b> Revisa las fotos de depósitos bancarios en alta definición y valida con un clic.",
            "• <b>Restablecer Contraseña:</b> Si un administrador olvida su contraseña, el sistema le envía un correo seguro en español y lo redirige automáticamente de vuelta al portal."
        ],
        bg_color="#F8FAFC",
        border_color="#E2E8F0",
        title_color="#1E293B"
    )
    story.append(admin_summary)
    story.append(Spacer(1, 6))

    # Contacto
    footer_card = create_colored_card(
        "⛪ Canales de Soporte y Contacto",
        [
            "Para dudas sobre inscripciones, pagos o configuraciones de la iglesia, puedes escribirnos mediante el formulario de <b>Contacto</b> de la web o por el canal oficial de WhatsApp.",
            "<i>El Aposento Alto Internacional © 2026 — Edificando vidas para el Reino.</i>"
        ],
        bg_color="#F1F5F9",
        border_color="#CBD5E1",
        title_color="#334155"
    )
    story.append(footer_card)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Visual PDF successfully generated at: {output_path}")


async def main():
    print("Step 1: Capturing real screenshots...")
    await capture_all_screenshots()
    
    out_pdf = "/home/yamoi/Documents/Proyectos/AposentoAltoIternacional/docs/Manual_Usuario_Aposento_Alto.pdf"
    print(f"Step 2: Compiling visual PDF to {out_pdf}...")
    build_pdf(out_pdf)

if __name__ == "__main__":
    asyncio.run(main())
