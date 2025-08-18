from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime

class PolicySection(BaseModel):
    included: str
    premium: str
    sum_insured: str
    sub_sections: List[str]
    excess: str

class QuoteResult(BaseModel):
    quote_number: int
    vendor: str
    total_premium: str
    payment_terms: str
    contact_phone: str
    contact_email: str
    risk_address: str
    client_details: str
    quote_reference: str
    quote_date: str
    policy_sections: Dict[str, PolicySection]

class FileInfo(BaseModel):
    original_name: str
    stored_path: str
    size: int
    uploaded_at: str

class QuoteUploadResponse(BaseModel):
    comparison_id: str
    status: str
    message: str
    quote_count: int
    results: List[QuoteResult]

class ComparisonResponse(BaseModel):
    comparison_id: str
    user_id: str
    files: List[FileInfo]
    results: List[QuoteResult]
    created_at: str
    status: str

class QuoteSummary(BaseModel):
    comparison_id: str
    created_at: str
    status: str
    quote_count: int
    file_names: List[str]
    total_premiums: List[str]

class UserQuotesResponse(BaseModel):
    total_comparisons: int
    comparisons: List[QuoteSummary]

class UserStats(BaseModel):
    total_quotes: int
    completed: int
    processing: int
    average_premium: str

class ReportGenerationResponse(BaseModel):
    report_id: str
    filename: str
    download_url: str
    generated_at: str

class HealthCheckResponse(BaseModel):
    status: str
    timestamp: str

class ErrorResponse(BaseModel):
    detail: str
    status_code: int
    timestamp: str 