# Web-Based Architecture - Technical Design

## Overview

This document outlines the technical architecture for transforming Mac Health Pulse from a PyQt6 desktop application into a scalable, cross-platform web application.

## Goals

1. **Cross-platform support** - Monitor Windows, Linux, and macOS
2. **Multi-user access** - Multiple users can access simultaneously
3. **Real-time updates** - Live system metrics without page refresh
4. **API-first design** - Enable integrations and automation
5. **Horizontal scalability** - Handle thousands of concurrent users
6. **Maintain UX** - Keep the cyberpunk aesthetic and smooth animations

## System Architecture

```
┌──────────────────────────────────────────────────────────┐
│                      Client Layer                         │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐         │
│  │  Browser   │  │ Mobile App │  │  Desktop   │         │
│  │  (React)   │  │   (React   │  │  (Electron)│         │
│  │            │  │   Native)  │  │  Optional  │         │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘         │
└────────┼───────────────┼───────────────┼────────────────┘
         │               │               │
         │        REST API + WebSocket   │
         │                               │
┌────────▼───────────────────────────────▼────────────────┐
│                   API Gateway (Nginx)                    │
│              Load Balancer + SSL Termination             │
└────────┬────────────────────────────────────────────────┘
         │
    ┌────┴─────┐
    │          │
┌───▼───┐  ┌──▼────┐
│ API   │  │ API   │  ... (Multiple instances)
│ Server│  │ Server│
│   #1  │  │   #2  │
└───┬───┘  └───┬───┘
    │          │
    └────┬─────┘
         │
    ┌────┴────────────────────┐
    │                         │
┌───▼────┐  ┌────────┐  ┌────▼─────┐  ┌──────────┐
│ Redis  │  │Postgres│  │  Celery  │  │  Agent   │
│ Cache  │  │   DB   │  │  Worker  │  │  (Host)  │
└────────┘  └────────┘  └──────────┘  └──────────┘
```

## Component Breakdown

### 1. Frontend (React/TypeScript)

#### Technology Stack

```json
{
  "framework": "React 18+ with TypeScript",
  "state": "Zustand or Redux Toolkit",
  "charts": "Recharts or Chart.js",
  "realtime": "Socket.IO client",
  "styling": "TailwindCSS + CSS-in-JS",
  "build": "Vite",
  "testing": "Vitest + React Testing Library"
}
```

#### Key Features

**Dashboard Component**
```typescript
// src/components/Dashboard.tsx
import { useRealTimeMetrics } from '@/hooks/useRealTimeMetrics'
import { CircularGauge } from '@/components/charts/CircularGauge'
import { LineChart } from '@/components/charts/LineChart'

export const Dashboard = () => {
  const { cpu, memory, processes } = useRealTimeMetrics()

  return (
    <div className="grid grid-cols-3 gap-4">
      <CircularGauge value={cpu} label="CPU" theme="cyan" />
      <CircularGauge value={memory} label="Memory" theme="magenta" />
      <LineChart data={processes} label="Processes" />
    </div>
  )
}
```

**Real-Time WebSocket Hook**
```typescript
// src/hooks/useRealTimeMetrics.ts
import { useEffect, useState } from 'react'
import { io } from 'socket.io-client'

export const useRealTimeMetrics = () => {
  const [metrics, setMetrics] = useState({})

  useEffect(() => {
    const socket = io(process.env.VITE_API_URL)

    socket.on('metrics', (data) => {
      setMetrics(data)
    })

    return () => socket.disconnect()
  }, [])

  return metrics
}
```

#### File Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard.tsx
│   │   ├── ProcessList.tsx
│   │   ├── StartupManager.tsx
│   │   └── charts/
│   │       ├── CircularGauge.tsx
│   │       ├── LineChart.tsx
│   │       └── BarChart.tsx
│   ├── hooks/
│   │   ├── useRealTimeMetrics.ts
│   │   └── useProcesses.ts
│   ├── services/
│   │   └── api.ts
│   ├── styles/
│   │   └── theme.ts (Cyberpunk theme)
│   ├── App.tsx
│   └── main.tsx
├── package.json
└── vite.config.ts
```

### 2. Backend API (FastAPI/Python)

#### Technology Stack

```python
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
websockets==12.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
redis==5.0.1
celery==5.3.4
psutil==5.9.6  # Reuse existing!
pydantic==2.5.0
python-jose[cryptography]==3.3.0  # JWT auth
```

#### API Structure

```python
# backend/app/main.py
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from .routes import metrics, processes, startup
from .websocket import manager

