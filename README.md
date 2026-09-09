
# Proyecto Finanzas — Backend API

Aplicación web para la gestión de finanzas personales, diseñada para registrar y administrar ingresos, egresos y flujos financieros. 

Este repositorio contiene la API fundacional construida con **Django** y **Django REST Framework (DRF)**, preparada para una futura integración con un frontend en **React** y microservicios de Inteligencia Artificial mediante **FastAPI**.

---

##  Tecnologías Utilizadas

* **Lenguaje:** Python 3.14+
* **Framework Web:** Django 6.1.1
* **API Framework:** Django REST Framework 3.18.1
* **Base de Datos:** SQLite (Desarrollo)

---

##  Requisitos Previos

Asegúrate de contar con **Python** (versión 3.14 o superior) y `pip` instalados en tu sistema operativo.

---

##  Instrucciones de Ejecución

Sigue estos pasos en orden para configurar y ejecutar el entorno de desarrollo local.

### 1. Clonar el repositorio y configurar el entorno virtual

```bash
# Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DE_LA_CARPETA>

# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Linux/macOS (Bash/Zsh):
source venv/bin/activate

# En Linux/macOS (Fish):
source venv/bin/activate.fish

# En Windows (CMD):
venv\Scripts\activate.bat

# En Windows (PowerShell):
venv\Scripts\Activate.ps1



### 2. Instalar dependencias

Instala todas las librerías necesarias ejecutando:

```bash
pip install -r requirements.txt

```

### 3. Configurar la Base de Datos

Aplica las migraciones para inicializar el esquema de la base de datos (*Usuarios*, *Categorías*, *Cuentas* y *Transacciones*):

```bash
python manage.py makemigrations
python manage.py migrate

```

*(Opcional)* Crea un superusuario para administrar la plataforma desde el panel de Django:

```bash
python manage.py createsuperuser

```

### 4. Ejecutar el Servidor

Inicia el servidor de desarrollo local:

```bash
python manage.py runserver

```

El servidor estará disponible en: **`http://127.0.0.1:8000/`**

---

## 🔌 Endpoints de la API

Actualmente, el sistema cuenta con el módulo fundacional de gestión de transacciones.

### Registrar Transacción Manual

* **URL:** `/api/transacciones/registrar/`
* **Método:** `POST`
* **Descripción:** Permite registrar un nuevo ingreso o gasto asociado a un usuario.

#### Ejemplo de Cuerpo de la Petición (`JSON`):

```json
{
  "usuario": 1,
  "tipo": "gasto",
  "monto": "45000.00",
  "fecha": "2026-09-08",
  "descripcion": "Compra de mercado en Tienda D1",
  "categoria": null,
  "cuenta": null
}

```

#### Respuestas:

| Código | Estado | Descripción |
| --- | --- | --- |
| `201 Created` | Éxito | Devuelve el objeto creado incluyendo su `id` asignado. |
| `400 Bad Request` | Error | Faltan campos obligatorios o los datos enviados son inválidos. |

---

##  Arquitectura del Sistema

El proyecto implementa principios de **Domain-Driven Design (DDD)** dentro de sus aplicaciones principales (ej. `transacciones/`), estructurando la lógica interna en capas claras:

* **Domain (`domain/`):** Modelos de dominio y reglas de negocio puras.
* **Infrastructure (`infra/`):** Interacción con la base de datos, ORM de Django y servicios externos.
* **Services (`services/`):** Casos de uso y orquestación de flujos financieros.

Esta separación desacoplada facilita la escalabilidad del sistema y la futura integración de módulos como gestión avanzada de cuentas bancarias y categorización automática mediante IA.

```

```
