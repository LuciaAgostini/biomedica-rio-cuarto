from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from .forms import DocumentoForm, ItemDocumentoFormSet
from .models import Documento
from .pdf import generar_pdf_documento
from .services import crear_documento


@login_required
def documento_crear(request, tipo_documento=None):
    if tipo_documento is not None and tipo_documento not in Documento.Tipo.values:
        raise PermissionDenied

    if request.method == "POST":
        formulario = DocumentoForm(request.POST)
        productos_formulario = ItemDocumentoFormSet(
            request.POST,
            prefix="productos",
        )
    else:
        formulario = DocumentoForm(
            initial={"tipo": tipo_documento} if tipo_documento else None
        )
        productos_formulario = ItemDocumentoFormSet(
            prefix="productos",
        )

    if tipo_documento:
        formulario.fields["tipo"].widget = formulario.fields["tipo"].hidden_widget()
        formulario.fields["tipo"].initial = tipo_documento

    if request.method == "POST" and formulario.is_valid() and productos_formulario.is_valid():
        datos = formulario.cleaned_data

        if tipo_documento and datos["tipo"] != tipo_documento:
            formulario.add_error(
                "tipo",
                "El tipo de documento no corresponde a esta sección.",
            )
        else:
            productos = [
                form.cleaned_data
                for form in productos_formulario
                if form.cleaned_data and not form.cleaned_data.get("DELETE")
            ]

            if not productos:
                productos_formulario._non_form_errors = productos_formulario.error_class(
                    ["Debés agregar al menos un producto."]
                )
            else:
                documento = crear_documento(
                    tipo=tipo_documento or datos["tipo"],
                    vendedor=datos["vendedor"],
                    cliente_nombre=datos["cliente_nombre"],
                    cliente_cuil=datos["cliente_cuil"],
                    cliente_localidad=datos["cliente_localidad"],
                    tipo_iva=datos["tipo_iva"],
                    porcentaje_iva=datos["porcentaje_iva"],
                    creado_por=request.user,
                    items=productos,
                )

                messages.success(
                    request,
                    f"{documento.get_tipo_display()} N.º "
                    f"{documento.numero_formateado} creado correctamente.",
                )

                if documento.tipo == Documento.Tipo.PRESUPUESTO:
                    return redirect("documentos:presupuesto_list")

                return redirect("documentos:remito_list")

    return render(
        request,
        "documentos/documento_form.html",
        {
            "formulario": formulario,
            "productos_formulario": productos_formulario,
            "tipo_documento": tipo_documento,
        },
    )


@login_required
def documento_list(request, tipo_documento=None):
    if tipo_documento is not None and tipo_documento not in Documento.Tipo.values:
        raise PermissionDenied

    tipo = tipo_documento or request.GET.get("tipo", "")

    documentos = Documento.objects.select_related(
        "creado_por"
    ).prefetch_related("items")

    if tipo in Documento.Tipo.values:
        documentos = documentos.filter(tipo=tipo)

    documentos = documentos.order_by("-creado_en")

    return render(
        request,
        "documentos/documento_list.html",
        {
            "documentos": documentos,
            "tipo_seleccionado": tipo,
            "tipo_documento": tipo_documento,
        },
    )


@login_required
def documento_pdf(request, pk):
    documento = get_object_or_404(
        Documento.objects.prefetch_related("items"),
        pk=pk,
    )

    if not request.user.is_staff and documento.creado_por_id != request.user.pk:
        raise PermissionDenied

    archivo_pdf = generar_pdf_documento(documento)

    nombre_cliente = slugify(documento.cliente_nombre).replace("-", "_")

    nombre_archivo = (
        f"{documento.tipo.lower()}_{nombre_cliente}_{documento.numero_formateado}.pdf"
    )

    return FileResponse(
        archivo_pdf,
        as_attachment=True,
        filename=nombre_archivo,
        content_type="application/pdf",
    )