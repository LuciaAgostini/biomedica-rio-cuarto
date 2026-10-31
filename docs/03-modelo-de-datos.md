# Modelo de datos

```mermaid
erDiagram
    USER ||--o{ MOVIMIENTO_STOCK : registra
    USER ||--o{ REGISTRO_ACTIVIDAD : genera
    CATEGORIA ||--o{ PRODUCTO : clasifica
    PRODUCTO ||--o{ LOTE : tiene
    PROVEEDOR ||--o{ LOTE : provee
    LOTE ||--o{ MOVIMIENTO_STOCK : mueve

    USER { int id string username string password string role bool is_active }
    CATEGORIA { int id string nombre bool activa }
    PRODUCTO { int id string codigo string nombre text descripcion int categoria_id int stock_minimo bool activo }
    PROVEEDOR { int id string razon_social string cuit string telefono string email bool activo }
    LOTE { int id int producto_id int proveedor_id string numero_lote date fecha_vencimiento int cantidad_disponible bool activo }
    MOVIMIENTO_STOCK { int id int lote_id string tipo int cantidad string motivo int usuario_id datetime fecha }
    REGISTRO_ACTIVIDAD { int id int usuario_id string accion string entidad text detalle datetime fecha }
    PARAMETRO { string clave string valor }
```

## Restricciones e índices
- `Producto.codigo` único. `Proveedor.cuit` único.
- `Lote`: único `(producto, numero_lote)`; índice en `fecha_vencimiento`; `CheckConstraint(cantidad_disponible >= 0)`.
- `MovimientoStock`: `CheckConstraint(cantidad > 0)`; índice en `(lote, fecha)`.
- Todas las FK con `on_delete=PROTECT`. Nada se borra físicamente.
- Migraciones versionadas en Git: `python manage.py makemigrations` y commitear el archivo generado.
