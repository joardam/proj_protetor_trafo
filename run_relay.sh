#!/bin/bash
clear
echo -e "\033[1;32m=================================================================\033[0m"
echo -e "\033[1;32m🚀 O AMBIENTE FOI CONFIGURADO E INICIADO AUTOMATICAMENTE!\033[0m"
echo -e "\033[1;32m=================================================================\033[0m"
echo -e ""
echo -e "👉 \033[1;36mPara abrir a tela do Simulador, CLIQUE NO LINK ABAIXO:\033[0m"
echo -e "🔗 http://localhost:6080"
echo -e ""
echo -e "   (No Windows/Linux: Segure a tecla CTRL e clique no link)"
echo -e "   (No Mac: Segure a tecla CMD e clique no link)"
echo -e ""
echo -e "\033[1;32m=================================================================\033[0m"

echo "================================================================="
echo ""

# 1. Conecta o terminal ao monitor virtual
export DISPLAY=$(ls /tmp/.X11-unix | tr 'X' ':' | head -n 1)

# 2. Roda o Python (Fica rodando infinitamente até o professor fechar)
python relay/main.py

echo "🔌 Conectando ao Monitor Virtual..."
export DISPLAY=$(ls /tmp/.X11-unix | tr 'X' ':' | head -n 1)

echo "⚡ Iniciando o Relé Diferencial..."
python relay/main.py