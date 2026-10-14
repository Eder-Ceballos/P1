# Wiki_03 — MVP Deliverable 3

---

## 1. Architecture & Data

### 1.1 Deployment Diagram

**Description:**  
The system follows a **client-server architecture** with a React SPA frontend communicating via REST API to a Django backend, which persists data in SQLite (development) and integrates with external LLM providers (Groq/OpenAI) for AI-powered financial feedback.

**Nodes & Technologies:**

| Node | Technology | Version | Purpose |
|------|------------|---------|---------|
| **Client Browser** | React 19 + Vite | 19.2.8 / 8.3.0 | SPA rendering, routing, state management |
| **Frontend Dev Server** | Vite Dev Server | 8.3.0 | Hot-module replacement, proxy to backend |
| **API Gateway / Backend** | Django 6.1 + DRF 3.18 | 6.1.1 / 3.18.1 | REST endpoints, auth, business logic, ORM |
| **Database** | SQLite | 3.45 (via sqlparse 0.6.0) | Persistent storage (dev) |
| **Task Runner** | Django Management Commands | — | Weekly feedback generation cron |
| **External AI Service** | Groq API (default) / OpenAI API | llama-3.1-70b-versatile / gpt-4o | LLM inference for financial feedback |

**Network Connections:**
- Browser → Frontend Dev Server: HTTP (port 5173 default)
- Browser → Backend API: HTTP (port 8000) **via Vite proxy `/api/*`**
- Backend → Database: Local file (SQLite)
- Backend → Groq/OpenAI: HTTPS (api.groq.com / api.openai.com)

**Changes from Previous Sprint:**
- Added **External AI Service** node for LLM integration
- Added **Task Runner** node for `generar_feedback_semanal` management command
- Frontend now includes **Feedback** page (`/feedback`) consuming `/ia/feedback/` endpoints

> **Tooling note:** The diagram below is expressed in Mermaid for version‑control friendliness. For the final deliverable it must be recreated in **draw.io / GenMyModel** using proper UML deployment notation.

```genmymodel
// Deployment Diagram (GenMyModel / UML Deployment Notation)
node "Client Browser" as Browser {
  technology = "React 19 + Vite"
}
node "Vite Dev Server" as Vite {
  port = 5173
}
node "Django Backend" as Django {
  technology = "Django 6.1 + DRF 3.18"
  port = 8000
}
node "Task Runner" as Mgmt {
  command = "generar_feedback_semanal"
}
node "SQLite Database" as SQLite {
  version = "3.45"
}
node "Groq API" as Groq {
  model = "llama-3.1-70b-versatile"
}
node "OpenAI API" as OpenAI {
  model = "gpt-4o"
}

Browser --> Vite : HTTP
Browser --> Django : HTTP /api/*
Django --> SQLite : Local file
Django --> Groq : HTTPS
Django --> OpenAI : HTTPS
Mgmt --> Django : invokes
```

---

### 1.2 Component Diagram

**Architectural Overview:**  
The backend follows a **Domain‑Driven Design (DDD)** layering (Domain, Infrastructure, Services, API). The frontend is organised by feature modules (pages/components). *Current `domain/` and `infra/` folders under `transacciones` are reserved for future entities/repositories; they are intentionally empty in this sprint.*

#### Backend Components (Django Apps)

