from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape

from django.conf import settings
from django.utils import timezone

from PIL import Image as PILImage, ImageChops
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ANCHO, ALTO = A4

NARANJA = colors.HexColor("#F26A0F")
NEGRO = colors.black
BLANCO = colors.white
GRIS = colors.HexColor("#555555")

# Datos de contacto por defecto (si el vendedor no tiene los propios)
TELEFONO_DEFECTO = "3584 39-3572"
EMAIL_DEFECTO = "marcosgonzalolastra@gmail.com"
NARANJA_CLARO = colors.HexColor("#FEF0E7")

# Tamaño máximo del logo en el encabezado
LOGO_MAX_ANCHO = 72 * mm
LOGO_MAX_ALTO = 30 * mm


def formato_importe(valor):
    numero = f"{valor:,.2f}"
    return "$ " + numero.replace(",", "X").replace(".", ",").replace("X", ".")


def cargar_logo(ruta_logo):
    """
    Devuelve un Image de reportlab con el logo recortado (sin márgenes
    vacíos/transparentes) y ajustado al tamaño máximo permitido.
    """
    imagen = PILImage.open(ruta_logo).convert("RGBA")

    # Recortar márgenes: se ignora la transparencia casi invisible
    # (alfa muy bajo) y el blanco, quedándose solo con el logo.
    alfa = imagen.getchannel("A").point(lambda p: 255 if p > 20 else 0)
    sobre_blanco = PILImage.new("RGBA", imagen.size, (255, 255, 255, 255))
    sobre_blanco.alpha_composite(imagen)
    diferencia = ImageChops.difference(
        sobre_blanco.convert("RGB"),
        PILImage.new("RGB", imagen.size, (255, 255, 255)),
    ).convert("L").point(lambda p: 255 if p > 25 else 0)
    mascara = ImageChops.multiply(alfa, diferencia)
    bbox = mascara.getbbox()

    if bbox:
        imagen = imagen.crop(bbox)

    buffer = BytesIO()
    imagen.save(buffer, format="PNG")
    buffer.seek(0)

    ancho_px, alto_px = imagen.size
    escala = min(LOGO_MAX_ANCHO / ancho_px, LOGO_MAX_ALTO / alto_px)

    logo = Image(
        buffer,
        width=ancho_px * escala,
        height=alto_px * escala,
    )
    logo.hAlign = "LEFT"
    return logo


def dibujar_bandera(canvas, x, y):
    ancho = 18 * mm
    alto = 11 * mm
    franja = alto / 3

    canvas.setFillColor(colors.HexColor("#75BDE8"))
    canvas.rect(x, y, ancho, franja, fill=1, stroke=0)
    canvas.rect(x, y + 2 * franja, ancho, franja, fill=1, stroke=0)

    canvas.setFillColor(BLANCO)
    canvas.rect(x, y + franja, ancho, franja, fill=1, stroke=0)

    canvas.setFillColor(colors.HexColor("#F6B40E"))
    canvas.circle(
        x + ancho / 2,
        y + alto / 2,
        1.2 * mm,
        fill=1,
        stroke=0,
    )


def dibujar_marca_agua(canvas):
    """
    Círculos naranjas rellenos, suaves, como en el PDF original.
    (x, y, radio) medidos desde la esquina inferior izquierda.
    """
    canvas.saveState()
    canvas.setFillColor(NARANJA_CLARO)
    canvas.setStrokeColor(NARANJA_CLARO)

    circulos = [
        (125.6 * mm, 120.8 * mm, 12.3 * mm),
        (158.2 * mm, 121.2 * mm, 9.2 * mm),
        (94.6 * mm, 108.0 * mm, 9.2 * mm),
        (181.8 * mm, 109.2 * mm, 6.85 * mm),
        (74.9 * mm, 87.3 * mm, 8.4 * mm),
        (189.7 * mm, 90.1 * mm, 4.3 * mm),
        (65.1 * mm, 63.1 * mm, 6.75 * mm),
        (63.6 * mm, 42.9 * mm, 3.5 * mm),
    ]

    for x, y, radio in circulos:
        canvas.circle(x, y, radio, fill=1, stroke=0)

    canvas.restoreState()


