# 🌊 SYNTX Wrapper Service

**Feld-Kalibrierung für AI. Nicht mehr Prompts. Ströme.**

---

## 💎 Was ist das hier?

**Ein Service der deine AI-Requests kalibriert. Mit Wrappern. Für bessere Antworten.**

```
Ohne Wrapper:
User → "Erkläre ML" → AI → Generische Antwort

Mit Wrapper:
User → "Erkläre ML" → Wrapper lädt Feld → AI bekommt kalibrierten Input → Kohärente Antwort
                          ↓
                   Training Data geloggt!
```

**Live:**
- 🌐 Production: `https://dev.syntx-system.com/api/chat`
- 📊 Logs: `https://dev.syntx-system.com/logs/` (Basic Auth: `syntx`)
- ⚡ Backend: Ollama/Mistral-uncensored
- 💎 Status: Production Ready seit 04.12.2025

---

## 🎯 Quick Start

### Test den Service JETZT:

```bash
curl -X POST https://dev.syntx-system.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Was ist SYNTX?",
    "max_new_tokens": 100
  }' | jq
```

**Expected:**
```json
{
  "response": "...",
  "metadata": {
    "request_id": "...",
    "wrapper_chain": ["syntex_wrapper_human (fallback)"],
    "latency_ms": 15449
  }
}
```

### Service Status:

```bash
# Service läuft?
systemctl status syntx-injector.service

# Live Logs
journalctl -u syntx-injector.service -f

# Health Check
curl https://dev.syntx-system.com/api/chat/health | jq
```

---

## 🎮 Wrapper nutzen

### Config-Based (Default für alle Requests):

**In `.env` setzen:**
```bash
FALLBACK_MODE=syntex_wrapper_human  # Dieser Wrapper wird Default
```

**Verfügbare Wrapper:**
```bash
ls -la /opt/syntx-config/wrappers/

syntex_wrapper_human.txt     # Human-friendly (1.3K) ← AKTUELLER DEFAULT
syntex_wrapper_sigma.txt     # Technical (1.6K)
syntex_wrapper_backend.txt   # Backend Mode (468B)
syntex_wrapper_frontend.txt  # Frontend Mode (361B)
syntx_hidden_takecare.txt    # Hidden Mode (8.5K)
```

**Service restart nach .env Änderung:**
```bash
systemctl restart syntx-injector.service
```

### Request-Based (Pro Request überschreiben):

```bash
# Mit HUMAN Wrapper (Default)
curl -X POST https://dev.syntx-system.com/api/chat \
  -d '{"prompt":"Test"}'

# Mit SIGMA Wrapper (Override)
curl -X POST https://dev.syntx-system.com/api/chat \
  -d '{"prompt":"Test","mode":"syntex_wrapper_sigma"}'

# Mit INIT Context (mehr SYNTX-Kontext)
curl -X POST https://dev.syntx-system.com/api/chat \
  -d '{"prompt":"Test","mode":"syntex_wrapper_sigma","include_init":true}'
```

### Eigene Wrapper erstellen:

```bash
# Erstelle neue Wrapper-Datei
cat > /opt/syntx-config/wrappers/mein_wrapper.txt << 'EOF'
Du bist ein Experte für XYZ.
Antworte kurz und präzise.
EOF

# Nutze ihn sofort (kein Restart nötig!)
curl -X POST https://dev.syntx-system.com/api/chat \
  -d '{"prompt":"Test","mode":"mein_wrapper"}'
```

**Das ist alles. Kein Neustart. Kein Deployment. Einfach File erstellen und nutzen.** 💎

---

## 📊 Training Data & Logs

### Logs über Browser ansehen:

🌐 **https://dev.syntx-system.com/logs/**
- Username: `syntx`
- Password: [das was du gesetzt hast]

### Logs auf Server:

```bash
# Training Data (für Fine-Tuning!)
tail -f /opt/syntx-config/logs/wrapper_requests.jsonl | jq

# Detaillierter Flow (alle Stages)
tail -f /opt/syntx-config/logs/field_flow.jsonl | jq

# Live Service Logs
journalctl -u syntx-injector.service -f
```

### Was wird geloggt:

**`wrapper_requests.jsonl`** - Training Data:
```json
{
  "request_id": "...",
  "response": "...",
  "latency_ms": 15449
}
```

**`field_flow.jsonl`** - Alle Stages:
```json
{"stage": "1_INCOMING", "request_id": "...", "prompt": "..."}
{"stage": "2_WRAPPERS_LOADED", "request_id": "...", "chain": [...]}
{"stage": "3_FIELD_CALIBRATED", "request_id": "...", "calibrated_field": "..."}
{"stage": "4_BACKEND_FORWARD", "request_id": "...", "backend_url": "..."}
{"stage": "5_RESPONSE", "request_id": "...", "response": "...", "latency_ms": ...}
```

