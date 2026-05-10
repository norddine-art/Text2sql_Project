#!/bin/bash
echo "🚀 Activation de l'environnement virtuel..."
source venv/bin/activate
echo "✅ Environnement activé ! Lancement de l'interface..."
streamlit run frontend/app.py
