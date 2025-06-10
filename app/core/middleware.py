"""
Custom middleware for HarvestHub FastAPI application
"""

import time
from typing import Callable
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    """Middleware to add process time header"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request logging"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Log request
        print(f"🔍 {request.method} {request.url.path} - {request.client.host}")
        
        response = await call_next(request)
        
        # Log response
        process_time = time.time() - start_time
        print(f"✅ {response.status_code} - {process_time:.4f}s")
        
        return response


def add_custom_middleware(app: FastAPI) -> None:
    """Add custom middleware to FastAPI app"""
    app.add_middleware(ProcessTimeMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
