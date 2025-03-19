from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
import traceback

from app.routers import demo
from app.utils.slack_logger import setup_logger

# Set up the logger
logger = setup_logger("main")

# Create the FastAPI app
app = FastAPI(
    title="Exception Logger API",
    description="A FastAPI application that logs exceptions to Slack",
    version="0.1.0",
)

# Include routers
app.include_router(demo.router)

@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.
    """
    logger.info("Root endpoint called")
    return {"message": "Welcome to the Exception Logger API"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler that logs all unhandled exceptions.
    """
    error_msg = f"Unhandled exception: {str(exc)}"
    logger.error(error_msg, exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred"},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 