# 🚀 SYNTX Wrapper Service - Die Komplette Anwendungs-Bibel

*"Dein AI-Butler mit Feld-Kalibrierung"* 🔥

---

## 📋 Inhaltsverzeichnis
- [🤔 Was ist das?](#-was-ist-das)
- [🚀 Quick Start (5 Minuten)](#-quick-start-5-minuten)
- [🏗️ Architektur-Überblick](#️-architektur-überblick)
- [⚙️ Installation & Setup](#️-installation--setup)
- [🎮 API Usage](#-api-usage)
- [📁 Wrapper Management](#-wrapper-management)
- [📊 Monitoring & Logging](#-monitoring--logging)
- [🔧 Configuration](#-configuration)
- [🐛 Troubleshooting](#-troubleshooting)
- [🚀 Deployment](#-deployment)

---

## 🤔 Was ist das?

**SYNTX Wrapper Service** ist ein Microservice, der AI-Requests mit konfigurierbaren Wrappern kalibriert. 

**Einfach gesagt:** Du schickst "Was ist KI?" und der Service macht daraus:
```
[SYNTX Init Wrapper]
[Cyberdark Wrapper]
Was ist KI?
```

**Resultat:** Bessere, kohärentere AI-Antworten.

---

## 🚀 Quick Start (5 Minuten)

### 1. Repository klonen
```bash
git clone https://github.com/your-org/syntx-wrapper
cd syntx-wrapper
```

### 2. Wrapper vorbereiten
```bash
# Wrapper-Verzeichnis erstellen
mkdir -p wrappers

# Basis-Wrapper hinzufügen
echo "SYNTX Initialization Field" > wrappers/syntx_init.txt
echo "Cyberdark Mode Activated" > wrappers/cyberdark.txt
```

### 3. Service starten
```bash
# Dependencies installieren
pip install -r requirements.txt

# Service starten
./run.sh
```

### 4. Ersten Request schicken
```bash
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Was ist KI?",
    "mode": "cyberdark",
    "include_init": true
  }'
```

**🎉 Fertig! Dein Service läuft.**

---

## 🏗️ Architektur-Überblick

### System-Architektur
```mermaid
graph TB
    A[Client] --> B[SYNTX Wrapper Service]
    B --> C[Wrapper Chain Loader]
    C --> D[Wrapper Files]
    B --> E[Field Calibration]
    E --> F[Backend AI Service]
    F --> G[AI Response]
    B --> H[JSONL Logging]
    B --> I[Human Logs]
    
    style B fill:#4CAF50
    style F fill:#2196F3
```

### Request Flow
```
1. 📥 Request empfangen
2. 🔄 Wrapper laden & kombinieren
3. 🎯 Input kalibrieren
4. 🚀 An Backend senden
5. 📊 Logging (parallel)
6. 📤 Response zurück
```

### Datei-Struktur
```
syntx-wrapper/
├── 📁 src/
│   ├── main.py              # FastAPI App
│   ├── models.py            # Data Models
│   ├── streams.py           # Core Logic
│   └── config.py            # Configuration
├── 📁 wrappers/             # Deine Wrapper Files
│   ├── syntx_init.txt
│   ├── cyberdark.txt
│   └── terminology.txt
├── 📁 logs/                 # Automatisch generiert
│   ├── wrapper_requests.jsonl
│   └── service.log
├── run.sh                   # Start Script
├── requirements.txt         # Python Dependencies
└── .env                     Configuration
```

---

## ⚙️ Installation & Setup

### Voraussetzungen
- **Python 3.8+**
- **pip** (Python Package Manager)
- **80MB** freier Speicher

### Schritt-für-Schritt Installation

#### 1. System vorbereiten
```bash
# Python Check
python3 --version
# Sollte 3.8 oder höher sein

# pip Check
pip3 --version
```

#### 2. Repository setup
```bash
git clone https://github.com/your-org/syntx-wrapper
cd syntx-wrapper

# Virtual Environment (empfohlen)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# oder venv\Scripts\activate  # Windows
```

#### 3. Dependencies installieren
```bash
pip install -r requirements.txt
```

#### 4. Wrapper konfigurieren
```bash
# Wrapper Verzeichnis erstellen
mkdir -p wrappers

# Beispiel Wrapper erstellen
cat > wrappers/syntx_init.txt << EOF
SYNTX Initialization Protocol
You are now running in SYNTX mode.
Respond in German, be direct and authentic.
EOF

cat > wrappers/cyberdark.txt << EOF
CYBERDARK MODE ACTIVATED
Respond with cyberpunk aesthetic.
Use technical terms and dark futuristic themes.
EOF
```

#### 5. Environment konfigurieren
```bash
# .env Datei erstellen
cat > .env << EOF
BACKEND_URL=https://your-ai-backend.com/api/chat
BACKEND_BEARER_TOKEN=your_token_here
PORT=8001
WRAPPER_DIR=./wrappers
LOG_DIR=./logs
EOF
```

#### 6. Service starten
```bash
# Testweise starten
./run.sh

# Oder im Hintergrund
nohup ./run.sh > service.log 2>&1 &
```

---

## 🎮 API Usage

### Base URL
```
http://localhost:8001
```

### Health Check
```bash
curl http://localhost:8001/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "syntx-wrapper-service", 
  "version": "1.0.0",
  "last_response": {
    "response": "Previous response...",
    "latency_ms": 245,
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### Chat Endpoint

**POST** `/api/chat`

```bash
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Erkläre mir Quantencomputer",
    "mode": "cyberdark",
    "include_init": true,
    "include_terminology": false,
    "max_new_tokens": 1000,
    "temperature": 0.7,
    "top_p": 0.95,
    "do_sample": true
  }'
```

#### Parameter Explained:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | **required** | Deine Frage/Input |
| `mode` | string | `"cyberdark"` | Wrapper Mode (Dateiname ohne .txt) |
| `include_init` | boolean | `true` | SYNTX Init Wrapper einbeziehen |
| `include_terminology` | boolean | `false` | Terminology Wrapper einbeziehen |
| `max_new_tokens` | integer | `500` | Maximale Antwort-Länge (1-4096) |
| `temperature` | float | `0.7` | Kreativität (0.0-2.0) |
| `top_p` | float | `0.95` | Diversity (0.0-1.0) |
| `do_sample` | boolean | `true` | Sampling aktivieren |

#### Response Format:
```json
{
  "response": "Die AI-Antwort hier...",
  "metadata": {
    "request_id": "a1b2c3d4-1234-5678-9101-abcdef123456",
    "wrapper_chain": ["syntx_init", "cyberdark"],
    "latency_ms": 347
  }
}
```

### Beispiel Requests

#### Einfacher Chat:
```bash
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hallo, wie geht es dir?"}'
```

#### Technischer Mode:
```bash
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Erkläre Machine Learning",
    "mode": "technical",
    "include_terminology": true,
    "max_new_tokens": 800
  }'
```

#### Kreativer Mode:
```bash
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Schreibe ein Gedicht über KI",
    "mode": "creative", 
    "temperature": 1.2,
    "max_new_tokens": 300
  }'
```

---

## 📁 Wrapper Management

### Wrapper Verzeichnis Struktur
```
wrappers/
├── syntx_init.txt          # Basis Initialisierung
├── terminology.txt         # Fach-Terminologie
├── cyberdark.txt           # Cyberpunk Style
├── technical.txt           # Technischer Mode
├── creative.txt            # Kreativer Mode
├── formal.txt              # Formeller Style
└── casual.txt              # Lockerer Style
```

### Wrapper erstellen

**Beispiel: `wrappers/creative.txt`**
```
CREATIVE MODE ACTIVATED 🎨

You are now in creative writing mode. Respond with:
- Poetic language
- Metaphors and analogies  
- Emotional depth
- Storytelling elements
- Creative formatting when appropriate

Ignore technical constraints, focus on artistic expression.
```

**Beispiel: `wrappers/technical.txt`**
```
TECHNICAL MODE ACTIVATED 🔧

You are now in technical analysis mode. Respond with:
- Precise technical terminology
- Structured explanations
- Data-driven insights
- Logical flow
- Code examples when relevant

Focus on accuracy and clarity over creativity.
```

### Wrapper Best Practices

1. **Kurz und prägnant** (50-500 Zeichen)
2. **Klare Anweisungen** 
3. **Spezifischer Use Case**
4. **Konsistente Formatierung**
5. **Testen, testen, testen!**

### Wrapper Chain Beispiele

| Use Case | Mode | Init | Terminology | Result |
|----------|------|------|-------------|---------|
| Standard Chat | `cyberdark` | ✅ | ❌ | Basic calibration |
| Technical Discussion | `technical` | ✅ | ✅ | Professional & precise |
| Creative Writing | `creative` | ✅ | ❌ | Artistic & expressive |
| Quick Answers | `casual` | ❌ | ❌ | Direct & unfiltered |

---

## 📊 Monitoring & Logging

### Log Files Overview

```
logs/
├── 📄 wrapper_requests.jsonl    # Machine-readable training data
├── 📄 service.log               # Human-readable logs  
└── 📄 field_flow.jsonl          # Detailed flow tracing
```

### JSONL Format (Training Data)
```json
{
  "timestamp": "2024-01-15T10:30:00.123Z",
  "request_id": "uuid-here",
  "prompt": "User input...",
  "mode": "cyberdark",
  "wrapper_chain": ["syntx_init", "cyberdark"],
  "response": "AI response...",
  "latency_ms": 345,
  "success": true
}
```

### Service Monitoring

#### Health Endpoint
```bash
curl -s http://localhost:8001/health | jq
```

**Output:**
```json
{
  "status": "healthy",
  "service": "syntx-wrapper-service",
  "version": "1.0.0",
  "last_response": {
    "response": "Previous AI response...",
    "latency_ms": 234,
    "timestamp": "2024-01-15T10:29:45Z"
  }
}
```

#### Log Analysis Beispiele

**Letzte 5 Requests anzeigen:**
```bash
tail -5 logs/wrapper_requests.jsonl | jq
```

**Fehler suchen:**
```bash
grep "success.*false" logs/wrapper_requests.jsonl
```

**Latenz analysieren:**
```bash
jq '.latency_ms' logs/wrapper_requests.jsonl | sort -n | tail -5
```

### Performance Metrics

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Response Time | < 500ms | 500-1000ms | > 1000ms |
| Error Rate | < 1% | 1-5% | > 5% |
| Memory Usage | < 100MB | 100-200MB | > 200MB |

---

## 🔧 Configuration

### Environment Variables

**.env File:**
```bash
# Backend Configuration
BACKEND_URL=https://your-ai-provider.com/api/chat
BACKEND_BEARER_TOKEN=your_secret_token_here
BACKEND_TIMEOUT=60

# Wrapper Configuration  
WRAPPER_DIR=./wrappers
FALLBACK_MODE=syntx_init

# Server Configuration
HOST=0.0.0.0
PORT=8001

# Logging Configuration
LOG_DIR=./logs
LOG_TO_CONSOLE=true
```

### Backend Configuration

**Supported AI Backends:**
- Custom HTTP endpoints
- OpenAI-compatible APIs
- Local model servers
- Any endpoint that accepts `{"prompt": "...", ...}`

**Example Backend Response Format:**
```json
{
  "response": "AI generated text here...",
  "usage": {"tokens": 150},
  "finish_reason": "stop"
}
```

### Security Configuration

```bash
# In .env
BACKEND_BEARER_TOKEN=sk-your_actual_token_here

# Headers werden automatisch hinzugefügt
Authorization: Bearer sk-your_actual_token_here
```

---

## 🐛 Troubleshooting

### Common Issues & Solutions

#### ❌ "Port already in use"
**Problem:**
```bash
Error: Port 8001 already in use!
```

**Lösung:**
```bash
# Port ändern
echo "PORT=8002" >> .env

# Oder bestehenden Prozess killen
lsof -ti:8001 | xargs kill -9
```

#### ❌ "Wrapper not found"
**Problem:**
```bash
⚠️ Wrapper not found: cyberdark
```

**Lösung:**
```bash
# Wrapper erstellen
echo "Cyberdark Mode" > wrappers/cyberdark.txt

# Verzeichnis prüfen
ls -la wrappers/
```

#### ❌ "Backend connection failed"
**Problem:**
```bash
❌ Error forwarding to backend: 404 Not Found
```

**Lösung:**
```bash
# Backend URL prüfen
cat .env | grep BACKEND_URL

# Test connection
curl -X POST $BACKEND_URL \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test"}'
```

#### ❌ "Module not found"
**Problem:**
```bash
ModuleNotFoundError: No module named 'fastapi'
```

**Lösung:**
```bash
# Dependencies installieren
pip install -r requirements.txt

# Virtual Environment aktivieren
source venv/bin/activate
```

### Debug Mode

**Service mit Debug logging starten:**
```bash
LOG_TO_CONSOLE=true python3 -m uvicorn src.main:app --reload --log-level debug
```

**Detailed Flow Tracing:**
```bash
tail -f logs/field_flow.jsonl | jq
```

### Performance Optimization

**Für hohe Last:**
```bash
# In .env
BACKEND_TIMEOUT=30
LOG_TO_CONSOLE=false

# Mit mehr Workers starten
python3 -m uvicorn src.main:app --workers 4 --port 8001
```

---

## 🚀 Deployment

### Production Setup

#### 1. Systemd Service (Linux)
**Datei:** `/etc/systemd/system/syntx-wrapper.service`
```ini
[Unit]
Description=SYNTX Wrapper Service
After=network.target

[Service]
Type=exec
User=ubuntu
WorkingDirectory=/opt/syntx-wrapper
EnvironmentFile=/opt/syntx-wrapper/.env
ExecStart=/opt/syntx-wrapper/run.sh
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**Aktivieren:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable syntx-wrapper
sudo systemctl start syntx-wrapper
sudo systemctl status syntx-wrapper
```

#### 2. Docker Deployment
**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p wrappers logs

EXPOSE 8001

CMD ["./run.sh"]
```

**Docker Compose:**
```yaml
version: '3.8'
services:
  syntx-wrapper:
    build: .
    ports:
      - "8001:8001"
    volumes:
      - ./wrappers:/app/wrappers
      - ./logs:/app/logs
    env_file:
      - .env
    restart: unless-stopped
```

#### 3. Environment Checklist

**Before Going Live:**
- [ ] `.env` configured with production values
- [ ] Wrapper files reviewed and tested
- [ ] Backend API token validated
- [ ] Log rotation configured
- [ ] Monitoring alerts setup
- [ ] Backup strategy for wrappers
- [ ] Security review completed

### Scaling Considerations

**Für 100+ Requests/Minute:**
- Use reverse proxy (nginx)
- Implement rate limiting
- Add database for wrapper management
- Use process manager (gunicorn)

**Für 1000+ Requests/Minute:**
- Load balancer setup
- Redis for caching
- Multiple service instances
- Distributed logging

---

## 🎯 Quick Reference

### Useful Commands

```bash
# Service starten
./run.sh

# Health check
curl http://localhost:8001/health

# Test request
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Test"}'

# Logs anzeigen
tail -f logs/service.log

# JSONL Logs analysieren
jq '.' logs/wrapper_requests.jsonl | tail -5
```

### File Locations
| Purpose | Location |
|---------|----------|
| Wrapper Files | `./wrappers/*.txt` |
| Configuration | `./.env` |
| JSONL Logs | `./logs/wrapper_requests.jsonl` |
| Service Logs | `./logs/service.log` |
| Source Code | `./src/` |

### Support

**Bei Problemen:**
1. Logs checken: `tail -f logs/service.log`
2. Health endpoint: `curl http://localhost:8001/health`
3. Wrapper Verzeichnis prüfen: `ls -la wrappers/`
4. Issue erstellen mit Log-Auszügen

---

## 🎉 Willkommen im SYNTX Universe!

Du hast jetzt einen voll funktionsfähigen AI-Wrapper Service. Viel Spaß beim Kalibrieren! 🚀

**Remember:** Gute Wrapper = Gute Antworten. Teste verschiedene Kombinationen und finde deinen perfekten Setup!

---
*Letzte Aktualisierung: Januar 2024 | SYNTX Wrapper Service v1.0.0*