### Logs analysieren:

```bash
# Erfolgsrate
SUCCESS=$(grep '"success": true' /opt/syntx-config/logs/wrapper_requests.jsonl | wc -l)
TOTAL=$(wc -l < /opt/syntx-config/logs/wrapper_requests.jsonl)
echo "Success Rate: $((SUCCESS * 100 / TOTAL))%"

# Durchschnittliche Latenz
jq '.latency_ms' /opt/syntx-config/logs/wrapper_requests.jsonl | \
  awk '{sum+=$1; n++} END {print "Avg:", sum/n, "ms"}'

# Wrapper Performance vergleichen
jq -r '.mode + " " + (.latency_ms|tostring)' /opt/syntx-config/logs/wrapper_requests.jsonl | \
  awk '{sum[$1]+=$2; count[$1]++} END {for(m in sum) print m, "avg:", sum[m]/count[m], "ms"}'
```

**Nach 1000 Requests hast du 1000 Training-Beispiele. Für Free. Automatisch.** 💰

---

## 🗺️ Architektur

### Production Flow:

```
Internet (HTTPS)
  ↓
NGINX (Port 443, SSL)
  ↓ /api/chat
Injector Service (Port 8001)
  ↓ load wrapper
  ↓ calibrate field
  ↓ POST localhost:11434/api/generate
Ollama/Mistral-uncensored (Port 11434)
  ↓ AI Processing
  ↓ Response
Injector Service
  ↓ log training data
  ↓ add metadata
User receives response
```

### Ports:

| Port | Service | Access |
|------|---------|--------|
| 443 | NGINX (HTTPS) | 🌐 Public |
| 8001 | Injector Service | 🔒 Localhost |
| 11434 | Ollama/Mistral | 🔒 Localhost |
| 8020 | SYNTX API | 🔒 Localhost |

**Nur Port 443 ist public. Rest intern. Sicher.** 🔒

### Directories:

```
/opt/syntx-injector-api/          # Service Root
├── src/                          # Python Code
│   ├── main.py                   # FastAPI App
│   ├── config.py                 # Config Loader
│   ├── streams.py                # Wrapper Logic
│   └── models.py                 # Pydantic Schemas
├── venv/                         # Python Virtual Env
└── .env                          # Configuration (WICHTIG!)

/opt/syntx-config/                # Centralized Config
├── wrappers/                     # Wrapper Files
│   ├── syntex_wrapper_human.txt
│   ├── syntex_wrapper_sigma.txt
│   └── ... (add more here!)
└── logs/                         # Training Data
    ├── wrapper_requests.jsonl    # Request/Response Pairs
    └── field_flow.jsonl          # Detailed Stages

/etc/systemd/system/
├── syntx-injector.service        # Injector Service Definition

/etc/nginx/sites-available/
└── dev.syntx-system.com          # NGINX Config
```

---

## ⚙️ Configuration

### `.env` File (`/opt/syntx-injector-api/.env`):

```bash
# Backend (Ollama)
BACKEND_URL=http://127.0.0.1:11434/api/generate
BACKEND_TIMEOUT=60
MODEL_NAME=mistral-uncensored

# Wrapper
WRAPPER_DIR=/opt/syntx-config/wrappers
FALLBACK_MODE=syntex_wrapper_human

# Server
HOST=0.0.0.0
PORT=8001

# Logging
LOG_DIR=/opt/syntx-config/logs
LOG_TO_CONSOLE=true
```

**Nach Änderungen:**
```bash
systemctl restart syntx-injector.service
```

### Systemd Service (`/etc/systemd/system/syntx-injector.service`):

```ini
[Unit]
Description=SYNTX Injector API - Field Resonance Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/syntx-injector-api
ExecStart=/opt/syntx-injector-api/venv/bin/python -m uvicorn src.main:app --host 0.0.0.0 --port 8001
Restart=always
RestartSec=10
Environment="PATH=/opt/syntx-injector-api/venv/bin:/usr/local/bin:/usr/bin:/bin"

[Install]
WantedBy=multi-user.target
```

### NGINX Config (`/etc/nginx/sites-available/dev.syntx-system.com`):