app = FastAPI(title="Mac Health Pulse API", version="2.0.0")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REST API routes
app.include_router(metrics.router, prefix="/api/v1/metrics")
app.include_router(processes.router, prefix="/api/v1/processes")
app.include_router(startup.router, prefix="/api/v1/startup")

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Send real-time metrics every second
            metrics = await get_current_metrics()
            await manager.send_json(metrics)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

#### Metrics API

```python
# backend/app/routes/metrics.py
from fastapi import APIRouter, Depends
from ..services.system_monitor import SystemMonitor
from ..schemas import SystemMetrics

router = APIRouter()

@router.get("/current", response_model=SystemMetrics)
async def get_current_metrics():
    """Get current system metrics"""
    monitor = SystemMonitor()
    return {
        "cpu_percent": monitor.cpu_percent(),
        "memory_percent": monitor.memory_percent(),
        "disk_usage": monitor.disk_usage(),
        "process_count": monitor.process_count(),
        "timestamp": datetime.utcnow()
    }

@router.get("/history")
async def get_metrics_history(
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """Get historical metrics"""
    return db.query(MetricsSnapshot)\
        .filter(MetricsSnapshot.timestamp > datetime.utcnow() - timedelta(hours=hours))\
        .all()
```

#### System Monitor Service

```python
# backend/app/services/system_monitor.py
import psutil
from typing import Dict, List

class SystemMonitor:
    """Reuse existing psutil logic from original app"""

    def cpu_percent(self, interval: float = 1.0) -> float:
        return psutil.cpu_percent(interval=interval)

    def memory_percent(self) -> float:
        return psutil.virtual_memory().percent

    def get_processes(self) -> List[Dict]:
        """Get all running processes with CPU/memory info"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return processes

    def get_top_processes(self, n: int = 10, sort_by: str = 'cpu') -> List[Dict]:
        """Get top N processes by CPU or memory"""
        processes = self.get_processes()
        key = 'cpu_percent' if sort_by == 'cpu' else 'memory_percent'
        return sorted(processes, key=lambda x: x[key], reverse=True)[:n]
```

