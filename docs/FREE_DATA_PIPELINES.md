# Free Data Pipeline Options for Black-Scholes Option Pricer

This document outlines free solutions for connecting the Black-Scholes Option Pricer backend to lightweight frontends.

## Architecture Overview

```
[Backend: FastAPI + Streamlit]  <-->  [Data Pipeline]  <-->  [Lightweight Frontend]
```

## Free Backend Hosting Options

### 1. **Render.com** (Recommended)
- **Free Tier**: 750 hours/month
- **Features**:
  - Deploy FastAPI directly from GitHub
  - Automatic HTTPS
  - WebSocket support
  - Environment variables
- **Limitations**: Spins down after 15 min inactivity (30s cold start)
- **Setup**:
  ```bash
  # Create render.yaml in project root
  services:
    - type: web
      name: black-scholes-api
      env: python
      buildCommand: pip install -r requirements.txt
      startCommand: uvicorn src.api.routes:app --host 0.0.0.0 --port $PORT
  ```

### 2. **Railway.app**
- **Free Tier**: $5 monthly credits
- **Features**:
  - Auto-deploy from GitHub
  - Built-in PostgreSQL (can replace MySQL)
  - Environment variables
  - No sleep on inactivity
- **Best For**: Development and testing
- **Setup**: Connect GitHub repo, Railway auto-detects Python

### 3. **Fly.io**
- **Free Tier**: 3 shared-cpu VMs, 160GB bandwidth/month
- **Features**:
  - Global deployment
  - WebSocket support
  - Persistent volumes for data
- **Setup**:
  ```bash
  fly launch
  fly deploy
  ```

### 4. **Streamlit Community Cloud** (For Streamlit GUI)
- **Free Tier**: Unlimited public apps
- **Features**:
  - Direct GitHub deployment
  - Automatic updates on git push
  - Built-in secrets management
- **Perfect For**: The existing Streamlit interface
- **URL**: https://streamlit.io/cloud

## Free Frontend Options

### 1. **Vercel** (Recommended for React/Next.js)
- **Free Tier**: Unlimited deployments
- **Features**:
  - Edge network (fast globally)
  - Automatic HTTPS
  - Serverless functions
  - Environment variables
- **Best For**: React, Next.js, Vue, Svelte frontends
- **Setup**: Connect GitHub repo, auto-deploy on push

### 2. **Netlify**
- **Free Tier**: 100GB bandwidth/month
- **Features**:
  - Form handling
  - Serverless functions
  - Split testing
- **Best For**: Static sites, React, Vue

### 3. **GitHub Pages**
- **Free Tier**: Unlimited (for public repos)
- **Limitations**: Static sites only (no backend)
- **Best For**: Simple HTML/CSS/JS frontends
- **Setup**: Enable in repo settings

### 4. **Cloudflare Pages**
- **Free Tier**: Unlimited bandwidth
- **Features**:
  - Fast global CDN
  - Workers for edge compute
  - R2 storage (10GB free)

## Data Pipeline Solutions

### Option 1: Direct REST API (Simplest)
```
Frontend (Vercel) --HTTP--> FastAPI (Render)
```

**Pros**: Simple, no middleware
**Cons**: Request/response only, no real-time updates

**Implementation**:
```javascript
// Frontend fetch example
const response = await fetch('https://your-api.onrender.com/monte-carlo', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    S: 100, K: 100, T: 1, r: 0.05, sigma: 0.2, option_type: 'call'
  })
});
const data = await response.json();
```

### Option 2: WebSocket for Real-Time Convergence Updates
```
Frontend (Vercel) <--WebSocket--> FastAPI + Socket.io (Render)
```

**Pros**: Real-time iteration updates for convergence plots
**Cons**: Requires WebSocket support

**Backend Enhancement** (add to requirements.txt):
```
python-socketio
websockets
```

**Implementation**:
```python
# Add to src/api/routes.py
from fastapi import WebSocket
import asyncio

@app.websocket("/ws/convergence")
async def convergence_stream(websocket: WebSocket):
    await websocket.accept()
    # Stream convergence data as it's calculated
    for iteration in range(num_simulations):
        if iteration % 1000 == 0:  # Update every 1000 iterations
            data = {"iteration": iteration, "price": current_price}
            await websocket.send_json(data)
```

