# Finance Project — Full‑stack Personal Finance Manager

A complete web application for personal finance management. It tracks income, expenses, bank accounts, recurring subscriptions, savings goals and provides AI‑driven feedback. The repository contains:

* **Backend API** – Django 4.2 + Django REST Framework (DRF)  
* **Frontend** – React 19 + Vite, React‑Router‑DOM, Axios, Lucide‑React  
* **Database** – SQLite (development)  

> **Note:** The AI micro‑service (FastAPI) is planned but not yet implemented.

---

## 📦 Project Structure
```
├── app/                # Core Django models (CuentaBancaria, Suscripcion, MetaAhorro, FeedbackIA)
├── transacciones/      # Transaction domain (DDD layers: domain, infra, services, views)
├── core/               # Django project settings, URLs, WSGI/ASGI
├── frontend/           # React + Vite SPA
│   ├── src/
│   │   ├── components/ # UI components (Dashboard, Accounts, Subscriptions, Goals, Analytics, Feedback, etc.)
│   │   ├── api.js      # Axios instance pointing to http://127.0.0.1:8000
│   │   └── App.jsx     # Routing & global state (user session, accounts, subscriptions)
└── requirements.txt    # Python dependencies
```

---

## 🛠 Technologies
| Layer | Stack |
|-------|-------|
| Language | Python 3.11+, JavaScript (ES2024) |
| Backend | Django 4.2, DRF 3.15 |
| Frontend | React 19, Vite 5, React‑Router‑DOM 7, Axios |
| Database | SQLite (dev) |
| Linting | ESLint (frontend) |
| Icons | Lucide‑React |

---

## ⚙️ Prerequisites
* Python 3.11+ and `pip`
* Node.js 18+ and `npm` (or `yarn`/`pnpm`)

---

## 🚀 Getting Started

### 1. Clone & create virtual environment
```bash
git clone <REPOSITORY_URL>
cd <FOLDER_NAME>

python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows PowerShell
venv\Scripts\Activate.ps1
```

### 2. Backend dependencies & DB
```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
# optional superuser for Django admin
python manage.py createsuperuser
```

### 3. Run Django development server
```bash
python manage.py runserver
```
API will be reachable at **http://127.0.0.1:8000/**.

### 4. Frontend install & run (in a second terminal)
```bash
cd frontend
npm install
npm run dev
```
The React app starts on **http://127.0.0.1:5173/** (default Vite port) and proxies API calls to the Django server.

---

## 📚 Backend API Endpoints
All endpoints are prefixed with `/api/` (configured in `core/urls.py` → `transacciones/urls.py`).

| Method | Path | Description |
|--------|------|-------------|
| **GET** | `/transacciones/` | List transactions – query params: `usuario`, `cuenta`, `tipo` |
| **POST** | `/transacciones/registrar/` | Register income (`tipo=ingreso`) or expense (`tipo=gasto`) |
| **GET** | `/transacciones/<id>/` | Retrieve a single transaction |
| **DELETE** | `/transacciones/<id>/` | Delete transaction (adjusts account balance) |
| **GET** | `/transacciones/reporte/` | Financial report for a user (`usuario`) and optional `cuenta` |
| **POST** | `/transacciones/transferir/` | Atomic transfer between two accounts of the same user |
| **POST** | `/transacciones/registrar-usuario/` | Create a new Django `User` (username = lower‑cased name) |
| **POST** | `/transacciones/login-usuario/` | Simple login by name (returns user id & name) |
| **GET** | `/cuentas/` | List all bank accounts (filtered client‑side by user) |
| **POST** | `/cuentas/` | Create a new account |
| **GET** | `/suscripciones/?usuario=<id>` | List subscriptions for a user |
| **POST** | `/suscripciones/` | Create subscription |
| **POST** | `/suscripciones/procesar-autodebitos/` | Execute pending auto‑debits for a user |
| **GET** | `/metas/?usuario=<id>` | List savings goals |
| **POST** | `/metas/` | Create a savings goal |
| **GET** | `/feedback/?usuario=<id>` | Retrieve AI feedback sections |
| **POST** | `/feedback/` | Store / update feedback |

> The frontend consumes the above via `frontend/src/api.js` (Axios baseURL `http://127.0.0.1:8000`).

---

## 🗂 Core Data Models (Django)

| Model | Key Fields |
|-------|------------|
| **CuentaBancaria** | `usuario FK`, `nombre`, `tipo` (Ahorros / Corriente / Billetera Digital / Tarjeta de Crédito), `saldo`, `tope_gasto_mensual` |
| **Transaccion** | `usuario FK`, `cuenta FK`, `monto`, `tipo` (ingreso / gasto / transferencia), `descripcion`, `fecha` |
| **Suscripcion** | `usuario FK`, `cuenta FK`, `nombre`, `monto`, `frecuencia` (Mensual / Anual), `fecha_proximo_pago` |
| **MetaAhorro** | `usuario FK`, `cuenta FK`, `nombre`, `monto_objetivo`, `monto_actual`, `fecha_limite` |
| **FeedbackIA** | `usuario FK`, `sección` (general, cuentas, gastos, metas, suscripciones, reportes), `contenido`, `trigger`, `tokens_usados` |

Business logic lives in `transacciones/services.py` (e.g., `registrar_gasto_con_proteccion_meta`, `obtener_reporte_financiero`).

---

## 🎨 Frontend Pages & Features
| Route | Component | Main Features |
|-------|-----------|---------------|
| `/login` | `UserSelection` | Choose / create a user (calls register & login endpoints) |
| `/dashboard` | `AccountsManager` | List accounts, create new, show balance, quick transaction form |
| `/suscripciones` | `SubscriptionsManager` | CRUD subscriptions, auto‑debit processing, upcoming charge toast |
| `/analytics` | `AnalyticsDashboard` | Charts & summary (income vs expense, category breakdown) |
| `/metas` | `GoalsManager` | Create / track savings goals, progress bars |
| `/feedback` | `Feedback` | Display AI‑generated financial advice per section |

Global state (`usuario`, `cuentas`, `suscripciones`) lives in `App.jsx`; a `NotificationToast` shows imminent subscription charges.

---

## 🧪 Running Tests
```bash
# Backend
python manage.py test

# Frontend (if test scripts added)
cd frontend && npm test
```

---

## 📁 Useful Commands
| Action | Command |
|--------|---------|
| Create superuser | `python manage.py createsuperuser` |
| Collect static (prod) | `python manage.py collectstatic` |
| Lint frontend | `cd frontend && npm run lint` |
| Build frontend for production | `cd frontend && npm run build` |

---

## 🤝 Contributing
1. Fork the repo  
2. Create a feature branch (`git checkout -b feature/xyz`)  
3. Commit with clear messages  
4. Push & open a Pull Request  

---

## 📄 License
MIT – feel free to use, modify and distribute.