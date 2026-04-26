#!/bin/bash
echo "🔌 Conectando ao Monitor Virtual..."
export DISPLAY=$(ls /tmp/.X11-unix | tr 'X' ':' | head -n 1)

echo "⚡ Iniciando o Relé Diferencial..."
python src/main.py