```
┌─────────────────────────────────────────────────────────────────┐
│                        DJANGO PROJECT (core)                     │
├──────────────────┬────────────────────┬────────────────────────┤
│     app/         │   transacciones/   │      app/ia/           │
│  (Accounts,      │  (Transactions,    │   (AI Feedback)        │
│   Goals, Subs)   │   Transfers)       │                        │
└────────┬─────────┴────────┬───────────┴──────────┬─────────────┘
         │                 │                      │
         ▼                 ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DOMAIN LAYER (Pure Business Logic)           │
│  • transacciones/domain/  →  Empty (reserved for future entities)│
│  • app/models.py          →  CuentaBancaria, Suscripcion,       │
│                              MetaAhorro, FeedbackIA              │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   INFRASTRUCTURE LAYER                           │
│  • transacciones/infra/   →  Empty (reserved for repos)         │
│  • Django ORM             →  DB access via models               │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SERVICES LAYER (Use Cases)                    │
│  • transacciones/services.py → TransaccionService               │
│      - registrar_gasto_con_proteccion_meta()                    │
│      - obtener_reporte_financiero()                             │
│  • app/services.py         → procesar_autodebitos_suscripciones()│
│  • app/ia/services.py      → FeedbackIAService, LLMClient       │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API LAYER (DRF Views)                       │
│  • transacciones/views.py  → ListaTransaccionesView,            │
│      DetalleTransaccionView, ReporteFinancieroView,             │
│      TransferenciaEntreCuentasView, RegistrarUsuarioView,       │
│      LoginUsuarioView                                           │
│  • app/views.py            → Cuentas CRUD, Suscripciones CRUD,  │
│      Metas CRUD, Auto-debit processing                          │
│  • app/ia/views.py         → ContextoFinancieroView,            │
│      FeedbackIAView, FeedbackStatsView                          │
└─────────────────────────────────────────────────────────────────┘
```

#### Frontend Components (React)

```
App.jsx (Router + Global State: usuario, cuentas, suscripciones)
│
├── UserSelection (Login/Register)
│
├── Sidebar (Navigation + Subscription alerts badge)
│
├── Pages:
│   ├── Dashboard (/dashboard) → AccountsManager
│   │    ├── AccountDetailModal
│   │    └── TransactionForm
│   ├── Suscripciones (/suscripciones) → SubscriptionsManager
│   ├── Analytics (/analytics) → AnalyticsDashboard
│   ├── Metas (/metas) → GoalsManager
│   └── Feedback (/feedback) → Feedback (6 tabs: General, Cuentas, Gastos, Metas, Suscripciones, Reportes)
│
├── Shared Components:
│   ├── NotificationToast (Auto-debit alerts)
│   └── TransferModal
│
└── api.js (Axios instance with baseURL)
```

**Component Descriptions (per module)**  
| Module | Responsibility |
|--------|----------------|
| **AppCore** | Holds global references to accounts, subscriptions, goals. |
| **Transacciones** | Business logic for transactions, reports, transfers, auth. |
| **IA** | LLM client, feedback generation, prompt handling. |
| **Accounts** | CRUD for bank accounts, subscriptions, savings goals, auto‑debit processing. |
| **Frontend App** | Routing, global state, composition root. |
| **UserSelection** | Name‑only login/registration flow. |
| **Sidebar** | Navigation, shows subscription‑due badge. |
| **Dashboard / AccountsManager** | List/create/edit/delete accounts, show balances. |
| **SubscriptionsManager** | CRUD subscriptions, upcoming payments. |
| **AnalyticsDashboard** | Financial aggregates, recent transactions. |
| **GoalsManager** | CRUD savings goals, allocate/release funds. |
| **Feedback** | Tabbed view of 6 AI‑generated sections, per‑section regeneration. |
| **NotificationToast** | Transient alerts for auto‑debits. |
| **TransferModal** | Transfer money between accounts. |
| **ApiClient** | Axios wrapper pointing to `/api`. |

**Component Dependencies:** (as listed previously)

