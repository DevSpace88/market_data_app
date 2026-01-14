"""
Sentiment Analysis Service

Analyzes news and social media sentiment using AI and keyword analysis.
"""
import logging
import feedparser
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class SentimentAnalysisService:
    """
    Analyzes sentiment from multiple sources:
    - Yahoo Finance News (RSS)
    - Social media (Twitter/X, Reddit) - Phase 2
    - Seeking Alpha - Phase 2

    Returns sentiment score (-100 to +100) with detailed breakdown.
    """

    def __init__(self, db: Session, ai_service=None):
        self.db = db
        self.ai_service = ai_service
        self.logger = logger
        self.cache = {}
        self.cache_duration = timedelta(minutes=10)

    async def analyze_sentiment(
        self,
        symbol: str,
        use_ai: bool = False
    ) -> Dict[str, Any]:
        """
        Perform comprehensive sentiment analysis.

        Args:
            symbol: Stock symbol
            use_ai: Whether to use AI for deeper analysis (requires user AI key)

        Returns:
            Dict with sentiment_score, breakdown, top_headlines, etc.
        """
        try:
            # Check cache
            cache_key = f"sentiment_{symbol}"
            if cache_key in self.cache:
                cached = self.cache[cache_key]
                if datetime.now() - cached['timestamp'] < self.cache_duration:
                    return cached['data']

            # Fetch news from multiple sources
            news_data = await self._fetch_news(symbol)

            if not news_data:
                return self._get_no_data_response(symbol)

            # Analyze sentiment
            sentiment_results = self._analyze_news_sentiment(news_data)

            # Calculate overall sentiment
            overall_sentiment = self._calculate_overall_sentiment(sentiment_results)

            # Get top headlines
            top_headlines = self._get_top_headlines(news_data, sentiment_results)

            # Prepare response
            response = {
                "symbol": symbol,
                "sentiment_score": overall_sentiment["score"],
                "sentiment_label": overall_sentiment["label"],
                "confidence": overall_sentiment["confidence"],
                "breakdown": {
                    "news": {
                        "score": sentiment_results.get("average_score", 0),
                        "count": len(news_data),
                        "positive": sentiment_results.get("positive_count", 0),
                        "negative": sentiment_results.get("negative_count", 0),
                        "neutral": sentiment_results.get("neutral_count", 0),
                    }
                },
                "top_headlines": top_headlines,
                "social_buzz": {
                    "score": 0,  # Phase 2
                    "trend": "STABLE",  # Phase 2
                    "mentions_24h": 0  # Phase 2
                },
                "price_correlation": None,  # Phase 2: Compare sentiment with price movement
                "data_sources": "Yahoo Finance RSS",
                "timestamp": datetime.now().isoformat()
            }

            # AI-enhanced analysis (if requested and available)
            if use_ai and self.ai_service:
                try:
                    ai_insights = await self._get_ai_sentiment_insights(symbol, news_data)
                    response["ai_insights"] = ai_insights
                except Exception as e:
                    self.logger.warning(f"AI sentiment analysis failed: {e}")

            # Cache response
            self.cache[cache_key] = {
                'data': response,
                'timestamp': datetime.now()
            }

            return response

        except Exception as e:
            self.logger.error(f"Error in sentiment analysis: {e}")
            return self._get_error_response(symbol)

    async def _fetch_news(self, symbol: str) -> List[Dict[str, Any]]:
        """Fetch news from multiple sources with fallback"""
        news_items = []

        # Method 1: Try yfinance news (most reliable)
        try:
            import yfinance as yf
            ticker = yf.Ticker(symbol)

            # yfinance returns news as a list of dicts with NEW structure:
            # [{'id': ..., 'content': {'title': ..., 'summary': ..., 'canonicalUrl': ..., 'pubDate': ...}}]
            yf_news = ticker.news

            if yf_news:
                for item in yf_news[:10]:  # Limit to 10 most recent
                    content = item.get('content', {})
                    if not content:
                        continue

                    # Extract title from nested content structure
                    title_text = content.get('title', '')

                    # Extract link from canonicalUrl or clickThroughUrl
                    canonical_url = content.get('canonicalUrl', {})
                    click_url = content.get('clickThroughUrl', {})
                    link_url = canonical_url.get('url', '') if isinstance(canonical_url, dict) else ''
                    if not link_url:
                        link_url = click_url.get('url', '') if isinstance(click_url, dict) else ''

                    # Extract published date
                    published = content.get('pubDate', '')

                    # Extract summary
                    summary = content.get('summary', '')[:500]  # Limit summary length

                    if title_text:  # Only add if we have a title
                        news_items.append({
                            "title": title_text,
                            "summary": summary,
                            "link": link_url,
                            "published": published,
                            "source": "Yahoo Finance"
                        })

                if news_items:
                    self.logger.info(f"Fetched {len(news_items)} news items from yfinance for {symbol}")
                    return news_items

        except Exception as e:
            self.logger.warning(f"yfinance news fetch failed for {symbol}: {e}")
            import traceback
            self.logger.warning(traceback.format_exc())

        # Method 2: Fallback to RSS feedparser
        try:
            rss_url = f"https://query1.finance.yahoo.com/rss?s={symbol}"
            feed = feedparser.parse(rss_url)

            for entry in feed.entries[:10]:
                news_items.append({
                    "title": entry.get('title', ''),
                    "summary": entry.get('summary', entry.get('description', '')),
                    "link": entry.get('link', ''),
                    "published": entry.get('published', ''),
                    "source": "Yahoo Finance RSS"
                })

            if news_items:
                self.logger.info(f"Fetched {len(news_items)} news items from RSS for {symbol}")
                return news_items

        except Exception as e:
            self.logger.warning(f"RSS fetch failed for {symbol}: {e}")

        # Method 3: Return mock data for testing (if nothing works)
        self.logger.warning(f"No news found for {symbol}, using placeholder data")
        return [{
            "title": f"No recent news available for {symbol}",
            "summary": "News service temporarily unavailable. Try again later.",
            "link": f"https://finance.yahoo.com/quote/{symbol}",
            "published": datetime.now().isoformat(),
            "source": "System"
        }]

    def _analyze_news_sentiment(self, news_data: List[Dict]) -> Dict[str, Any]:
        """Analyze sentiment using keyword-based approach"""
        if not news_data:
            return {"average_score": 0, "positive_count": 0, "negative_count": 0, "neutral_count": 0}

        # Bullish and bearish keywords
        bullish_keywords = [
            'surge', 'rally', 'gain', 'profit', 'growth', 'bullish', 'upgrade',
            'beat', 'exceed', 'strong', 'record', 'soar', 'jump', 'rise',
            'outperform', 'buy', 'target', 'momentum', 'breakout', 'rally',
            'positive', 'up', 'higher', 'boom', 'bull', 'breakthrough'
        ]

        bearish_keywords = [
            'fall', 'drop', 'decline', 'loss', 'bearish', 'downgrade',
            'miss', 'weak', 'plunge', 'slump', 'collapse', 'sell', 'risk',
            'concern', 'warning', 'cut', 'layoff', 'struggle', 'uncertain',
            'negative', 'down', 'lower', 'crash', 'bear', 'fear'
        ]

        total_score = 0
        positive_count = 0
        negative_count = 0
        neutral_count = 0

        for article in news_data:
            # Title is now a string directly from the new yfinance structure
            title = article.get('title', '')
            title = str(title).lower() if title else ''

            summary = article.get('summary', '')
            summary = str(summary).lower() if summary else ''

            text = f"{title} {summary}"

            # Count bullish and bearish mentions
            bullish_count = sum(1 for word in bullish_keywords if word in text)
            bearish_count = sum(1 for word in bearish_keywords if word in text)

            # Calculate sentiment score for this article (-100 to +100)
            total_mentions = bullish_count + bearish_count
            if total_mentions > 0:
                article_score = ((bullish_count - bearish_count) / total_mentions) * 100
            else:
                article_score = 0
                neutral_count += 1

            total_score += article_score

            if article_score > 20:
                positive_count += 1
            elif article_score < -20:
                negative_count += 1
            else:
                neutral_count += 1

        average_score = total_score / len(news_data) if news_data else 0

        return {
            "average_score": average_score,
            "positive_count": positive_count,
            "negative_count": negative_count,
            "neutral_count": neutral_count
        }

    def _calculate_overall_sentiment(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall sentiment score and label"""
        score = results.get("average_score", 0)

        # Determine label
        if score >= 60:
            label = "Extremely Bullish"
            confidence = "HIGH" if results.get("positive_count", 0) > 2 else "MEDIUM"
        elif score >= 30:
            label = "Bullish"
            confidence = "HIGH" if results.get("positive_count", 0) > 2 else "MEDIUM"
        elif score >= -30:
            label = "Neutral"
            confidence = "HIGH"
        elif score >= -60:
            label = "Bearish"
            confidence = "HIGH" if results.get("negative_count", 0) > 2 else "MEDIUM"
        else:
            label = "Extremely Bearish"
            confidence = "HIGH" if results.get("negative_count", 0) > 2 else "MEDIUM"

        return {
            "score": round(score, 2),
            "label": label,
            "confidence": confidence
        }

    def _get_top_headlines(
        self,
        news_data: List[Dict],
        sentiment_results: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Get top 3 headlines with sentiment contribution"""
        if not news_data:
            return []

        headlines = []
        for item in news_data[:3]:
            # Title is now a string directly from the new yfinance structure
            title = item.get('title', '')
            title = str(title)[:100] if title else ''  # Truncate long titles

            # Determine sentiment contribution based on keywords
            title_lower = title.lower()
            if any(word in title_lower for word in ['surge', 'rally', 'gain', 'profit', 'growth', 'bullish', 'upgrade', 'beat', 'record', 'soar']):
                sentiment = "Positive"
            elif any(word in title_lower for word in ['fall', 'drop', 'decline', 'loss', 'bearish', 'downgrade', 'miss', 'plunge', 'slump']):
                sentiment = "Negative"
            else:
                sentiment = "Neutral"

            headlines.append({
                "title": title,
                "sentiment_contribution": sentiment,
                "timestamp": item.get('published', ''),
                "link": item.get('link', '')
            })

        return headlines

    async def _get_ai_sentiment_insights(
        self,
        symbol: str,
        news_data: List[Dict]
    ) -> Dict[str, Any]:
        """Use AI to generate deeper sentiment insights"""
        if not self.ai_service or not news_data:
            return {}

        try:
            # Prepare news summary
            news_summary = "\n".join([
                f"- {item.get('title', '')}: {item.get('summary', '')[:200]}"
                for item in news_data[:5]
            ])

            prompt = f"""Analyze the sentiment for {symbol} based on these recent news headlines:

{news_summary}

Provide:
1. Overall sentiment score (-100 to +100)
2. Key themes (max 3)
3. Potential impact on stock price
4. Confidence level (HIGH/MEDIUM/LOW)

Respond in JSON format with keys: score, themes, impact, confidence"""

            # Call AI service (implementation depends on your AI service)
            # This is a placeholder - implement based on your ai_analysis_service
            return {
                "score": 0,
                "themes": [],
                "impact": "Analysis pending",
                "confidence": "LOW"
            }

        except Exception as e:
            self.logger.error(f"AI sentiment insights failed: {e}")
            return {}

    def _get_no_data_response(self, symbol: str) -> Dict[str, Any]:
        """Return response when no data is available"""
        return {
            "symbol": symbol,
            "sentiment_score": 0,
            "sentiment_label": "No Data Available",
            "confidence": "LOW",
            "breakdown": {
                "news": {"score": 0, "count": 0, "positive": 0, "negative": 0, "neutral": 0}
            },
            "top_headlines": [],
            "social_buzz": {"score": 0, "trend": "STABLE", "mentions_24h": 0},
            "price_correlation": None,
            "data_sources": "None",
            "timestamp": datetime.now().isoformat(),
            "warning": f"No recent news found for {symbol}"
        }

    def _get_error_response(self, symbol: str) -> Dict[str, Any]:
        """Return error response"""
        return {
            "symbol": symbol,
            "sentiment_score": 0,
            "sentiment_label": "Analysis Error",
            "confidence": "LOW",
            "breakdown": {
                "news": {"score": 0, "count": 0, "positive": 0, "negative": 0, "neutral": 0}
            },
            "top_headlines": [],
            "social_buzz": {"score": 0, "trend": "STABLE", "mentions_24h": 0},
            "price_correlation": None,
            "data_sources": "Error",
            "timestamp": datetime.now().isoformat(),
            "error": "Sentiment analysis temporarily unavailable"
        }
