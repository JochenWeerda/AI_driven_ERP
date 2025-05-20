# AI-Driven ERP

Ein modernes, Open-Source Warenwirtschaftssystem mit KI-Integration.

## 🚀 Features

- Moderne Web-Oberfläche (React)
- RESTful API (FastAPI)
- KI-Integration via Model Context Protocol (MCP)
- PostgreSQL Datenbank
- OAuth 2.0 Authentifizierung
- Responsive Design

## 🛠️ Technologie-Stack

### Backend
- FastAPI (Python)
- PostgreSQL
- MongoDB (für KI-Module)
- gRPC für interne Kommunikation

### Frontend
- React
- Tailwind CSS
- Material UI

### KI & Integration
- Model Context Protocol (MCP)
- LLM-Integration
- ML-Module für Prognosen und Automatisierung

## 📋 Voraussetzungen

- Python 3.9+
- Node.js 18+
- PostgreSQL 14+
- Docker (optional)

## 🚀 Installation

1. Repository klonen:
```bash
git clone https://github.com/JochenWeerda/AI_driven_ERP.git
cd AI_driven_ERP
```

2. Backend einrichten:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Unter Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

3. Frontend einrichten:
```bash
cd frontend
npm install
```

4. Umgebungsvariablen konfigurieren:
```bash
cp .env.example .env
# Bearbeiten Sie .env mit Ihren Konfigurationen
```

5. Datenbank initialisieren:
```bash
cd backend
alembic upgrade head
```

## 🏃‍♂️ Entwicklungsserver starten

### Backend
```bash
cd backend
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm run dev
```

## 📚 Dokumentation

- API-Dokumentation: http://localhost:8000/docs
- Frontend-Dokumentation: [docs/frontend.md](docs/frontend.md)
- MCP-Integration: [docs/mcp.md](docs/mcp.md)

## 🤝 Mitwirken

Beiträge sind willkommen! Bitte lesen Sie unsere [Contributing Guidelines](CONTRIBUTING.md).

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz - siehe [LICENSE](LICENSE) für Details.

## 📞 Kontakt

- GitHub Issues für Bug-Reports und Feature-Requests
- Pull Requests für Code-Beiträge
- Diskussionsforum (in Planung)