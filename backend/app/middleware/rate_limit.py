"""
Rate limiting middleware using slowapi.

Provides IP-based and user-based rate limiting for API endpoints.
"""
from typing import Callable
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging

logger = logging.getLogger(__name__)

# Create limiter instance
# In development, we use IP-based limiting
# In production, you can use Redis backend with: storage_uri="redis://localhost:6379"
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],  # No default limit, set per endpoint
    storage_uri="memory://",  # In-memory storage for development
    enabled=True
)


def get_user_id_from_request(request: Request) -> str:
    """
    Get user identifier from request for rate limiting.

    Falls back to IP address if user is not authenticated.
    """
    # Try to get user from request state (set by auth middleware)
    if hasattr(request.state, "user") and request.state.user:
        return f"user:{request.state.user.username}"

    # Fall back to IP address
    return f"ip:{get_remote_address(request)}"


# Rate limit configurations
RATE_LIMITS = {
    # Auth endpoints (IP-based)
    "auth_login": "5/minute",       # 5 login attempts per minute per IP
    "auth_register": "3/hour",      # 3 registrations per hour per IP

    # General API (user-based if authenticated, IP-based otherwise)
    "api_general": "100/minute",    # 100 requests per minute

    # Market data endpoints (more restrictive due to external API calls)
    "market_data": "60/minute",     # 60 requests per minute

    # AI analysis (very restrictive due to API costs)
    "ai_analysis": "10/minute",     # 10 AI analyses per minute

    # Watchlist operations
    "watchlist": "30/minute",       # 30 watchlist operations per minute
}


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle rate limit errors and add rate limit headers.
    """

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except RateLimitExceeded as e:
            logger.warning(f"Rate limit exceeded for {get_remote_address(request)}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Rate limit exceeded",
                    "retry_after": str(e.retry_after) if hasattr(e, 'retry_after') else "60"
                },
                headers={
                    "Retry-After": str(getattr(e, 'retry_after', 60)),
                    "X-RateLimit-Limit": str(getattr(e, 'limit', 'unknown')),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(getattr(e, 'reset', 'unknown')),
                }
            )


def rate_limit(limit_value: str):
    """
    Decorator to apply rate limit to an endpoint.

    Args:
        limit_value: Rate limit string (e.g., "5/minute", "100/hour")

    Usage:
        @router.get("/api/endpoint")
        @rate_limit("10/minute")
        async def endpoint():
            ...
    """
    def decorator(func: Callable):
        return limiter.limit(limit_value)(func)
    return decorator


# Convenience decorators for common rate limits
def auth_rate_limit(func: Callable) -> Callable:
    """Rate limit for auth endpoints (5/minute)."""
    return limiter.limit(RATE_LIMITS["auth_login"])(func)


def register_rate_limit(func: Callable) -> Callable:
    """Rate limit for registration (3/hour)."""
    return limiter.limit(RATE_LIMITS["auth_register"])(func)


def api_rate_limit(func: Callable) -> Callable:
    """Rate limit for general API endpoints (100/minute)."""
    return limiter.limit(RATE_LIMITS["api_general"])(func)


def market_rate_limit(func: Callable) -> Callable:
    """Rate limit for market data endpoints (60/minute)."""
    return limiter.limit(RATE_LIMITS["market_data"])(func)


def ai_rate_limit(func: Callable) -> Callable:
    """Rate limit for AI analysis (10/minute)."""
    return limiter.limit(RATE_LIMITS["ai_analysis"])(func)


def watchlist_rate_limit(func: Callable) -> Callable:
    """Rate limit for watchlist operations (30/minute)."""
    return limiter.limit(RATE_LIMITS["watchlist"])(func)
