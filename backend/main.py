#!/usr/bin/env python3
"""
Enhanced Insurance Quote Comparison Backend API
Comprehensive LLMWhisperer + LLM + PDF Report Generation Pipeline
"""

import os
import uuid
import time
import shutil
import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials  
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

# Import our enhanced services
from config import settings
from services.pdf_extractor import PDFExtractor
from services.fpdf_report_generator import FPDFReportGenerator
from services.llm_integration import LLMIntegrationService
from openai import AsyncOpenAI
import asyncio

# Initialize services
pdf_extractor = PDFExtractor()
report_generator = FPDFReportGenerator()
llm_service = LLMIntegrationService()

# FastAPI app setup
app = FastAPI(
    title="🤖 AI-Enhanced Insurance Quote Comparison API",
    description="Comprehensive insurance quote analysis with LLMWhisperer + LLM + PDF Reports",
    version="3.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer(auto_error=False)

# In-memory storage (replace with database in production)
comparison_results: Dict[str, Dict] = {}
user_quotes: Dict[str, List[Dict]] = {}

# Pydantic models
class QuoteUploadResponse(BaseModel):
    comparison_id: str
    status: str
    message: str
    quote_count: int
    results: List[Dict]
    processing_time: float
    llm_analysis_enabled: bool
    report_generated: bool
    report_filename: Optional[str] = None

class UserStats(BaseModel):
    total_quotes: int
    completed: int
    processing: int
    average_premium: str

class QuoteSummary(BaseModel):
    comparison_id: str
    created_at: str
    status: str
    quote_count: int
    file_names: List[str]
    total_premiums: List[str]
    report_generated: bool = False
    report_filename: Optional[str] = None
    report_generated_at: Optional[str] = None

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Demo authentication - replace with real auth
    return {"user_id": "demo-user", "username": "demo"}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "🤖 AI-Enhanced Insurance Quote Comparison API",
        "version": "3.0",
        "features": [
            "LLMWhisperer v2 PDF text extraction",
            "Multi-LLM analysis (OpenAI, Anthropic, Google)",
            "Comprehensive PDF report generation",
            "40+ insurance policy sections",
            "AI-powered insights and recommendations"
        ],
        "endpoints": {
            "upload": "/api/quotes/upload",
            "my_quotes": "/api/quotes/my-quotes", 
            "health": "/api/health",
            "docs": "/docs"
        }
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "llmwhisperer": "✅ Available" if pdf_extractor.api_key else "❌ No API Key",
            "llm_integration": "✅ Ready",
            "pdf_generator": "✅ Ready"
        }
    }

@app.options("/api/quotes/upload")
async def upload_quotes_options():
    """Handle CORS preflight for upload endpoint"""
    return {"message": "OK"}

