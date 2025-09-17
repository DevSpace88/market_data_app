# Market Analysis Platform

Real-time market analysis with technical indicators, patterns, signals, risk metrics and AI-powered insights. Backend runs on port 8000, frontend on 5173.

## Features

- Real-time market data via WebSocket
- Technical analysis with multiple indicators
- Pattern recognition and trading signals
- AI-powered market insights
- Interactive charts and dashboards
- Watchlist functionality

## Installation

### Backend

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
cd backend
pip install -r requirements.txt

# Optional: Environment variables
# SECRET_KEY and DB are required; AI keys are configured in the app UI.
cp .env.example .env
vi .env

# Start the server
uvicorn app.main:app --reload
```

### Frontend

```bash
# Install dependencies
cd frontend
npm install

# Install shadcn/vue components
npx shadcn-vue init
npx shadcn-vue add button card input badge progress

# Start development server
npm run dev

# Optional: disable WebSockets during dev to avoid console noise
# create .env.local with:
# VITE_ENABLE_WS=false
```

## Environment Variables (Backend)

Create a `.env` in `backend/` (no OpenAI key required here):

```env
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///./market_analysis.db
BACKEND_CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

AI Provider keys (OpenAI, DeepSeek, etc.) werden in der App unter „AI Settings“ gespeichert (plaintext) und serverseitig sicher verwendet. Kein Key in `.env` nötig.

## Usage

1. ```cd backend```
2. ```uvicorn app.main:app```
3. ```cd frontend```
4. ```npm run dev```
5. Open `http://localhost:5173` in your browser
6. Use the search bar to find stocks
7. View real-time data and analysis
8. Add symbols to your watchlist
9. Login (Default Admin)
   - username: admin
   - password: admin123

## API Documentation

Access the interactive API documentation at `http://localhost:8000/docs`

## Technology Stack

### Backend
- FastAPI
- SQLAlchemy
- LangChain
- yfinance
- pandas-ta

### Quant Features
- Indicators: RSI, MACD, SMA/EMA, Stochastic, Williams %R, CCI, ADX, Bollinger, ATR, OBV, VROC, AD-Line, Pivot Points
- Patterns: Candlestick, Chart, Trend, Volume, Support/Resistance
- Signals: short/medium/long-term with strength
- Risk: volatility, drawdown, momentum, liquidity, S/R, overall score

### Frontend
- Vue 3
- Vite
- Pinia
- Shadcn/Vue
- ECharts
- TailwindCSS

## Caching
- Frontend: market data (2 min), AI analysis (10 min), watchlist (1 min), hot stocks (5 min)
- Backend: AI analysis 24h, hot stocks 5–15 min

## Internationalization (i18n)
- Deutsch/Englisch umschaltbar in der Navbar
- Default wird aus `localStorage.language` gelesen

## WebSockets
- Endpoint: `ws://localhost:8000/api/v1/ws/market/{symbol}?token=JWT`
- Im Dev standardmäßig per Flag deaktivierbar: `VITE_ENABLE_WS=false`

```
## Login
- User: admin
- PW: admin123
```
