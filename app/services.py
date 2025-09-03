import instaloader
import logging
from typing import Dict, List, Optional
from datetime import datetime

from app.models import (
    UserProfile, PostData, StoryData, HighlightData,
    CommentData, HashtagInfo
)
from app.exceptions import (
    ProfileNotFoundError, PostNotFoundError, PrivateProfileError,
    InstagramConnectionError, RateLimitError
)
from app.utils import (
    extract_hashtags, extract_mentions, sanitize_text,
    clean_caption, get_engagement_rate
)

# Setup logging
logger = logging.getLogger(__name__)

class InstagramService:
    """Service class untuk menghandle operasi Instagram"""
    
    def __init__(self):
        self.loader = instaloader.Instaloader(
            download_pictures=False,
            download_videos=False,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False
        )
        
    def get_profile_data(self, username: str) -> UserProfile:
        """Get user profile data"""
        try:
            profile = instaloader.Profile.from_username(self.loader.context, username)            
            
            return UserProfile(
                username=profile.username,
                full_name=sanitize_text(profile.full_name),
                biography=clean_caption(profile.biography),
                followers=profile.followers,
                followees=profile.followees,
                posts_count=profile.mediacount,
                is_private=profile.is_private,
                profile_pic_url=profile.profile_pic_url,
                external_url=profile.external_url,
                is_verified=profile.is_verified
            )
            
        except instaloader.exceptions.ProfileNotExistsException:
            raise ProfileNotFoundError(username)
        except instaloader.exceptions.ConnectionException:
            raise InstagramConnectionError()
        except instaloader.exceptions.TooManyRequestsException:
            raise RateLimitError()
        except Exception as e:
            logger.error(f"Error getting profile data for {username}: {str(e)}")
            raise InstagramConnectionError()

    def get_post_data_from_post(self, post) -> PostData:
        """Convert Instaloader Post object to PostData"""
        for attr in dir(post):
            if not attr.startswith("_"):  # skip private/internal
                try:
                    value = getattr(post, attr)
                    if isinstance(value, object) and not isinstance(value, (str, int, float, bool)):
                        for sub_attr in dir(value):
                            if not sub_attr.startswith("_"):  # skip private/internal
                                try:
                                    sub_value = getattr(value, sub_attr)
                                    logger.info(f"{attr}.{sub_attr}: {sub_value}")
                                    
                                except Exception as e:
                                    logger.warning(f"{attr}.{sub_attr}: <error {e}>")
                    else:
                        logger.info(f"{attr}: {value}")
                        
                except Exception as e:
                    logger.warning(f"{attr}: <error {e}>")

        try:
            media_urls = []                            
            # Get all media URLs for carousel posts
            if post.typename == 'GraphSidecar':
                try:
                    for node in post.get_sidecar_nodes():
                        logger.info(f"Sidecar node: {node}")
                        if node.is_video:
                            media_urls.append(node.video_url)
                        else:
                            media_urls.append(node.display_url)
                except:
                    # Fallback if sidecar nodes fail
                    media_urls.append(post.url)
            else:
                if post.is_video:
                    media_urls.append(post.video_url)
                else:
                    media_urls.append(post.url)
            
            # Extract hashtags and mentions from caption
            caption = clean_caption(post.caption) if post.caption else ""
            hashtags = extract_hashtags(caption)
            mentions = extract_mentions(caption)
            
            # Get location if available
            location = None
            if hasattr(post, 'location') and post.location:
                location = post.location.name
                
            return PostData(
                shortcode=post.shortcode,
                url=f"https://instagram.com/p/{post.shortcode}",
                caption=caption,
                likes=post.likes,
                comments=post.comments,
                plays=getattr(post, 'video_play_count', None),
                views=getattr(post, 'video_view_count', None),
                date=post.date,
                is_video=post.is_video,
                media_url=media_urls[0] if media_urls else "",
                media_urls=media_urls,
                location=location,
                hashtags=hashtags,
                mentions=mentions
            )
            
        except Exception as e:
            logger.error(f"Error converting post data: {str(e)}")
            # Return minimal data if conversion fails
            return PostData(
                shortcode=post.shortcode,
                url=f"https://instagram.com/p/{post.shortcode}",
                caption="",
                likes=0,
                comments=0,
                date=post.date,
                is_video=post.is_video,
                media_url="",
                media_urls=[]
            )

    def get_user_posts(self, username: str, max_posts: int = 50) -> List[PostData]:
        """Get list of user posts"""
        try:
            profile = instaloader.Profile.from_username(self.loader.context, username)
            
            if profile.is_private:
                raise PrivateProfileError(username)
            
            posts_data = []
            posts = profile.get_posts()
            
            count = 0
            for post in posts:
                if count >= max_posts:
                    break
                try:
                    posts_data.append(self.get_post_data_from_post(post))
                    count += 1
                except Exception as e:
                    logger.warning(f"Error processing post {post.shortcode}: {str(e)}")
                    continue
            
            return posts_data
            
        except instaloader.exceptions.ProfileNotExistsException:
            raise ProfileNotFoundError(username)
        except PrivateProfileError:
            raise
        except instaloader.exceptions.ConnectionException:
            raise InstagramConnectionError()
        except instaloader.exceptions.TooManyRequestsException:
            raise RateLimitError()
        except Exception as e:
            logger.error(f"Error getting posts for {username}: {str(e)}")
            raise InstagramConnectionError()

    def get_post_by_shortcode(self, shortcode: str) -> PostData:
        """Get specific post data by shortcode"""
        try:
            post = instaloader.Post.from_shortcode(self.loader.context, shortcode)
            return self.get_post_data_from_post(post)
            
        except instaloader.exceptions.PostNotExistsException:
            raise PostNotFoundError(shortcode)
        except instaloader.exceptions.ConnectionException:
            raise InstagramConnectionError()
        except instaloader.exceptions.TooManyRequestsException:
            raise RateLimitError()
        except Exception as e:
            logger.error(f"Error getting post data for {shortcode}: {str(e)}")
            raise InstagramConnectionError()

    def get_user_stories(self, username: str) -> List[StoryData]:
        """Get user stories (requires login)"""
        try:
            profile = instaloader.Profile.from_username(self.loader.context, username)
            
            if profile.is_private:
                raise PrivateProfileError(username)
            
            stories_data = []
            
            # Note: Getting stories requires authentication
            # This is a placeholder implementation
            stories = self.loader.get_stories([profile.userid])
            
            for story in stories:
                for item in story.get_items():
                    stories_data.append(StoryData(
                        story_id=str(item.mediaid),
                        url=item.video_url if item.is_video else item.url,
                        is_video=item.is_video,
                        date=item.date,
                        expires_at=item.date.replace(hour=23, minute=59, second=59)
                    ))
            
            return stories_data
            
        except instaloader.exceptions.ProfileNotExistsException:
            raise ProfileNotFoundError(username)
        except Exception as e:
            logger.error(f"Error getting stories for {username}: {str(e)}")
            return []  # Return empty list if stories can't be fetched

    def get_user_highlights(self, username: str) -> List[HighlightData]:
        """Get user highlights"""
        try:
            profile = instaloader.Profile.from_username(self.loader.context, username)
            
            highlights_data = []
            
            for highlight in self.loader.get_highlights(profile):
                highlights_data.append(HighlightData(
                    highlight_id=str(highlight.unique_id),
                    title=highlight.title,
                    cover_url=highlight.cover_url,
                    story_count=highlight.itemcount
                ))
            
            return highlights_data
            
        except instaloader.exceptions.ProfileNotExistsException:
            raise ProfileNotFoundError(username)
        except Exception as e:
            logger.error(f"Error getting highlights for {username}: {str(e)}")
            return []

    def get_post_comments(self, shortcode: str, max_comments: int = 50) -> List[CommentData]:
        """Get post comments"""
        try:
            post = instaloader.Post.from_shortcode(self.loader.context, shortcode)
            
            comments_data = []
            comments = post.get_comments()
            
            count = 0
            for comment in comments:
                if count >= max_comments:
                    break
                    
                try:
                    comments_data.append(CommentData(
                        comment_id=str(comment.id),
                        username=comment.owner.username,
                        text=sanitize_text(comment.text),
                        likes=comment.likes_count,
                        date=comment.created_at,
                        replies_count=comment.answers_count
                    ))
                    count += 1
                except Exception as e:
                    logger.warning(f"Error processing comment: {str(e)}")
                    continue
            
            return comments_data
            
        except instaloader.exceptions.PostNotExistsException:
            raise PostNotFoundError(shortcode)
        except Exception as e:
            logger.error(f"Error getting comments for post {shortcode}: {str(e)}")
            return []

    def get_hashtag_info(self, hashtag_name: str) -> HashtagInfo:
        """Get hashtag information"""
        try:
            # Remove # if present
            hashtag_name = hashtag_name.lstrip('#')
            
            hashtag = instaloader.Hashtag.from_name(self.loader.context, hashtag_name)
            
            return HashtagInfo(
                name=hashtag.name,
                post_count=hashtag.mediacount
            )
            
        except Exception as e:
            logger.error(f"Error getting hashtag info for {hashtag_name}: {str(e)}")
            raise InstagramConnectionError()

    def search_profiles(self, query: str, max_results: int = 20) -> List[dict]:
        """Search for profiles (basic implementation)"""
        try:
            # This is a simplified implementation
            # Real implementation would require more sophisticated search
            results = []
            
            # Try to get profile if query is exact username
            try:
                profile = instaloader.Profile.from_username(self.loader.context, query)
                results.append({
                    'username': profile.username,
                    'full_name': sanitize_text(profile.full_name),
                    'profile_pic_url': profile.profile_pic_url,
                    'is_verified': profile.is_verified,
                    'is_private': profile.is_private,
                    'followers': profile.followers
                })
            except:
                pass
            
            return results[:max_results]
            
        except Exception as e:
            logger.error(f"Error searching profiles for '{query}': {str(e)}")
            return []