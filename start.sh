#!/bin/bash
# Criar ambiente virtual se não existir
if [ ! -d ".venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv .venv
fi

# Ativar ambiente virtual
source .venv/bin/activate

# Instalar dependências
if [ -f "requirements.txt" ]; then
    echo "Instalando dependências..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "Arquivo requirements.txt não encontrado!"
    exit 1
fi

# Executar o script principal
if [ -f "main.py" ]; then
    echo "Executando main.py..."
    python3 main.py
else
    echo "Arquivo main.py não encontrado!"
    exit 1
fi
