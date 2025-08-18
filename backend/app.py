 from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import shutil, os, re, time, requests, uvicorn
from typing import Dict, List, Optional
import json
from datetime import datetime
import uuid
from pathlib import Path

# Import services
from services.pdf_extractor import PDFExtractor
from services.quote_processor import QuoteProcessor
from services.enhanced_report_generator import EnhancedReportGenerator  # Updated import
from services.dashboard_generator import DashboardGenerator  # New import
from models.schemas import QuoteUploadResponse, ComparisonResponse, UserStats
from config import settings

# File upload configuration
MAX_FILE_SIZE = settings.MAX_FILE_SIZE  # Use config value

# === FastAPI Application ===
app = FastAPI(
    title="Insurance Quote Comparison API",
    description="Backend API for analyzing and comparing insurance quotes",
    version="2.0"
)

# Configure maximum file size (20MB)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,  # Must be False when allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

# Security
security = HTTPBearer()

# Initialize services
pdf_extractor = PDFExtractor()
quote_processor = QuoteProcessor()
report_generator = EnhancedReportGenerator()  # Updated to use enhanced version
dashboard_generator = DashboardGenerator()  # New dashboard generator

# In-memory storage (replace with database in production)
comparison_results = {}
user_quotes = {}

# === Authentication ===
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Simple authentication - replace with proper JWT validation in production"""
    if credentials.credentials != "demo-token":
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return {"user_id": "demo-user", "username": "demo"}

# === API ENDPOINTS ===

@app.get("/")
def read_root():
    """API Health check"""
    return {
        "message": "Insurance Quote Comparison API",
        "version": "2.0",
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.options("/api/quotes/upload")
async def upload_options():
    """Handle CORS preflight for upload endpoint"""
    from fastapi.responses import Response
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Max-Age"] = "600"
    return response

@app.post("/api/quotes/upload", response_model=QuoteUploadResponse)
async def upload_quotes(
    files: list[UploadFile] = File(..., max_length=MAX_FILE_SIZE),
    current_user: dict = Depends(get_current_user)
):
    """Upload and process insurance quote files"""
    # Add explicit CORS headers
    from fastapi.responses import Response
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    
    if len(files) < 1:
        raise HTTPException(status_code=400, detail="Please upload at least 1 quote file.")

    user_id = current_user["user_id"]
    comparison_id = str(uuid.uuid4())
    
    # Process uploaded files
    documents = []
    file_info = []
    
    for file in files:
        if not file.filename.lower().endswith('.pdf'):
            continue

        # Check file size (20MB limit)
        if file.size and file.size > MAX_FILE_SIZE:
            max_size_mb = MAX_FILE_SIZE // (1024 * 1024)
            raise HTTPException(
                status_code=413, 
                detail=f"File {file.filename} is too large. Maximum size is {max_size_mb}MB."
            )

        # Create unique filename
        timestamp = int(time.time())
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(settings.UPLOAD_DIR, safe_filename)
        
        with open(file_path, "wb") as output_file:
            shutil.copyfileobj(file.file, output_file)

        print(f"📄 Extracting text from: {file.filename}")
        try:
            extracted_text = pdf_extractor.extract_text(file_path)
            documents.append(extracted_text)
            
            file_info.append({
                "original_name": file.filename,
                "stored_path": file_path,
                "size": os.path.getsize(file_path),
                "uploaded_at": datetime.now().isoformat()
            })
        except Exception as e:
            print(f"❌ Error processing {file.filename}: {e}")
            # Continue with other files
            continue

    if not documents:
        raise HTTPException(status_code=400, detail="No valid PDF files could be processed.")

    try:
        # Process documents using quote processor
        results = []
        for i, doc in enumerate(documents):
            result = quote_processor.parse_insurance_quote(doc, i + 1)
            results.append(result)

        # Store results
        comparison_data = {
            "comparison_id": comparison_id,
            "user_id": user_id,
            "files": file_info,
            "results": results,
            "created_at": datetime.now().isoformat(),
            "status": "completed"
        }
        
        comparison_results[comparison_id] = comparison_data
        
        if user_id not in user_quotes:
            user_quotes[user_id] = []
        user_quotes[user_id].append(comparison_data)

        return {
            "comparison_id": comparison_id,
            "status": "success",
            "message": f"Successfully processed {len(results)} quotes",
            "quote_count": len(results),
            "results": results
        }

    except Exception as e:
        print(f"❌ Error processing quotes: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing quotes: {str(e)}")

@app.get("/api/quotes/compare/{comparison_id}", response_model=ComparisonResponse)
def get_comparison(
    comparison_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get comparison results by ID"""
    if comparison_id not in comparison_results:
        raise HTTPException(status_code=404, detail="Comparison not found")
    
    data = comparison_results[comparison_id]
    
    # Check user ownership
    if data["user_id"] != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return ComparisonResponse(**data)

