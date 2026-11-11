# Biomédica Río Cuarto

## Sistema de gestión de stock e insumos médicos

Biomédica Río Cuarto es un sistema web desarrollado para facilitar la administración de productos e insumos médicos.

Su objetivo es llevar un control organizado del inventario, registrar movimientos de stock, consultar vencimientos y generar documentación comercial.

Este proyecto fue realizado en el marco de **Práctica Profesionalizante II**, correspondiente a la Tecnicatura Superior en Desarrollo de Software, año 2026.

---

## Índice

1. [Descripción del proyecto](#descripción-del-proyecto)
2. [Objetivos](#objetivos)
3. [Funcionalidades principales](#funcionalidades-principales)
4. [Tecnologías utilizadas](#tecnologías-utilizadas)
5. [Estructura del proyecto](#estructura-del-proyecto)
6. [Instalación y ejecución](#instalación-y-ejecución)
7. [Pruebas](#pruebas)
8. [Documentación](#documentación)
9. [Estado del proyecto](#estado-del-proyecto)
10. [Información académica](#información-académica)

---

## Descripción del proyecto

Biomédica Río Cuarto es un sistema de gestión destinado a una distribuidora de insumos médicos y de laboratorio.

Permite administrar productos, proveedores, lotes y movimientos de inventario desde una misma plataforma.

También facilita el seguimiento de los vencimientos y la generación de presupuestos y remitos en formato PDF.

## Objetivos

**Objetivo general**

Desarrollar un sistema web que permita organizar y controlar el inventario de una distribuidora de insumos médicos.

**Objetivos específicos**

- Facilitar el registro y la consulta de productos.
- Organizar la información de proveedores.
- Controlar las cantidades disponibles de cada lote.
- Identificar productos vencidos o próximos a vencer.
- Registrar entradas y salidas de stock.
- Mantener un historial de descartes.
- Generar presupuestos y remitos.
- Centralizar la información para facilitar las tareas administrativas.

## Funcionalidades principales

### Gestión de productos

- Registrar productos.
- Consultar y modificar sus datos.
- Organizar productos por categorías.
- Desactivar productos sin eliminarlos definitivamente.
- Consultar productos con stock bajo.

### Gestión de proveedores

- Registrar proveedores.
- Consultar y modificar información.
- Buscar proveedores.
- Activar y desactivar proveedores.

### Control de inventario

- Registrar lotes de productos.
- Consultar cantidades disponibles.
- Controlar fechas de vencimiento.
- Identificar lotes vencidos y próximos a vencer.
- Registrar movimientos de entrada y salida.
- Descartar lotes.
- Consultar el historial de descartes.
- Revertir descartes cuando corresponda.

### Documentos comerciales

- Registrar vendedores.
- Crear presupuestos.
- Crear remitos.
- Incorporar productos y cantidades.
- Calcular importes e IVA.
- Generar documentos en PDF.

### Panel principal

El sistema cuenta con un panel que muestra información general del inventario:

- Cantidad de productos activos.
- Stock disponible.
- Productos con stock bajo.
- Lotes vencidos.
- Lotes próximos a vencer.

### Acceso al sistema

El sistema utiliza autenticación de usuarios mediante Django.

Cuenta con dos roles definidos:

- Administrador.
- Superadministrador.

Está pensado principalmente para la gestión interna de una distribuidora.

## Tecnologías utilizadas

- Python 3.12
- Django 5
- Django REST Framework
- HTML
- CSS
- Bootstrap
- Base de datos relacional
- Git y GitHub
- pytest y pytest-django

## Estructura del proyecto

El sistema está organizado en diferentes aplicaciones de Django.

| Aplicación | Función |
|---|---|
| `accounts` | Usuarios y autenticación |
| `catalog` | Productos y categorías |
| `suppliers` | Proveedores |
| `inventory` | Lotes, movimientos de stock y descartes |
| `documentos` | Presupuestos, remitos y documentos PDF |
| `core` | Panel principal y funcionalidades generales |
| `audit` | Aplicación destinada a auditoría |

Esta organización permite separar las responsabilidades y mantener el código ordenado.

Se utilizan modelos para representar los datos, vistas para gestionar las solicitudes, formularios para validar información y servicios para aplicar las reglas de negocio.

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/LuciaAgostini/biomedica-rio-cuarto.git
cd biomedica-rio-cuarto
```

### 2. Crear y activar el entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

Crear un archivo `.env` a partir de `.env.example`.

Completar las variables necesarias para el funcionamiento de Django y la conexión con la base de datos.

### 5. Aplicar las migraciones

```bash
python manage.py migrate
```

### 6. Crear un usuario administrador

```bash
python manage.py createsuperuser
```

### 7. Ejecutar el servidor

```bash
python manage.py runserver
```

Ingresar desde el navegador a la dirección local indicada por Django.

## Pruebas

El proyecto incluye pruebas automatizadas para verificar algunas funcionalidades.

Para ejecutarlas:

```bash
python -m pytest -q
```

Para comprobar la configuración de Django:

```bash
python manage.py check
```

**Resultados de la última ejecución:**

- 3 pruebas aprobadas.
- Ningún error de configuración detectado.
- 3 advertencias relacionadas con el directorio de archivos estáticos.

## Documentación

El repositorio incluye una carpeta `docs/` con documentación complementaria:

| Archivo | Contenido |
|---|---|
| `01-historias-de-usuario.md` | Historias de usuario |
| `02-reglas-de-negocio-y-tests.md` | Reglas de negocio y pruebas |
| `03-modelo-de-datos.md` | Modelo de datos |
| `04-tablero-kanban.md` | Organización de tareas |
| `05-convenciones-git.md` | Convenciones de Git |
| `06-checklist-autoevaluacion.md` | Autoevaluación del proyecto |
| `07-deploy.md` | Información sobre despliegue |

## Estado del proyecto

Biomédica Río Cuarto cuenta con funcionalidades operativas para gestionar productos, proveedores, inventario y documentación comercial.

Actualmente se encuentra en etapa de revisión y preparación para su entrega final.

## Información académica

**Proyecto:** Biomédica Río Cuarto  
**Materia:** Práctica Profesionalizante II  
**Carrera:** Tecnicatura Superior en Desarrollo de Software  
**Institución:** ITEC Río Cuarto  
**Año:** 2026  
**Estudiante:** Lucía Cindy Agostini