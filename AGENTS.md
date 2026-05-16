# Agents & Tools

Multi-agent system for elderly bracelet monitoring, built on top of the Bracelet API.

## Architecture

```
┌──────────────────────────────────┐
│           Coordinator            │
│  (CLI entry, routes queries)     │
└──────────┬───────────┬───────────┘
           │           │
┌──────────▼──┐ ┌──────▼───────────┐
│  GPS Agent  │ │   Health Agent   │
│ (locații)   │ │ (SpO2, puls)     │
└──────────┬──┘ └──────┬───────────┘
           │           │
┌──────────▼───────────▼───────────┐
│          Bracelet API            │
│      (FastAPI + PostgreSQL)      │
└──────────────────────────────────┘
```

## Agents

### Coordinator (`src/agents/coordinator.py`)
CLI entry point (`python -m agents.coordinator`). Routes user queries to the appropriate agent and generates LLM responses via local Ollama.

- **Responsibilities**: Query routing, LLM response generation.
- **Route triggers**: keyword matching (e.g. "gps", "heartbeat", "spo2").

### GPS Agent (`src/agents/gps_agent.py`)
Handles GPS location queries and location recording.

- **Tools**: `get_latest_gps`, `record_gps`
- **Skills**: `get_device_locations`

### Health Agent (`src/agents/health_agent.py`)
Handles health monitoring queries (SpO2, heartbeat).

- **Tools**: `get_latest_health`, `record_health`
- **Skills**: `get_highest_heartbeat`, `find_low_spo2`, `find_high_heartbeat`

## Running

```bash
# Start the API
bracelet_dev

# Start the CLI agent
python -m agents.coordinator
```

## Data Model

```
Device (1) ──┬── (many) HealthRecord
             └── (many) GPSRecord
```

- **Device**: UUID, created_at
- **Health**: device_id, sp0 (SpO2), heartbeat, created_at
- **GPS**: device_id, latitude, longitude, created_at

## Migrations

Database migrations use Alembic with async SQLAlchemy.

| Command | Description |
|---------|-------------|
| `alembic revision --autogenerate -m "message"` | Create a new migration from model changes |
| `alembic upgrade head` | Apply pending migrations |
| `alembic downgrade -1` | Rollback last migration |

- Migration scripts live in `migrations/versions/`.
- The database URL is read from `bracelet_api.config.settings` at runtime.
- Import new models in `migrations/env.py` so autogenerate detects them.

## Adding a New Agent

1. Create `src/agents/<name>_agent.py` with a class that exposes the agent's methods.
2. Register the agent in the coordinator's routing logic.
3. Add tests in `tests/agents/`.
