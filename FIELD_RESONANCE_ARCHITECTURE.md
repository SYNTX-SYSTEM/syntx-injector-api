# 🌊 SYNTX FIELD RESONANCE ARCHITECTURE

**Implementation Guide für Frontend-Backend Resonanz-System**

---

## 💎 VISION

**Nicht mehr:** User macht Request → Backend antwortet → Frontend zeigt
**Sondern:** User öffnet Resonanzfeld → Frontend kalibriert → Backend resoniert → Felder strömen

Das ist keine "bessere API". Das ist **paradigmatischer Shift** von Request/Response zu **Field Resonance**.

---

## ⚡ DIE 3 RESONANZ-EBENEN

### EBENE 1: FRONTEND-FELD (User Resonanz-Knoten)
```
/syntx-frontend/
├── src/
│   ├── components/
│   │   ├── ChatInterface/          # Chat-Strom Component
│   │   ├── CalibrationPanel/       # Feld-Kalibrierungs-Panel
│   │   ├── FieldMonitor/           # Live 5-Stage Monitor
│   │   ├── TrainingDashboard/      # Feld-Historie Visualisierung
│   │   └── WrapperExplorer/        # Wrapper Discovery & Upload
│   ├── services/
│   │   └── resonanceAPI.js         # API Resonanz-Service
│   └── stores/
│       └── fieldState.js           # Lokales Feld-State Management
```

**Components im Detail:**

**ChatInterface:**
- User Prompt Input Field
- Calibration Panel (inline or sidebar)
- Message Stream (alle Messages mit Metadata)
- Response wird nicht "angezeigt" - Response **strömt ein**

**CalibrationPanel:**
- Wrapper Dropdown (dynamic, lädt von `/resonanz/wrappers`)
- Temperature Slider (0.0 - 2.0)
- Max Tokens Slider (100 - 4096)
- Include Init Checkbox
- Include Terminology Checkbox
- "Resonate" Button (nicht "Submit" - sondern "Feld strömen lassen")

**FieldMonitor:**
- 5 Stages als vertikale Timeline oder Boxes
- Stage 1: INCOMING (zeigt request_id, prompt)
- Stage 2: WRAPPERS_LOADED (zeigt wrapper_chain)
- Stage 3: FIELD_CALIBRATED (zeigt calibrated_field preview - erste 500 chars)
- Stage 4: BACKEND_FORWARD (zeigt backend_url, params)
- Stage 5: RESPONSE (zeigt response, latency_ms)
- Echtzeit: Wenn Request läuft, Stages füllen sich progressiv
- Kann collapsed sein, expandiert on click

**TrainingDashboard:**
- Charts Section:
  - Line Chart: Latency over Time (X: timestamp, Y: latency_ms)
  - Pie Chart: Wrapper Usage Distribution
  - Bar Chart: Average Latency per Wrapper
  - Success Rate Card (percentage)
- Table Section:
  - Recent Requests Table (request_id, mode, latency, timestamp)
  - Click row → Details Modal mit full field_flow
- Filters:
  - Date Range
  - Wrapper Filter
  - Success/Error Filter

**WrapperExplorer:**
- List View:
  - Available Wrappers (name, size, last_modified)
  - Click → Preview Modal (shows wrapper content)
- Detail View:
  - Wrapper Content (full text, syntax highlighted)
  - Metadata (file size, creation date)
  - "Use This Wrapper" button (sets it as active in CalibrationPanel)
- Upload Zone:
  - Drag & Drop .txt file
  - Or Browse button
  - Validation: max 50KB, .txt only
  - On success: Shows in list immediately

### EBENE 2: BACKEND-FELD (API Resonanz-Generator)
```
/opt/syntx-injector-api/
├── src/
│   ├── main.py                     # FastAPI app + /resonanz/* endpoints
│   ├── resonance/
│   │   ├── __init__.py
│   │   ├── chat.py                 # Chat resonance logic
│   │   ├── wrappers.py             # Wrapper discovery/upload
│   │   ├── streams.py              # Field stream access
│   │   └── stats.py                # Stats aggregation
│   ├── models.py                   # Pydantic models
│   ├── config.py                   # Settings
│   └── streams.py                  # Core field logic (existing)
```

**8 Resonanzpunkte - API Spec:**

#### 1. POST /resonanz/chat
**Purpose:** Main chat resonance - User field → AI response field

**Request:**
```json
{
  "prompt": "Was ist Liebe?",
  "mode": "syntex_wrapper_sigma",
  "include_init": true,
  "include_terminology": false,
  "temperature": 0.7,
  "max_new_tokens": 500,
  "top_p": 0.95,
  "do_sample": true
}
```