### Option 3: Server-Sent Events (SSE) - Recommended
```
Frontend (Vercel) <--SSE--> FastAPI (Render)
```

**Pros**: Simpler than WebSocket, one-way streaming, built into FastAPI
**Cons**: One-way only (server to client)

**Implementation**:
```python
from fastapi.responses import StreamingResponse

@app.get("/stream/convergence")
async def stream_convergence():
    async def generate():
        for i in range(100):
            data = f"data: {json.dumps({'iteration': i, 'price': price})}\n\n"
            yield data
            await asyncio.sleep(0.1)
    return StreamingResponse(generate(), media_type="text/event-stream")
```

### Option 4: Supabase (Free Realtime Database)
```
Backend (Render) --> Supabase DB <-- Frontend (Vercel)
```

**Free Tier**: 500MB database, 2GB bandwidth
**Pros**: Real-time subscriptions, authentication, storage
**Cons**: PostgreSQL only (need to migrate from MySQL)

**Setup**:
```bash
pip install supabase
```

## Recommended Stack for This Project

### **Best Free Stack**:
1. **Backend API**: Render.com (FastAPI with convergence endpoints)
2. **GUI**: Streamlit Community Cloud (existing Streamlit app)
3. **Frontend**: Vercel (lightweight React dashboard for convergence visualization)
4. **Database**: Supabase (free PostgreSQL) or keep MySQL in Docker locally
5. **Real-time Updates**: Server-Sent Events for streaming convergence data

### **Architecture**:
```
┌─────────────────────────────────────────────────────────┐
│                    GitHub Repository                     │
└───┬─────────────────────┬───────────────────────┬───────┘
    │                     │                       │
    v                     v                       v
┌─────────────┐   ┌──────────────┐      ┌─────────────────┐
│  Streamlit  │   │ FastAPI      │      │ React Frontend  │
│  Cloud      │   │ (Render.com) │      │ (Vercel)        │
│             │   │              │      │                 │
│ - Main GUI  │   │ - REST API   │      │ - Convergence   │
│ - Heatmaps  │   │ - Convergence│      │   Plots         │
│ - Analysis  │   │ - SSE Stream │      │ - Real-time     │
└─────────────┘   └──────┬───────┘      └────────┬────────┘
                         │                       │
                         v                       v
                  ┌──────────────────────────────┐
                  │   Supabase (Optional)        │
                  │   - PostgreSQL               │
                  │   - Real-time subscriptions  │
                  └──────────────────────────────┘
```

## Quick Deployment Guide

### 1. Deploy FastAPI to Render
```bash
# Create render.yaml
cat > render.yaml << EOF
services:
  - type: web
    name: black-scholes-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn src.api.routes:app --host 0.0.0.0 --port \$PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
EOF

# Push to GitHub
git add render.yaml
git commit -m "Add Render deployment config"
git push

# Go to render.com, connect GitHub repo, deploy
```

### 2. Deploy Streamlit to Streamlit Cloud
1. Go to https://share.streamlit.io
2. Connect GitHub repo
3. Set main file: `src/gui/streamlit_app.py`
4. Add secrets (MySQL credentials) in dashboard
5. Deploy

### 3. Create Simple React Frontend (Optional)
```bash
npx create-react-app black-scholes-frontend
cd black-scholes-frontend

# Install Chart.js for convergence plots
npm install chart.js react-chartjs-2

# Deploy to Vercel
vercel --prod
```

## Cost Comparison

| Service | Free Tier | Limitations | Best For |
|---------|-----------|-------------|----------|
| Render | 750 hrs/mo | Spins down after 15 min | Production-ready API |
| Railway | $5 credits/mo | Limited usage | Development |
| Streamlit Cloud | Unlimited | Public repos only | Demos, prototypes |
| Vercel | Unlimited | 100GB bandwidth | Production frontends |
| Supabase | 500MB DB | 2GB bandwidth | Small projects |

## Next Steps

1. **Immediate**: Deploy Streamlit app to Streamlit Cloud (5 minutes)
2. **Short-term**: Deploy FastAPI to Render for API access (10 minutes)
3. **Optional**: Build lightweight React frontend with Vercel for convergence visualization (1-2 hours)

All of these options are **completely free** for the scale of this project.
