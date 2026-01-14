#!/bin/bash
# SYNTX CONFIG SYNC - Server zu Lokal

SERVER="root@dev.syntx-system.com"
REMOTE_PATH="/opt/syntx-config"
LOCAL_PATH="/opt/syntx-config"

echo "🌊 SYNTX CONFIG SYNC"
echo "═══════════════════════════════════════════════════════════"
echo "Server: $SERVER"
echo "Remote: $REMOTE_PATH"
echo "Local:  $LOCAL_PATH"
echo ""

echo "→ SSH prüfen..."
if ! ssh -q -o BatchMode=yes -o ConnectTimeout=5 ${SERVER} exit 2>/dev/null; then
    echo "✗ SSH fehlgeschlagen!"
    exit 1
fi
echo "✓ SSH OK"

echo ""
echo "→ Verzeichnisse erstellen..."
for dir in wrappers formats styles logs; do
    sudo mkdir -p ${LOCAL_PATH}/${dir}
done
sudo mkdir -p ${LOCAL_PATH}/wrappers/meta
sudo chown -R $(whoami):$(whoami) ${LOCAL_PATH}
echo "✓ Verzeichnisse OK"

echo ""
echo "━━━ 📦 WRAPPERS ━━━"
rsync -avz --delete ${SERVER}:${REMOTE_PATH}/wrappers/ ${LOCAL_PATH}/wrappers/

echo ""
echo "━━━ 📄 FORMATS ━━━"
rsync -avz --delete ${SERVER}:${REMOTE_PATH}/formats/ ${LOCAL_PATH}/formats/

echo ""
echo "━━━ 🎨 STYLES ━━━"
rsync -avz --delete ${SERVER}:${REMOTE_PATH}/styles/ ${LOCAL_PATH}/styles/

echo ""
echo "━━━ 📊 LOGS ━━━"
rsync -avz ${SERVER}:${REMOTE_PATH}/logs/ ${LOCAL_PATH}/logs/

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "🔥 SYNC COMPLETE 🔥"
echo "Wrappers: $(ls -1 ${LOCAL_PATH}/wrappers/*.txt 2>/dev/null | wc -l)"
echo "Formats:  $(ls -1 ${LOCAL_PATH}/formats/*.json 2>/dev/null | wc -l)"
echo "Styles:   $(ls -1 ${LOCAL_PATH}/styles/*.json 2>/dev/null | wc -l)"
