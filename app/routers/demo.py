from fastapi import APIRouter, HTTPException, Depends
from app.utils.slack_logger import setup_logger

router = APIRouter(prefix="/demo", tags=["demo"])
logger = setup_logger("demo_router")

@router.get("/")
async def root():
    """
    A simple endpoint that returns a welcome message.
    """
    logger.info("Root endpoint called")
    return {"message": "Welcome to the demo API"}

@router.get("/error")
async def trigger_error():
    """
    An endpoint that deliberately raises an exception to test error logging.
    """
    logger.info("Error endpoint called")
    try:
        # Deliberately cause an error
        result = 1 / 0
    except Exception as e:
        logger.error(f"Division by zero error occurred", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred")

@router.get("/warning")
async def trigger_warning():
    """
    An endpoint that logs a warning message.
    """
    logger.warning("This is a warning message")
    return {"message": "Warning logged"}

@router.get("/custom-error")
async def custom_error(message: str = "Custom error message"):
    """
    An endpoint that logs a custom error message.
    """
    logger.error(f"Custom error: {message}")
    return {"message": "Custom error logged"} 