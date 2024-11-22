# Market Analysis Platform

A real-time market analysis platform with technical indicators and AI-powered insights.

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

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

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
```

## Environment Variables

Create a `.env` file in the backend directory:

```env
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///./market_analysis.db
```

## Usage

1. ```cd backend```
2. ```uvicorn app.main:app```
3. ```cd frontend```
4. ```npm run dev```
5. Open `http://localhost:5173` in your browser
6. Use the search bar to find stocks
7. View real-time data and analysis
8. Add symbols to your watchlist

## API Documentation

Access the interactive API documentation at `http://localhost:8000/docs`

## Technology Stack

### Backend
- FastAPI
- SQLAlchemy
- LangChain
- yfinance
- pandas-ta

### Frontend
- Vue 3
- Vite
- Pinia
- Shadcn/Vue
- ECharts
- TailwindCSS

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT