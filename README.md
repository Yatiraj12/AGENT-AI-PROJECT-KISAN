# Crop Disease AI Agent 🌱

An AI-powered crop disease analysis system that allows users to upload leaf images and receive disease detection, severity assessment, and treatment recommendations in multiple languages.

## Features
- Leaf image upload
- AI-based disease detection
- Severity estimation
- Treatment & prevention recommendations
- Multilingual support (English, Kannada, Hindi)
- Knowledge-base grounded responses
- History storage using SQLite

## Tech Stack
- Backend: FastAPI (Python)
- AI: Groq LLM (Qwen)
- Database: SQLite
- Frontend: HTML, CSS, JavaScript

## Project Structure
crop_disease_ai_agent/
├── app/
│ ├── agents/
│ ├── api/
│ ├── models/
│ ├── services/
│ ├── utils/
│ └── main.py
├── frontend/
│ ├── index.html
│ ├── style.css
│ └── script.js
├── knowledge_base/
├── data/
├── .env
└── README.md