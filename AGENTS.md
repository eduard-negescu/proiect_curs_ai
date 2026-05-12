# Agents & Tools

Multi-agent system for elderly bracelet monitoring, built on top of the Bracelet API.

## Architecture

```
┌──────────────────────────────────┐
│           Orchestrator           │
│  (entry point, routes requests)  │
└──────────────┬───────────────────┘
               │
┌──────────────▼───────────────────┐
│         Bracelet Agent           │
│  (all bracelet operations)       │
└──────────────┬───────────────────┘
               │
┌──────────────▼───────────────────┐
│          Bracelet API            │
│      (FastAPI + PostgreSQL)      │
└──────────────────────────────────┘
```

## Tools

The Bracelet Agent wraps all Bracelet API endpoints as tools.

| Tool | Endpoint | Description |
|------|----------|-------------|
| `create_device` | `POST /device` | Register a new bracelet |
| `list_devices` | `GET /device` | List all registered devices |
| `record_health` | `POST /health` | Record SpO2 and heartbeat for a device |
| `get_latest_health` | `GET /health` | Get latest health readings per device |
| `record_gps` | `POST /gps` | Record a GPS position for a device |
| `get_latest_gps` | `GET /gps` | Get latest GPS position per device |

## Agent

### Orchestrator (`src/agents/orchestrator.py`)
Entry point that receives user requests, invokes the Bracelet Agent, and returns results.

- **Responsibilities**: Request routing, response formatting.
- **Triggers**: User messages.

### Bracelet Agent (`src/agents/bracelet_agent.py`)
Handles all interactions with the Bracelet API — device management, health data, and GPS tracking.

- **Tools**: all 6 tools listed above.
- **Capabilities**:
  - Register and list devices.
  - Record and retrieve health data (SpO2, heartbeat).
  - Record and retrieve GPS positions.

## Data Model

```
Device (1) ──┬── (many) HealthRecord
             └── (many) GPSRecord
```

- **Device**: UUID, created_at
- **Health**: device_id, sp0 (SpO2), heartbeat, created_at
- **GPS**: device_id, latitude, longitude, created_at

## Adding a New Agent

1. Create `src/agents/<name>_agent.py` with a class that exposes async methods.
2. Register the agent in the orchestrator's agent registry.
3. Define the tools the agent needs (wrap API calls).
4. Add tests in `tests/agents/`.
