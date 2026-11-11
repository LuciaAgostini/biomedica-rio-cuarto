from django.db import transaction

from .models import Documento, ItemDocumento, NumeracionDocumento, Vendedor


@transaction.atomic
def crear_documento(
    *,
    tipo,
    vendedor,
    cliente_nombre,
    cliente_cuil,
    cliente_localidad,
    tipo_iva,
    porcentaje_iva,
    creado_por,
    items,
):
    if tipo not in Documento.Tipo.values:
        raise ValueError("El tipo de documento no es válido.")

    if tipo_iva not in Documento.TipoIVA.values:
        raise ValueError("El tipo de IVA no es válido.")

    if not items:
        raise ValueError("El documento debe tener al menos un producto.")

    if not isinstance(vendedor, Vendedor) or not vendedor.activo:
        raise ValueError("Debés seleccionar un vendedor activo.")

    numeracion, _ = NumeracionDocumento.objects.get_or_create(
        tipo=tipo,
        defaults={"ultimo_numero": 0},
    )

    numeracion = NumeracionDocumento.objects.select_for_update().get(
        pk=numeracion.pk
    )

    numeracion.ultimo_numero += 1
    numeracion.save(update_fields=["ultimo_numero"])

    documento = Documento.objects.create(
        tipo=tipo,
        numero=numeracion.ultimo_numero,
        vendedor=vendedor,
        vendedor_nombre=vendedor.nombre,
        vendedor_cuil=vendedor.cuit,
        vendedor_razon_social=vendedor.razon_social,
        vendedor_telefono=vendedor.telefono,
        vendedor_email=vendedor.email,
        cliente_nombre=cliente_nombre,
        cliente_cuil=cliente_cuil,
        cliente_localidad=cliente_localidad,
        tipo_iva=tipo_iva,
        porcentaje_iva=porcentaje_iva,
        creado_por=creado_por,
    )

    for item in items:
        producto = item["producto"]

        ItemDocumento.objects.create(
            documento=documento,
            producto=producto,
            codigo=producto.codigo,
            descripcion=producto.nombre,
            cantidad=item["cantidad"],
            precio_unitario=item["precio_unitario"],
        )

    return documento