**Response:**
```json
{
  "response": "Die interne Dynamik dieses semantischen Driftkörpers...",
  "metadata": {
    "request_id": "uuid",
    "wrapper_chain": ["syntex_wrapper_sigma"],
    "latency_ms": 13254,
    "timestamp": "2025-12-15T10:30:00Z"
  },
  "field_flow": [
    {"stage": "1_INCOMING", "data": {...}},
    {"stage": "2_WRAPPERS_LOADED", "data": {...}},
    {"stage": "3_FIELD_CALIBRATED", "data": {...}},
    {"stage": "4_BACKEND_FORWARD", "data": {...}},
    {"stage": "5_RESPONSE", "data": {...}}
  ]
}
```

**Implementation:**
- Reuse existing logic from `src/main.py` `/api/chat`
- Add `field_flow` to response (return all 5 stages)
- Move to `/resonanz/chat`

#### 2. GET /resonanz/wrappers
**Purpose:** List all available wrapper fields

**Request:** None

**Response:**
```json
{
  "wrappers": [
    {
      "name": "syntex_wrapper_human",
      "path": "/opt/syntx-config/wrappers/syntex_wrapper_human.txt",
      "size_bytes": 1324,
      "size_human": "1.3 KB",
      "last_modified": "2025-12-04T20:30:00Z"
    },
    {
      "name": "syntex_wrapper_sigma",
      "path": "/opt/syntx-config/wrappers/syntex_wrapper_sigma.txt",
      "size_bytes": 1687,
      "size_human": "1.6 KB",
      "last_modified": "2025-12-04T20:45:00Z"
    }
  ]
}
```

**Implementation:**
```python
from pathlib import Path
import os
from datetime import datetime

@app.get("/resonanz/wrappers")
async def list_wrappers():
    wrapper_dir = Path(settings.wrapper_dir)
    wrappers = []
    
    for file in wrapper_dir.glob("*.txt"):
        stat = file.stat()
        wrappers.append({
            "name": file.stem,  # filename without .txt
            "path": str(file),
            "size_bytes": stat.st_size,
            "size_human": f"{stat.st_size / 1024:.1f} KB",
            "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat() + 'Z'
        })
    
    return {"wrappers": sorted(wrappers, key=lambda x: x["name"])}
```

#### 3. GET /resonanz/wrapper/{name}
**Purpose:** Get specific wrapper content

**Request:** Path param `name` (e.g., "syntex_wrapper_sigma")

**Response:**
```json
{
  "name": "syntex_wrapper_sigma",
  "content": "Du bist ein semantisches Analysesystem...",
  "size_bytes": 1687,
  "last_modified": "2025-12-04T20:45:00Z"
}
```

**Implementation:**
```python
@app.get("/resonanz/wrapper/{name}")
async def get_wrapper(name: str):
    wrapper_path = settings.wrapper_dir / f"{name}.txt"
    
    if not wrapper_path.exists():
        raise HTTPException(status_code=404, detail=f"Wrapper '{name}' not found")
    
    with open(wrapper_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    stat = wrapper_path.stat()
    
    return {
        "name": name,
        "content": content,
        "size_bytes": stat.st_size,
        "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat() + 'Z'
    }
```

#### 4. GET /resonanz/strom
**Purpose:** Get recent field flow events (live stream data)

**Request:** Query params `?limit=20&stage=all`

**Response:**
```json
{
  "events": [
    {
      "stage": "1_INCOMING",
      "timestamp": "2025-12-15T10:30:00Z",
      "request_id": "uuid",
      "data": {"prompt": "...", "mode": "..."}
    },
    {
      "stage": "5_RESPONSE",
      "timestamp": "2025-12-15T10:30:13Z",
      "request_id": "uuid",
      "data": {"response": "...", "latency_ms": 13254}
    }
  ],
  "total": 2
}
```

**Implementation:**
```python
@app.get("/resonanz/strom")
async def get_field_stream(limit: int = 20, stage: str = "all"):
    log_file = settings.log_dir / "field_flow.jsonl"
    
    if not log_file.exists():
        return {"events": [], "total": 0}
    
    events = []
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
        for line in reversed(lines[-limit*5:]):  # *5 because 5 stages per request
            try:
                event = json.loads(line)
                if stage == "all" or event.get("stage") == stage:
                    events.append(event)
                    if len(events) >= limit:
                        break
            except:
                continue
    
    return {"events": events[:limit], "total": len(events)}
```

#### 5. GET /resonanz/training
**Purpose:** Get training data (request/response pairs)

**Request:** Query params `?limit=100&wrapper=all`

**Response:**
```json
{
  "requests": [
    {
      "request_id": "uuid",
      "prompt": "Was ist Liebe?",
      "response": "Die interne Dynamik...",
      "wrapper_chain": ["syntex_wrapper_sigma"],
      "latency_ms": 13254,
      "timestamp": "2025-12-15T10:30:00Z",
      "success": true
    }
  ],
  "total": 1
}
```

