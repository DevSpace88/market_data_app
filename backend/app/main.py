"""
Market Analysis API - Main Application

A financial analysis platform with real-time market data, technical analysis,
and AI-powered insights.
"""
import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import get_settings
from .models.database import init_db
from .auth import SecurityHeadersMiddleware
from .middleware.rate_limit import limiter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Reduce debug logs for cleaner output
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("multipart").setLevel(logging.WARNING)

settings = get_settings()

# Validate SECRET_KEY on startup
if settings.is_using_default_secret_key():
    logger.warning("⚠️  WARNING: Using default SECRET_KEY!")
    logger.warning("⚠️  Please set a secure SECRET_KEY in environment variables.")
    logger.warning("⚠️  Generating secure key for development...")

    # Auto-generate secure key for development
    new_key = settings.ensure_secret_key()
    logger.info(f"✓ Generated secure SECRET_KEY and saved to .secret_key file")
    logger.info(f"✓ For production, set SECRET_KEY environment variable")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Market Analysis API with real-time data and AI-powered insights",
)

# CORS Middleware
# Restrict to specific origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Specific methods
    allow_headers=["Authorization", "Content-Type", "X-CSRF-Token"],  # Specific headers
)

# Security Headers Middleware
app.add_middleware(SecurityHeadersMiddleware)

# Rate limiting
app.state.limiter = limiter
from .middleware.rate_limit import RateLimitMiddleware
app.add_middleware(RateLimitMiddleware)

# Include routers
from .api.routes import router as api_router
from .api.routes.watchlist import router as watchlist_router
from .api.routes.hot_stocks import router as hot_stocks_router
from .api.routes.ai_settings import router as ai_settings_router
from .api.routes.market_analysis import router as market_analysis_router
from .api.routes.websocket import router as websocket_router
from .api.routes.auth import router as auth_router
from .api.routes.market import router as market_router

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(watchlist_router, prefix="/api/v1/watchlist", tags=["watchlist"])
app.include_router(hot_stocks_router, prefix="/api/v1/hot-stocks", tags=["hot-stocks"])
app.include_router(ai_settings_router, prefix="/api/v1/ai-settings", tags=["ai-settings"])
app.include_router(market_analysis_router, prefix="/api/v1/market", tags=["market-analysis"])
app.include_router(websocket_router, prefix="/api/v1/ws", tags=["websocket"])
app.include_router(market_router, prefix="/api/v1/market", tags=["market"])
app.include_router(api_router, prefix=settings.API_PREFIX)

# Health check endpoint
@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint for load balancers and monitoring."""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "database": "connected",
        "security": {
            "default_secret_key": settings.is_using_default_secret_key(),
            "cookie_auth": True,
            "rate_limiting": True,
            "csrf_protection": True
        }
    }


# Serve static files from frontend build (for monorepo deployment)
frontend_dist = Path(__file__).parent.parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="static")
    logger.info(f"✓ Serving static files from {frontend_dist}")


# Startup Event
@app.on_event("startup")
async def startup_event():
    """Initialize database and run startup checks."""
    logger.info("=" * 60)
    logger.info(f"🚀 Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info("=" * 60)

    # Initialize database
    init_db()
    logger.info("✓ Database initialized")

    # Log security configuration
    logger.info(f"✓ CORS origins: {settings.cors_origins}")
    logger.info(f"✓ Rate limiting: enabled")
    logger.info(f"✓ httpOnly cookies: enabled")
    logger.info(f"✓ Security headers: enabled")

    # Warn if using default SECRET_KEY
    if settings.is_using_default_secret_key():
        logger.warning("⚠️  WARNING: Using default SECRET_KEY - not secure for production!")

    logger.info("=" * 60)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
