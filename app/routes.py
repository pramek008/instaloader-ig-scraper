from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional
import logging

from app.models import (
    ProfileResponse, PostListResponse, PostData, 
    StoryData, HighlightData, CommentData, HashtagInfo,
    SearchResult, ErrorResponse
)
from app.services import InstagramService
from app.utils import extract_shortcode_from_url, validate_username
from app.exceptions import (
    ProfileNotFoundError, PostNotFoundError, PrivateProfileError,
    InvalidURLError, RateLimitError, InstagramConnectionError
)

# Setup logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Initialize service
instagram_service = InstagramService()

@router.get("/", summary="Root endpoint")
async def root():
    """Root endpoint untuk mengecek status API"""
    return {
        "message": "Instagram Scraper API is running",
        "version": "2.0.0",
        "status": "active"
    }

@router.get("/health", summary="Health check")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "instagram-scraper-api",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@router.get(
    "/profile/{username}", 
    response_model=ProfileResponse,
    summary="Get user profile",
    description="Mendapatkan data profil pengguna Instagram beserta post terbaru"
)
async def get_user_profile(
    username: str = Path(..., description="Username Instagram (tanpa @)", min_length=1, max_length=30),
    include_posts: bool = Query(True, description="Apakah menyertakan post terbaru"),
    max_posts: int = Query(12, description="Maksimal jumlah post yang diambil", ge=1, le=50)
):
    """Get user profile data with optional recent posts"""
    try:
        # Validate username format
        if not validate_username(username):
            raise HTTPException(status_code=400, detail="Invalid username format")
        
        profile_data = instagram_service.get_profile_data(username)
        recent_posts = []
        
        if include_posts and not profile_data.is_private:
            try:
                recent_posts = instagram_service.get_user_posts(username, max_posts)
            except Exception as e:
                logger.warning(f"Error getting posts for {username}: {str(e)}")
        return ProfileResponse(
            profile=profile_data,
            recent_posts=recent_posts
        )
        
    except (ProfileNotFoundError, PrivateProfileError, RateLimitError, InstagramConnectionError) as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in get_user_profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get(
    "/posts/{username}", 
    response_model=PostListResponse,
    summary="Get user posts",
    description="Mendapatkan daftar post dari pengguna Instagram"
)
async def get_user_posts(
    username: str = Path(..., description="Username Instagram", min_length=1, max_length=30),
    max_posts: int = Query(50, description="Maksimal jumlah post", ge=1, le=100)
):
    """Get list of user posts"""
    try:
        if not validate_username(username):
            raise HTTPException(status_code=400, detail="Invalid username format")
        
        posts_data = instagram_service.get_user_posts(username, max_posts)
        
        return PostListResponse(
            username=username,
            posts=posts_data,
            total_posts=len(posts_data)
        )
        
    except (ProfileNotFoundError, PrivateProfileError, RateLimitError, InstagramConnectionError) as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in get_user_posts: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get(
    "/post", 
    response_model=PostData,
    summary="Get post by URL",
    description="Mendapatkan data post Instagram berdasarkan URL"
)
async def get_post_by_url(
    url: str = Query(..., description="URL post Instagram")
):
    """Get specific post data by Instagram URL"""
    try:
        shortcode = extract_shortcode_from_url(url)
        return instagram_service.get_post_by_shortcode(shortcode)
        
    except InvalidURLError as e:
        raise e
    except (PostNotFoundError, RateLimitError, InstagramConnectionError) as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in get_post_by_url: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get(
    "/post/{shortcode}", 
    response_model=PostData,
    summary="Get post by shortcode",
    description="Mendapatkan data post Instagram berdasarkan shortcode"
)
async def get_post_by_shortcode(
    shortcode: str = Path(..., description="Shortcode post Instagram", min_length=11, max_length=11)
):
    """Get specific post data by shortcode"""
    try:
        return instagram_service.get_post_by_shortcode(shortcode)
        
    except (PostNotFoundError, RateLimitError, InstagramConnectionError) as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in get_post_by_shortcode: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get(
    "/stories/{username}", 
    response_model=List[StoryData],
    summary="Get user stories",
    description="Mendapatkan stories pengguna (membutuhkan autentikasi)"
)
async def get_user_stories(
    username: str = Path(..., description="Username Instagram", min_length=1, max_length=30)
):
    """Get user stories (requires login)"""
    try:
        if not validate_username(username):
            raise HTTPException(status_code=400, detail="Invalid username format")
        
        stories = instagram_service.get_user_stories(username)
        return stories
        
    except (ProfileNotFoundError, PrivateProfileError) as e:
        raise e
    except Exception as e:
        logger.warning(f"Stories not available for {username}: {str(e)}")
        return []

