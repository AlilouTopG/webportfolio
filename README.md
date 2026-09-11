# ◈ ISE.LAB — Industrial & Systems Engineer Portfolio

> **OLED Cyberpunk** — `#0A0A0A` background · `#00E5FF` electric cyan · JetBrains Mono + Inter

A high-end, responsive portfolio for an **Industrial & Systems Engineer** specializing in **Python, Docker, DevOps & SCADA**. Built as a static site for **GitHub Pages** with a **Streamlit Cloud** wrapper from the same codebase.

Live: `https://<username>.github.io/<repo>/` (after first push — see Deploy)

---

## ✨ Flagship Projects

### 1 — NEXUS v5.0 Enterprise
**Hybrid Industrial SCADA & Digital Twin Platform**

Hybrid OT/IT platform that binds physical assets to a real-time digital twin.

- **Modbus TCP + MQTT (TLS, QoS 1/2)** — deterministic polling + pub/sub with offline buffering
- **Supabase RBAC / RLS** — Operator / Engineer / Admin roles, JWT, audit logs, Realtime
- **Ziegler-Nichols PID Auto-Tuning** — Ku/Tu detection → Kp/Ki/Kd, twin simulation, <4% overshoot
- **Digital Twin Engine** — live state replication, historical replay, what-if, canary deploys
- **Dockerized & Observable** — Compose (API/worker/broker/DB) + Prometheus/Grafana

→ Repository: `https://github.com/your-username/nexus-v5-enterprise` *(update link in `index.html`)*

Architecture:
```
Sensors / PLCs (Modbus TCP) → Edge Gateway (MQTT TLS) → NEXUS Core (FastAPI + Twin Engine) → Supabase (Postgres + RBAC + Realtime) → Dashboard (PID + Analytics)
```

### 2 — Server & Infrastructure Manager
**Robust System Administration & Server Monitoring Toolkit**

Agentless fleet ops for Linux homelabs → production.

- Real-time metrics: CPU/RAM/disk/network/systemd/Docker (10s granularity)
- Agentless orchestration via SSH + Python — bulk exec, playbooks, rollback
- Smart alerts + auto-heal, anomaly detection, incident timeline
- Vaulted secrets, key rotation, RBAC, full audit trail

→ Repository: `https://github.com/your-username/server-infra-manager` *(update link in `index.html`)*

Architecture:
```
Fleet (Linux / SSH) → Collector (Python + cron) → Core API (FastAPI + Postgres) → Alert Engine (Webhook / Email)
```

---

## 🧱 Stack

**Languages:** Python, FastAPI/Flask, JavaScript/TypeScript, SQL/PostgreSQL  
**DevOps:** Docker, Docker Compose, Kubernetes, GitHub Actions, Nginx, Linux, CI/CD, Terraform  
**SCADA / OT / IoT:** SCADA, Modbus TCP, MQTT, OPC UA, Digital Twin, PID Control, Ziegler-Nichols, Supabase RBAC

---

## 📁 Structure

```
/
├── index.html              # Single-page portfolio (hero, about, projects, contact)
├── css/style.css           # OLED theme (#0A0A0A / #00E5FF)
├── js/main.js              # Nav, reveal, parallax, contact handler
├── streamlit_app.py        # Streamlit Cloud wrapper (inlines the static site)
├── requirements.txt        # streamlit==1.40.2
├── .github/workflows/deploy.yml  # GitHub Pages auto-deploy
├── .nojekyll
└── .gitignore
```

---

## 🚀 Deploy

### Option A — GitHub Pages (Recommended, Automated)

1. Create a new GitHub repo (e.g. `webportfolio`) — **do NOT** initialize with README.
2. Push (commands are already run locally — see below):

```powershell
git remote add origin https://github.com/<USERNAME>/<REPO>.git
git branch -M main
git push -u origin main
```

3. In GitHub: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
4. The workflow `.github/workflows/deploy.yml` deploys on every `push` to `main`.  
   Live URL: `https://<USERNAME>.github.io/<REPO>/`

> Local verification: open `index.html` directly or `python -m http.server 8000`.

### Option B — Streamlit Cloud

1. Push the same repo (already includes `streamlit_app.py` + `requirements.txt`).
2. Go to **share.streamlit.io → New app →** select your repo → entry point `streamlit_app.py` → Deploy.

### Option C — Any Static Host (Netlify / Vercel / Nginx)

Upload the repo root as static files. No build step required.

---

## 🔧 Customize

- Update repository links: search `your-username` in `index.html`.
- Replace `hello@iselab.dev`, LinkedIn/GitHub URLs, and CV link.
- Colors: edit CSS variables in `css/style.css:1` (`--bg`, `--cyan`).
- Contact form: `handleContact()` in `js/main.js` is a demo — wire to Formspree / Supabase / your API.

---

## 📄 License

MIT — use freely for your own portfolio.
