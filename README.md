# Instagram Scraper API

API untuk scraping data Instagram menggunakan FastAPI dan Instaloader. API ini menyediakan endpoint untuk mengakses data profil, post, stories, comments, dan analytics dari Instagram.

## 🚀 Features

- ✅ **Profile Data** - Mendapatkan informasi profil pengguna lengkap
- ✅ **Posts Scraping** - Mengambil post dan media dari pengguna
- ✅ **Stories & Highlights** - Akses stories dan highlights (terbatas)
- ✅ **Comments** - Mengambil komentar dari post
- ✅ **Analytics** - Analisis engagement dan statistik sederhana
- ✅ **Search** - Pencarian profil pengguna
- ✅ **Hashtags Info** - Informasi tentang hashtag
- ✅ **Rate Limiting** - Perlindungan dari spam
- ✅ **Error Handling** - Penanganan error yang comprehensive
- ✅ **Dokumentasi API** - Swagger/OpenAPI documentation

## 📁 Struktur Proyek

```
instagram-scraper-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app dan konfigurasi
│   ├── routes.py            # API endpoints
│   ├── services.py          # Business logic dan Instagram service
│   ├── models.py            # Pydantic models
│   ├── exceptions.py        # Custom exceptions
│   ├── utils.py             # Utility functions
│   └── config.py            # Configuration settings
├── requirements.txt         # Python dependencies
├── run.py                   # Script untuk menjalankan aplikasi
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
├── .env.example           # Environment variables template
└── README.md              # Dokumentasi ini
```

## 🛠 Installation

### Prerequisites

- Python 3.8+
- pip atau pipenv

### Local Setup

1. **Clone repository**

   ```bash
   git clone <repository-url>
   cd instagram-scraper-api
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Setup environment variables**

   ```bash
   cp .env.example .env
   # Edit .env sesuai kebutuhan
   ```

4. **Run aplikasi**

   ```bash
   python run.py
   ```

   Atau menggunakan uvicorn langsung:

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Akses API Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Docker Setup

1. **Build dan run dengan docker-compose**

   ```bash
   docker-compose up --build
   ```

2. **Atau build manual**
   ```bash
   docker build -t instagram-api .
   docker run -p 8000:8000 instagram-api
   ```

## 📚 API Endpoints

### Base URL

```
http://localhost:8000/api/v1
```

### Profile Endpoints

#### Get User Profile

```http
GET /profile/{username}?include_posts=true&max_posts=12
```

**Parameters:**

- `username` (path): Instagram username
- `include_posts` (query, optional): Include recent posts (default: true)
- `max_posts` (query, optional): Maximum posts to fetch (default: 12, max: 50)

**Response:**

```json
{
  "profile": {
    "username": "example_user",
    "full_name": "Example User",
    "biography": "Bio text here...",
    "followers": 1000,
    "followees": 500,
    "posts_count": 100,
    "is_private": false,
    "profile_pic_url": "https://...",
    "external_url": null,
    "is_verified": false
  },
  "recent_posts": [...]
}
```

### Posts Endpoints

#### Get User Posts

```http
GET /posts/{username}?max_posts=50
```

#### Get Post by URL

```http
GET /post?url=https://instagram.com/p/ABC123/
```

#### Get Post by Shortcode

```http
GET /post/{shortcode}
```

### Analytics Endpoint

#### Get Profile Analytics

```http
GET /analytics/{username}?days=30
```

**Response:**

```json
{
  "username": "example_user",
  "followers": 1000,
  "posts_analyzed": 25,
  "average_likes": 150.5,
  "average_comments": 25.3,
  "engagement_rate": 17.58,
  "most_used_hashtags": [
    { "hashtag": "photography", "count": 5 },
    { "hashtag": "nature", "count": 3 }
  ],
  "posting_frequency": 0.83
}
```

### Other Endpoints

#### Get Stories

```http
GET /stories/{username}
```

#### Get Highlights

```http
GET /highlights/{username}
```

#### Get Post Comments

```http
GET /comments/{shortcode}?max_comments=50
```

#### Get Hashtag Info

```http
GET /hashtag/{hashtag_name}
```

#### Search Profiles

```http
GET /search?query=example&max_results=20
```

## ⚙️ Configuration

### Environment Variables

```env
# App Configuration
APP_NAME="Instagram Scraper API"
VERSION="2.0.0"
DEBUG=False

# Server Configuration
HOST="0.0.0.0"
PORT=8000

# Instagram Credentials (Optional)
INSTAGRAM_USERNAME=""
INSTAGRAM_PASSWORD=""

# Rate Limiting
RATE_LIMIT_PER_MINUTE=30
RATE_LIMIT_PER_HOUR=1000

# Logging
LOG_LEVEL="INFO"
```

### Rate Limiting

API menggunakan rate limiting untuk mencegah abuse:

- 30 requests per menit per IP
- 1000 requests per jam per IP

### Error Handling

API mengembalikan error dalam format konsisten:

```json
{
  "detail": "Profile not found",
  "error_code": "PROFILE_NOT_FOUND",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

**Error Codes:**

- `PROFILE_NOT_FOUND` - Profil tidak ditemukan
- `POST_NOT_FOUND` - Post tidak ditemukan
- `PRIVATE_PROFILE` - Profil bersifat privat
- `INVALID_URL` - URL Instagram tidak valid
- `RATE_LIMIT_EXCEEDED` - Rate limit terlampaui
- `CONNECTION_ERROR` - Koneksi ke Instagram gagal

## 🔒 Security & Limitations

### Limitations

1. **Private Profiles**: Tidak dapat mengakses konten dari profil privat
2. **Rate Limiting**: Instagram menerapkan rate limiting yang ketat
3. **Stories**: Membutuhkan autentikasi untuk mengakses stories
4. **Real-time Data**: Data mungkin tidak real-time karena caching

### Best Practices

1. **Respect Rate Limits**: Jangan spam request
2. **Handle Errors**: Selalu handle error response dengan proper
3. **Cache Results**: Cache hasil untuk mengurangi API calls
4. **Monitor Usage**: Monitor penggunaan untuk avoid blocking

## 🧪 Testing

### Manual Testing

```bash
# Test basic endpoint
curl http://localhost:8000/api/v1/health

# Test profile endpoint
curl http://localhost:8000/api/v1/profile/instagram

# Test with parameters
curl "http://localhost:8000/api/v1/profile/instagram?include_posts=true
```
