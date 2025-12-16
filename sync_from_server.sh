#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# 🌊 SYNTX - Sync Testdaten vom Server
# ═══════════════════════════════════════════════════════════════

SERVER="root@dev.syntx-system.com"
REMOTE_PATH="/opt/syntx-config"
LOCAL_PATH="/opt/syntx-config"

echo "🌊 SYNTX Data Sync"
echo "═══════════════════════════════════════════════════════════"

echo "📦 Syncing Wrappers..."
scp -r ${SERVER}:${REMOTE_PATH}/wrappers/* ${LOCAL_PATH}/wrappers/

echo "📊 Syncing Logs..."
scp -r ${SERVER}:${REMOTE_PATH}/logs/* ${LOCAL_PATH}/logs/

echo ""
echo "✅ Done! Local data:"
ls -la ${LOCAL_PATH}/wrappers/
echo ""
echo "📊 Log files:"
ls -la ${LOCAL_PATH}/logs/