@app.get("/api/quotes/my-quotes")
def get_user_quotes_endpoint(current_user: dict = Depends(get_current_user)):
    """Get all quotes for the current user"""
    user_id = current_user["user_id"]
    user_comparisons = user_quotes.get(user_id, [])
    
    # Return summary info
    summaries = []
    for comp in user_comparisons:
        summary = {
            "comparison_id": comp["comparison_id"],
            "created_at": comp["created_at"],
            "status": comp["status"],
            "quote_count": len(comp["results"]),
            "file_names": [f["original_name"] for f in comp["files"]],
            "total_premiums": [r.get("total_premium", "N/A") for r in comp["results"]],
            # 🆕 Add report information for download functionality
            "report_generated": comp.get("report_generated", False),
            "report_filename": comp.get("report_filename", None),
            "report_generated_at": comp.get("report_generated_at", None)
        }
        summaries.append(summary)
    
    return {
        "total_comparisons": len(summaries),
        "comparisons": summaries
    }

@app.get("/api/quotes/stats", response_model=UserStats)
def get_user_stats(current_user: dict = Depends(get_current_user)):
    """Get user statistics for dashboard"""
    user_id = current_user["user_id"]
    user_comparisons = user_quotes.get(user_id, [])
    
    total_quotes = sum(len(comp["results"]) for comp in user_comparisons)
    completed = len([comp for comp in user_comparisons if comp["status"] == "completed"])
    processing = len([comp for comp in user_comparisons if comp["status"] == "processing"])
    
    # Calculate average premium
    all_premiums = []
    for comp in user_comparisons:
        for result in comp["results"]:
            premium_str = result.get("total_premium", "R0")
            amount = re.sub(r'[^\d.]', '', premium_str)
            if amount:
                try:
                    all_premiums.append(float(amount))
                except ValueError:
                    pass
    
    avg_premium = sum(all_premiums) / len(all_premiums) if all_premiums else 0
    
    return UserStats(
        total_quotes=total_quotes,
        completed=completed,
        processing=processing,
        average_premium=f"R{avg_premium:,.2f}".rstrip('0').rstrip('.') if avg_premium > 0 else "R0"
    )

@app.post("/api/quotes/generate-report/{comparison_id}")
def generate_report(
    comparison_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Generate PDF report for comparison"""
    if comparison_id not in comparison_results:
        raise HTTPException(status_code=404, detail="Comparison not found")
    
    data = comparison_results[comparison_id]
    
    # Check user ownership
    if data["user_id"] != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        # Generate report
        report_path = report_generator.generate_pdf_report(data["results"], comparison_id)
        
        filename = os.path.basename(report_path)
        
        return {
            "report_id": comparison_id,
            "filename": filename,
            "download_url": f"/api/reports/download/{filename}",
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating PDF report: {str(e)}")

@app.get("/api/reports/download/{filename}")
def download_report(filename: str):
    """Download generated report"""
    file_path = os.path.join(settings.REPORTS_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Report not found")
    
    return FileResponse(
        file_path,
        filename=filename,
        media_type='application/pdf'
    )

@app.get("/api/quotes/dashboard/{comparison_id}")
def get_dashboard(
    comparison_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Generate and return interactive dashboard HTML"""
    if comparison_id not in comparison_results:
        raise HTTPException(status_code=404, detail="Comparison not found")
    
    data = comparison_results[comparison_id]
    
    # Check user ownership
    if data["user_id"] != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        # Generate interactive dashboard HTML
        dashboard_html = dashboard_generator.create_dashboard_html(data["results"])
        
        from fastapi.responses import HTMLResponse
        return HTMLResponse(content=dashboard_html)
        
    except Exception as e:
        print(f"❌ Error generating dashboard: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating dashboard: {str(e)}")

# === Application Startup ===
if __name__ == "__main__":
    print("🚀 Starting Insurance Quote Comparison Backend API...")
    print("📋 Professional backend for Next.js frontend integration")
    print("🔗 Backend API will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")

    uvicorn.run(
        "app:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )