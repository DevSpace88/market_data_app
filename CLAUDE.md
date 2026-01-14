# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A **financial analysis platform** built as a monorepo with FastAPI backend and Vue 3 frontend. It provides real-time market data, technical analysis, AI-powered insights, and watchlist management.

**Tech Stack:**
- **Backend:** FastAPI + SQLAlchemy + Pydantic v2 + yfinance/pandas-ta + LangChain
- **Frontend:** Vue 3 (Composition API) + Vite + Pinia + Vue Router + Shadcn/Vue + TailwindCSS
- **Charts:** ECharts + Lightweight Charts
- **i18n:** Vue I18n (English/German)

## Development Commands

### Backend
```bash
cd backend
source .venv/bin/activate  # Activate venv
uvicorn app.main:app --reload  # Dev server on :8000
```

### Frontend
```bash
cd frontend
npm run dev    # Vite dev server on :5173
npm run build  # Production build to dist/
npm run preview  # Preview production build on :3000
```

### Adding Shadcn Components
```bash
cd frontend
npx shadcn-vue add <component-name>
```
**IMPORTANT:** Always use Shadcn components (Button, Card, Input, Tabs, Alert, Badge, Progress, etc.) instead of building custom UI. This is enforced by the project's component library discipline.

## Architecture

### Backend Structure (`backend/app/`)
- **`api/routes/`** - Modular routers: auth, market, watchlist, hot-stocks, ai-settings, websocket
- **`models/`** - SQLAlchemy ORM models (User, MarketData, Watchlist, AISettings)
- **`schemas/`** - Pydantic v2 schemas for request/response validation
- **`services/`** - Business logic layer (ai_provider_service, market_service, etc.)
- **`auth.py`** - JWT authentication with `get_current_active_user` dependency
- **`config.py`** - Pydantic BaseSettings for environment configuration
- **`main.py`** - FastAPI app with CORS, static file serving, route mounting

All API routes use `/api/v1/` prefix.

### Frontend Structure (`frontend/src/`)
- **`stores/`** - Pinia stores (auth, market, language, theme). The `market.js` store is the largest (837 lines) and handles WebSocket connection management.
- **`views/`** - Page components (LoginView, MarketDashboard, SymbolAnalysis, etc.)
- **`components/ui/`** - Shadcn/Vue components (DO NOT build custom components when these exist)
- **`services/cacheService.js`** - TTL-based caching (market: 2min, AI: 10min, watchlist: 1min, hot-stocks: 5min)
- **`router/index.js`** - Vue Router with auth guard (`requiresAuth`)
- **`i18n/`** - EN/DE translations with nested key structure
- **`composables/`** - Reusable Vue composition functions
- **`lib/`** - Utilities and helpers

### Key Patterns

**Authentication Flow:**
1. JWT token stored in `localStorage` (`auth` store)
2. Axios interceptor injects `Authorization: Bearer <token>` header
3. Backend validates via `get_current_active_user` dependency
4. Route guard in `router/index.js` redirects unauthenticated users to `/login`

**WebSocket (Optional):**
- Controlled by `VITE_ENABLE_WS` env var (default: disabled)
- Only active on SymbolAnalysis view
- Requires valid JWT token (60s buffer before expiration)
- Ping every 30s, exponential backoff reconnection (max 3 retries)
- Endpoint: `/api/v1/ws/market/{symbol}`

**State Management:**
- Pinia stores use Composition API pattern
- Market store separates fetchers for each data type (indicators, patterns, signals, risk metrics)
- CacheService integrated into store actions

**Component Philosophy:**
- **Shadcn/Vue ONLY** - Never build custom modals, dropdowns, or buttons from scratch
- Radix Vue primitives under the hood for accessibility
- Wrap/style Shadcn components to achieve custom look, but always use the library primitive

## Configuration

### Environment Variables (`backend/.env`)
```
DATABASE_URL=sqlite:///./market_analysis.db  # or postgresql://...
RAILWAY_DATABASE_URL=  # PostgreSQL for Railway deployment
SECRET_KEY=  # JWT signing
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend Environment (`frontend/.env`)
```
VITE_API_BASE_URL=http://localhost:8000
VITE_ENABLE_WS=false  # Set to 'true' for WebSocket
```

### Vite Proxy (`frontend/vite.config.js`)
Proxies `/api` and `/ws` to backend port 8000 in development.

### Path Alias
`@/` maps to `src/` in Vite config.

## Internationalization

- Two languages: English (`en`) and German (`de`)
- Language toggle in Header component
- Locale persisted in localStorage
- Translation keys use dot notation: `nav.dashboard`, `symbolAnalysis.indicators`
- Default: locale from localStorage or `'en'`

## Database

- **Development:** SQLite (`market_analysis.db`)
- **Production:** PostgreSQL via Railway
- **Default admin:** `admin` / `admin123` (auto-created on first run)
- **AI Provider Keys:** Stored per-user in `ai_settings` table (plaintext, configured in UI)

## API Integration

**Market Data:** yfinance library for real-time and historical data
**Technical Analysis:** pandas-ta for indicators, patterns, signals
**AI Analysis:** LangChain with multiple providers (OpenAI, DeepSeek, Anthropic, Google, Ollama)
**Users configure AI keys in the application** - not in server environment variables.

## Deployment

- Monorepo deployment: Backend serves frontend static files from `frontend/dist/`
- Railway supports PostgreSQL via `RAILWAY_DATABASE_URL`
- CORS configured for `localhost:5173` and `localhost:3000`
