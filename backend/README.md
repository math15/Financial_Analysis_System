# Insurance Quote Comparison Backend API

A professional FastAPI backend for analyzing and comparing commercial insurance quotes with AI-powered text extraction and comprehensive policy section analysis.

## 🚀 Features

- **PDF Text Extraction**: Uses LLMWhisperer API with PyPDF2 fallback
- **AI-Powered Analysis**: Enhanced pattern matching for 33+ policy sections
- **Professional Reports**: Generate PDF comparison reports
- **RESTful API**: Clean API endpoints for frontend integration
- **CORS Support**: Pre-configured for Next.js frontend
- **Comprehensive Coverage**: All major commercial insurance sections

## 📋 Supported Policy Sections

### Core Sections
- Fire & Allied Perils
- Buildings Combined
- Office Contents
- Business Interruption
- Motor General/Fleet
- Public Liability
- Employers' Liability
- SASRIA

### Additional Commercial Sections
- Professional Indemnity
- Cyber Insurance
- Machinery Breakdown
- Electronic Equipment
- Accounts Receivable
- Plant All Risk
- Contractor All Risk
- And 20+ more sections...

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip or conda

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Environment Setup (Optional)
Create a `.env` file:
```env
LLM_API_KEY=your_llm_whisperer_api_key
API_HOST=0.0.0.0
API_PORT=5000
```

### 3. Start the Server
```bash
python run.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

The API will be available at:
- **Local Development**: http://localhost:5000
- **Production**: https://mailbroker.ddns.net:5000
- **Documentation**: http://localhost:5000/docs (or https://mailbroker.ddns.net:5000/docs)
- **Redoc**: http://localhost:5000/redoc (or https://mailbroker.ddns.net:5000/redoc)

## 📚 API Endpoints

### Health & Status
- `GET /` - Root endpoint with API info
- `GET /api/health` - Health check

### Quote Processing
- `POST /api/quotes/upload` - Upload and process PDF quotes
- `GET /api/quotes/compare/{comparison_id}` - Get comparison results
- `GET /api/quotes/my-quotes` - Get user's quote history
- `GET /api/quotes/stats` - Get dashboard statistics

### Report Generation
- `POST /api/quotes/generate-report/{comparison_id}` - Generate PDF report
- `GET /api/reports/download/{filename}` - Download generated reports

## 🔗 Frontend Integration

### Next.js Integration (Running on Port 3000)

1. Copy the API client files to your Next.js project:
```bash
# Copy the API client
cp frontend-integration/api.ts /path/to/your/nextjs/lib/api.ts

# Copy the React hooks (optional)
cp frontend-integration/hooks.ts /path/to/your/nextjs/lib/hooks.ts
```

2. The API client auto-detects the environment:
   - **Development**: Uses `http://localhost:5000`
   - **Production** (on mailbroker.ddns.net): Uses `https://mailbroker.ddns.net:5000`

3. Use the API client in your components:
```typescript
import { insuranceAPI } from '@/lib/api';
// If using hooks:
import { useUserStats } from '@/lib/hooks';

// In a React component
const { stats, loading, error } = useUserStats();

// Upload quotes
const handleUpload = async (files: File[]) => {
  const response = await insuranceAPI.uploadQuotes(files);
  if (response.data) {
    console.log('Upload successful:', response.data);
  }
};
```

### Dashboard Integration Example
```typescript
// app/dashboard/page.tsx
import { useUserStats } from '@/lib/hooks';

export default function DashboardPage() {
  const { stats, loading, error } = useUserStats();

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="dashboard">
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Quotes</h3>
          <p>{stats?.total_quotes || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Completed</h3>
          <p>{stats?.completed || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Average Premium</h3>
          <p>{stats?.average_premium || 'R0'}</p>
        </div>
      </div>
    </div>
  );
}
```

## 🌐 Production Deployment

Your setup configuration:
- **Frontend**: Next.js on port 3000 → https://mailbroker.ddns.net:3000
- **Backend**: FastAPI on port 5000 → https://mailbroker.ddns.net:5000

### Environment Variables for Production
```env
LLM_API_KEY=your_production_api_key
API_HOST=0.0.0.0
API_PORT=5000
CORS_ORIGINS=["https://mailbroker.ddns.net:3000", "https://mailbroker.ddns.net"]
```

### Nginx Configuration (if needed)
```nginx
# Backend proxy
location /api/ {
    proxy_pass http://localhost:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

# Frontend proxy
location / {
    proxy_pass http://localhost:3000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

## 📊 Response Examples

### Upload Response
```json
{
  "comparison_id": "uuid-123",
  "status": "success",
  "message": "Successfully processed 2 quotes",
  "quote_count": 2,
  "results": [
    {
      "quote_number": 1,
      "vendor": "Hollard Insurance",
      "total_premium": "R3,250.50",
      "policy_sections": {
        "Fire": {
          "included": "Y",
          "premium": "R450.00",
          "sum_insured": "R1,200,000",
          "sub_sections": ["Building structure", "Contents"],
          "excess": "R5,000"
        }
      }
    }
  ]
}
```

### User Stats Response
```json
{
  "total_quotes": 8,
  "completed": 6,
  "processing": 0,
  "average_premium": "R2,875.25"
}
```

## 🎯 Key Improvements Over Original

### Enhanced Data Accuracy
- **Better Pattern Matching**: More sophisticated regex patterns for data extraction
- **Validation Logic**: Premium and sum insured validation by section type
- **Context-Aware Extraction**: Analyzes surrounding text for better accuracy

### Comprehensive Policy Coverage
- **33+ Policy Sections**: Complete commercial insurance coverage
- **Detailed Sub-sections**: Granular analysis of policy components
- **Enhanced Vendor Detection**: Improved insurance company identification

### Professional Architecture
- **Modular Design**: Clean separation of concerns
- **Type Safety**: Full Pydantic models for request/response
- **Error Handling**: Comprehensive error handling and logging
- **Scalable Structure**: Easy to extend and maintain

## 🚦 Development & Testing

### Run Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### API Testing
Use the built-in docs for testing:
- Visit http://localhost:5000/docs (or https://mailbroker.ddns.net:5000/docs)
- Click "Try it out" on any endpoint
- Upload sample PDFs and test responses

## 🎯 Quick Start Guide

1. **Start the Backend** (Port 5000):
```bash
cd /root/Sushi_Food/Financial_Analysis_System/backend
python run.py
```

2. **Test API**: Visit http://localhost:5000/docs

3. **Integrate with Your Next.js Frontend** (Port 3000):
```bash
# Copy API files to your Next.js project
cp frontend-integration/api.ts /path/to/nextjs/lib/
cp frontend-integration/hooks.ts /path/to/nextjs/lib/
```

4. **Access Your Application**:
   - Frontend: https://mailbroker.ddns.net:3000
   - Backend API: https://mailbroker.ddns.net:5000
   - API Docs: https://mailbroker.ddns.net:5000/docs

The backend is now configured to run on port 5000 and will automatically handle CORS for your frontend running on port 3000! 