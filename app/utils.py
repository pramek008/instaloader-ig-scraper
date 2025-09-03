import re
from typing import List, Tuple
from urllib.parse import urlparse
from app.exceptions import InvalidURLError

def extract_shortcode_from_url(url: str) -> str:
    """Extract shortcode from Instagram post URL"""
    patterns = [
        r'instagram\.com/p/([A-Za-z0-9_-]+)',
        r'instagram\.com/reel/([A-Za-z0-9_-]+)',
        r'instagram\.com/tv/([A-Za-z0-9_-]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    raise InvalidURLError(url)

def validate_username(username: str) -> bool:
    """Validasi format username Instagram"""
    # Username Instagram hanya boleh mengandung huruf, angka, underscore, dan titik
    # Panjang 1-30 karakter
    pattern = r'^[a-zA-Z0-9_.]{1,30}$'
    return bool(re.match(pattern, username))

def extract_hashtags(text: str) -> List[str]:
    """Extract hashtags from text"""
    if not text:
        return []
    
    hashtag_pattern = r'#([A-Za-z0-9_]+)'
    hashtags = re.findall(hashtag_pattern, text)
    return hashtags

def extract_mentions(text: str) -> List[str]:
    """Extract mentions from text"""
    if not text:
        return []
    
    mention_pattern = r'@([A-Za-z0-9_.]+)'
    mentions = re.findall(mention_pattern, text)
    return mentions

def sanitize_text(text: str) -> str:
    """Sanitize text by removing unwanted characters"""
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text

def format_number(number: int) -> str:
    """Format large numbers with K, M, B suffixes"""
    if number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.1f}B"
    elif number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number / 1_000:.1f}K"
    else:
        return str(number)

def is_valid_instagram_url(url: str) -> bool:
    """Check if URL is a valid Instagram URL"""
    try:
        parsed = urlparse(url)
        return parsed.netloc in ['instagram.com', 'www.instagram.com']
    except:
        return False

def get_media_type(url: str) -> str:
    """Determine media type from URL"""
    if not url:
        return "unknown"
    
    video_extensions = ['.mp4', '.mov', '.avi', '.webm']
    image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    
    url_lower = url.lower()
    
    for ext in video_extensions:
        if ext in url_lower:
            return "video"
    
    for ext in image_extensions:
        if ext in url_lower:
            return "image"
    
    return "unknown"

def clean_caption(caption: str) -> str:
    """Clean and format caption text"""
    if not caption:
        return ""
    
    # Remove excessive line breaks
    caption = re.sub(r'\n{3,}', '\n\n', caption)
    
    # Remove trailing whitespace from each line
    lines = [line.rstrip() for line in caption.split('\n')]
    
    return '\n'.join(lines).strip()

def get_engagement_rate(likes: int, comments: int, followers: int) -> float:
    """Calculate engagement rate"""
    if followers == 0:
        return 0.0
    
    return ((likes + comments) / followers) * 100

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length"""
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix