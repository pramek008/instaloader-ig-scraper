from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler
import logging
import time
from datetime import datetime

from app.routes import router
from app.exceptions import InstagramAPIException
from app.models import ErrorResponse

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Instagram Scraper API",
    description="""
    API untuk scraping data Instagram menggunakan Instaloader.
    
    ## Features
    
    * **Profile Data** - Mendapatkan informasi profil pengguna
    * **Posts** - Mengambil post dan media dari pengguna
    * **Stories & Highlights** - Akses stories dan highlights (terbatas)
    * **Comments** - Mengambil komentar dari post
    * **Analytics** - Analisis engagement dan statistik
    * **Search** - Pencarian profil pengguna
    * **Hashtags** - Informasi tentang hashtag
    
    ## Rate Limits
    
    API ini menggunakan rate limiting untuk mencegah spam dan melindungi server.
    
    ## Authentication
    
    Beberapa endpoint mungkin memerlukan autentikasi Instagram untuk akses penuh.
    """,
    version="2.0.0",
    contact={
        "name": "Developer",
        "email": "developer@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - {process_time:.4f}s")
    
    return response

# Custom exception handlers
@app.exception_handler(InstagramAPIException)
async def instagram_api_exception_handler(request: Request, exc: InstagramAPIException):
    """Handle custom Instagram API exceptions"""
    error_response = ErrorResponse(
        detail=exc.detail,
        error_code=exc.error_code,
        timestamp=datetime.now()
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict()
    )

@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc):
    """Handle internal server errors"""
    logger.error(f"Internal server error: {str(exc)}")
    
    error_response = ErrorResponse(
        detail="Internal server error",
        error_code="INTERNAL_ERROR",
        timestamp=datetime.now()
    )
    
    return JSONResponse(
        status_code=500,
        content=error_response.dict()
    )

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Handle not found errors"""
    error_response = ErrorResponse(
        detail="Endpoint not found",
        error_code="NOT_FOUND",
        timestamp=datetime.now()
    )
    
    return JSONResponse(
        status_code=404,
        content=error_response.dict()
    )

# Include routes
app.include_router(router, prefix="/api/v1", tags=["Instagram API"])

# Add root redirect
@app.get("/", include_in_schema=False)
async def root_redirect():
    """Redirect root to API docs"""
    return {"message": "Instagram Scraper API", "docs": "/docs", "redoc": "/redoc"}

# Add startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Actions to perform on startup"""
    logger.info("Instagram Scraper API starting up...")
    logger.info("API documentation available at /docs")

@app.on_event("shutdown")
async def shutdown_event():
    """Actions to perform on shutdown"""
    logger.info("Instagram Scraper API shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )