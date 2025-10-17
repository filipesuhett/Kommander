#!/bin/bash

# --- Configurações do Bot ---
# Substitua com seus próprios valores
export DISCORD_TOKEN="MTQyNDYwMzM2OTY5MTAyNTQ4OA.G1qEMH.LuFfd3cO6rXY4vPU8-yeXPQO8S_Gb2TaU88X4M"
export GUILD_ID="1263637394096132206"
export CHANNEL_NAME="kommander" # Opcional, mas recomendado para evitar spam
export TIMEOUT="60"

echo "Iniciando o bot Kommander localmente..."

# --- Executando o Bot ---
# O primeiro argumento é o arquivo de regras.
# O segundo argumento é o arquivo de comandos.
python3 kommander-app/app/main.py rules.yaml commands.yaml

echo "Bot encerrado."

