# Historias de usuario

Formato: *Como [rol] quiero [acción] para [beneficio]*. Criterios en formato Dado / Cuando / Entonces.
Prioridad: **M** = MVP, **S** = si da el tiempo.

## Épica A · Acceso y roles
**HU-01 · Iniciar y cerrar sesión (M)**
Como usuario quiero ingresar con usuario y contraseña para operar el sistema de forma segura.
- Dado credenciales válidas, cuando ingreso, entonces veo el listado de productos.
- Dado credenciales inválidas, cuando ingreso, entonces veo un mensaje de error sin revelar cuál dato falló.
- Cuando cierro sesión, entonces no puedo volver a ninguna pantalla con el botón «atrás».

**HU-02 · Control de acceso por rol (M)**
Como sistema quiero restringir pantallas según el rol para que el Administrador no acceda a configuración.
- Dado un Administrador, cuando abre la gestión de usuarios, entonces recibe 403.
- Dado un visitante sin sesión, cuando abre cualquier pantalla interna, entonces se lo redirige al login.

**HU-03 · Gestionar usuarios (M, Superadmin)**
Como Superadministrador quiero crear, editar, desactivar usuarios y asignar su rol.
- Las contraseñas se guardan con hash (Argon2) y nunca se muestran.
- No puedo desactivar mi propio usuario.
- Un usuario desactivado no puede iniciar sesión.

## Épica B · Catálogo
**HU-04 · CRUD de productos (M)**
Como Administrador quiero alta, consulta, edición y baja lógica de productos.
- El código es único y se normaliza a mayúsculas.
- Un producto dado de baja no aparece en listados ni en nuevos movimientos, pero conserva su historial.
- Validación en el formulario (frontend) y en el servidor.

**HU-05 · Gestionar categorías (M, Superadmin)**
Como Superadministrador quiero administrar categorías para organizar los productos.
- No se puede dar de baja una categoría con productos activos.

**HU-06 · Buscar y filtrar productos (S)**
- Puedo buscar por nombre/código y filtrar por categoría.

## Épica C · Proveedores
**HU-07 · CRUD de proveedores (M)**
- CUIT válido (11 dígitos) y único.
- Baja lógica; no se puede dar de baja un proveedor con lotes con stock.

## Épica D · Lotes, stock y vencimientos
**HU-08 · Registrar entrada de mercadería (M)**
Como Administrador quiero registrar una compra creando o sumando a un lote.
- Pido producto, proveedor, número de lote, cantidad > 0 y fecha de vencimiento.
- Si el lote ya existe para ese producto, se suma la cantidad.
- La fecha de vencimiento no puede ser anterior a hoy.
- Se crea un movimiento de tipo ENTRADA con mi usuario y la fecha.

**HU-09 · Registrar salida de mercadería (M)**
Como Administrador quiero registrar una venta/egreso descontando de un lote.
- El sistema sugiere el lote que vence primero (FEFO).
- No puedo sacar más que la cantidad disponible.
- No puedo sacar de un lote vencido.
- Se crea un movimiento SALIDA con motivo.

**HU-10 · Consultar stock por producto (M)**
- Veo la suma de lotes vigentes con cantidad > 0, y el detalle por lote.

**HU-11 · Alerta de stock bajo (S)**
- Los productos con stock total ≤ stock mínimo se marcan en el listado y hay un contador en el menú.

**HU-12 · Próximos a vencer (M)**
Como Administrador quiero ver qué lotes vencen pronto para venderlos primero o gestionarlos.
- Listado de lotes con cantidad > 0 y vencimiento dentro del umbral configurado, ordenado por fecha.
- Colores: vencido (rojo), próximo (amarillo), vigente (verde).
- Filtro por umbral (30/60/90 días) y badge con la cantidad en el menú.

**HU-13 · Historial de movimientos (M)**
- Listado paginado con filtros por producto, tipo y rango de fechas. Los movimientos no se editan ni se borran.

## Épica E · Configuración y auditoría (Superadmin)
**HU-14 · Parámetro de días de alerta (M)**
- El Superadmin define `dias_alerta_vencimiento` (entero 1–365). Afecta a HU-12.

**HU-15 · Registro de actividad (S)**
- Se registra quién, qué, sobre qué entidad y cuándo, para altas, bajas, modificaciones y movimientos. Solo lo ve el Superadmin.

## Épica F · Calidad transversal
**HU-16 · Mensajes de feedback (M)**
- Toda operación muestra mensaje de éxito, error controlado o advertencia.

**HU-17 · Interfaz responsive (M)**
- Todas las pantallas se usan en celular y escritorio.

**HU-18 · API documentada (M)**
- Endpoints de productos, proveedores, lotes y movimientos en `/api/docs/` (Swagger).
