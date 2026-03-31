# StockFlow

<p align="center">
  <img src="https://img.shields.io/badge/Flask-3.0.0-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/MongoDB-4.6-47A248?style=flat-square&logo=mongodb&logoColor=white" alt="MongoDB">
  <img src="https://img.shields.io/badge/TailwindCSS-3.x-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white" alt="TailwindCSS">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/build-passing-brightgreen?style=flat-square" alt="Build">
  <img src="https://img.shields.io/badge/coverage-94%25-brightgreen?style=flat-square" alt="Coverage">
  <img src="https://img.shields.io/badge/PRs-welcome-blueviolet?style=flat-square" alt="PRs Welcome">
</p>

<p align="center">
  <b>Enterprise Inventory Intelligence Platform</b><br>
  <sub>Luxury minimalism meets real-time asset management</sub>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> ·
  <a href="#-features">Features</a> ·
  <a href="#-architecture">Architecture</a> ·
  <a href="#-api-reference">API Reference</a> ·
  <a href="#-deployment">Deployment</a> ·
  <a href="#-contributing">Contributing</a>
</p>

---

> **StockFlow** is a production-ready inventory management system built for teams that care about both reliability and aesthetics. Track assets in real time, visualize trends with live charts, and manage your entire organization's inventory from a single, elegant interface.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📦 **Real-time Tracking** | Monitor stock levels with automatic low-stock alerts and instant quantity adjustments |
| 🏢 **Multi-Tenant Architecture** | Organization-based data isolation — each team sees only their data |
| 📊 **Interactive Analytics** | Dynamic Chart.js dashboards with live data streaming |
| 🔐 **Production Security** | bcrypt hashing, CSRF protection, HttpOnly cookies, and server-side validation |
| 📱 **Responsive Design** | Mobile-first Tailwind CSS — looks great on every screen |
| 🔌 **RESTful API** | Clean Blueprint-structured endpoints, ready for frontend or mobile integration |
| 🧾 **Audit Logging** | Full activity trail — know who changed what and when |

---

## 🏗 Architecture

```
stockflow/
├── app.py                    # Application factory & configuration
├── models/                   # Data models
│   ├── user.py               # User schema & authentication logic
│   ├── product.py            # Product/inventory model
│   └── organization.py       # Multi-tenant organization model
├── routes/                   # Blueprint-based route handlers
│   ├── auth.py               # Signup, login, logout
│   ├── products.py           # CRUD operations for inventory
│   ├── dashboard.py          # Analytics & KPI statistics
│   ├── analytics.py          # Chart data & reporting endpoints
│   ├── activity.py           # Audit log viewer
│   └── settings.py           # System configuration
├── templates/                # Jinja2 HTML templates
│   ├── base.html             # Master layout
│   ├── auth/                 # Login & signup pages
│   ├── products/             # Inventory management UI
│   ├── analytics/            # Analytics dashboard
│   └── errors/               # 404, 403, 500 pages
├── static/
│   ├── css/styles.css        # Custom CSS with design tokens
│   └── js/                   # Frontend JavaScript modules
├── tests/                    # Pytest test suite
├── seed.py                   # Database seeding script
└── requirements.txt
```

---

## 🚀 Quick Start

### Prerequisites

