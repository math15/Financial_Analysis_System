# 🚀 Production Deployment Guide

## Production Domains
- **Frontend**: `https://mailbroker.ddns.net`
- **Backend**: `https://apimailbroker.ddns.net`

## ✅ Configuration Status

### Frontend Integration
The frontend (`lib/api.ts`) is already configured to automatically detect production vs development:

```typescript
if (hostname === 'mailbroker.ddns.net') {
  // Production environment - backend on apimailbroker.ddns.net
  return `${protocol}//apimailbroker.ddns.net`;
}
```

### Backend CORS Configuration
The backend (`backend/config.py`) is configured with proper CORS settings:

```python
ALLOWED_ORIGINS = [
    # Production domains
    "https://mailbroker.ddns.net",
    "http://mailbroker.ddns.net", 
    "https://apimailbroker.ddns.net",
    "http://apimailbroker.ddns.net",
    # Development
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5000",
    "http://127.0.0.1:5000"
]
```

## 🔧 Production Environment Setup

### 1. Create Production Environment File
```bash
cd backend
cp .env.example .env
```

### 2. Configure Production Environment Variables
Edit `backend/.env`:

```env
# LLMWhisperer Configuration (Required)
LLM_API_KEY=your_production_llmwhisperer_api_key
LLM_API_URL=https://llmwhisperer-api.us-central.unstract.com/api/v2

# Optional LLM APIs for enhanced analysis
OPENAI_API_KEY=your_production_openai_key
ANTHROPIC_API_KEY=your_production_anthropic_key
GOOGLE_API_KEY=your_production_google_key

# Production API Configuration
API_HOST=0.0.0.0
API_PORT=5000

# Processing Settings
USE_LLM_API=true
FALLBACK_TO_LOCAL=true
LOCAL_PROCESSING_ONLY=false

# File Upload Settings
MAX_FILE_SIZE=20971520  # 20MB
PROCESSING_TIMEOUT=300  # 5 minutes

# Logging
LLMWHISPERER_LOGGING_LEVEL=INFO
```

## 🚀 Deployment Commands

### Backend Deployment (apimailbroker.ddns.net)
```bash
# 1. Install dependencies
cd backend
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with production values

# 3. Start production server
python main.py
```

### Frontend Deployment (mailbroker.ddns.net)
```bash
# 1. Install dependencies
npm install

# 2. Build for production
npm run build

# 3. Start production server
npm start
```

## 🧪 Testing Production Setup

### 1. Test Backend Health
```bash
curl https://apimailbroker.ddns.net/api/health
```

### 2. Test Frontend API Connection
```bash
curl https://apimailbroker.ddns.net/
```

### 3. Test CORS
```bash
curl -H "Origin: https://mailbroker.ddns.net" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: X-Requested-With" \
     -X OPTIONS \
     https://apimailbroker.ddns.net/api/quotes/upload
```

## 📊 System Monitoring

### Backend Logs
```bash
# Monitor backend logs
tail -f backend/logs/app.log  # if logging to file
```

### Health Check Endpoints
- Backend Health: `https://apimailbroker.ddns.net/api/health`
- API Documentation: `https://apimailbroker.ddns.net/docs`
- Frontend: `https://mailbroker.ddns.net`

## 🔐 Security Considerations

1. **HTTPS**: Ensure both domains use HTTPS certificates
2. **API Keys**: Store production API keys securely
3. **CORS**: Already configured for your domains
4. **File Upload**: 20MB limit configured
5. **Authentication**: Update demo-token for production

## 🎯 Ready to Deploy!

Your system is now configured for production with:
- ✅ Frontend-Backend domain integration
- ✅ CORS configuration
- ✅ LLMWhisperer v2 official client
- ✅ Multi-LLM support
- ✅ Professional PDF reports
- ✅ Comprehensive error handling 