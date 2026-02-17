# CharacterForge: D&D 5e Character Builder & Sheet

CharacterForge is a modern web application for building and managing Dungeons & Dragons 5e (2024 Ruleset) characters. It features a step-by-step Character Creation Wizard and an interactive digital character sheet with integrated dice rolling.

## Project Overview

- **Backend:** Python (FastAPI) providing a RESTful API.
- **Database:** SQLite with SQLAlchemy (Asynchronous) for persistent storage.
- **Frontend:** Responsive HTML/JS styled with Tailwind CSS, served directly by FastAPI.
- **Modular Design:** Features, Classes, and Species are stored in the database, allowing for easy expansion and "modding."

## Architecture

- `backend/app/`: Core API logic, models, schemas, and database configuration.
- `frontend/public/`: Static assets, HTML, and client-side JavaScript.
- `data/`: Database seeding scripts and SRD content.
- `prompts/`: Instructional prompts for generating UI assets with AI.

## Building and Running

### 1. Setup Environment
```bash
python3 -m venv venv
./venv/bin/pip install -r backend/requirements.txt
```

### 2. Initialize and Seed Database
```bash
export PYTHONPATH=$PYTHONPATH:.
./venv/bin/python3 data/seed_srd.py
```

### 3. Run the Application
```bash
./run.sh
```

### 4. Run with Docker
```bash
docker-compose up --build
```
The application will be available at `http://localhost:8000`.

## Development Conventions

- **Database:** Use SQLAlchemy for all database interactions. The schema is designed to be modular via the `Feature` and `feature_association` models.
- **API:** Follow RESTful principles. All API routes should be prefixed with `/api/`.
- **Frontend:** Keep logic in `script.js` and use Tailwind CSS for styling. Use the `rollDice` utility for all interactive d20 checks.
- **Git:** Commit frequently with descriptive messages. Always push changes to the main branch after significant updates.
