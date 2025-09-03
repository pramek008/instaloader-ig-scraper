# app/__init__.py
"""
Instagram Scraper API

A FastAPI-based API for scraping Instagram data using Instaloader.
"""

__version__ = "2.0.0"
__author__ = "Developer"
__email__ = "developer@example.com"

from .main import app

__all__ = ["app"]