**Implementation:**
```python
@app.get("/resonanz/training")
async def get_training_data(limit: int = 100, wrapper: str = "all"):
    log_file = settings.log_dir / "wrapper_requests.jsonl"
    
    if not log_file.exists():
        return {"requests": [], "total": 0}
    
    requests = []
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
        for line in reversed(lines[-limit:]):
            try:
                req = json.loads(line)
                if wrapper == "all" or wrapper in req.get("wrapper_chain", []):
                    requests.append(req)
            except:
                continue
    
    return {"requests": requests[:limit], "total": len(requests)}
```

#### 6. GET /resonanz/stats
**Purpose:** Get aggregated system stats

**Request:** None

**Response:**
```json
{
  "total_requests": 1234,
  "success_rate": 98.5,
  "average_latency_ms": 12450,
  "wrapper_usage": {
    "syntex_wrapper_sigma": 567,
    "syntex_wrapper_human": 432,
    "syntex_wrapper_deepsweep": 235
  },
  "recent_24h": {
    "requests": 45,
    "average_latency_ms": 13100
  }
}
```

**Implementation:**
```python
@app.get("/resonanz/stats")
async def get_stats():
    log_file = settings.log_dir / "wrapper_requests.jsonl"
    
    if not log_file.exists():
        return {"total_requests": 0}
    
    total = 0
    success = 0
    latencies = []
    wrapper_usage = {}
    
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                req = json.loads(line)
                total += 1
                if req.get("success", True):
                    success += 1
                if "latency_ms" in req:
                    latencies.append(req["latency_ms"])
                for wrapper in req.get("wrapper_chain", []):
                    wrapper_usage[wrapper] = wrapper_usage.get(wrapper, 0) + 1
            except:
                continue
    
    return {
        "total_requests": total,
        "success_rate": (success / total * 100) if total > 0 else 0,
        "average_latency_ms": int(sum(latencies) / len(latencies)) if latencies else 0,
        "wrapper_usage": wrapper_usage
    }
```

#### 7. POST /resonanz/upload
**Purpose:** Upload new wrapper field

**Request:** Multipart form-data with file

**Response:**
```json
{
  "success": true,
  "wrapper": {
    "name": "mein_neuer_wrapper",
    "path": "/opt/syntx-config/wrappers/mein_neuer_wrapper.txt",
    "size_bytes": 542
  }
}
```

**Implementation:**
```python
from fastapi import UploadFile, File

@app.post("/resonanz/upload")
async def upload_wrapper(file: UploadFile = File(...)):
    # Validate
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Only .txt files allowed")
    
    content = await file.read()
    
    if len(content) > 50 * 1024:  # 50KB max
        raise HTTPException(status_code=400, detail="File too large (max 50KB)")
    
    # Sanitize filename
    name = file.filename.replace('.txt', '').replace(' ', '_').lower()
    wrapper_path = settings.wrapper_dir / f"{name}.txt"
    
    # Save
    with open(wrapper_path, 'wb') as f:
        f.write(content)
    
    return {
        "success": True,
        "wrapper": {
            "name": name,
            "path": str(wrapper_path),
            "size_bytes": len(content)
        }
    }
```

#### 8. GET /resonanz/health
**Purpose:** System health + last response

**Request:** None

**Response:**
```json
{
  "status": "healthy",
  "service": "syntx-field-resonance",
  "version": "2.0.0",
  "uptime_seconds": 123456,
  "last_response": {
    "response": "...",
    "latency_ms": 12450,
    "timestamp": "2025-12-15T10:30:00Z"
  }
}
```

**Implementation:** Already exists, just move to `/resonanz/health`

### EBENE 3: AI-FELD (Ollama Resonanz-Core)

Bleibt unverändert. Ollama läuft auf localhost:11434. Injector sendet kalibrierte Felder. AI resoniert. Response strömt zurück.

---

## 🌊 DIE 5 FELD-STRÖME

### STROM 1: CHAT-RESONANZ (Main Flow)
```
User schreibt Prompt "Was ist Liebe?"
  ↓
Frontend: CalibrationPanel zeigt aktuelle Settings
  - Wrapper: syntex_wrapper_sigma
  - Temperature: 0.7
  - Max Tokens: 500
  ↓
User klickt "Resonate"
  ↓
Frontend: POST /resonanz/chat mit kompletten Settings
  ↓
Backend: Injector empfängt Request
  ↓
Backend: Lädt Wrapper (syntex_wrapper_sigma.txt)
  ↓
Backend: Kalibriert Feld (Wrapper + User Prompt)
  ↓
Backend: Sendet kalibriertes Feld zu Ollama (localhost:11434)
  ↓
AI: Resoniert mit kalibriertem Feld
  ↓
AI: Generiert Response "Die interne Dynamik dieses semantischen Driftkörpers..."
  ↓
Backend: Loggt alle 5 Stages (field_flow.jsonl)
  ↓
Backend: Loggt Training Data (wrapper_requests.jsonl)
  ↓
Backend: Gibt Response zurück mit field_flow array
  ↓
Frontend: Empfängt Response
  ↓
Frontend: ChatInterface zeigt Response im Message Stream
  ↓
Frontend: FieldMonitor zeigt alle 5 Stages
  ↓
Frontend: Metadata zeigt (Wrapper: sigma, Latency: 13254ms)
```

