# # from fastapi import FastAPI, HTTPException, Request
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.responses import JSONResponse
# # from datetime import datetime
# # from .api.routes import router as api_router
# # from .config import get_settings
# #
# # settings = get_settings()
# #
# # app = FastAPI(
# #     title=settings.PROJECT_NAME,
# #     version=settings.VERSION,
# #     description="Market Analysis API with real-time data and AI-powered insights"
# # )
# #
# # # CORS middleware
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=settings.cors_origins,
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )
# #
# # @app.exception_handler(HTTPException)
# # async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
# #     return JSONResponse(
# #         status_code=exc.status_code,
# #         content={
# #             "error": exc.detail,
# #             "status_code": exc.status_code,
# #             "timestamp": datetime.now().isoformat()
# #         }
# #     )
# #
# # @app.exception_handler(Exception)
# # async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
# #     return JSONResponse(
# #         status_code=500,
# #         content={
# #             "error": "Internal server error",
# #             "detail": str(exc),
# #             "status_code": 500,
# #             "timestamp": datetime.now().isoformat()
# #         }
# #     )
# #
# # app.include_router(api_router, prefix=settings.API_PREFIX)
# # # Health check endpoint
# # @app.get("/health")
# # async def health_check():
# #     return {
# #         "status": "healthy",
# #         "version": settings.VERSION
# #     }
# #
# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
#
#
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from .api.routes import router as api_router
# from .config import get_settings
# from .models.database import init_db
#
# settings = get_settings()
#
# app = FastAPI(
#     title=settings.PROJECT_NAME,
#     version=settings.VERSION,
#     description="Market Analysis API with real-time data and AI-powered insights"
# )
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.cors_origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# # Initialisiere die Datenbank beim Start
# @app.on_event("startup")
# async def startup_event():
#     init_db()
#
# app.include_router(api_router, prefix=settings.API_PREFIX)
#
# @app.get("/health")
# async def health_check():
#     return {
#         "status": "healthy",
#         "version": settings.VERSION
#     }
#
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


# main.py
import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router as api_router
from .config import get_settings
from .models.database import init_db
from .auth import get_current_admin_user

# Reduziere Debug-Logs für saubere Ausgabe
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("multipart").setLevel(logging.WARNING)

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Market Analysis API with real-time data and AI-powered insights",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Normal routes
app.include_router(api_router, prefix=settings.API_PREFIX)

# Include watchlist routes directly
from .api.routes.watchlist import router as watchlist_router
app.include_router(watchlist_router, prefix="/api/v1/watchlist", tags=["watchlist"])

# Include hot stocks routes
from .api.routes.hot_stocks import router as hot_stocks_router
app.include_router(hot_stocks_router, prefix="/api/v1/hot-stocks", tags=["hot-stocks"])

# Include AI settings routes
from .api.routes.ai_settings import router as ai_settings_router
app.include_router(ai_settings_router, prefix="/api/v1/ai-settings", tags=["ai-settings"])

# Include market analysis routes
from .api.routes.market_analysis import router as market_analysis_router
app.include_router(market_analysis_router, prefix="/api/v1/market", tags=["market-analysis"])

# Include WebSocket routes
from .api.routes.websocket import router as websocket_router
app.include_router(websocket_router, prefix="/api/v1/ws", tags=["websocket"])

# Startup Event
@app.on_event("startup")
async def startup_event():
    init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)