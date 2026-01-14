# Product Requirements Document: Investment Decision Engine

**Version**: 1.0
**Date**: 2025-01-14
**Author**: Sarah (Product Owner)
**Quality Score**: 91/100

---

## Executive Summary

Die **Investment Decision Engine** transformiert die bestehende Market Analysis Platform von einer reinen Technical-Analysis-Tool zu einer umfassenden, KI-gestützten Entscheidungsplattform. Semi-professionelle Trader erhalten einen echten Competitive Edge durch die Kombination von vier innovativen Features:

1. **Master Investment Score (0-100)** – Kombiniert alle technischen Indikatoren zu einer klaren Kauf/Verkauf-Entscheidung
2. **AI Sentiment Analysis** – Real-time Analyse von Nachrichten, Social Media und Earnings-Calls
3. **Unusual Activity Detection** – Erkennt institutionelle Aktivitäten (Dark Pools, Options Flow)
4. **Signal Accuracy Tracking** – Historische Performance-Metriken für jedes Signal

Der Unique Selling Point ist die **Multi-Factor Decision Engine**: Anstatt Dutzende einzelner Indikatoren manuell zu interpretieren, erhält der User eine transparente, KI-gestützte Empfehlung – ähnlich wie institutionelle Trader, aber zugänglich für Retail-Investors.

**Business Impact**: Reduzierung der Entscheidungszeit von Minuten auf Sekunden, objektivierbare Entscheidungsgrundlage und messbare Portfolio-Performance vs. Benchmark.

---

## Problem Statement

**Current Situation**:
Die Plattform bietet bereits umfassende technische Indikatoren (RSI, MACD, Bollinger, etc.), Pattern Recognition und Risk-Metriken. Jedoch müssen User diese Daten manuell interpretieren und kombinieren – ein zeitraubender, subjektiver Prozess, der Erfahrung erfordert und zu Analyseparalyse führen kann.

**Proposed Solution**:
Eine zentrale Decision Engine, die alle Datenpunkte automatisiert zu einer klaren Handlungsempfehlung mit Konfidenz-Level kombiniert. User sehen sofort: **"82/100 – Strong Buy"** mit einer nachvollziehbaren Begründung.

**Business Impact**:
- **Zeitersparnis**: Entscheidungszeit von ~5 Minuten auf <10 Sekunden
- **Objektivität**: Emotionsfreie, datenbasierte Entscheidungen
- **Messbarkeit**: Portfolio Performance vs. Benchmark (S&P 500, DAX)
- **Competitive Edge**: Access zu institutionellen Insights (Dark Pools, Options Flow)

---

## Success Metrics

**Primary KPIs**:

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Portfolio Performance vs. Benchmark | +5% p.a. über S&P 500 | Tracking-Option: User loggen Trades, System vergleicht mit Benchmark |
| User Engagement (DAU/MAU Ratio) | >40% | Aktive User, die täglich ≥1 Analyse abrufen |
| Signal Accuracy (Win-Rate) | >60% | Anteil profitabler Trades basierend auf Buy/Sell-Signalen |
| Decision Time Reduction | >90% | Zeit von Symbol-Input bis zur Entscheidung (<10 Sekunden) |

**Validation**:
- Portfolio Performance via voluntary User-Tracking (Opt-in)
- A/B-Testing: User mit vs. ohne Decision Engine
- Quartalsweise Analyse der Signal Accuracy

---

## User Personas

### Primary: Alex (Semi-Professional Trader)

**Role**: Trading-Enthusiast mit 2-5 Jahren Erfahrung, handelt nebenberuflich oder als kleiner Side-Income

**Goals**:
- Systematische, datenbasierte Entscheidungen treffen
- Emotionen aus dem Trading herausnehmen
- Zeit sparen bei der Analyse (hat Hauptjob oder Familie)
- Einen Edge gegenüber "emotionalen" Retail-Tradern haben

**Pain Points**:
- **Entscheidungslähmung**: Zu viele Indikatoren, unklar, was gewichtet werden soll
- **Zeitmangel**: Kann nicht stundenlang Charts analysieren
- **Fehlende Transparenz**: Warum sagen verschiedene Tools Unterschiedliches?
- **Kein Track Record**: Weiß nicht, wie gut seine Strategie wirklich performs

**Technical Level**: Advanced – versteht technische Analyse, will aber keine eigene Quant-Strategie bauen

**Usage Frequency**: 3-7x pro Woche, abends oder am Wochenende

---

## User Stories & Acceptance Criteria

### Story 1: Master Investment Score