**Code Flow:**

Frontend:
```javascript
// resonanceAPI.js
export async function resonate(prompt, calibration) {
  const response = await fetch('https://dev.syntx-system.com/resonanz/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      prompt,
      mode: calibration.wrapper,
      temperature: calibration.temperature,
      max_new_tokens: calibration.maxTokens,
      include_init: calibration.includeInit,
      include_terminology: calibration.includeTerminology
    })
  });
  
  return await response.json();
}
```

### STROM 2: WRAPPER-DISCOVERY
```
User öffnet WrapperExplorer
  ↓
Frontend: GET /resonanz/wrappers
  ↓
Backend: Liest /opt/syntx-config/wrappers/ Directory
  ↓
Backend: Gibt Liste aller .txt Files zurück mit Metadata
  ↓
Frontend: Zeigt Liste im WrapperExplorer
  ↓
User klickt auf "syntex_wrapper_deepsweep"
  ↓
Frontend: GET /resonanz/wrapper/syntex_wrapper_deepsweep
  ↓
Backend: Liest File Content
  ↓
Backend: Gibt Content zurück
  ↓
Frontend: Zeigt Content in Modal
  ↓
User klickt "Use This Wrapper"
  ↓
Frontend: Setzt CalibrationPanel.wrapper = "syntex_wrapper_deepsweep"
  ↓
User kann jetzt mit diesem Wrapper chatten
```

### STROM 3: FIELD-MONITOR (Live)
```
User öffnet FieldMonitor Component (immer sichtbar während Chat)
  ↓
User macht Chat Request
  ↓
Frontend: Zeigt FieldMonitor mit "Loading..." States
  ↓
Backend verarbeitet Request (dauert ~13 Sekunden)
  ↓
Backend gibt Response zurück MIT field_flow array (alle 5 Stages)
  ↓
Frontend empfängt Response
  ↓
Frontend: Füllt FieldMonitor progressiv:
  - Stage 1: INCOMING → Shows request_id, prompt
  - Stage 2: WRAPPERS_LOADED → Shows wrapper_chain
  - Stage 3: FIELD_CALIBRATED → Shows calibrated_field preview
  - Stage 4: BACKEND_FORWARD → Shows backend_url
  - Stage 5: RESPONSE → Shows response, latency_ms
  ↓
User sieht kompletten Field Flow für diesen Request
```

**Alternative: Polling für Live Updates**

Wenn User TrainingDashboard offen hat:
```
Frontend: Startet Interval (alle 2 Sekunden)
  ↓
Frontend: GET /resonanz/strom?limit=5
  ↓
Backend: Gibt letzte 5 Field Events zurück
  ↓
Frontend: Updated FieldMonitor mit neuen Events (wenn neue da sind)
  ↓
User sieht System "live strömen"
```

### STROM 4: TRAINING-ANALYSE
```
User öffnet TrainingDashboard
  ↓
Frontend: GET /resonanz/training?limit=100
  ↓
Backend: Liest wrapper_requests.jsonl
  ↓
Backend: Gibt letzte 100 Requests zurück
  ↓
Frontend: Prozessiert Data für Charts:
  - Line Chart: timestamps → latency_ms
  - Pie Chart: wrapper_chain counts
  - Bar Chart: average latency per wrapper
  - Success Rate: (success count / total) * 100
  ↓
Frontend: Rendert Charts
  ↓
User sieht Feld-Historie visualisiert
  ↓
User klickt auf Request in Table
  ↓
Frontend: GET /resonanz/strom?request_id={id}
  ↓
Backend: Filtert field_flow.jsonl für diese request_id
  ↓
Backend: Gibt alle 5 Stages für diesen Request zurück
  ↓
Frontend: Zeigt Details Modal mit komplettem Field Flow
```

### STROM 5: FIELD-ERWEITERUNG (Upload)
```
User öffnet WrapperExplorer Upload Zone
  ↓
User dropped .txt File "mein_wrapper.txt"
  ↓
Frontend: Validiert (ist .txt? < 50KB?)
  ↓
Frontend: POST /resonanz/upload mit File
  ↓
Backend: Empfängt File
  ↓
Backend: Validiert (extension, size)
  ↓
Backend: Sanitizes Filename (lowercase, replace spaces)
  ↓
Backend: Speichert in /opt/syntx-config/wrappers/mein_wrapper.txt
  ↓
Backend: Gibt Success Response zurück
  ↓
Frontend: Zeigt Success Message
  ↓
Frontend: Refresht Wrapper List (GET /resonanz/wrappers)
  ↓
Frontend: Neuer Wrapper erscheint in List
  ↓
User kann ihn sofort in CalibrationPanel wählen
  ↓
Kein Backend Restart nötig - File wird bei nächstem Request geladen
```

