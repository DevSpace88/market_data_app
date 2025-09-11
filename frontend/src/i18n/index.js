import { createI18n } from 'vue-i18n'

const messages = {
  en: {
    // Navigation
    nav: {
      home: 'Home',
      dashboard: 'Dashboard',
      settings: 'Settings',
      logout: 'Logout',
      login: 'Login',
      language: 'Language'
    },
    
    // Dashboard
    dashboard: {
      title: 'Market Dashboard',
      mySymbols: 'My Symbols',
      hotStocks: 'Hot Stocks',
      addSymbol: 'Add Symbol',
      searchPlaceholder: 'Search Symbol (e.g. AAPL, GOOGL)...',
      noSymbols: 'No symbols in watchlist',
      removeFromWatchlist: 'Remove from Watchlist'
    },
    
    // Symbol Analysis
    symbolAnalysis: {
      title: 'Symbol Analysis',
      currentPrice: 'Current Price',
      priceChange: 'Price Change',
      marketCap: 'Market Cap',
      volume: 'Volume',
      technicalIndicators: 'Technical Indicators',
      tradingSignals: 'Trading Signals',
      technicalPatterns: 'Technical Patterns',
      riskMetrics: 'Risk Metrics',
      aiInsights: 'AI Market Insights',
      marketSentiment: 'Market Sentiment',
      technicalOverview: 'Technical Overview',
      keyInsights: 'Key Insights',
      supportLevels: 'Support Levels',
      resistanceLevels: 'Resistance Levels',
      riskFactors: 'Risk Factors',
      noData: 'No data available',
      loading: 'Loading...'
    },
    
    // Technical Indicators
    indicators: {
      rsi: 'RSI (14)',
      macd: 'MACD',
      sma20: 'SMA (20)',
      sma50: 'SMA (50)',
      sma200: 'SMA (200)',
      ema12: 'EMA (12)',
      ema26: 'EMA (26)',
      stochastic: 'Stochastic Oscillator',
      williams: 'Williams %R',
      cci: 'Commodity Channel Index',
      adx: 'Average Directional Index',
      bollinger: 'Bollinger Bands',
      atr: 'Average True Range',
      obv: 'On-Balance Volume',
      vroc: 'Volume Rate of Change',
      adLine: 'Accumulation/Distribution Line',
      pivotPoints: 'Pivot Points',
      info: 'Technical indicators show various aspects of price movement and help with trend analysis. RSI measures overbought/oversold, MACD shows momentum, SMA/EMA are moving averages, Bollinger Bands show volatility.'
    },
    
    // Trading Signals
    signals: {
      shortTerm: 'Short-term Signals (Minutes to Hours)',
      mediumTerm: 'Medium-term Signals (Days to Weeks)',
      longTerm: 'Long-term Signals (Weeks to Months)',
      noSignals: 'No active signals',
      buy: 'Buy',
      sell: 'Sell',
      hold: 'Hold',
      strong: 'Strong',
      moderate: 'Moderate',
      weak: 'Weak',
      info: 'Trading signals are based on technical indicators and patterns. BUY = Buy recommendation, SELL = Sell recommendation, HOLD = Wait.'
    },
    
    // Patterns
    patterns: {
      candlestick: 'Candlestick Patterns',
      chart: 'Chart Patterns',
      trend: 'Trend Patterns',
      volume: 'Volume Patterns',
      supportResistance: 'Support/Resistance Patterns',
      noPatterns: 'No patterns detected',
      high: 'High',
      medium: 'Medium',
      low: 'Low'
    },
    
    // Risk Metrics
    risk: {
      overallRisk: 'Overall Risk Score',
      volatility: 'Volatility Metrics',
      drawdown: 'Drawdown Metrics',
      momentum: 'Momentum & Trend Risk',
      liquidity: 'Liquidity Metrics',
      priceAction: 'Price Action & S/R',
      veryLow: 'Very Low',
      low: 'Low',
      medium: 'Medium',
      high: 'High',
      veryHigh: 'Very High'
    },
    
    // Timeframes
    timeframes: {
      '1D': '1D',
      '1W': '1W',
      '1M': '1M',
      '3M': '3M',
      '6M': '6M',
      '1Y': '1Y',
      'YTD': 'YTD'
    },
    
    // Common
    common: {
      close: 'Close',
      open: 'Open',
      high: 'High',
      low: 'Low',
      volume: 'Volume',
      change: 'Change',
      percentage: 'Percentage',
      value: 'Value',
      info: 'Info'
    },
    
    // Patterns Info
    patterns: {
      info: 'Technical patterns show recurring price formations. Candlestick patterns show short-term sentiment changes, chart patterns show longer-term trends.'
    },
    
    // Risk Info
    risk: {
      info: 'Risk metrics help assess investment risks. Low values = less risk, high values = more risk. Important for position sizing and risk management.'
    }
    ,
    // Footer
    footer: {
      appName: 'Market Data App',
      tagline: 'Professional market data analysis with real-time data and AI insights.',
      liveData: 'Live Data',
      features: 'Features',
      realtimeCharts: 'Real-time Charts',
      aiAnalysis: 'AI Analysis',
      watchlist: 'Watchlist',
      hotStocks: 'Hot Stocks',
      dataSources: 'Data Sources',
      poweredBy: 'Powered by {provider}',
      aiVia: 'AI via {provider}',
      updatedEvery: 'Data updated every 15 minutes',
      cacheStatus: 'Cache Status',
      active: 'Active',
      rights: 'All rights reserved.',
      version: 'Version {version}'
    }
  },
  
  de: {
    // Navigation
    nav: {
      home: 'Startseite',
      dashboard: 'Dashboard',
      settings: 'Einstellungen',
      logout: 'Abmelden',
      login: 'Anmelden',
      language: 'Sprache'
    },
    
    // Dashboard
    dashboard: {
      title: 'Markt Dashboard',
      mySymbols: 'Meine Symbole',
      hotStocks: 'Hot Stocks',
      addSymbol: 'Symbol hinzufügen',
      searchPlaceholder: 'Symbol suchen (z.B. AAPL, GOOGL)...',
      noSymbols: 'Keine Symbole in der Watchlist',
      removeFromWatchlist: 'Aus Watchlist entfernen'
    },
    
    // Symbol Analysis
    symbolAnalysis: {
      title: 'Symbol Analyse',
      currentPrice: 'Aktueller Preis',
      priceChange: 'Preisänderung',
      marketCap: 'Marktkapitalisierung',
      volume: 'Volumen',
      technicalIndicators: 'Technische Indikatoren',
      tradingSignals: 'Trading Signale',
      technicalPatterns: 'Technische Muster',
      riskMetrics: 'Risiko Metriken',
      aiInsights: 'KI Markt Insights',
      marketSentiment: 'Marktstimmung',
      technicalOverview: 'Technische Übersicht',
      keyInsights: 'Wichtige Erkenntnisse',
      supportLevels: 'Unterstützungslevel',
      resistanceLevels: 'Widerstandslevel',
      riskFactors: 'Risikofaktoren',
      noData: 'Keine Daten verfügbar',
      loading: 'Lädt...'
    },
    
    // Technical Indicators
    indicators: {
      rsi: 'RSI (14)',
      macd: 'MACD',
      sma20: 'SMA (20)',
      sma50: 'SMA (50)',
      sma200: 'SMA (200)',
      ema12: 'EMA (12)',
      ema26: 'EMA (26)',
      stochastic: 'Stochastischer Oszillator',
      williams: 'Williams %R',
      cci: 'Commodity Channel Index',
      adx: 'Average Directional Index',
      bollinger: 'Bollinger Bänder',
      atr: 'Average True Range',
      obv: 'On-Balance Volume',
      vroc: 'Volume Rate of Change',
      adLine: 'Accumulation/Distribution Line',
      pivotPoints: 'Pivot Points',
      info: 'Technische Indikatoren zeigen verschiedene Aspekte der Preisbewegung und helfen bei der Trendanalyse. RSI misst Überkauft/Überverkauft, MACD zeigt Momentum, SMA/EMA sind gleitende Durchschnitte, Bollinger Bänder zeigen Volatilität.'
    },
    
    // Trading Signals
    signals: {
      shortTerm: 'Kurzfristige Signale (Minuten bis Stunden)',
      mediumTerm: 'Mittelfristige Signale (Tage bis Wochen)',
      longTerm: 'Langfristige Signale (Wochen bis Monate)',
      noSignals: 'Keine aktiven Signale',
      buy: 'Kaufen',
      sell: 'Verkaufen',
      hold: 'Halten',
      strong: 'Stark',
      moderate: 'Moderat',
      weak: 'Schwach',
      info: 'Trading-Signale basieren auf technischen Indikatoren und Mustern. BUY = Kaufempfehlung, SELL = Verkaufsempfehlung, HOLD = Warten.'
    },
    
    // Patterns
    patterns: {
      candlestick: 'Candlestick Muster',
      chart: 'Chart Muster',
      trend: 'Trend Muster',
      volume: 'Volumen Muster',
      supportResistance: 'Support/Resistance Muster',
      noPatterns: 'Keine Muster erkannt',
      high: 'Hoch',
      medium: 'Mittel',
      low: 'Niedrig'
    },
    
    // Risk Metrics
    risk: {
      overallRisk: 'Gesamtrisiko Score',
      volatility: 'Volatilitäts Metriken',
      drawdown: 'Drawdown Metriken',
      momentum: 'Momentum & Trend Risiko',
      liquidity: 'Liquiditäts Metriken',
      priceAction: 'Price Action & S/R',
      veryLow: 'Sehr Niedrig',
      low: 'Niedrig',
      medium: 'Mittel',
      high: 'Hoch',
      veryHigh: 'Sehr Hoch'
    },
    
    // Timeframes
    timeframes: {
      '1D': '1T',
      '1W': '1W',
      '1M': '1M',
      '3M': '3M',
      '6M': '6M',
      '1Y': '1J',
      'YTD': 'YTD'
    },
    
    // Common
    common: {
      close: 'Schluss',
      open: 'Eröffnung',
      high: 'Hoch',
      low: 'Tief',
      volume: 'Volumen',
      change: 'Änderung',
      percentage: 'Prozent',
      value: 'Wert',
      info: 'Info'
    },
    
    // Patterns Info
    patterns: {
      info: 'Technische Muster zeigen wiederkehrende Preisformationen. Candlestick-Muster zeigen kurzfristige Sentiment-Änderungen, Chart-Muster zeigen längerfristige Trends.'
    },
    
    // Risk Info
    risk: {
      info: 'Risikokennzahlen helfen bei der Bewertung von Investitionsrisiken. Niedrige Werte = weniger Risiko, hohe Werte = mehr Risiko. Wichtig für Position Sizing und Risikomanagement.'
    }
    ,
    // Footer
    footer: {
      appName: 'Market Data App',
      tagline: 'Professionelle Marktdatenanalyse mit Echtzeitdaten und KI-gestützten Insights.',
      liveData: 'Live Daten',
      features: 'Features',
      realtimeCharts: 'Echtzeit-Charts',
      aiAnalysis: 'KI-Analyse',
      watchlist: 'Watchlist',
      hotStocks: 'Hot Stocks',
      dataSources: 'Datenquellen',
      poweredBy: 'Powered by {provider}',
      aiVia: 'KI-Integration via {provider}',
      updatedEvery: 'Daten werden alle 15 Minuten aktualisiert',
      cacheStatus: 'Cache Status',
      active: 'Aktiv',
      rights: 'Alle Rechte vorbehalten.',
      version: 'Version {version}'
    }
  }
}

const i18n = createI18n({
  legacy: false, // Use Composition API mode
  locale: localStorage.getItem('language') || 'en', // default locale
  fallbackLocale: 'en',
  messages
})

export default i18n