**As a** Semi-Professional Trader
**I want to** einen klaren Investment Score (0-100) sehen, der alle Indikatoren kombiniert
**So that** ich schnell eine fundierte Kauf/Verkauf-Entscheidung treffen kann

**Acceptance Criteria**:
- [ ] User gibt Symbol ein → sieht Score innerhalb 5 Sekunden
- [ ] Score ist 0-100 mit Farbcodierung (0-30 Rot/Strong Sell, 31-70 Gelb/Hold, 71-100 Grün/Strong Buy)
- [ ] Score zeigt Konfidenz-Level (Hoch/Mittel/Niedrig) basierend auf Datenqualität
- [ ] Detail-Ansicht zeigt Gewichtung der Top-3-Faktoren (z.B. "RSI: 25%, MACD: 20%, Sentiment: 15%")
- [ ] Score ist reproduzierbar: Gleiche Eingabe = gleicher Score (innerhalb Cache-Zeit)

### Story 2: AI Sentiment Analysis

**As a** Semi-Professional Trader
**I want to** Real-time Sentiment aus Nachrichten und Social Media sehen
**So that** ich Hype vs. Fundamentalen Daten erkennen kann

**Acceptance Criteria**:
- [ ] Sentiment-Score (-100 bis +100) mit Label (Extremely Bullish bis Extremely Bearish)
- [ ] Anzeige der Top-3-Nachrichten mit Sentiment-Beitrag
- [ ] Social Media Buzz-Score (Reddit/Twitter) mit Trend-Indikator (Steigend/Fallend)
- [ ] Sentiment vs. Preis-Performance: Korrelation visualisieren ("Sentiment sagt +, Preis fällt - Opportunity?")
- [ ] Maximal 5 Sekunden Ladezeit

### Story 3: Unusual Activity Detection

**As a** Semi-Professional Trader
**I want to** sehen, was institutionelle Trader tun (Dark Pools, Options Flow)
**So that** ich Smart Money folgen kann

**Acceptance Criteria**:
- [ ] Alert bei ungewöhnlicher Volumen-Spitze (>3x Durchschnitt)
- [ ] Options Flow Indicator: Put/Call Ratio unusual, Large OI Changes
- [ ] Dark Pool Activity Indicator (falls via yfinance verfügbar)
- [ ] Time-Since-Last-Activity: "Letzte ungewöhnliche Aktivität vor 2 Stunden"
- [ ] Confidence-Level basierend auf Datenverfügbarkeit

### Story 4: Signal Accuracy Tracking

**As a** Semi-Professional Trader
**I want to** sehen, wie准确 vergangene Signale waren
**So that** ich dem System vertrauen kann

**Acceptance Criteria**:
- [ ] Win-Rate Anzeige (z.B. "65% der Strong Buy Signals waren profitabel in 6 Monaten")
- [ ] Performance nach Zeitraum: 1 Woche, 1 Monat, 3 Monate, 6 Monate
- [ ] Filter nach Signal-Typ (Strong Buy, Buy, Hold, Sell, Strong Sell)
- [ ] Vergleich mit Buy & Hold S&P 500
- [ ] Optional: User kann eigene Trades loggen für personalisierte Accuracy

### Story 5: Multi-Tab Dashboard

**As a** Semi-Professional Trader
**I want to** verschiedene Analyse-Aspekte in Tabs sehen
**So that** ich gezielt tief eintauchen kann, ohne überfordert zu sein

**Acceptance Criteria**:
- [ ] 4 Tabs: "Overview" (Score Summary), "Technical" (Indikatoren), "Sentiment" (News/Social), "Activity" (Unusual)
- [ ] Overview Tab zeigt alle 4 Scores auf einen Blick mit Master-Score prominent
- [ ] Tab-Wechsel ohne Neuladen (Client-side State)
- [ ] Jeder Tab hat "Deep Dive" Button für Details
- [ ] Mobile-optimiert: Tabs scrollbar horizontally

---

## Functional Requirements

### Core Features

#### Feature 1: Master Investment Score Engine

**Description**:
Ein gewichteter Algorithmus, der alle bestehenden technischen Indikatoren, Risk-Metriken und Patterns zu einem Score (0-100) kombiniert.

**User Flow**:
1. User gibt Symbol ein (z.B. "AAPL")
2. System ruft alle Indikatoren ab (existing: RSI, MACD, Bollinger, etc.)
3. Algorithmus berechnet Score basierend auf Gewichtung:
   - Short-term Signals (30%): RSI, Stochastic, Williams %R
   - Medium-term Signals (30%): MACD, SMA/EMA Crossovers
   - Long-term Signals (20%): Trend Patterns, Support/Resistance
   - Risk Metrics (20%): Volatility, Drawdown, Liquidity