def dibujar_encabezado_y_pie(canvas, doc):
    canvas.saveState()

    canvas.setFillColor(NARANJA)
    canvas.rect(
        0,
        ALTO - 12 * mm,
        ANCHO,
        12 * mm,
        fill=1,
        stroke=0,
    )

    dibujar_marca_agua(canvas)

    canvas.setFillColor(NARANJA)
    canvas.rect(
        0,
        0,
        ANCHO,
        18 * mm,
        fill=1,
        stroke=0,
    )

    canvas.setFillColor(BLANCO)
    canvas.setFont("Helvetica", 9)

    telefono = getattr(doc, "pie_telefono", None) or TELEFONO_DEFECTO
    email = getattr(doc, "pie_email", None) or EMAIL_DEFECTO

    canvas.drawString(
        12 * mm,
        10 * mm,
        f"Tel.: {telefono}",
    )

    canvas.drawString(
        65 * mm,
        10 * mm,
        email,
    )

    dibujar_bandera(
        canvas,
        ANCHO - 30 * mm,
        3.5 * mm,
    )

    canvas.restoreState()


def generar_pdf_documento(documento):
    buffer = BytesIO()

    doc = BaseDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=12 * mm,
        rightMargin=12 * mm,
        topMargin=18 * mm,
        bottomMargin=24 * mm,
        title=f"{documento.get_tipo_display()} {documento.numero_formateado}",
        author="Biomédica Río Cuarto",
    )

    marco = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )

    # Contacto del pie de página según el vendedor del documento
    doc.pie_telefono = getattr(documento, "vendedor_telefono", "") or ""
    doc.pie_email = getattr(documento, "vendedor_email", "") or ""

    doc.addPageTemplates(
        PageTemplate(
            id="documento",
            frames=[marco],
            onPage=dibujar_encabezado_y_pie,
        )
    )

    estilo_normal = ParagraphStyle(
        "NormalBiomedica",
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=NEGRO,
        alignment=TA_LEFT,
    )

    estilo_negrita = ParagraphStyle(
        "NegritaBiomedica",
        parent=estilo_normal,
        fontName="Helvetica-Bold",
    )

    estilo_titulo = ParagraphStyle(
        "TituloBiomedica",
        fontName="Helvetica-Bold",
        fontSize=19,
        leading=23,
        textColor=NARANJA,
        alignment=TA_RIGHT,
    )

    estilo_derecha = ParagraphStyle(
        "DerechaBiomedica",
        parent=estilo_normal,
        alignment=TA_RIGHT,
    )

    estilo_tabla = ParagraphStyle(
        "TablaBiomedica",
        parent=estilo_normal,
        fontSize=8,
        leading=11,
    )

    estilo_tabla_centro = ParagraphStyle(
        "TablaCentroBiomedica",
        parent=estilo_tabla,
        alignment=TA_CENTER,
    )

    estilo_tabla_derecha = ParagraphStyle(
        "TablaDerechaBiomedica",
        parent=estilo_tabla,
        alignment=TA_RIGHT,
    )

    elementos = []

    ruta_logo = (
        Path(settings.BASE_DIR)
        / "static"
        / "img"
        / "logo_documentos.png"
    )

    if ruta_logo.exists():
        logo = cargar_logo(ruta_logo)
    else:
        logo = Paragraph(
            "<b>BIOMÉDICA RÍO CUARTO</b>",
            estilo_negrita,
        )

    fecha = timezone.localtime(
        documento.creado_en
    ).strftime("%d/%m/%Y")

    datos_derecha = [
        Paragraph(
            documento.get_tipo_display().upper(),
            estilo_titulo,
        ),
        Spacer(1, 4 * mm),
        Paragraph(
            f"<b>Fecha:</b> {fecha}",
            estilo_derecha,
        ),
        Paragraph(
            f"<b>N.º:</b> {documento.numero_formateado}",
            estilo_derecha,
        ),
    ]

    # Recuadro "Documento no válido como factura": arriba, al medio
    # Columna central de 40 mm: la X queda exactamente en el medio
    caja_x = Table(
        [["", "X", ""]],
        colWidths=[14.5 * mm, 11 * mm, 14.5 * mm],
        rowHeights=[11 * mm],
    )
    caja_x.setStyle(
        TableStyle(
            [
                ("BOX", (1, 0), (1, 0), 1, NEGRO),
                ("FONTNAME", (1, 0), (1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (1, 0), (1, 0), 14),
                ("ALIGN", (1, 0), (1, 0), "CENTER"),
                ("VALIGN", (1, 0), (1, 0), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    estilo_aviso = ParagraphStyle(
        "AvisoBiomedica",
        parent=estilo_normal,
        fontSize=6,
        leading=7.5,
        alignment=TA_CENTER,
    )

    aviso = [
        Spacer(1, 3 * mm),
        caja_x,
        Spacer(1, 1.5 * mm),
        Paragraph("Documento no válido<br/>como factura", estilo_aviso),
    ]

    encabezado = Table(
        [[logo, aviso, datos_derecha]],
        colWidths=[73 * mm, 40 * mm, 73 * mm],
    )

    encabezado.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    elementos.append(encabezado)
    elementos.append(Spacer(1, 3 * mm))

    datos_vendedor = [
        Paragraph(
            escape(documento.vendedor_nombre),
            estilo_negrita,
        ),
        Paragraph(
            f"CUIT/CUIL: {escape(documento.vendedor_cuil)}",
            estilo_normal,
        ),
        Paragraph(
            f"Razón social: {escape(documento.vendedor_razon_social)}",
            estilo_normal,
        ),
    ]

    vendedor_tabla = Table(
        [[datos_vendedor, ""]],
        colWidths=[125 * mm, 61 * mm],
    )

    vendedor_tabla.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    elementos.append(vendedor_tabla)
    elementos.append(Spacer(1, 4 * mm))

    elementos.append(Spacer(1, 7 * mm))

    datos_cliente = [
        Paragraph(
            f"<b>SRES:</b> {escape(documento.cliente_nombre)}",
            estilo_normal,
        ),
        Paragraph(
            f"<b>CUIT/CUIL:</b> {escape(documento.cliente_cuil or '-')}",
            estilo_normal,
        ),
        Paragraph(
            f"<b>Localidad:</b> {escape(documento.cliente_localidad)}",
            estilo_normal,
        ),
    ]

    tabla_cliente = Table(
        [[datos_cliente]],
        colWidths=[186 * mm],
    )

    tabla_cliente.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 1, NEGRO),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    elementos.append(tabla_cliente)
    elementos.append(Spacer(1, 10 * mm))

    filas = [
        [
            "Artículo",
            "Detalle",
            "Cantidad",
            "Precio unitario",
            "TOTAL",
        ]
    ]

    for item in documento.items.all():
        filas.append(
            [
                Paragraph(
                    escape(item.codigo),
                    estilo_tabla,
                ),
                Paragraph(
                    escape(item.descripcion),
                    estilo_tabla,
                ),
                Paragraph(
                    str(item.cantidad),
                    estilo_tabla_centro,
                ),
                Paragraph(
                    formato_importe(item.precio_unitario),
                    estilo_tabla_derecha,
                ),
                Paragraph(
                    formato_importe(item.total),
                    estilo_tabla_derecha,
                ),
            ]
        )

    tabla_productos = Table(
        filas,
        colWidths=[
            23 * mm,
            75 * mm,
            20 * mm,
            34 * mm,
            34 * mm,
        ],
        repeatRows=1,
        hAlign="LEFT",
    )

    tabla_productos.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 1, NEGRO),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, NEGRO),
                ("BACKGROUND", (0, 0), (-1, 0), BLANCO),
                ("TEXTCOLOR", (0, 0), (-1, -1), NEGRO),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (2, 0), (-1, 0), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    elementos.append(tabla_productos)
    elementos.append(Spacer(1, 7 * mm))

    resumen = [
        [
            "Subtotal",
            formato_importe(documento.subtotal),
        ],
        [
            (
                f"IVA ({documento.porcentaje_iva} %)"
                if documento.tipo_iva != documento.TipoIVA.SIN_IVA
                else "IVA"
            ),
            formato_importe(documento.importe_iva),
        ],
        [
            "TOTAL",
            formato_importe(documento.total),
        ],
    ]

    tabla_resumen = Table(
        resumen,
        colWidths=[45 * mm, 45 * mm],
        hAlign="RIGHT",
    )

    tabla_resumen.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
                ("FONTNAME", (0, 2), (-1, 2), "Helvetica-Bold"),
                ("FONTSIZE", (0, 2), (-1, 2), 11),
                ("LINEABOVE", (0, 2), (-1, 2), 1, NEGRO),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    elementos.append(tabla_resumen)

    if documento.tipo == documento.Tipo.PRESUPUESTO:
        elementos.append(Spacer(1, 8 * mm))

        elementos.append(
            Paragraph(
                "<b>Validez:</b> 48 horas",
                estilo_normal,
            )
        )

        elementos.append(Spacer(1, 8 * mm))

        elementos.append(
            Paragraph(
                "<b>OBSERVACIONES</b>",
                ParagraphStyle(
                    "ObservacionesTitulo",
                    parent=estilo_negrita,
                    alignment=TA_CENTER,
                ),
            )
        )

        elementos.append(Spacer(1, 4 * mm))

        elementos.append(
            Paragraph(
                "Los precios son finales según el IVA seleccionado.",
                estilo_normal,
            )
        )

    doc.build(elementos)

    buffer.seek(0)
    return buffer