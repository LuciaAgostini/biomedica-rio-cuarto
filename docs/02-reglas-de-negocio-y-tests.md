# Reglas de negocio y casos de test

Las reglas viven en `apps/inventory/services.py`, no en las vistas.

| ID | Regla | Test (nombre sugerido) |
|---|---|---|
| RN-01 | La cantidad de un movimiento debe ser > 0 | `test_movimiento_rechaza_cantidad_cero_o_negativa` |
| RN-02 | La entrada exige vencimiento ≥ hoy | `test_entrada_rechaza_vencimiento_pasado` |
| RN-03 | Entrada con lote existente (mismo producto + número) suma cantidad | `test_entrada_suma_a_lote_existente` |
| RN-04 | Entrada con lote nuevo crea el lote | `test_entrada_crea_lote_nuevo` |
| RN-05 | No se puede sacar más de lo disponible en el lote | `test_salida_rechaza_stock_insuficiente` |
| RN-06 | No se puede sacar de un lote vencido | `test_salida_rechaza_lote_vencido` |
| RN-07 | El lote sugerido es el de vencimiento más cercano con stock | `test_lote_sugerido_es_fefo` |
| RN-08 | Stock del producto = suma de lotes vigentes con cantidad > 0 | `test_stock_ignora_lotes_vencidos_y_vacios` |
| RN-09 | Producto con stock ≤ mínimo figura en stock bajo | `test_stock_bajo_incluye_productos_en_el_minimo` |
| RN-10 | Próximos a vencer: vence entre hoy y hoy + N días, cantidad > 0 | `test_proximos_a_vencer_respeta_umbral` |
| RN-11 | Los movimientos no se modifican ni se borran | `test_movimiento_no_se_puede_editar` |
| RN-12 | Salida y descuento de lote ocurren en una transacción atómica | `test_salida_es_atomica_si_falla_el_registro` |
| RN-13 | Un Administrador no accede a vistas de Superadmin | `test_admin_recibe_403_en_usuarios` |
| RN-14 | Baja lógica: el registro sigue en la base con `activo=False` | `test_baja_es_logica` (ya hecho para Producto) |

## Pista para la implementación
```python
# apps/inventory/services.py
from django.db import transaction

@transaction.atomic
def registrar_salida(*, lote_id, cantidad, motivo, usuario):
    lote = Lote.objects.select_for_update().get(pk=lote_id)
    # validar RN-01, RN-05, RN-06 -> lanzar ValidationError con mensaje claro
    # descontar, crear MovimientoStock, devolver el movimiento
```
Cobertura objetivo: ≥ 80 % en `services.py`.