4. User sieht Score + Empfehlung + Top-3-Faktoren

**Edge Cases**:
- **Unzureichende Daten**: Wenn <50% der Indikatoren verfügbar → Score mit "Low Confidence" label
- **Widersprüchliche Signale**: RSI says Overbought, MACD says Bullish → Zeigt beizw. in Detail-Ansicht
- **Neue IPOs**: Weniger als 30 Tage Daten → "Insufficient History" warning

**Error Handling**:
- yfinance API timeout → Fallback auf Cache-Daten (max 2 Stunden alt)
- Berechnungsfehler → Loggen, User sieht "Analysis temporarily unavailable"

#### Feature 2: AI Sentiment Analysis Engine

**Description**:
KI-gestützte Analyse von Nachrichten, Social Media und Earnings-Transcripts mit Sentiment-Score (-100 bis +100).

**User Flow**:
1. System scrapes Datenquellen parallel:
   - Yahoo Finance News (RSS)
   - Seeking Alpha (Scraping)
   - Twitter/X (Free API, Rate Limit beachten)
   - Reddit (WallStreetBets via API)
2. KI (via LangChain + gewählter Provider) analysiert Text:
   - Sentiment pro Artikel/Post (Positive/Negative/Neutral)
   - Gewichteter Durchschnitt (Neuere Nachrichten höher gewichtet)
   - Entity Extraction: Welche Firmen werden erwähnt?
3. User sieht Sentiment-Score + Top-3-Nachrichten + Trend

**Edge Cases**:
- **No News Available**: Symbol ist zu klein/unbekannt → "No recent news found" mit fallback auf Sektor-News
- **Spam/Bot Content**: Reddit/Twitter Filter für Low-Quality Content (<10 Karma oder verified Accounts)
- **Conflicting Sentiment**: News bullish, Social bearish → Zeigt beide getrennt

**Error Handling**:
- Scraping blocked → Fallback auf yfinance News-integriert
- Rate Limit hit → Queue mit Retry, User sieht "Updating..."
- AI provider unavailable → Cache (max 24 Stunden) oder "Sentiment unavailable"

#### Feature 3: Unusual Activity Detector

**Description**:
Erkennt abnormale Handelsaktivitäten, die auf institutionelle Order hinweisen (Dark Pools, Large Options Orders, Volume Spikes).

**User Flow**:
1. System berechnet statistische Baselines aus 30-Tage-Historie:
   - Durchschnittsvolumen pro Stunde
   - Typische Put/Call Ratio
   - Standardabweichung der Preisbewegung
2. Real-time Check: Aktuelle Daten vs. Baseline
3. Wenn >3 Standardabweichungen → Trigger Alert
4. User sieht Alert in "Activity" Tab mit Erklärung

**Edge Cases**:
- **Earnings Day**: Volumen ist ohnehin hoch → Adjusted Baseline (historische Earnings-Daten)
- **After-Hours Trading**: Weniger Volumen → Adjusted Threshold
- **Splits/Dividends**: Volumen-Anomalie erklärt → Kein Alert

**Error Handling**:
- yfinance keine Volume-Daten → "Volume data not available"
- Berechnungsfehler → Loggen, User sieht keine falschen Alerts

#### Feature 4: Signal Accuracy Tracker

**Description**:
Historische Performance-Analyse aller generierten Signale mit Win-Rate, Average Return und Benchmark-Vergleich.

**User Flow**:
1. System speichert alle generierten Signale in DB mit Timestamp
2. Nightly Job berechnet Performance pro Signal:
   - Preis nach X Tagen (1, 7, 30)
   - Profitable? (Ja/Nein)
   - Return % vs. Buy & Hold S&P 500
3. User sieht Accuracy-Dashboard mit Filtern

**Edge Cases**:
- **Neues Signal**: <7 Tage alt → "Performance pending"
- **Market Crash**: Alle Signale schlecht → Context-Berichtigung
- **Survivorship Bias**: Nur Signale zeigen, die noch aktiv sind → Alle zeigen, inkl. Delisted

**Error Handling**:
- Historische Daten nicht verfügbar → "No historical data yet"
- Berechnung fehlerhaft → Fallback auf manueller Input

### Out of Scope (Phase 1)

- Kein automatisierter Trade Execution (User entscheidet selbst)
- Kein Backtesting-Interface (nur Accuracy Tracking)
- Keine Portfolio-Management-Features (nur einzelne Symbole)
- Keine Mobile App (nur responsive Web)
- Keine Multi-Asset-Klasse (nur Stocks, keine Crypto/FX)

