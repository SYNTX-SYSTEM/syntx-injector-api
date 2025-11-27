# 🚀 AI Wrapper Service - Dein intelligenter Request-Butler

*"Warum einfach prompten, wenn du auch kalibrieren kannst?"* 🔥

---

## 🤔 Was ist das hier?

**AI Wrapper Service** ist dein smarter Middleman zwischen Usern und AI-Backends. Er kalibriert Requests mit konfigurierbaren Wrappern für bessere, kohärentere Antworten.

### Die Fakten:
- ✅ **Service deployed**: `https://dev.syntx-system.com/api/chat`
- ✅ **Systemd Service**: Läuft stabil im Hintergrund  
- ✅ **NGINX Routing**: Alle Calls fließen durch unseren Service
- ✅ **Production Ready**: Echtzeit-Kalibrierung aktiv
- ✅ **Daten-Sampling**: Jeder Request wird für Training gespeichert

### Live Beweis - Der Service läuft JETZT:
```bash
# 🔥 Teste es selbst - das ist LIVE!
curl -X POST https://dev.syntx-system.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Bin ich gerade im Wrapper Service?",
    "mode": "sigma"
  }'