#### File Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── routes/
│   │   ├── metrics.py
│   │   ├── processes.py
│   │   └── startup.py
│   ├── services/
│   │   ├── system_monitor.py  # Reuse psutil logic
│   │   ├── process_manager.py
│   │   └── startup_manager.py
│   ├── models/
│   │   ├── metrics.py
│   │   └── user.py
│   ├── schemas/
│   │   └── metrics.py
│   └── websocket.py
├── tests/
├── requirements.txt
└── Dockerfile
```

### 3. Database Layer

#### PostgreSQL Schema

```sql
-- Metrics snapshots (time-series data)
CREATE TABLE metrics_snapshots (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    cpu_percent FLOAT NOT NULL,
    memory_percent FLOAT NOT NULL,
    disk_usage_percent FLOAT,
    process_count INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create index for time-based queries
CREATE INDEX idx_metrics_timestamp ON metrics_snapshots(timestamp DESC);

-- Process snapshots
CREATE TABLE process_snapshots (
    id SERIAL PRIMARY KEY,
    snapshot_id INTEGER REFERENCES metrics_snapshots(id),
    pid INTEGER NOT NULL,
    name VARCHAR(255),
    cpu_percent FLOAT,
    memory_percent FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Users (optional, for multi-user)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Alerts configuration
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    metric_type VARCHAR(50),  -- 'cpu', 'memory', 'disk'
    threshold FLOAT,
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### Redis Cache Strategy

```python
# backend/app/services/cache.py
import redis
import json
from typing import Optional

class CacheService:
    def __init__(self):
        self.redis = redis.Redis(
            host='redis',
            port=6379,
            decode_responses=True
        )

    def get_current_metrics(self) -> Optional[dict]:
        """Get cached metrics (TTL: 1 second)"""
        data = self.redis.get('metrics:current')
        return json.loads(data) if data else None

    def set_current_metrics(self, metrics: dict):
        """Cache current metrics"""
        self.redis.setex(
            'metrics:current',
            1,  # 1 second TTL
            json.dumps(metrics)
        )
```

### 4. Background Workers (Celery)

```python
# backend/app/celery_app.py
from celery import Celery
from .services.system_monitor import SystemMonitor
from .models import MetricsSnapshot

celery_app = Celery(
    'health_pulse',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

@celery_app.task
def collect_metrics():
    """Collect and store metrics every 10 seconds"""
    monitor = SystemMonitor()

    # Save to database
    snapshot = MetricsSnapshot(
        cpu_percent=monitor.cpu_percent(),
        memory_percent=monitor.memory_percent(),
        process_count=len(monitor.get_processes())
    )
    db.add(snapshot)
    db.commit()

@celery_app.task
def cleanup_old_metrics():
    """Delete metrics older than 30 days"""
    cutoff = datetime.utcnow() - timedelta(days=30)
    db.query(MetricsSnapshot)\
        .filter(MetricsSnapshot.timestamp < cutoff)\
        .delete()
    db.commit()

# Schedule tasks
celery_app.conf.beat_schedule = {
    'collect-metrics': {
        'task': 'collect_metrics',
        'schedule': 10.0,  # Every 10 seconds
    },
    'cleanup-metrics': {
        'task': 'cleanup_old_metrics',
        'schedule': crontab(hour=0, minute=0),  # Daily at midnight
    },
}
```

### 5. Agent for Host Monitoring (Optional)

For monitoring the actual host system (not the container), deploy a lightweight agent:

```python
# agent/main.py
"""
Lightweight agent that runs on host and sends metrics to API
"""
import psutil
import requests
import time

API_URL = "https://api.healthpulse.example.com"
API_KEY = "your-api-key"

def send_metrics():
    metrics = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "processes": [p.info for p in psutil.process_iter(['pid', 'name', 'cpu_percent'])]
    }

    requests.post(
        f"{API_URL}/api/v1/metrics",
        json=metrics,
        headers={"Authorization": f"Bearer {API_KEY}"}
    )

if __name__ == "__main__":
    while True:
        send_metrics()
        time.sleep(10)
```

## Deployment

### Development

```bash
# Start all services
docker-compose up

# Frontend runs on: http://localhost:3000
# Backend API: http://localhost:8000
# API docs: http://localhost:8000/docs
```

### Production (docker-compose)

```yaml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    environment:
      - VITE_API_URL=https://api.healthpulse.com

  api:
    build: ./backend
    deploy:
      replicas: 3
    environment:
      - DATABASE_URL=postgresql://db/healthpulse
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis

  worker:
    build: ./backend
    command: celery -A app.celery_app worker
    depends_on:
      - redis

  beat:
    build: ./backend
    command: celery -A app.celery_app beat
    depends_on:
      - redis

  postgres:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  postgres_data:
```

## API Examples

### REST API

```bash
# Get current metrics
GET /api/v1/metrics/current

# Response
{
  "cpu_percent": 45.2,
  "memory_percent": 62.8,
  "disk_usage": 78.5,
  "process_count": 247,
  "timestamp": "2025-01-15T10:30:00Z"
}

# Get top processes
GET /api/v1/processes/top?limit=10&sort=cpu

# Kill a process
DELETE /api/v1/processes/1234

# Get historical data
GET /api/v1/metrics/history?hours=24&interval=5m
```

### WebSocket API

```javascript
// Connect to WebSocket
const socket = io('wss://api.healthpulse.com')

// Listen for real-time metrics
socket.on('metrics', (data) => {
  console.log('CPU:', data.cpu_percent)
  console.log('Memory:', data.memory_percent)
})

// Request specific data
socket.emit('subscribe', { metrics: ['cpu', 'memory'] })
```

## Migration Plan

### Step 1: Proof of Concept (1 week)

- [ ] Basic FastAPI server with /metrics endpoint
- [ ] Simple React frontend with one chart
- [ ] WebSocket connection for real-time updates
- [ ] Docker setup

### Step 2: Feature Parity (2-3 weeks)

- [ ] All dashboard metrics
- [ ] Process list with search/filter
- [ ] Top resource consumers
- [ ] Cyberpunk theme CSS

### Step 3: Database Integration (1 week)

- [ ] PostgreSQL setup
- [ ] Historical data storage
- [ ] Celery workers for background tasks

### Step 4: Production Ready (2 weeks)

- [ ] Authentication/authorization
- [ ] API rate limiting
- [ ] Error handling and logging
- [ ] Unit and integration tests
- [ ] Documentation

## Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| **API Response Time** | < 100ms | 95th percentile |
| **WebSocket Latency** | < 50ms | Real-time feel |
| **Concurrent Users** | 1,000+ | With 3 API instances |
| **Data Retention** | 30 days | Configurable |
| **Database Queries** | < 50ms | With indexes |

## Security Considerations

1. **Authentication**: JWT tokens with refresh
2. **Authorization**: Role-based access control (RBAC)
3. **Rate Limiting**: 100 req/min per user
4. **Input Validation**: Pydantic schemas
5. **SQL Injection**: SQLAlchemy ORM
6. **XSS Protection**: React auto-escaping
7. **HTTPS Only**: SSL/TLS in production

## Next Steps

1. Review this architecture
2. Start with Step 1 (PoC)
3. Deploy demo to Railway/Render
4. Gather feedback
5. Iterate

Questions? Open a GitHub issue or discussion.