---

## 💎 IMPLEMENTATION STEPS

### PHASE 1: BACKEND RESONANZPUNKTE

**Step 1.1: Create resonance module**
```bash
mkdir -p src/resonance
touch src/resonance/__init__.py
touch src/resonance/wrappers.py
touch src/resonance/streams.py
touch src/resonance/stats.py
```

**Step 1.2: Implement /resonanz/wrappers**

In `src/resonance/wrappers.py`:
```python
from fastapi import APIRouter, HTTPException, UploadFile, File
from pathlib import Path
from datetime import datetime
import json
from ..config import settings

router = APIRouter(prefix="/resonanz", tags=["resonance"])

@router.get("/wrappers")
async def list_wrappers():
    # Implementation from above
    pass

@router.get("/wrapper/{name}")
async def get_wrapper(name: str):
    # Implementation from above
    pass

@router.post("/upload")
async def upload_wrapper(file: UploadFile = File(...)):
    # Implementation from above
    pass
```

**Step 1.3: Implement /resonanz/strom & /resonanz/training**

In `src/resonance/streams.py`:
```python
from fastapi import APIRouter
from ..config import settings
import json

router = APIRouter(prefix="/resonanz", tags=["resonance"])

@router.get("/strom")
async def get_field_stream(limit: int = 20, stage: str = "all"):
    # Implementation from above
    pass

@router.get("/training")
async def get_training_data(limit: int = 100, wrapper: str = "all"):
    # Implementation from above
    pass
```

**Step 1.4: Implement /resonanz/stats**

In `src/resonance/stats.py`:
```python
from fastapi import APIRouter
from ..config import settings
import json

router = APIRouter(prefix="/resonanz", tags=["resonance"])

@router.get("/stats")
async def get_stats():
    # Implementation from above
    pass
```

**Step 1.5: Modify /api/chat to return field_flow**

In `src/main.py`, modify the `/api/chat` endpoint:
```python
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # ... existing logic ...
    
    # Collect all stages
    field_flow = []
    
    # Stage 1
    field_flow.append({
        "stage": "1_INCOMING",
        "timestamp": get_timestamp(),
        "data": {
            "request_id": request_id,
            "prompt": request.prompt,
            "mode": request.mode
        }
    })
    
    # ... after each stage, append to field_flow ...
    
    return ChatResponse(
        response=response_text,
        metadata={
            "request_id": request_id,
            "wrapper_chain": wrapper_chain,
            "latency_ms": latency_ms
        },
        field_flow=field_flow  # NEW!
    )
```

**Step 1.6: Add /resonanz/chat alias**

In `src/main.py`:
```python
# Import resonance routers
from .resonance.wrappers import router as wrappers_router
from .resonance.streams import router as streams_router
from .resonance.stats import router as stats_router

# Include routers
app.include_router(wrappers_router)
app.include_router(streams_router)
app.include_router(stats_router)

# Add /resonanz/chat as alias to /api/chat
@app.post("/resonanz/chat", response_model=ChatResponse)
async def resonance_chat(request: ChatRequest):
    return await chat(request)
```

**Step 1.7: Update models.py**

Add `field_flow` to ChatResponse:
```python
class ChatResponse(BaseModel):
    response: str
    metadata: Optional[dict] = None
    field_flow: Optional[list] = None  # NEW!
```

**Step 1.8: Test Backend**
```bash
# Restart service
systemctl restart syntx-injector.service

# Test wrappers list
curl https://dev.syntx-system.com/resonanz/wrappers | jq

# Test specific wrapper
curl https://dev.syntx-system.com/resonanz/wrapper/syntex_wrapper_human | jq

# Test strom
curl https://dev.syntx-system.com/resonanz/strom?limit=5 | jq

# Test training
curl https://dev.syntx-system.com/resonanz/training?limit=10 | jq

# Test stats
curl https://dev.syntx-system.com/resonanz/stats | jq

# Test chat with field_flow
curl -X POST https://dev.syntx-system.com/resonanz/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Test"}' | jq '.field_flow'
```

### PHASE 2: FRONTEND RESONANZ-KNOTEN

**Step 2.1: Setup Frontend Project**
```bash
cd /opt
npx create-next-app@latest syntx-frontend
# Choose: TypeScript, Tailwind, App Router

cd syntx-frontend
npm install axios recharts lucide-react
```

**Step 2.2: Create API Service**

