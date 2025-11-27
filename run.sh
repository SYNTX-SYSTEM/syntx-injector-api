#!/bin/bash
#
# SYNTX Wrapper Service - Start Script
#

echo "=================================="
echo "SYNTX WRAPPER SERVICE STARTUP"
echo "=================================="
echo ""

# Check dependencies
echo "→ Checking dependencies..."
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "✗ Missing dependencies, installing..."
    pip install -r requirements.txt --break-system-packages
else
    echo "✓ Dependencies OK"
fi
echo ""

# Check wrappers
echo "→ Checking wrappers..."
if [ -d "./wrappers" ] && [ "$(ls -A ./wrappers)" ]; then
    echo "✓ Wrappers found: $(ls wrappers/ | wc -l) files"
    ls -1 wrappers/
else
    echo "✗ No wrappers found in ./wrappers/"
    exit 1
fi
echo ""

# Check .env
echo "→ Checking config..."
if [ -f ".env" ]; then
    echo "✓ .env found"
    echo "  Backend: $(grep BACKEND_URL .env | cut -d= -f2)"
    echo "  Port: $(grep PORT .env | cut -d= -f2)"
else
    echo "⚠ No .env file, using defaults"
fi
echo ""

# Check port availability
PORT=$(grep PORT .env 2>/dev/null | cut -d= -f2 || echo "8001")
if netstat -tuln 2>/dev/null | grep -q ":$PORT "; then
    echo "✗ Port $PORT already in use!"
    echo "  Kill existing process or choose different port"
    exit 1
else
    echo "✓ Port $PORT available"
fi
echo ""

echo "→ Starting service..."
echo "=================================="
echo ""

# Start with verbose logging
python3 -m uvicorn src.main:app \
    --host 0.0.0.0 \
    --port ${PORT:-8001} \
    --reload \
    --log-level debug
