# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A **financial analysis platform** built as a monorepo with FastAPI backend and Vue 3 frontend. It provides real-time market data, technical analysis, AI-powered insights, and watchlist management.

**Tech Stack:**
- **Backend:** FastAPI + SQLAlchemy + Pydantic v2 + yfinance/pandas-ta + LangChain
- **Frontend:** Vue 3 (Composition API + TypeScript) + Vite + Pinia + Vue Router + Shadcn/Vue + TailwindCSS
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
npm run dev           # Vite dev server on :5173
npm run build         # Production build to dist/
npm run preview       # Preview production build on :3000
npm run type-check    # TypeScript type checking
```

### Adding Shadcn Components
```bash
cd frontend
npx shadcn-vue add <component-name>
```
**IMPORTANT:** Always use Shadcn components (Button, Card, Input, Tabs, Alert, Badge, Progress, Label, Toast, etc.) instead of building custom UI. This is enforced by the project's component library discipline.

## Architecture

### Backend Structure (`backend/app/`)
- **`api/routes/`** - Modular routers: auth, market, market_analysis, watchlist, hot-stocks, ai-settings, websocket
- **`models/`** - SQLAlchemy ORM models (User with AI provider settings, Watchlist)
- **`schemas/`** - Pydantic v2 schemas for request/response validation
- **`services/`** - Business logic layer:
  - `ai_provider_service.py` - Multi-provider AI (OpenAI, DeepSeek, Anthropic, Google, Ollama)
  - `api_token_service.py` - API key encryption/decryption
  - `market_service.py` - Market data fetching with currency detection
  - `technical_indicators.py` - RSI, MACD, SMA/EMA, Stochastic, Williams %R, CCI, ADX, Bollinger, ATR, OBV, VROC, AD-Line, Pivot Points
  - `pattern_detection.py` - Candlestick, chart, trend, volume, support/resistance patterns
  - `signal_generation.py` - Short/medium/long-term trading signals
  - `risk_metrics.py` - Volatility, drawdown, momentum, liquidity risk metrics
- **`middleware/`** - Rate limiting, security headers
- **`auth.py`** - JWT authentication with httpOnly cookie support, `get_current_active_user` dependency
- **`config.py`** - Pydantic BaseSettings with auto-generated SECRET_KEY for development
- **`main.py`** - FastAPI app with CORS, security middleware, static file serving

All API routes use `/api/v1/` prefix. Backend serves frontend static files from `frontend/dist/` in production.

### Frontend Structure (`frontend/src/`)
- **`stores/`** - Pinia stores (auth.ts, market.ts, language.ts, theme.ts)
  - `market.ts` orchestrates composables (useMarketData, useMarketWebSocket, useMarketIndicators)
- **`views/`** - Page components (LoginView, MarketDashboard, SymbolAnalysis, AISettings)
- **`composables/`** - Reusable composition functions:
  - `useMarketData.ts` - Data fetching with cache integration
  - `useMarketWebSocket.ts` - WebSocket management (only with VITE_ENABLE_WS=true)
  - `useMarketIndicators.ts` - Individual indicator fetchers
- **`services/`** - `cacheService.ts` with TTL-based caching (market: 2min, AI: 10min, watchlist: 1min, hot-stocks: 5min)
- **`router/index.ts`** - Vue Router with auth guard, symbol validation
- **`i18n/`** - EN/DE translations with nested key structure
- **`components/ui/`** - Shadcn/Vue components (DO NOT build custom components when these exist)
- **`lib/`** - Utilities and helpers

### Key Patterns

**Authentication Flow:**
1. JWT token stored in **httpOnly cookie** by backend (secure, XSS-protected)
2. localStorage fallback for cross-origin scenarios
3. Backend validates via `get_current_active_user` dependency (accepts cookie or Authorization header)
4. Route guard in `router/index.ts` redirects unauthenticated users to `/login`
5. SecurityHeadersMiddleware adds security headers (X-Content-Type-Options, X-Frame-Options, HSTS)

**WebSocket (Optional):**
- Controlled by `VITE_ENABLE_WS` env var (default: disabled)
- Only active on SymbolAnalysis view
- Requires valid JWT with 60s buffer before expiration
- Ping every 30s, exponential backoff reconnection (max 3 retries)
- Endpoint: `/api/v1/ws/market/{symbol}`

**State Management:**
- Pinia stores use Composition API pattern (TypeScript)
- Market store is a thin orchestrator layer combining composables
- CacheService integrated into data fetching actions

**Component Philosophy:**
- **Shadcn/Vue ONLY** - Never build custom modals, dropdowns, or buttons from scratch
- Radix Vue primitives for accessibility
- Available components: Button, Card, Input, Tabs, Alert, Badge, Progress, Label, Toast

**Currency Detection:**
Backend automatically detects currency based on stock symbol suffixes (.T for Tokyo, .L for London, .HK for Hong Kong, .KS for Seoul, .SS/.SZ for Shanghai/Shenzhen).

## Configuration

### Environment Variables (`backend/.env`)
```
DATABASE_URL=sqlite:///./market_analysis.db  # or postgresql://...
RAILWAY_DATABASE_URL=  # PostgreSQL for Railway deployment
SECRET_KEY=  # JWT signing (auto-generated if not set)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend Environment (`frontend/.env`)
```
VITE_API_BASE_URL=http://localhost:8000
VITE_ENABLE_WS=false  # Set to 'true' for WebSocket
```

### Vite Proxy (`frontend/vite.config.ts`)
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
- **AI Provider Keys:** Stored per-user in `api_key_token` field (encrypted via APITokenService)

## API Integration

**Market Data:** yfinance library for real-time and historical data
**Technical Analysis:** pandas-ta for indicators, patterns, signals
**AI Analysis:** LangChain with multiple providers (OpenAI, DeepSeek, Anthropic, Google, Ollama)
**Users configure AI keys in the application** - not in server environment variables.

## Deployment

- Monorepo deployment: Backend serves frontend static files from `frontend/dist/`
- Railway supports PostgreSQL via `RAILWAY_DATABASE_URL`
- Health check endpoint: `/api/v1/health`
