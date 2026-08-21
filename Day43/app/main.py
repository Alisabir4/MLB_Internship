import logging
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.routes.video import router as video_router


# --------------------------------------------------
# Application Configuration
# --------------------------------------------------

APP_VERSION = "1.0.0"

BASE_DIR = Path(__file__).resolve().parents[1]

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

LOG_FILE = LOG_DIR / "app.log"


# --------------------------------------------------
# Logging Configuration
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),
    handlers=[
        logging.FileHandler(
            LOG_FILE,
            encoding="utf-8",
        ),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("ai_video_api")


# --------------------------------------------------
# FastAPI Application
# --------------------------------------------------

app = FastAPI(
    title="AI Video Processing API",
    description=(
        "Production-ready FastAPI backend "
        "for YOLO-based video processing."
    ),
    version=APP_VERSION,
)


# --------------------------------------------------
# Include Video Routes
# --------------------------------------------------

app.include_router(video_router)


# --------------------------------------------------
# Request ID Middleware
# --------------------------------------------------

@app.middleware("http")
async def request_id_middleware(
    request: Request,
    call_next,
):
    request_id = (
        f"req_{uuid.uuid4().hex[:12]}"
    )

    request.state.request_id = request_id

    start_time = time.time()

    logger.info(
        f"Request started | "
        f"request_id={request_id} | "
        f"method={request.method} | "
        f"path={request.url.path}"
    )

    try:
        response = await call_next(request)

        processing_time = round(
            time.time() - start_time,
            3,
        )

        response.headers[
            "X-Request-ID"
        ] = request_id

        logger.info(
            f"Request completed | "
            f"request_id={request_id} | "
            f"status_code={response.status_code} | "
            f"time={processing_time}s"
        )

        return response

    except Exception as exc:

        processing_time = round(
            time.time() - start_time,
            3,
        )

        logger.error(
            f"Unhandled request error | "
            f"request_id={request_id} | "
            f"time={processing_time}s | "
            f"error={str(exc)}",
            exc_info=True,
        )

        raise


# --------------------------------------------------
# Request Validation Error Handler
# --------------------------------------------------

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    request_id = getattr(
        request.state,
        "request_id",
        "unknown",
    )

    logger.warning(
        f"Request validation failed | "
        f"request_id={request_id}"
    )

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "Invalid request data.",
            "request_id": request_id,
        },
    )


# --------------------------------------------------
# Global Exception Handler
# --------------------------------------------------

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    request_id = getattr(
        request.state,
        "request_id",
        "unknown",
    )

    logger.error(
        f"Unhandled application error | "
        f"request_id={request_id} | "
        f"error={str(exc)}",
        exc_info=True,
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error.",
            "request_id": request_id,
        },
    )


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
async def root():
    return {
        "success": True,
        "message": (
            "AI Video Processing API "
            "is running"
        ),
        "version": APP_VERSION,
        "docs": "/docs",
    }


# --------------------------------------------------
# Health Endpoint
# --------------------------------------------------

@app.get("/health")
async def health():
    model_status = "not_loaded"

    try:
        from app.services.detector import detector

        if detector.model is not None:
            model_status = "loaded"

    except Exception as exc:

        logger.error(
            f"Model health check failed | "
            f"error={str(exc)}"
        )

    return {
        "success": True,
        "api_status": "healthy",
        "model_status": model_status,
        "version": APP_VERSION,
    }