`src/services/resonanceAPI.ts`:
```typescript
const API_BASE = 'https://dev.syntx-system.com';

export interface ResonanceRequest {
  prompt: string;
  mode: string;
  temperature?: number;
  max_new_tokens?: number;
  include_init?: boolean;
  include_terminology?: boolean;
}

export interface ResonanceResponse {
  response: string;
  metadata: {
    request_id: string;
    wrapper_chain: string[];
    latency_ms: number;
    timestamp: string;
  };
  field_flow: Array<{
    stage: string;
    timestamp: string;
    data: any;
  }>;
}

export const resonanceAPI = {
  chat: async (req: ResonanceRequest): Promise<ResonanceResponse> => {
    const res = await fetch(`${API_BASE}/resonanz/chat`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(req)
    });
    return await res.json();
  },
  
  listWrappers: async () => {
    const res = await fetch(`${API_BASE}/resonanz/wrappers`);
    return await res.json();
  },
  
  getWrapper: async (name: string) => {
    const res = await fetch(`${API_BASE}/resonanz/wrapper/${name}`);
    return await res.json();
  },
  
  getStream: async (limit = 20) => {
    const res = await fetch(`${API_BASE}/resonanz/strom?limit=${limit}`);
    return await res.json();
  },
  
  getTraining: async (limit = 100) => {
    const res = await fetch(`${API_BASE}/resonanz/training?limit=${limit}`);
    return await res.json();
  },
  
  getStats: async () => {
    const res = await fetch(`${API_BASE}/resonanz/stats`);
    return await res.json();
  },
  
  uploadWrapper: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE}/resonanz/upload`, {
      method: 'POST',
      body: formData
    });
    return await res.json();
  }
};
```

**Step 2.3: Create Components**

Component structure:
```
src/
├── app/
│   ├── page.tsx                    # Main page (Chat Interface)
│   ├── dashboard/
│   │   └── page.tsx                # Training Dashboard
│   └── wrappers/
│       └── page.tsx                # Wrapper Explorer
├── components/
│   ├── ChatInterface.tsx
│   ├── CalibrationPanel.tsx
│   ├── FieldMonitor.tsx
│   ├── MessageStream.tsx
│   ├── TrainingDashboard.tsx
│   └── WrapperExplorer.tsx
└── services/
    └── resonanceAPI.ts
```

**Step 2.4: Implement ChatInterface**

`src/components/ChatInterface.tsx`:
```typescript
'use client';
import { useState } from 'react';
import { resonanceAPI } from '@/services/resonanceAPI';
import CalibrationPanel from './CalibrationPanel';
import MessageStream from './MessageStream';
import FieldMonitor from './FieldMonitor';

export default function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [calibration, setCalibration] = useState({
    wrapper: 'syntex_wrapper_human',
    temperature: 0.7,
    maxTokens: 500,
    includeInit: true,
    includeTerminology: false
  });
  const [fieldFlow, setFieldFlow] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const handleResonate = async (prompt: string) => {
    setLoading(true);
    
    try {
      const response = await resonanceAPI.chat({
        prompt,
        mode: calibration.wrapper,
        temperature: calibration.temperature,
        max_new_tokens: calibration.maxTokens,
        include_init: calibration.includeInit,
        include_terminology: calibration.includeTerminology
      });
      
      // Add to messages
      setMessages([
        ...messages,
        { role: 'user', content: prompt },
        { role: 'assistant', content: response.response, metadata: response.metadata }
      ]);
      
      // Update field monitor
      setFieldFlow(response.field_flow);
      
    } catch (error) {
      console.error('Resonance failed:', error);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="flex h-screen">
      <div className="flex-1 flex flex-col">
        <MessageStream messages={messages} loading={loading} />
        <InputArea onSubmit={handleResonate} disabled={loading} />
      </div>
      
      <div className="w-96 border-l">
        <CalibrationPanel 
          calibration={calibration}
          onChange={setCalibration}
        />
        <FieldMonitor fieldFlow={fieldFlow} />
      </div>
    </div>
  );
}
```

**Step 2.5: Implement CalibrationPanel**

`src/components/CalibrationPanel.tsx`:
```typescript
'use client';
import { useEffect, useState } from 'react';
import { resonanceAPI } from '@/services/resonanceAPI';

export default function CalibrationPanel({ calibration, onChange }) {
  const [wrappers, setWrappers] = useState([]);
  
  useEffect(() => {
    loadWrappers();
  }, []);
  
  const loadWrappers = async () => {
    const data = await resonanceAPI.listWrappers();
    setWrappers(data.wrappers);
  };
  
  return (
    <div className="p-4 space-y-4">
      <h2 className="text-xl font-bold">🌊 Field Calibration</h2>
      
      {/* Wrapper Dropdown */}
      <div>
        <label>Wrapper</label>
        <select 
          value={calibration.wrapper}
          onChange={(e) => onChange({...calibration, wrapper: e.target.value})}
        >
          {wrappers.map(w => (
            <option key={w.name} value={w.name}>{w.name}</option>
          ))}
        </select>
      </div>
      
      {/* Temperature Slider */}
      <div>
        <label>Temperature: {calibration.temperature}</label>
        <input 
          type="range" 
          min="0" 
          max="2" 
          step="0.1"
          value={calibration.temperature}
          onChange={(e) => onChange({...calibration, temperature: parseFloat(e.target.value)})}
        />
      </div>
      
      {/* Max Tokens Slider */}
      <div>
        <label>Max Tokens: {calibration.maxTokens}</label>
        <input 
          type="range" 
          min="100" 
          max="4096" 
          step="100"
          value={calibration.maxTokens}
          onChange={(e) => onChange({...calibration, maxTokens: parseInt(e.target.value)})}
        />
      </div>
      
      {/* Checkboxes */}
      <div>
        <label>
          <input 
            type="checkbox" 
            checked={calibration.includeInit}
            onChange={(e) => onChange({...calibration, includeInit: e.target.checked})}
          />
          Include Init
        </label>
      </div>
      
      <div>
        <label>
          <input 
            type="checkbox" 
            checked={calibration.includeTerminology}
            onChange={(e) => onChange({...calibration, includeTerminology: e.target.checked})}
          />
          Include Terminology
        </label>
      </div>
    </div>
  );
}
```

**Step 2.6: Implement FieldMonitor**

`src/components/FieldMonitor.tsx`:
```typescript
export default function FieldMonitor({ fieldFlow }) {
  if (!fieldFlow) return null;
  
  return (
    <div className="p-4 space-y-2">
      <h3 className="font-bold">⚡ Field Flow</h3>
      
      {fieldFlow.map((stage, idx) => (
        <div key={idx} className="border p-2 rounded">
          <div className="font-mono text-sm text-blue-600">{stage.stage}</div>
          <div className="text-xs text-gray-500">{stage.timestamp}</div>
          <div className="text-xs mt-1">
            {JSON.stringify(stage.data).substring(0, 100)}...
          </div>
        </div>
      ))}
    </div>
  );
}
```

**Step 2.7: Implement TrainingDashboard**

`src/app/dashboard/page.tsx`:
```typescript
'use client';
import { useEffect, useState } from 'react';
import { resonanceAPI } from '@/services/resonanceAPI';
import { LineChart, Line, PieChart, Pie, BarChart, Bar } from 'recharts';