@app.post("/api/quotes/upload", response_model=QuoteUploadResponse)
async def upload_quotes(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    🚀 COMPREHENSIVE UPLOAD & PROCESSING PIPELINE - 2-3 QUOTES COMPARISON
    1. Upload 2-3 PDF quotes for comparison
    2. Extract text with LLMWhisperer v2 Official Client
    3. Analyze with LLM (if available) 
    4. Generate comprehensive side-by-side PDF comparison report
    """
    start_time = time.time()
    
    # Validate number of files (2-3 quotes for optimal comparison)
    if len(files) < 2:
        raise HTTPException(
            status_code=400, 
            detail="Please upload at least 2 quote files for comparison. The system works best with 2-3 quotes."
        )
    
    if len(files) > 3:
        raise HTTPException(
            status_code=400, 
            detail="Please upload maximum 3 quote files for optimal comparison display. Additional files will be ignored."
        )

    user_id = current_user["user_id"]
    comparison_id = str(uuid.uuid4())
    
    print(f"🚀 Starting comprehensive processing for comparison {comparison_id}")
    print(f"📁 Processing {len(files)} files for side-by-side comparison...")
    
    # Limit to 3 files for optimal display
    files_to_process = files[:3]
    
    # Step 1: Upload and extract text from PDFs
    documents = []
    file_info = []
    
    for i, file in enumerate(files_to_process):
        if not file.filename.lower().endswith('.pdf'):
            continue

        # Check file size
        if file.size and file.size > settings.MAX_FILE_SIZE:
            max_size_mb = settings.MAX_FILE_SIZE // (1024 * 1024)
            raise HTTPException(
                status_code=413, 
                detail=f"File {file.filename} is too large. Maximum size is {max_size_mb}MB."
            )

        # Save uploaded file
        timestamp = int(time.time())
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(settings.UPLOAD_DIR, safe_filename)
        
        with open(file_path, "wb") as output_file:
            shutil.copyfileobj(file.file, output_file)

        # Extract text using LLMWhisperer
        print(f"📄 Extracting text from: {file.filename}")
        try:
            extracted_text = pdf_extractor.extract_text(file_path)
            
            if not extracted_text or len(extracted_text.strip()) < 50:
                print(f"⚠️ Low quality extraction for {file.filename}, using fallback...")
                extracted_text = pdf_extractor._extract_fallback(file_path)
            
            documents.append({
                'extracted_text': extracted_text,
                'file_path': file_path,
                'original_filename': file.filename,
                'quote_id': f"quote_{i+1}"
            })
            
            file_info.append({
                "original_name": file.filename,
                "stored_path": file_path,
                "size": os.path.getsize(file_path),
                "uploaded_at": datetime.now().isoformat(),
                "extraction_success": True,
                "text_length": len(extracted_text)
            })
            
            print(f"✅ Successfully extracted {len(extracted_text):,} characters from {file.filename}")
            
        except Exception as e:
            print(f"❌ Error processing {file.filename}: {e}")
            continue

    if not documents:
        raise HTTPException(status_code=400, detail="No valid PDF files could be processed.")

    try:
        # Step 2: Enhanced LLM Analysis
        print(f"🧠 Starting LLM-enhanced analysis of {len(documents)} documents...")
        results = []
        
        for i, doc in enumerate(documents):
            print(f"🔍 Analyzing document {i+1}/{len(documents)}: {doc['original_filename']}")
            
            # Use LLM service for comprehensive analysis
            try:
                llm_analysis = llm_service.analyze_insurance_quote(doc['extracted_text'], i+1)
                structured_data = llm_service.extract_structured_data(doc['extracted_text'])
                risk_assessment = llm_service.assess_risks(doc['extracted_text'])
                coverage_gaps = llm_service.identify_coverage_gaps(doc['extracted_text'])
                
                # Create comprehensive result
                result = {
                    "quote_number": i + 1,
                    "quote_id": doc['quote_id'],
                    "original_filename": doc['original_filename'],
                    "extracted_text": doc['extracted_text'],
                    
                    # LLM Analysis Results
                    "llm_analysis": llm_analysis,
                    "structured_data": structured_data,
                    "risk_assessment": risk_assessment,
                    "coverage_gaps": coverage_gaps,
                    
                    # Extract key fields for backward compatibility
                    "vendor": llm_analysis.get("company_name", f"Insurance Company {i+1}"),
                    "total_premium": llm_analysis.get("total_premium", "N/A"),
                    "policy_type": llm_analysis.get("policy_type", "Commercial Insurance"),
                    "policy_sections": llm_analysis.get("policy_sections", {}),
                    "key_benefits": llm_analysis.get("key_benefits", []),
                    "contact_info": llm_analysis.get("contact_info", {}),
                    "broker_details": llm_analysis.get("broker_details", {}),
                    
                    # Processing metadata
                    "processing_method": "LLM Enhanced" if (llm_service.openai_api_key or llm_service.anthropic_api_key or llm_service.google_api_key) else "Pattern Matching",
                    "analysis_timestamp": datetime.now().isoformat()
                }
                
                results.append(result)
                print(f"✅ Analysis complete for {doc['original_filename']} - {result['vendor']}")
                
            except Exception as e:
                print(f"❌ Analysis failed for {doc['original_filename']}: {e}")
                # Create basic result as fallback
                result = {
                    "quote_number": i + 1,
                    "quote_id": doc['quote_id'],
                    "original_filename": doc['original_filename'],
                    "extracted_text": doc['extracted_text'],
                    "vendor": f"Insurance Company {i+1}",
                    "total_premium": "N/A",
                    "policy_type": "Commercial Insurance",
                    "processing_method": "Basic Extraction",
                    "analysis_timestamp": datetime.now().isoformat(),
                    "error": str(e)
                }
                results.append(result)

        # Step 3: Store comparison data
        comparison_data = {
            "comparison_id": comparison_id,
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "status": "completed",
            "results": results,
            "files": file_info,
            "processing_time": time.time() - start_time,
            "llm_analysis_enabled": bool(llm_service.openai_api_key or llm_service.anthropic_api_key or llm_service.google_api_key)
        }
        
        comparison_results[comparison_id] = comparison_data
        
        if user_id not in user_quotes:
            user_quotes[user_id] = []
        user_quotes[user_id].append(comparison_data)

        # Step 4: 🆕 AUTOMATIC PDF REPORT GENERATION
        print(f"📊 Automatically generating comprehensive PDF report for comparison {comparison_id}...")
        try:
            pdf_path = report_generator.generate_pdf_report(results, comparison_id)
            filename = os.path.basename(pdf_path)
            print(f"✅ Comprehensive PDF report generated: {filename}")
            
            # Update comparison data with report info
            comparison_data["report_generated"] = True
            comparison_data["report_filename"] = filename
            comparison_data["report_generated_at"] = datetime.now().isoformat()
            comparison_data["report_path"] = pdf_path
            
            # Update stored data
            comparison_results[comparison_id] = comparison_data
            if user_id in user_quotes:
                for quote in user_quotes[user_id]:
                    if quote["comparison_id"] == comparison_id:
                        quote.update({
                            "report_generated": True,
                            "report_filename": filename,
                            "report_generated_at": datetime.now().isoformat()
                        })
                        break
            
        except Exception as e:
            print(f"⚠️ PDF report generation failed: {e}")
            comparison_data["report_generated"] = False
            comparison_data["report_error"] = str(e)

        processing_time = time.time() - start_time
        print(f"🎉 Complete processing finished in {processing_time:.2f} seconds")

        return QuoteUploadResponse(
            comparison_id=comparison_id,
            status="completed",
            message=f"Successfully processed {len(results)} quotes with comprehensive LLM analysis and PDF report generation",
            quote_count=len(results),
            results=results,
            processing_time=processing_time,
            llm_analysis_enabled=comparison_data["llm_analysis_enabled"],
            report_generated=comparison_data.get("report_generated", False),
            report_filename=comparison_data.get("report_filename")
        )

    except Exception as e:
        print(f"❌ Processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/api/quotes/compare/{comparison_id}")
async def get_comparison(comparison_id: str, current_user: dict = Depends(get_current_user)):
    """Get comparison results"""
    if comparison_id not in comparison_results:
        raise HTTPException(status_code=404, detail="Comparison not found")
    
    return comparison_results[comparison_id]["results"]

@app.get("/api/quotes/my-quotes")
async def get_user_quotes(current_user: dict = Depends(get_current_user)):
    """Get user's quotes with enhanced information"""
    user_id = current_user["user_id"]
    user_comparisons = user_quotes.get(user_id, [])
    
    # Return enhanced summary info
    summaries = []
    for comp in user_comparisons:
        summary = {
            "comparison_id": comp["comparison_id"],
            "created_at": comp["created_at"],
            "status": comp["status"],
            "quote_count": len(comp["results"]),
            "file_names": [f["original_name"] for f in comp["files"]],
            "total_premiums": [r.get("total_premium", "N/A") for r in comp["results"]],
            "processing_time": comp.get("processing_time", 0),
            "llm_analysis_enabled": comp.get("llm_analysis_enabled", False),
            # Report information
            "report_generated": comp.get("report_generated", False),
            "report_filename": comp.get("report_filename", None),
            "report_generated_at": comp.get("report_generated_at", None)
        }
        summaries.append(summary)
    
    return {
        "total_comparisons": len(summaries),
        "comparisons": summaries
    }

@app.get("/api/quotes/stats")
async def get_user_stats(current_user: dict = Depends(get_current_user)):
    """Get user statistics"""
    user_id = current_user["user_id"]
    user_comparisons = user_quotes.get(user_id, [])
    
    total_quotes = sum(len(comp["results"]) for comp in user_comparisons)
    completed = len([comp for comp in user_comparisons if comp["status"] == "completed"])
    processing = len([comp for comp in user_comparisons if comp["status"] == "processing"])
    
    # Calculate average premium
    all_premiums = []
    for comp in user_comparisons:
        for result in comp["results"]:
            premium_str = result.get("total_premium", "N/A")
            if premium_str != "N/A" and premium_str.startswith("R "):
                try:
                    amount = float(premium_str.replace("R ", "").replace(",", ""))
                    all_premiums.append(amount)
                except:
                    continue
    
    average_premium = f"R {sum(all_premiums) / len(all_premiums):,.2f}" if all_premiums else "N/A"
    
    return UserStats(
        total_quotes=total_quotes,
        completed=completed,
        processing=processing,
        average_premium=average_premium
    )

@app.get("/api/reports/download/{filename}")
async def download_report(filename: str, current_user: dict = Depends(get_current_user)):
    """Download generated PDF report"""
    file_path = os.path.join(settings.REPORTS_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Report not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/pdf',
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.post("/api/quotes/generate-report/{comparison_id}")
async def generate_report_manual(comparison_id: str, current_user: dict = Depends(get_current_user)):
    """Manual PDF report generation (backup endpoint)"""
    if comparison_id not in comparison_results:
        raise HTTPException(status_code=404, detail="Comparison not found")
    
    comparison_data = comparison_results[comparison_id]
    
    try:
        print(f"📊 Manually generating PDF report for comparison {comparison_id}...")
        pdf_path = report_generator.generate_pdf_report(comparison_data["results"], comparison_id)
        filename = os.path.basename(pdf_path)
        
        # Update comparison data
        comparison_data["report_generated"] = True
        comparison_data["report_filename"] = filename
        comparison_data["report_generated_at"] = datetime.now().isoformat()
        
        return {
            "report_id": comparison_id,
            "filename": filename,
            "download_url": f"/api/reports/download/{filename}",
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting AI-Enhanced Insurance Quote Comparison Backend...")
    print("📋 Comprehensive LLMWhisperer + LLM + PDF Report Pipeline")
    print(f"🔗 Backend API will be available at: http://{settings.API_HOST}:{settings.API_PORT}")
    print(f"📚 API Documentation: http://{settings.API_HOST}:{settings.API_PORT}/docs")
    
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
        log_level="info"
    ) 