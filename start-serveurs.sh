#!/bin/bash

# 📁 Aller dans le dossier du backend
cd /workspaces/eventworld

echo "🚀 Démarrage du serveur backend (Django)..."
python manage.py migrate
nohup python manage.py runserver 0.0.0.0:8000 > backend.log 2>&1 &

# 📁 Aller dans le dossier du frontend
cd frontend/frontendEventWorld

echo "🚀 Démarrage du serveur frontend (Vite)..."
nohup npm run dev > frontend.log 2>&1 &

# ✅ Retour à la racine et confirmation
cd /workspaces/eventworld
echo "✅ Les serveurs backend et frontend sont activés."