---

## Technical Constraints

### Performance

- **Maximale Ladezeit**: 5 Sekunden für vollständige Analyse (Master Score + Sentiment + Activity)
- **API Response**: <2 Sekunden für Score-only, <5 Sekunden für Full Analysis
- **Caching**:
  - Master Score: 2 Minuten (existing)
  - Sentiment: 10 Minuten (new)
  - Unusual Activity: 1 Minute (real-time)
  - Accuracy Data: 24 Stunden (täglich aktualisiert)
- **Scalability**: Support 100 konkurrierende Anfragen ohne Degradation

### Security

- **Rate Limiting**: Max 100 Anfragen/User/Minute (existing SlowAPI)
- **Data Scraping Compliance**: Respect robots.txt, User-Agent header
- **User Privacy**: Opt-in für Portfolio Tracking, keine Finanzberatung
- **AI Key Security**: Bestehende Verschlüsselung via APITokenService

### Integration

**Datenquellen (Phase 1)**:
- **yfinance**: Market Data, Historical Data, News-integriert (existing)
- **Yahoo Finance RSS**: News Feed (new)
- **Seeking Alpha**: Scraping (new, respects robots.txt)
- **Twitter/X Free API**: Social Media Sentiment (new, Rate Limit: 450 Tweets/15min)
- **Reddit API**: r/wallstreetbets (new, Rate Limit: 60 requests/minute)

**AI Provider**: LangChain mit bestehenden Providern (OpenAI, DeepSeek, Anthropic, etc.)

### Technology Stack

**Backend** (existing):
- FastAPI, SQLAlchemy, Pydantic v2
- LangChain für KI-Integration
- yfinance, pandas-ta für technische Analyse
- BeautifulSoup4 für Scraping
- HTTPX/API-Clients für Twitter/Reddit

**Frontend** (existing):
- Vue 3 + Composition API + TypeScript
- Shadcn/Vue Components (Card, Badge, Progress, Tabs, Alert)
- ECharts für Visualisierungen
- TailwindCSS für Styling

**Database**:
- SQLite (Dev), PostgreSQL (Production)
- New Tables: `sentiment_analysis`, `unusual_activity`, `signal_performance`

**Infrastructure**:
- Railway Deployment (existing)
- Celery/Background Tasks für nightly Accuracy-Jobs (optional in Phase 1)

---

## MVP Scope & Phasing

### Phase 1: MVP (Required for Initial Launch)

**Core Features**:
- [ ] Master Investment Score Engine (gewichteter Algorithmus aller Indikatoren)
- [ ] AI Sentiment Analysis (Yahoo Finance News + einfache Keyword-Analyse)
- [ ] Unusual Activity Detection (Volume Spikes, Basics)
- [ ] Signal Accuracy Dashboard (historische Win-Rate)
- [ ] Multi-Tab UI (Overview, Technical, Sentiment, Activity)

**Data Sources**:
- yfinance (Market Data + News-integriert)
- Yahoo Finance RSS
- Basic Sentiment via LangChain (optional User AI Key)

**MVP Definition**:
User gibt Symbol ein → sieht Master Score 0-100 mit Buy/Sell/Hold + Tabs für Details innerhalb 5 Sekunden.

### Phase 2: Enhanced Sentiment (Post-Launch, 2-3 Monate)

**Features**:
- [ ] Twitter/X API Integration (Real-time Social Sentiment)
- [ ] Reddit API Integration (WallStreetBets Sentiment)
- [ ] Seeking Alpha Scraping (Premium Analysis)
- [ ] Sentiment vs. Price Correlation Chart
- [ ] Earnings-Call Transcript Analysis (via KI)

### Phase 3: Advanced Activity (Post-Launch, 3-4 Monate)

**Features**:
- [ ] Dark Pool Activity Detection (via alternative Datenquelle)
- [ ] Unusual Options Flow (Put/Call Ratio, Large OI Changes)
- [ ] Insider Trading Patterns (SEC Form 4 Analysis)
- [ ] Institutional Ownership Changes

### Phase 4: Portfolio & Automation (Future, 6+ Monate)

**Features**:
- [ ] Portfolio Tracker mit Auto-Import (Broker API)
- [ ] Personalisierte Accuracy pro User
- [ ] Alerts/Notifications bei Score-Changes
- [ ] Backtesting-Interface für eigene Strategien
- [ ] Mobile App (React Native)

### Future Considerations

