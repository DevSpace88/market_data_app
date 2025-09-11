import json
import time
from typing import Optional, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class MemoryCache:
    """
    Simple in-memory cache for hot stocks data
    """
    def __init__(self):
        self._cache = {}
        self._timestamps = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key not in self._cache:
            return None
        
        # Check if expired (15 minutes = 900 seconds)
        if time.time() - self._timestamps[key] > 900:
            del self._cache[key]
            del self._timestamps[key]
            return None
        
        return self._cache[key]
    
    def set(self, key: str, value: Any) -> None:
        """Set value in cache with current timestamp"""
        self._cache[key] = value
        self._timestamps[key] = time.time()
        logger.info(f"Cached data for key: {key}")
    
    def clear(self, key: Optional[str] = None) -> None:
        """Clear cache entry or all cache"""
        if key:
            self._cache.pop(key, None)
            self._timestamps.pop(key, None)
            logger.info(f"Cleared cache for key: {key}")
        else:
            self._cache.clear()
            self._timestamps.clear()
            logger.info("Cleared all cache")
    
    def is_cached(self, key: str) -> bool:
        """Check if key exists and is not expired"""
        if key not in self._cache:
            return False
        
        # Check if expired
        if time.time() - self._timestamps[key] > 900:
            del self._cache[key]
            del self._timestamps[key]
            return False
        
        return True
    
    def get_cache_info(self) -> dict:
        """Get cache statistics"""
        current_time = time.time()
        valid_entries = 0
        expired_entries = 0
        
        for key, timestamp in self._timestamps.items():
            if current_time - timestamp > 900:
                expired_entries += 1
            else:
                valid_entries += 1
        
        return {
            "total_entries": len(self._cache),
            "valid_entries": valid_entries,
            "expired_entries": expired_entries,
            "cache_hit_ratio": "N/A"  # Would need hit/miss tracking
        }

# Global cache instance
cache = MemoryCache()