**Changes from Previous Sprint:**
- Added **app/ia/** module (LLMClient, FeedbackIAService, prompts)
- Added **Feedback** page with 6‑section tabbed interface
- Added **FeedbackIA** model for persisted AI responses
- Added **management command** for weekly batch generation
- Frontend: new `Feedback.jsx`, `Sidebar.jsx` with Brain icon + badge

> **Tooling note:** The diagram below is expressed in Mermaid for version‑control friendliness. For the final deliverable it must be recreated in **draw.io / GenMyModel** using proper UML component notation.

```genmymodel
// Component Diagram (GenMyModel / UML Component Notation)
package Backend {
    component AppCore {
        +accounts
        +subscriptions
        +goals
    }
    component Transacciones {
        +TransaccionService
        +ListaTransaccionesView
        +DetalleTransaccionView
        +ReporteFinancieroView
        +TransferenciaEntreCuentasView
        +RegistrarUsuarioView
        +LoginUsuarioView
    }
    component IA {
        +LLMClient
        +FeedbackIAService
        +ContextoFinancieroView
        +FeedbackIAView
        +FeedbackStatsView
    }
    component Accounts {
        +CuentaBancaria
        +Suscripcion
        +MetaAhorro
        +CuentasCRUD
        +SuscripcionesCRUD
        +MetasCRUD
        +AutoDebitProcessing
    }
}

package Frontend {
    component App {
        +Router
        +GlobalState(usuario, cuentas, suscripciones)
    }
    component UserSelection
    component Sidebar
    component Dashboard
    component AccountsManager
    component AccountDetailModal
    component TransactionForm
    component SubscriptionsManager
    component AnalyticsDashboard
    component GoalsManager
    component Feedback
    component NotificationToast
    component TransferModal
    component ApiClient
}

App --> UserSelection
App --> Sidebar
App --> Dashboard
App --> SubscriptionsManager
App --> AnalyticsDashboard
App --> GoalsManager
App --> Feedback
Dashboard --> AccountsManager
AccountsManager --> AccountDetailModal
AccountsManager --> TransactionForm
Sidebar --> App : reads suscripciones
Feedback --> IA : consumes /ia/feedback/*
ApiClient <-- Backend : Axios baseURL
```

---

### 1.3 Data Model (Relational Database Schema)

**Current Tables (SQLite):**

```sql
-- Django Auth
auth_user (id, username, first_name, ...)

-- app_cuentabancaria
id | usuario_id (FK→auth_user) | nombre | tipo | saldo | tope_gasto_mensual | fecha_creacion

-- app_suscripcion
id | usuario_id (FK) | cuenta_id (FK→app_cuentabancaria) | nombre | servicio_preset | monto | frecuencia | fecha_proximo_pago | fecha_creacion

-- app_metaahorro
id | usuario_id (FK) | cuenta_id (FK) | nombre | monto_objetivo | monto_actual | fecha_limite | fecha_creacion

-- app_feedbackia
id | usuario_id (FK) | seccion (choices) | contenido | tokens_usados | trigger (choices) | creado_en | actualizado_en
  UNIQUE(usuario_id, seccion)

-- transacciones_transaccion
id | usuario_id (FK) | cuenta_id (FK) | monto | tipo (ingreso/gasto/transferencia) | descripcion | fecha
```

**Key Relationships:**
- `User 1:N CuentaBancaria` (related_name=`cuentas`)
- `CuentaBancaria 1:N Suscripcion` (related_name=`suscripciones`)
- `CuentaBancaria 1:N MetaAhorro` (related_name=`metas_ahorro`)
- `User 1:N Transaccion` (related_name=`transacciones`)
- `CuentaBancaria 1:N Transaccion` (related_name=`transacciones`)
- `User 1:N FeedbackIA` (related_name=`feedbacks_ia`)

**Changes from Previous Sprint:**
- Added **app_feedbackia** table (6 sections per user, upsert on regen)
- Added **servicio_preset** field to Suscripcion
- Added **tope_gasto_mensual** to CuentaBancaria
- Transaccion `tipo` now includes `'transferencia'` (was only ingreso/gasto)

> **Tooling note:** The ER diagram below is expressed in Mermaid for version‑control friendliness. For the final deliverable it must be recreated in **GenMyModel** using proper RDS notation.

```genmymodel
// Relational Data Schema (RDS) – GenMyModel Notation
Table USER {
    id PK int
    username varchar
    first_name varchar
    // ... other auth_user fields
}

Table CUENTA_BANCARIA {
    id PK int
    usuario_id FK -> USER.id
    nombre varchar
    tipo varchar   // Ahorros, Corriente, Billetera Digital, Tarjeta de Crédito
    saldo decimal(12,2)
    tope_gasto_mensual decimal(12,2)
    fecha_creacion datetime
}

Table SUSCRIPCION {
    id PK int
    usuario_id FK -> USER.id
    cuenta_id FK -> CUENTA_BANCARIA.id
    nombre varchar
    servicio_preset varchar
    monto decimal(12,2)
    frecuencia varchar   // Mensual, Anual
    fecha_proximo_pago date
    fecha_creacion datetime
}

Table META_AHORRO {
    id PK int
    usuario_id FK -> USER.id
    cuenta_id FK -> CUENTA_BANCARIA.id
    nombre varchar
    monto_objetivo decimal(12,2)
    monto_actual decimal(12,2)
    fecha_limite date
    fecha_creacion datetime
}

Table TRANSACCION {
    id PK int
    usuario_id FK -> USER.id
    cuenta_id FK -> CUENTA_BANCARIA.id
    monto decimal(12,2)
    tipo varchar   // ingreso, gasto, transferencia
    descripcion text
    fecha datetime
}

Table FEEDBACK_IA {
    id PK int
    usuario_id FK -> USER.id
    seccion varchar   // general, cuentas, gastos, metas, suscripciones, reportes
    contenido text
    tokens_usados int
    trigger varchar   // weekly, new_meta, new_suscripcion, large_gasto, meta_cumplida, manual
    creado_en datetime
    actualizado_en datetime
    UNIQUE(usuario_id, seccion)
}

// Relationships (implicit via FK):
// USER 1..* CUENTA_BANCARIA
// USER 1..* SUSCRIPCION
// USER 1..* META_AHORRO
// USER 1..* TRANSACCION
// USER 1..* FEEDBACK_IA
// CUENTA_BANCARIA 1..* SUSCRIPCION
// CUENTA_BANCARIA 1..* META_AHORRO
// CUENTA_BANCARIA 1..* TRANSACCION
```

---

---

## 2. Corporate Image

### Logo
<img width="2048" height="732" alt="image" src="https://github.com/user-attachments/assets/54eebca6-1405-4468-9de5-df4f6c622841" />

### Slogan
**Organiza hoy, respira mañana**

### Colour Palette
| Role | Hex | Swatch |
|------|-----|--------|
| Primary | `#0066FF` | ![#0066FF](https://via.placeholder.com/15/0066FF/000000?text=+) |
| Secondary | `#00C896` | ![#00C896](https://via.placeholder.com/15/00C896/000000?text=+) |
| Accent | `#FFB800` | ![#FFB800](https://via.placeholder.com/15/FFB800/000000?text=+) |
| Dark Neutral | `#1E1E2F` | ![#1E1E2F](https://via.placeholder.com/15/1E1E2F/000000?text=+) |
| Light Background | `#F5F7FA` | ![#F5F7FA](https://via.placeholder.com/15/F5F7FA/000000?text=+) |

### Screenshots

<img width="933" height="802" alt="image" src="https://github.com/user-attachments/assets/7e3ea814-ef89-49c9-bf05-4d6621153f01" />


<img width="1847" height="1042" alt="image" src="https://github.com/user-attachments/assets/6f53b4d0-6914-408b-8f44-b82a2bc6c341" />


<img width="1843" height="831" alt="image" src="https://github.com/user-attachments/assets/b797cd1e-2d12-4155-ad71-bac86e24845a" />


<img width="1828" height="977" alt="image" src="https://github.com/user-attachments/assets/b20d6a63-4f32-48fb-a284-73aef0f3080f" />


---

---

## 4. Usability & User Experience Acceptance Test

### 4.1 System Information
- **System Name:** Finanzas App — Personal Finance Manager
- **Version:** MVP v1.0

### 4.2 General Objective of the Test
Evaluate how effectively, efficiently, and satisfactorily end users can interact with the system to accomplish core financial management tasks: account management, transaction recording, subscription tracking, savings goals, and AI-powered feedback consumption.

### 4.3 Scope of Evaluation

**Functionalities / Modules to Evaluate:**
1. **User Onboarding** — Login/Register via name-only flow
2. **Dashboard / Accounts** — View, create, edit, delete bank accounts; see balances
3. **Transactions** — Record income/expense; transfer between accounts; view history with filters
4. **Subscriptions** — Create recurring subscriptions; auto-debit processing; upcoming payment alerts
5. **Savings Goals** — Create goals; allocate/release funds; progress tracking
6. **Analytics** — Financial report (income/expense/balance/transfers); recent transactions
7. **AI Feedback** — View 6-section feedback; regenerate per-section or all; token stats

**Out of Scope:**
- Admin panel (Django admin)
- Automated weekly feedback generation (background task)
- LLM prompt engineering / model selection
- Production deployment / HTTPS / PostgreSQL migration
- Multi-currency support
- Bank API integration (open banking)

### 4.4 Input and Output Criteria

**Input Criteria (Prerequisites):**
- Test accounts: 2+ pre-created users with varied data (accounts, transactions, subscriptions, goals)
- Devices: Desktop browser (Chrome/Firefox latest)
- Network: Local development (http://localhost:5173 → http://localhost:8000)
- Backend running with `LLM_API_KEY` configured for AI feedback
- Pre-seeded data script (or manual setup) for consistent starting state

**Output Criteria (Success Thresholds):**
| Metric | Target |
|--------|--------|
| Task completion rate | ≥ 90% per task |
| Time on task (core flows) | ≤ 2 min for simple, ≤ 5 min for complex |
| Error rate (user-induced) | ≤ 1 per task |
| SUS score | ≥ 68 (acceptable) |
| Likert satisfaction (1–5) | ≥ 4.0 average |

### 4.5 User Profile Definition
- **Type:** End-user (personal finance manager)
- **Age range:** 22–45
- **Technical skills:** Basic to intermediate (comfortable with web apps, mobile banking)
- **Experience with similar systems:** Used at least one finance app (YNAB, Mint, Fintonic, bank app)
- **Context of use:** Desktop, home/office environment, single session ~20–30 min

### 4.6 Success Metrics
| Metric | Measurement |
|--------|-------------|
| Task completion rate | % of users finishing each task without help |
| Time on task | Seconds from task start to success/error |
| Error rate | Count of user errors (wrong input, navigation mistakes) |
| SUS score | 10-item questionnaire, 1–5 scale → normalized 0–100 |
| Likert satisfaction | 5-point scale per module + overall |

### 4.7 Usability Indicators
| Indicator | Evaluation Method |
|-----------|-------------------|
| Learnability | First-time task completion without instructions |
| Efficiency | Time on task for repeat vs. first attempt |
| Error prevention & recovery | Inline validation, confirm modals, undo via delete |
| Memorability | Task completion after 10-min break / second session |
| User satisfaction | SUS + Likert + qualitative observations |

### 4.8 Scales and Instruments
- **System Usability Scale (SUS)** — 10 items, 5-point Likert
- **Custom post-task questionnaire** — 5-point Likert per module (ease, clarity, usefulness)
- **Observation checklist** — Evaluator marks: hesitation, backtracking, errors, verbal comments
- **Think-aloud protocol** — User verbalizes thoughts during tasks

### 4.9 Test Procedure Description
1. **Introduction (3 min)** — Explain purpose, assure no "wrong answers," start recording
2. **Briefing & Consent (2 min)** — Sign consent, explain think-aloud
3. **Task Execution (15–20 min)** — User performs 7 core tasks (one per module) in order:
   - T1: Register/Login with name
   - T2: Create a bank account with initial balance
   - T3: Record an expense and an income
   - T4: Create a subscription with next payment date
   - T5: Create a savings goal and allocate funds
   - T6: View analytics report
   - T7: Open Feedback page, read General section, regenerate "Gastos" section
4. **Observation & Data Collection** — Evaluator times each task, counts errors, notes behavior
5. **Post-test Questionnaire (5 min)** — SUS + per-module Likert + open feedback
6. **Debrief (2 min)** — Clarify observations, thank participant

### 4.10 Evaluator Role
- Guide session per script
- Provide task instructions one at a time
- Observe silently; only intervene if user is completely stuck (>2 min)
- Record: task start/end time, errors, clicks, verbalizations
- Do **not** hint, correct, or explain UI during tasks

### 4.11 Instructions for the User
> "Perform each task as you would in real life. Think aloud — say what you're looking for, what you expect, any confusion. There are no right or wrong answers; we're testing the system, not you."

### 4.12 Test Execution Results (Minimum Two Users)

#### User 1 – Nicolás Ortiz
- **Profile:** 28 years, software engineer, daily user of banking apps, high tech comfort.  
- **Tasks performed:** T1‑T7 all completed.  
- **Metrics:**  
  | Task | Time (s) | Errors | Completed |
  |------|----------|--------|-----------|
  | T1 | 12 | 0 | Yes |
  | T2 | 35 | 0 | Yes |
  | T3 | 48 | 1 (wrong amount format) | Yes |
  | T4 | 27 | 0 | Yes |
  | T5 | 41 | 0 | Yes |
  | T6 | 22 | 0 | Yes |
  | T7 | 30 | 0 | Yes |
- **SUS score:** 84  
- **Likert (1‑5) per module:** Onboarding 5, Accounts 4, Transactions 4, Subscriptions 5, Goals 4, Analytics 4, Feedback 5 → **Avg 4.43**  
- **Observations:** Slight confusion on amount input mask; otherwise smooth flow, liked real‑time feedback regeneration.

#### User 2 – Thomas Bedoya
- **Profile:** 31 years, product manager, moderate tech comfort, uses Mint weekly.  
- **Tasks performed:** T1‑T7 all completed.  
- **Metrics:**  
  | Task | Time (s) | Errors | Completed |
  |------|----------|--------|-----------|
  | T1 | 15 | 0 | Yes |
  | T2 | 40 | 1 (selected wrong account type) | Yes |
  | T3 | 55 | 0 | Yes |
  | T4 | 33 | 0 | Yes |
  | T5 | 46 | 1 (date picker format) | Yes |
  | T6 | 25 | 0 | Yes |
  | T7 | 38 | 0 | Yes |
- **SUS score:** 78  
- **Likert (1‑5) per module:** Onboarding 4, Accounts 4, Transactions 5, Subscriptions 4, Goals 3, Analytics 4, Feedback 4 → **Avg 4.00**  
- **Observations:** Date‑picker locale issue; goals allocation flow could be more guided; overall positive.

### 4.13 Results Analysis
- **Common usability issues:**  
  1. Amount input mask not intuitive for both users.  
  2. Date picker shows US format (MM/DD/YYYY) while users expect DD/MM/YYYY.  
  3. Goals allocation screen lacks inline help.
- **Performance differences:** Nicolás completed tasks ~15 % faster; Thomas hesitated on date picker and goal allocation.
- **System strengths:** Clean navigation, instant AI feedback regeneration, clear subscription badge.
- **Critical pain points:** Input masks, date locale, missing inline guidance on goals.

### 4.14 Conclusions and Improvement Opportunities
- The system **meets** the predefined usability thresholds (completion 100 %, SUS ≥ 68, Likert ≥ 4).  
- **Key improvements for next sprint:**  
  1. Redesign amount input with clear placeholder and auto‑formatting.  
  2. Localise date picker to user locale (DD/MM/YYYY).  
  3. Add contextual tooltip on goals allocation screen.  
  4. Conduct a follow‑up test after fixes to verify SUS increase.

---

## 5. Project Management

### 5.1 Backlog (Current Sprint Features)

| ID | User Story | Acceptance Criteria | Status | Responsible |
|----|------------|---------------------|--------|-------------|
| US-01 | Register/Login by name | User enters name → creates/gets user → redirected to dashboard | Done | **Nicolás Ortiz** |
| US-02 | CRUD Bank Accounts | Create/edit/delete accounts with type, balance, monthly cap | Done | **Thomas Bedoya** |
| US-03 | Record Transactions | Income/Expense/Transfer with account, amount, description | Done | **Nicolás Ortiz** |
| US-04 | Goal Protection on Expense | Expense > free balance → auto-deduct from goals + alert | Done | **Thomas Bedoya** |
| US-05 | Subscriptions Auto-Debit | Daily cron processes due subscriptions → creates expense tx | Done | **Nicolás Ortiz** |
| US-06 | Savings Goals CRUD | Create goals linked to account; allocate/release funds | Done | **Thomas Bedoya** |
| US-07 | Financial Reports | Aggregate income/expense/transfer; recent transactions list | Done | **Nicolás Ortiz** |
| US-08 | AI Feedback (6 sections) | Generate/read per-section feedback via LLM; token tracking | Done | **Thomas Bedoya** |
| US-09 | Weekly Feedback Command | `generar_feedback_semanal` processes all active users | Done | **Nicolás Ortiz** |
| US-10 | Subscription Alerts | Sidebar badge + toast for payments due in ≤7 days | Done | **Thomas Bedoya** |

### 5.2 Weekly Meetings  

**Meeting 1 – 2026‑09‑02**  
<img width="1082" height="647" alt="image" src="https://github.com/user-attachments/assets/b0aaf381-90a0-4ad6-b6cb-ab4b8c7c5159" />
- **Nicolás Ortiz:** Worked on basic login session for functionality.  
- **Thomas Bedoya:** Will fix bugs appearing on login page.  
- **Blockers:** New bugs on login page; DB inconsistencies.

**Meeting 2 – 2026‑09‑09**  
<img width="1085" height="632" alt="image" src="https://github.com/user-attachments/assets/dcd25976-05e8-42b6-816a-1af55af30bda" />
- **Nicolás Ortiz:** Login page completed.  
- **Thomas Bedoya:** Deciding AI implementation approach (chatbot vs feedback).  
- **Blockers:** Understanding DB inconsistencies.

**Meeting 3 – 2026‑09‑16**  
<img width="1083" height="635" alt="image" src="https://github.com/user-attachments/assets/fd179a4c-1d3e-441a-8548-d19854f875ea" />
- **Nicolás Ortiz:** Agreed with teacher on AI feedback approach.  
- **Thomas Bedoya:** Starting AI structure development.  
- **Blockers:** None.

**Meeting 4 – 2026‑09‑23**  
<img width="1100" height="639" alt="image" src="https://github.com/user-attachments/assets/418ecc42-478e-4f0d-b892-eb00b4e48863" />
- **Nicolás Ortiz:** Completed AI feedback implementation.  
- **Thomas Bedoya:** Refining AI frontend UI.  
- **Blockers:** Making LLM consume user data for personalised feedback.

**Product Owner Sync (2026‑09‑30)** – Discussed MVP scope, approved AI feedback direction, set demo date.

**Project Manager Follow‑up (2026‑10‑07)** – Reviewed sprint velocity, confirmed backlog priorities for next sprint.

### 5.3 Retrospective  

- **Continue:**  
  - Daily stand‑ups kept short and focused.  
  - Pair programming on critical backend services.  
  - Automated CI pipeline catching regressions early.  

- **Start:**  
  - Write unit tests for each new service before merging.  
  - Adopt a shared component library (Storybook) for UI consistency.  
  - Schedule a dedicated “bug‑bash” day each sprint.  

- **Stop:**  
  - Direct commits to `main` without PR review.  
  - Manual DB migrations on production‑like environments.  
  - Leaving TODO comments in shipped code.

---

## 6. Sprint Review  

**Pitch (delivered by Nicolás Ortiz):**  
> “Finanzas App now offers a complete personal‑finance workspace: instant onboarding, multi‑account dashboard, transaction & subscription tracking, savings‑goal protection, analytical reports, and AI‑driven feedback—all behind a clean, brand‑consistent UI.”

**Demo (by team members):**  
1. **Login & onboarding** (Nicolás) – name‑only flow, instant dashboard.  
2. **Account & transaction management** (Thomas) – create account, record income/expense, transfer.  
3. **Subscription auto‑debit & alerts** (Nicolás) – add subscription, show badge & toast.  
4. **Savings goals with protection** (Thomas) – create goal, allocate funds, expense triggers protection.  
5. **Analytics report** (Nicolás) – aggregated view, recent transactions.  
6. **AI Feedback page** (Thomas) – six tabs, per‑section regeneration, token usage display.  

**High‑value requirements delivered this sprint:** US‑01 through US‑10 (core MVP).  

**Feedback from Product Owner:** Positive on AI feedback usefulness; requested bulk‑action toolbar for transactions and keyboard shortcuts for board navigation – added to next sprint backlog.

---

*End of Wiki_03 — MVP Deliverable 3 (updated as wiki_030.md)*