@router.get(
    "/highlights/{username}", 
    response_model=List[HighlightData],
    summary="Get user highlights",
    description="Mendapatkan highlights pengguna Instagram"
)
async def get_user_highlights(
    username: str = Path(..., description="Username Instagram", min_length=1, max_length=30)
):
    """Get user highlights"""
    try:
        if not validate_username(username):
            raise HTTPException(status_code=400, detail="Invalid username format")
        
        highlights = instagram_service.get_user_highlights(username)
        return highlights
        
    except ProfileNotFoundError as e:
        raise e
    except Exception as e:
        logger.warning(f"Highlights not available for {username}: {str(e)}")
        return []

@router.get(
    "/comments/{shortcode}", 
    response_model=List[CommentData],
    summary="Get post comments",
    description="Mendapatkan komentar dari sebuah post"
)
async def get_post_comments(
    shortcode: str = Path(..., description="Shortcode post Instagram", min_length=11, max_length=11),
    max_comments: int = Query(50, description="Maksimal jumlah komentar", ge=1, le=200)
):
    """Get post comments"""
    try:
        comments = instagram_service.get_post_comments(shortcode, max_comments)
        return comments
        
    except PostNotFoundError as e:
        raise e
    except Exception as e:
        logger.warning(f"Comments not available for {shortcode}: {str(e)}")
        return []

@router.get(
    "/hashtag/{hashtag_name}", 
    response_model=HashtagInfo,
    summary="Get hashtag info",
    description="Mendapatkan informasi hashtag"
)
async def get_hashtag_info(
    hashtag_name: str = Path(..., description="Nama hashtag (tanpa #)", min_length=1, max_length=100)
):
    """Get hashtag information"""
    try:
        hashtag_info = instagram_service.get_hashtag_info(hashtag_name)
        return hashtag_info
        
    except Exception as e:
        logger.error(f"Error getting hashtag info for {hashtag_name}: {str(e)}")
        raise HTTPException(status_code=404, detail="Hashtag not found or unavailable")

@router.get(
    "/search", 
    response_model=List[SearchResult],
    summary="Search profiles",
    description="Mencari profil pengguna Instagram"
)
async def search_profiles(
    query: str = Query(..., description="Kata kunci pencarian", min_length=1, max_length=100),
    max_results: int = Query(20, description="Maksimal hasil pencarian", ge=1, le=50)
):
    """Search for profiles"""
    try:
        results = instagram_service.search_profiles(query, max_results)
        return results
        
    except Exception as e:
        logger.error(f"Error searching profiles for '{query}': {str(e)}")
        return []

@router.get(
    "/analytics/{username}",
    summary="Get profile analytics",
    description="Mendapatkan analytics sederhana dari profil"
)
async def get_profile_analytics(
    username: str = Path(..., description="Username Instagram", min_length=1, max_length=30),
    days: int = Query(30, description="Periode analisis (hari)", ge=1, le=90)
):
    """Get basic profile analytics"""
    try:
        if not validate_username(username):
            raise HTTPException(status_code=400, detail="Invalid username format")
        
        # Get profile and recent posts
        profile = instagram_service.get_profile_data(username)
        
        if profile.is_private:
            raise PrivateProfileError(username)
        
        # Get posts for analysis
        posts = instagram_service.get_user_posts(username, min(50, days))
        
        if not posts:
            return {
                "username": username,
                "followers": profile.followers,
                "posts_analyzed": 0,
                "average_likes": 0,
                "average_comments": 0,
                "engagement_rate": 0,
                "most_used_hashtags": [],
                "posting_frequency": 0
            }
        
        # Calculate analytics
        total_likes = sum(post.likes for post in posts)
        total_comments = sum(post.comments for post in posts)
        avg_likes = total_likes / len(posts) if posts else 0
        avg_comments = total_comments / len(posts) if posts else 0
        
        # Calculate engagement rate
        total_engagement = total_likes + total_comments
        engagement_rate = (total_engagement / (len(posts) * profile.followers)) * 100 if profile.followers > 0 else 0
        
        # Get most used hashtags
        all_hashtags = []
        for post in posts:
            all_hashtags.extend(post.hashtags)
        
        hashtag_counts = {}
        for hashtag in all_hashtags:
            hashtag_counts[hashtag] = hashtag_counts.get(hashtag, 0) + 1
        
        most_used_hashtags = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "username": username,
            "followers": profile.followers,
            "posts_analyzed": len(posts),
            "average_likes": round(avg_likes, 2),
            "average_comments": round(avg_comments, 2),
            "engagement_rate": round(engagement_rate, 2),
            "most_used_hashtags": [{"hashtag": tag, "count": count} for tag, count in most_used_hashtags],
            "posting_frequency": round(len(posts) / days, 2) if days > 0 else 0
        }
        
    except (ProfileNotFoundError, PrivateProfileError, RateLimitError, InstagramConnectionError) as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in get_profile_analytics: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")