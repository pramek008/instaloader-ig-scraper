from fastapi import HTTPException
from typing import Optional

class InstagramAPIException(HTTPException):
    """Base exception untuk Instagram API"""
    def __init__(self, status_code: int, detail: str, error_code: Optional[str] = None):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code

class ProfileNotFoundError(InstagramAPIException):
    """Exception ketika profil tidak ditemukan"""
    def __init__(self, username: str):
        super().__init__(
            status_code=404,
            detail=f"Profile '{username}' not found",
            error_code="PROFILE_NOT_FOUND"
        )

class PostNotFoundError(InstagramAPIException):
    """Exception ketika post tidak ditemukan"""
    def __init__(self, identifier: str):
        super().__init__(
            status_code=404,
            detail=f"Post '{identifier}' not found",
            error_code="POST_NOT_FOUND"
        )

class PrivateProfileError(InstagramAPIException):
    """Exception ketika profil bersifat privat"""
    def __init__(self, username: str):
        super().__init__(
            status_code=403,
            detail=f"Profile '{username}' is private",
            error_code="PRIVATE_PROFILE"
        )

class InvalidURLError(InstagramAPIException):
    """Exception ketika URL Instagram tidak valid"""
    def __init__(self, url: str):
        super().__init__(
            status_code=400,
            detail=f"Invalid Instagram URL: {url}",
            error_code="INVALID_URL"
        )

class RateLimitError(InstagramAPIException):
    """Exception ketika rate limit terlampaui"""
    def __init__(self):
        super().__init__(
            status_code=429,
            detail="Rate limit exceeded. Please try again later",
            error_code="RATE_LIMIT_EXCEEDED"
        )

class InstagramConnectionError(InstagramAPIException):
    """Exception ketika tidak bisa terhubung ke Instagram"""
    def __init__(self):
        super().__init__(
            status_code=503,
            detail="Unable to connect to Instagram",
            error_code="CONNECTION_ERROR"
        )