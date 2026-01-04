# Restaurant Voice Agent - ElevenLabs Integration

Backend API pour un agent vocal conversationnel de restaurant utilisant **ElevenLabs Conversational AI**.

## 🏗️ Architecture

```
📞 Appel Twilio / Widget Web
         ↓
ElevenLabs Conversational AI Agent
    (STT + LLM + TTS intégré)
         ↓
    Webhooks / Tools
         ↓
  FastAPI Backend ← (ce projet)
         ↓
    Supabase DB
```

## 🚀 Quick Start

### 1. Installation

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configuration

```bash
cp .env.example .env
# Éditer .env avec vos credentials Supabase
```

### 3. Lancer le serveur

```bash
uvicorn app.main:app --reload --port 8000
```

### 4. Tester

- Ouvrir http://localhost:8000/docs pour Swagger UI
- Le serveur fonctionne en **mode démo** sans Supabase

---

## 📡 API Endpoints

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `POST` | `/api/availability` | Vérifier disponibilité |
| `POST` | `/api/reservations` | Créer réservation |
| `GET` | `/api/menu` | Menu (filter: `?category=plats`) |
| `POST` | `/api/orders` | Commander à emporter |
| `GET` | `/api/restaurant-info` | Infos restaurant |
| `POST` | `/webhook/call-ended` | Webhook ElevenLabs |

---

## 🗄️ Supabase Setup

Exécuter les migrations dans l'ordre :

1. `supabase/migrations/001_initial_schema.sql`
2. `supabase/migrations/002_seed_data.sql`

---

## 🤖 ElevenLabs Configuration

1. Créer un agent dans le [dashboard ElevenLabs](https://elevenlabs.io/conversational-ai)
2. Copier le contenu de `elevenlabs/agent_config.json`
3. Remplacer `YOUR-API-URL` par votre URL déployée

---

## 🚢 Déploiement

| Service | Option Gratuite |
|---------|----------------|
| Backend | Railway, Render, Fly.io |
| Database | Supabase Cloud |
| Téléphonie | Twilio (via ElevenLabs) |

### Exemple Railway

```bash
railway login
railway init
railway up
```

---

## 📁 Structure

```
backend/
├── app/
│   ├── main.py          # FastAPI app
│   ├── routers/
│   │   ├── reservations.py
│   │   ├── menu.py
│   │   ├── orders.py
│   │   ├── info.py
│   │   └── webhooks.py
│   ├── services/
│   │   └── supabase.py
│   └── models/
│       └── schemas.py
├── requirements.txt
└── .env.example
```

---

## 📞 Flow d'un appel

1. Client appelle le numéro Twilio
2. Twilio route vers ElevenLabs Agent
3. Agent: "Bonjour, restaurant Chez Marcel !"
4. Client: "Je voudrais réserver pour 4 samedi"
5. Agent → `POST /api/availability`
6. Backend → Supabase → `{available: true}`
7. Agent: "C'est disponible ! À quel nom ?"
8. ... conversation continue ...
9. Agent → `POST /api/reservations`
10. Agent: "Réservation confirmée !"
11. Appel terminé → `POST /webhook/call-ended`
12. Transcription sauvegardée ✓