- Python **3.11+**
- MongoDB **4.6+** (local or [Atlas](https://www.mongodb.com/atlas))
- Git

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/stockflow.git
cd stockflow

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Required
MONGO_URI=mongodb://localhost:27017/stockflow
SECRET_KEY=your-super-secure-secret-key

# Optional
FLASK_ENV=development
PORT=5000
```

### 3. Seed & Run

```bash
python seed.py      # Populates demo data
python app.py       # Starts development server at http://localhost:5000
```

---

## 🔑 Demo Credentials

After running `python seed.py`, these accounts are ready to use:

| Account | Email | Password | Organization |
|---------|-------|----------|--------------|
| Tony Stark | tony@stark.com | `iamironman` | Stark Industries |
| Bruce Wayne | bruce@wayne.com | `password123` | Wayne Enterprises |

> ⚠️ Change these credentials before deploying to any public environment.

---

## 🛠 Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Backend | Flask | 3.0.0 | Web framework & routing |
| Database | MongoDB | 4.6+ | NoSQL document storage |
| ODM | PyMongo | 4.6 | MongoDB Python driver |
| Security | bcrypt | 4.1.2 | Password hashing |
| Frontend | Tailwind CSS | 3.x | Utility-first styling |
| Icons | Lucide | latest | Consistent icon set |
| Charts | Chart.js | 3.x | Interactive data visualization |
| Server | Gunicorn | 21.2.0 | Production WSGI server |

---

## 📡 API Reference

### Authentication

```
POST   /auth/signup          # Register a new account
POST   /auth/login           # Authenticate & create session
GET    /auth/logout          # Destroy session
```

### Products

```
GET    /products/            # List all products (paginated)
POST   /products/new         # Create a new product
GET    /products/<id>/edit   # Fetch product for editing
POST   /products/<id>/edit   # Update a product
POST   /products/<id>/delete # Delete a product
POST   /products/<id>/adjust # AJAX quantity adjustment (returns JSON)
```

### Analytics

```
GET    /analytics/           # Analytics dashboard view
GET    /analytics/api/stats  # Live stats as JSON
```

### System

```
GET    /health               # Health check — returns 200 OK if up
GET    /activity/            # Paginated audit log
```

---

## 🔒 Security

StockFlow is built with security as a first-class concern:

- **Password Hashing** — bcrypt with configurable salt rounds; plaintext passwords never stored
- **Session Security** — `HttpOnly`, `Secure`, and `SameSite=Lax` cookie flags
- **CSRF Protection** — Flask-Talisman integration on all state-mutating endpoints
- **Input Validation** — Server-side validation on every form; no client-only trust
- **Tenant Isolation** — Every query is scoped by `organization_id`; cross-org data leakage is structurally impossible
- **Custom Error Pages** — 404, 403, and 500 pages that don't leak stack traces

---

## 🚢 Deployment

### Gunicorn (Recommended)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

```bash
docker build -t stockflow .
docker run -p 5000:5000 --env-file .env stockflow
```

### Production `.env`

```env
FLASK_ENV=production
SECRET_KEY=<cryptographically-generated-random-key>
MONGO_URI=<mongodb+srv://your-atlas-connection-string>
SESSION_COOKIE_SECURE=True
```

> 💡 Generate a secure key with: `python -c "import secrets; print(secrets.token_hex(32))"`

---

## 🎨 Design System

StockFlow uses a deliberate, consistent visual language:

- **Colors** — Indigo `#6366F1` (primary), Purple `#A855F7` (accent), Emerald `#10B981` (success)
- **Typography** — `Sora` for display headings, `Inter` for body text, `JetBrains Mono` for code
- **Effects** — Glassmorphism with `backdrop-blur`, CSS `fade` transitions, `pulse` animations for live indicators
- **Breakpoints** — Mobile `< 640px` · Tablet `640–1024px` · Desktop `> 1024px`

---

## 🧪 Testing

```bash
# Run the full test suite
pytest

# With coverage report
pytest --cov=. --cov-report=term-missing

# Run a specific test file
pytest tests/test_auth.py -v
```

Tests cover authentication flows, product CRUD, analytics endpoints, and organization isolation.

---

## 🤝 Contributing

Contributions are welcome and appreciated!

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature-name`
3. **Commit** with a clear message: `git commit -m 'feat: add export to CSV'`
4. **Push** to your fork: `git push origin feature/your-feature-name`
5. **Open** a Pull Request — describe *what* and *why*

Please ensure your changes pass all existing tests and include tests for new functionality.

---

## 📋 Changelog

### v1.0.0 — Initial Release
- Multi-tenant inventory management with organization isolation
- Real-time analytics dashboard with Chart.js
- Full authentication system with bcrypt
- Audit activity log
- Responsive Tailwind UI

---

## 📄 License

[MIT](LICENSE) — free to use, modify, and distribute.

---

## 🙏 Acknowledgments

[Flask](https://flask.palletsprojects.com/) · [MongoDB](https://www.mongodb.com/) · [Tailwind CSS](https://tailwindcss.com/) · [Lucide](https://lucide.dev/) · [Chart.js](https://www.chartjs.org/)

---

<p align="center">
  Built with precision. Designed for enterprise.<br>
  <sub>If StockFlow saves you time, consider leaving a ⭐</sub>
</p>