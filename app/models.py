from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class UserProfile(BaseModel):
    """Model untuk data profil pengguna Instagram"""
    username: str = Field(..., description="Username Instagram")
    full_name: str = Field(..., description="Nama lengkap pengguna")
    biography: str = Field(..., description="Bio profil pengguna")
    followers: int = Field(..., description="Jumlah followers")
    followees: int = Field(..., description="Jumlah following")
    posts_count: int = Field(..., description="Total jumlah post")
    is_private: bool = Field(..., description="Status privat akun")
    profile_pic_url: str = Field(..., description="URL foto profil")
    external_url: Optional[str] = Field(None, description="Link eksternal di bio")
    is_verified: bool = Field(..., description="Status verifikasi akun")

class PostData(BaseModel):
    """Model untuk data post Instagram"""
    shortcode: str = Field(..., description="Kode unik post")
    url: str = Field(..., description="URL post Instagram")
    caption: Optional[str] = Field(None, description="Caption post")
    likes: int = Field(..., description="Jumlah likes")
    comments: int = Field(..., description="Jumlah komentar")
    plays: Optional[int] = Field(None, description="Jumlah play untuk video")
    views: Optional[int] = Field(None, description="Jumlah views untuk video")
    date: datetime = Field(..., description="Tanggal post dibuat")
    is_video: bool = Field(..., description="Apakah post berupa video")
    media_url: str = Field(..., description="URL media utama")
    media_urls: List[str] = Field(default=[], description="List semua URL media (untuk carousel)")
    location: Optional[str] = Field(None, description="Lokasi post")
    hashtags: List[str] = Field(default=[], description="List hashtag dalam post")
    mentions: List[str] = Field(default=[], description="List mention dalam post")

class PostListResponse(BaseModel):
    """Response model untuk daftar post"""
    username: str = Field(..., description="Username pemilik post")
    posts: List[PostData] = Field(..., description="Daftar post")
    total_posts: int = Field(..., description="Total jumlah post yang diambil")

class ProfileResponse(BaseModel):
    """Response model untuk data profil lengkap"""
    profile: UserProfile = Field(..., description="Data profil pengguna")
    recent_posts: List[PostData] = Field(..., description="Post terbaru pengguna")

class StoryData(BaseModel):
    """Model untuk data story Instagram"""
    story_id: str = Field(..., description="ID story")
    url: str = Field(..., description="URL media story")
    is_video: bool = Field(..., description="Apakah story berupa video")
    date: datetime = Field(..., description="Tanggal story dibuat")
    expires_at: datetime = Field(..., description="Tanggal story berakhir")

class HighlightData(BaseModel):
    """Model untuk data highlight Instagram"""
    highlight_id: str = Field(..., description="ID highlight")
    title: str = Field(..., description="Judul highlight")
    cover_url: str = Field(..., description="URL cover highlight")
    story_count: int = Field(..., description="Jumlah story dalam highlight")

class SearchResult(BaseModel):
    """Model untuk hasil pencarian"""
    username: str = Field(..., description="Username")
    full_name: str = Field(..., description="Nama lengkap")
    profile_pic_url: str = Field(..., description="URL foto profil")
    is_verified: bool = Field(..., description="Status verifikasi")
    is_private: bool = Field(..., description="Status privat akun")
    followers: int = Field(..., description="Jumlah followers")

class HashtagInfo(BaseModel):
    """Model untuk informasi hashtag"""
    name: str = Field(..., description="Nama hashtag")
    post_count: int = Field(..., description="Jumlah post dengan hashtag ini")

class CommentData(BaseModel):
    """Model untuk data komentar"""
    comment_id: str = Field(..., description="ID komentar")
    username: str = Field(..., description="Username pemberi komentar")
    text: str = Field(..., description="Isi komentar")
    likes: int = Field(..., description="Jumlah likes komentar")
    date: datetime = Field(..., description="Tanggal komentar dibuat")
    replies_count: int = Field(..., description="Jumlah balasan komentar")

class ErrorResponse(BaseModel):
    """Model untuk response error"""
    detail: str = Field(..., description="Pesan error")
    error_code: Optional[str] = Field(None, description="Kode error spesifik")
    timestamp: datetime = Field(default_factory=datetime.now, description="Waktu error terjadi")