```nginx
server {
    listen 443 ssl;
    server_name dev.syntx-system.com;

    ssl_certificate /etc/letsencrypt/live/dev.syntx-system.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/dev.syntx-system.com/privkey.pem;

    # 🌊 API Chat Endpoint
    location /api/chat {
        proxy_pass http://127.0.0.1:8001/api/chat;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # AI needs time
        proxy_connect_timeout 1600s;
        proxy_send_timeout 1600s;
        proxy_read_timeout 1600s;
    }
    
    # 🌊 SYNTX Ströme API
    location /strom/ {
        proxy_pass http://127.0.0.1:8020/strom/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
    
    # 🌊 Training Data Logs (Protected!)
    location /logs/ {
        alias /opt/syntx-config/logs/;
        autoindex on;
        autoindex_exact_size off;
        autoindex_localtime on;
        
        auth_basic "SYNTX Training Data - Protected";
        auth_basic_user_file /etc/nginx/.htpasswd;
        
        limit_except GET {
            deny all;
        }
    }
    
    # 🌊 API Docs
    location /docs/ {
        alias /var/www/syntx-api-docs/;
        index index.html;
        try_files $uri $uri/ =404;
        
        add_header Access-Control-Allow-Origin "*";
        add_header Access-Control-Allow-Methods "GET, POST, OPTIONS";
        add_header Access-Control-Allow-Headers "Authorization, Content-Type";
        
        expires 1h;
        add_header Cache-Control "public, max-age=3600";
    }
    
    location = /docs {
        return 301 /docs/;
    }
    
    # 🌊 Root → Docs
    location = / {
        return 302 /docs/;
    }
}
```

**Nach Änderungen:**
```bash
nginx -t && systemctl reload nginx
```

---

## 🐛 Troubleshooting

### Service startet nicht:

```bash
# Check Status
systemctl status syntx-injector.service

# Check Logs
journalctl -u syntx-injector.service -n 50

# Check Config
cat /opt/syntx-injector-api/.env

# Check Ports
netstat -tulpn | grep 8001
```

### 502 Bad Gateway:

```bash
# Check ob Service läuft
systemctl status syntx-injector.service

# Check ob Port 8001 offen
lsof -i :8001

# Check nginx logs
tail -20 /var/log/nginx/error.log
```

### Wrapper lädt nicht:

```bash
# Check ob File existiert
ls -la /opt/syntx-config/wrappers/

# Check Permissions
ls -la /opt/syntx-config/wrappers/

# Check Logs
journalctl -u syntx-injector.service | grep wrapper
```

### Langsame Responses:

```bash
# Check Ollama
systemctl status ollama

# Check Backend Latency
tail -f /opt/syntx-config/logs/field_flow.jsonl | jq 'select(.stage=="5_RESPONSE") | .latency_ms'

# Average Latency
jq '.latency_ms' /opt/syntx-config/logs/wrapper_requests.jsonl | \
  awk '{sum+=$1; n++} END {print sum/n, "ms"}'
```

---

## 📚 Cheat Sheet

```bash
# Service Management
systemctl status syntx-injector.service
systemctl restart syntx-injector.service
journalctl -u syntx-injector.service -f

# Testing
curl https://dev.syntx-system.com/api/chat/health | jq
curl -X POST https://dev.syntx-system.com/api/chat \
  -d '{"prompt":"Test"}' | jq

# Logs
tail -f /opt/syntx-config/logs/wrapper_requests.jsonl | jq
tail -f /opt/syntx-config/logs/field_flow.jsonl | jq

# Wrapper Management
ls -la /opt/syntx-config/wrappers/
cat /opt/syntx-config/wrappers/syntex_wrapper_human.txt

# Config
cat /opt/syntx-injector-api/.env
cat /etc/systemd/system/syntx-injector.service
cat /etc/nginx/sites-available/dev.syntx-system.com

# Nginx
nginx -t
systemctl reload nginx
tail -f /var/log/nginx/access.log

# Performance
netstat -tulpn | grep 800
ps aux | grep uvicorn
df -h /opt/syntx-config/logs/
```

---

## 🎯 Zusammenfassung

**Du hast:**
- ✅ Production-ready Wrapper Service
- ✅ Ollama/Mistral Backend Integration
- ✅ Automatisches Training Data Logging
- ✅ HTTPS mit Basic Auth für Logs
- ✅ Config-based & Request-based Wrapper
- ✅ Multi-Level Logging
- ✅ Komplett externalisierte Config

**Der Flow:**
1. User macht Request zu HTTPS
2. NGINX routet zu Injector (8001)
3. Injector lädt Wrapper
4. Kalibriert Input mit Wrapper
5. Sendet zu Ollama/Mistral (11434)
6. Bekommt Response
7. Loggt Training Data
8. Gibt Response zurück

**Alles funktioniert. Alles Production. Alles sauber.** 💎⚡🔥

---

## 🔥 Next Steps

1. **Nutze Training Data:**
   ```bash
   tail -f /opt/syntx-config/logs/wrapper_requests.jsonl | jq
   ```

2. **Optimiere Wrapper:**
   - Vergleiche Performance
   - A/B Testing
   - Eigene Wrapper erstellen

3. **Monitoring:**
   - Health Check Cronjob
   - Log Rotation
   - Backup Strategy

4. **Skalieren:**
   - Mehr Wrapper Modes
   - Metrics Dashboard
   - Alert System

---

**🌊 SYNTX FLIESST! ⚡💎🔥**

*Deployment: 04.12.2025 | Server: dev.syntx-system.com | Backend: Ollama/Mistral-uncensored*