- **Multi-Asset**: Krypto, ETFs, Options
- **Social Features**: Community Scores, Leaderboards
- **API Access**: Für Quant-Trader mit eigenen Strategien
- **White Label**: B2B-Lizenz für andere Plattformen

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| **API Rate Limits** (Twitter/Reddit) | Hoch | Mittel | 1) Aggressive Caching (10 min), 2) Queue System, 3) Paid API Upgrade wenn nötig |
| **Legal Issues** (Scraping) | Mittel | Hoch | 1) Respect robots.txt, 2) Terms of Service Review, 3) Fallback auf RSS/APIs |
| **AI Hallucination** (Falsche Sentiment) | Mittel | Mittel | 1) Confidence Score anzeigen, 2) Multiple Sources vergleichen, 3) Human-in-the-Loop Feedback |
| **Performance Bottleneck** (>5s Ladezeit) | Mittel | Mittel | 1) Parallel Scraping, 2) Redis Cache, 3) Async Backend, 4) Progressive Loading UI |
| **User Expectation Mismatch** (Verluste) | Hoch | Hoch | 1) Disclaimer: Keine Finanzberatung, 2) Accuracy Tracking zeigt Realität, 3) Risk Management Education |
| **Data Quality** (yfinance Fehler) | Niedrig | Mittel | 1) Multi-Source Validation, 2) Fallback auf Cache, 3) Error Logging |

---

## Dependencies & Blockers

**Dependencies**:
- **yfinance Stability**: API kann ändern ohne Notice → Monitoring nötig
- **LangChain Provider**: User muss AI Key konfigurieren → Onboarding Flow
- **Twitter/X Free API**: Rate Limitierung → Queue System
- **Frontend Shadcn Components**: Tabs, Card, Badge müssen installiert sein → `npx shadcn-vue add`

**Known Blockers**:
- **Seeking Alpha Anti-Scraping**: Möglicher IP-Ban → Alternative: Alpha Vantage News API
- **Reddit API Changes**: Reddit ändert oft API-Policies → Backup: Subreddit-Scraping mit PRAW
- **Celery Setup**: Für nightly Jobs notwendig → Alternativ: Cron Job auf Railway

**Resolution Plan**:
1. Week 1: Dependencies checken (Twitter API Test, Reddit Auth)
2. Week 2: Anti-Scraping Maßnahmen (Proxies, Delays)
3. Week 3: Celery/Background Task Setup

---

## Appendix

### Glossary

- **Master Score**: Gewichteter Durchschnitt aller technischen Indikatoren (0-100)
- **Sentiment Score**: KI-basierter Score aus News/Social (-100 bis +100)
- **Unusual Activity**: Abnormale Handelsaktivitäten, die auf institutionelle Orders hindeuten
- **Win-Rate**: Anteil profitabler Signale in historischer Analyse
- **Dark Pool**: Privater Handelsplatz für institutionelle Investor, nicht öffentlich sichtbar

### References

- **yfinance Documentation**: https://github.com/ranaroussi/yfinance
- **LangChain Documentation**: https://python.langchain.com/
- **Twitter API Docs**: https://developer.twitter.com/en/docs
- **Reddit API Docs**: https://www.reddit.com/dev/api/
- **Shadcn/Vue Components**: https://www.shadcn-vue.com/

### Technical Implementation Notes

**Gewichtung Master Score (Beispiel)**:
```python
SCORE_WEIGHTS = {
    "short_term": 0.30,    # RSI, Stochastic, Williams %R
    "medium_term": 0.30,   # MACD, SMA/EMA
    "long_term": 0.20,     # Trends, Support/Resistance
    "risk": 0.20           # Volatility, Drawdown
}
```

**Sentiment KI Prompt (LangChain)**:
```
"Analysiere den folgenden Finanznachrichten-Text auf Sentiment.
Gib zurück: Score von -100 (extrem negativ) bis +100 (extrem positiv),
sowie eine 1-Sentence-Begründung. Text: {news_text}"
```

**Unusual Activity Threshold**:
```python
VOLUME_THRESHOLD = 3.0  # 3x Standardabweichung
PUT_CALL_THRESHOLD = 1.5  # 50% über normaler Ratio
```

---

*This PRD was created through interactive requirements gathering with quality scoring to ensure comprehensive coverage of business, functional, UX, and technical dimensions.*

**Next Steps**:
1. Review mit Stakeholder
2. Technical Architecture Design (Backend Endpoints, Frontend Components)
3. UI/UX Mockups für Multi-Tab Dashboard
4. Implementation Sprint 1: Master Score Engine