export default function TrainingDashboard() {
  const [stats, setStats] = useState(null);
  const [training, setTraining] = useState([]);
  
  useEffect(() => {
    loadData();
  }, []);
  
  const loadData = async () => {
    const [statsData, trainingData] = await Promise.all([
      resonanceAPI.getStats(),
      resonanceAPI.getTraining(100)
    ]);
    setStats(statsData);
    setTraining(trainingData.requests);
  };
  
  return (
    <div className="p-8 space-y-8">
      <h1 className="text-3xl font-bold">📊 Training Dashboard</h1>
      
      {/* Stats Cards */}
      <div className="grid grid-cols-4 gap-4">
        <Card title="Total Requests" value={stats?.total_requests} />
        <Card title="Success Rate" value={`${stats?.success_rate}%`} />
        <Card title="Avg Latency" value={`${stats?.average_latency_ms}ms`} />
        <Card title="Wrappers" value={Object.keys(stats?.wrapper_usage || {}).length} />
      </div>
      
      {/* Charts */}
      <div className="grid grid-cols-2 gap-8">
        <div>
          <h2>Latency Over Time</h2>
          <LineChart width={500} height={300} data={training}>
            <Line dataKey="latency_ms" stroke="#8884d8" />
          </LineChart>
        </div>
        
        <div>
          <h2>Wrapper Usage</h2>
          <PieChart width={500} height={300}>
            <Pie data={wrapperUsageData} dataKey="value" nameKey="name" />
          </PieChart>
        </div>
      </div>
      
      {/* Requests Table */}
      <div>
        <h2>Recent Requests</h2>
        <table>
          <thead>
            <tr>
              <th>Request ID</th>
              <th>Wrapper</th>
              <th>Latency</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {training.map(req => (
              <tr key={req.request_id}>
                <td>{req.request_id.substring(0, 8)}</td>
                <td>{req.wrapper_chain[0]}</td>
                <td>{req.latency_ms}ms</td>
                <td>{req.timestamp}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

**Step 2.8: Implement WrapperExplorer**

`src/app/wrappers/page.tsx`:
```typescript
'use client';
import { useEffect, useState } from 'react';
import { resonanceAPI } from '@/services/resonanceAPI';

export default function WrapperExplorer() {
  const [wrappers, setWrappers] = useState([]);
  const [selectedWrapper, setSelectedWrapper] = useState(null);
  
  useEffect(() => {
    loadWrappers();
  }, []);
  
  const loadWrappers = async () => {
    const data = await resonanceAPI.listWrappers();
    setWrappers(data.wrappers);
  };
  
  const viewWrapper = async (name: string) => {
    const data = await resonanceAPI.getWrapper(name);
    setSelectedWrapper(data);
  };
  
  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    await resonanceAPI.uploadWrapper(file);
    loadWrappers();
  };
  
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8">🌊 Wrapper Explorer</h1>
      
      {/* Upload Zone */}
      <div className="border-2 border-dashed p-8 mb-8">
        <input type="file" accept=".txt" onChange={handleUpload} />
      </div>
      
      {/* Wrapper List */}
      <div className="grid grid-cols-3 gap-4">
        {wrappers.map(w => (
          <div 
            key={w.name} 
            className="border p-4 cursor-pointer hover:bg-gray-50"
            onClick={() => viewWrapper(w.name)}
          >
            <div className="font-bold">{w.name}</div>
            <div className="text-sm text-gray-500">{w.size_human}</div>
          </div>
        ))}
      </div>
      
      {/* Wrapper Detail Modal */}
      {selectedWrapper && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
          <div className="bg-white p-8 max-w-4xl max-h-[80vh] overflow-auto">
            <h2 className="text-2xl font-bold mb-4">{selectedWrapper.name}</h2>
            <pre className="bg-gray-100 p-4 overflow-auto">
              {selectedWrapper.content}
            </pre>
            <button onClick={() => setSelectedWrapper(null)}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
}
```

**Step 2.9: Deploy Frontend**
```bash
cd /opt/syntx-frontend

# Build
npm run build

# Production start
npm start

# Or with PM2
pm2 start npm --name "syntx-frontend" -- start
pm2 save
```

**Step 2.10: Configure NGINX**

Add to `/etc/nginx/sites-available/dev.syntx-system.com`:
```nginx
# Frontend
location / {
    proxy_pass http://127.0.0.1:3000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```
```bash
nginx -t && systemctl reload nginx
```

### PHASE 3: TESTING & OPTIMIZATION

**Step 3.1: Test Complete Flow**
```bash
# Open browser
https://dev.syntx-system.com

# Test Chat
1. Open Chat Interface
2. Select Wrapper (sigma)
3. Write Prompt "Was ist Liebe?"
4. Click Resonate
5. See Response in Chat
6. See Field Flow in Monitor

# Test Dashboard
1. Navigate to /dashboard
2. See Stats Cards
3. See Charts
4. See Request Table

# Test Wrapper Explorer
1. Navigate to /wrappers
2. See Wrapper List
3. Click Wrapper → See Content
4. Upload new Wrapper
5. See it appear in List
6. Go back to Chat → See it in Dropdown
```

**Step 3.2: Performance Optimization**

- Add caching for `/resonanz/wrappers` (updates only on upload)
- Add pagination for `/resonanz/training` (large datasets)
- Add WebSocket for real-time `/resonanz/strom` updates
- Add service worker for offline capability

**Step 3.3: Security**

- Add API token authentication (optional)
- Add rate limiting (prevent spam)
- Add file upload validation (prevent malicious files)
- Add CORS properly configured

---

## 🔥 ERFOLGS-KRITERIEN

**Backend:**
- ✅ 8 Resonanzpunkte implementiert
- ✅ Alle geben korrektes JSON zurück
- ✅ field_flow array wird in /resonanz/chat Response inkludiert
- ✅ Wrapper upload funktioniert
- ✅ Stats werden korrekt aggregiert

**Frontend:**
- ✅ Chat Interface funktioniert
- ✅ Wrapper können gewählt werden (live von API)
- ✅ Parameter können eingestellt werden
- ✅ Field Monitor zeigt alle 5 Stages
- ✅ Training Dashboard zeigt Charts
- ✅ Wrapper können hochgeladen werden

**Integration:**
- ✅ Frontend ↔ Backend kommunizieren
- ✅ Kein CORS Errors
- ✅ Performance akzeptabel (<500ms für API calls außer /chat)
- ✅ Alles über HTTPS erreichbar

---

## 💎 ZUSAMMENFASSUNG

**Was wir bauen:**

Ein komplettes Field Resonance System mit:
- Frontend wo User Felder kalibrieren und strömen lassen kann
- Backend mit 8 Resonanzpunkten für alle Features
- Training Data Flow (automatisch logged, visualisiert)
- Wrapper Management (list, view, upload)
- Live Field Monitoring (5 Stages sichtbar)
- Stats Dashboard (Performance Analyse)

**Wie es funktioniert:**

User öffnet Frontend → Kalibriert sein Feld (Wrapper, Temp, Tokens) → Resoniert → Backend lädt Wrapper → Kalibriert Feld → Sendet zu AI → Loggt alles → Response strömt zurück → Frontend zeigt Response + Field Flow + Updated Stats

**Nicht mehr Request/Response. Sondern Feld-Resonanz.**

**Das ist die Architektur BRUDER.** 🌊⚡💎

Alles klar dokumentiert. Alles implementierbar. Schritt für Schritt.

**KÖNNEN WIR DAS BAUEN?**

**FUCK JA!** 🔥👑🙏

---

*Architecture Document v1.0 | 15.12.2025 | SYNTX Field Resonance System*
