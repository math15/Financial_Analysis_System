import os
from pathlib import Path

class Settings:
    """Application settings and configuration"""
    
    # API Configuration
    API_TITLE = "Insurance Quote Comparison API"
    API_VERSION = "2.0"
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "5000"))
    
    # Directories
    BASE_DIR = Path(__file__).parent
    UPLOAD_DIR = BASE_DIR / "uploads"
    REPORTS_DIR = BASE_DIR / "reports"
    
    # Create directories if they don't exist
    UPLOAD_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)
    
    # LLM API Configuration (LLMWhisperer v2)
    LLM_API_KEY = os.getenv("LLM_API_KEY", os.getenv("LLMWHISPERER_API_KEY", "T4HccvP3IujppTUdbQFX8aLIXs_9y0o3yLPQNiWinQQ"))
    LLM_API_URL = "https://llmwhisperer-api.us-central.unstract.com/api/v2"  # v2 API (current version)
    # EU Region alternative: https://llmwhisperer-api.eu-west.unstract.com/api/v2
    
    # Processing Mode Configuration
    USE_LLM_API = os.getenv("USE_LLM_API", "true").lower() == "true"  # Enable/disable LLM API
    FALLBACK_TO_LOCAL = os.getenv("FALLBACK_TO_LOCAL", "true").lower() == "true"  # Always fallback to local
    LOCAL_PROCESSING_ONLY = os.getenv("LOCAL_PROCESSING_ONLY", "false").lower() == "true"  # Force local only
    
    # CORS Settings  
    ALLOWED_ORIGINS = [
        # Allow all origins temporarily for testing
        "*"
        # Development
        # "http://localhost:3000",
        # "http://127.0.0.1:3000",
        # Production - Frontend domain
        # "https://mailbroker.ddns.net",
        # "http://mailbroker.ddns.net",
        # Production - Backend domain (if needed)
        # "https://apimailbroker.ddns.net",
        # "http://apimailbroker.ddns.net"
    ]
    
    # File Upload Settings
    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB
    ALLOWED_EXTENSIONS = [".pdf"]
    
    # Processing Settings
    MAX_CONCURRENT_UPLOADS = 5
    PROCESSING_TIMEOUT = 300  # 5 minutes
    
    # Enhanced Insurance Policy Sections - Complete Commercial Coverage
    POLICY_SECTIONS = [
        # Core Commercial Sections
        "Fire", "Buildings combined", "Office contents", "Business interruption",
        "General", "Theft", "Money", "Glass", "Fidelity guarantee", "Goods in transit",
        "Business all risks", "Accidental damage", "Public liability", "Employers' liability",
        "Stated benefits", "Group personal accident", "Motor personal accident",
        "Motor General", "Motor Specific/Specified", "Motor Fleet", "Electronic equipment",
        "Umbrella liability", "Assist/Value services/ VAS", "SASRIA", "Intermediary fee",
        
        # Additional Commercial Insurance Sections (as per requirements)
        "Accounts receivable", "Motor Industry Risks", "Houseowners", "Machinery Breakdown",
        "Householders", "Personal, All Risks", "Watercraft", "Personal Legal Liability",
        "Deterioration of Stock", "Personal Umbrella Liability", "Greens and Irrigation Systems",
        "Commercial Umbrella Liability", "Professional Indemnity", "Cyber", 
        "Community & Sectional Title", "Plant All risk", "Contractor All Risk", "Hospitality"
    ]
    
    # Sub-sections for detailed analysis - Complete Commercial Coverage
    SECTION_SUBSECTIONS = {
        # Core Sections with Enhanced Sub-sections
        "Fire": ["Building structure", "Contents", "Stock", "Loss of rent", "Debris removal", "Alternative accommodation", "Rent receivable", "Machinery", "Equipment"],
        "Buildings combined": ["Main building", "Outbuildings", "Boundary walls", "Fixed improvements", "Tenant's improvements", "Signs", "Landscaping", "Carports", "Storage facilities"],
        "Office contents": ["Furniture & fittings", "Office equipment", "Computer equipment", "Personal effects", "Stock", "Documents", "Artwork", "Antiques", "Electronics"],
        "Motor General": ["Comprehensive cover", "Third party", "Fire & theft", "Windscreen cover", "Roadside assistance", "Courtesy car", "Hire car", "Medical expenses"],
        "Public liability": ["General public liability", "Products liability", "Professional indemnity", "Legal costs", "Cross liability", "Tenant's liability", "Employer's liability"],
        "SASRIA": ["Riot damages", "Strike damages", "Civil commotion", "Terrorism cover", "Political violence", "Social unrest", "Malicious damage"],
        
        # Additional Commercial Sections with Detailed Sub-sections
        "Accounts receivable": ["Books of account", "Computer records", "Outstanding debtors", "Mercantile collections", "Credit sales", "Bad debts", "Collection costs"],
        "Motor Industry Risks": ["Stock in trade", "Customers vehicles", "Tools and equipment", "Liability", "Showroom contents", "Spare parts", "Workshop equipment"], 
        "Machinery Breakdown": ["Mechanical breakdown", "Electrical breakdown", "Explosion", "Expediting expenses", "Replacement parts", "Labour costs", "Loss of income"],
        "Professional Indemnity": ["Errors and omissions", "Legal costs", "Documents", "Loss of data", "Defense costs", "Settlement costs", "Regulatory fines"],
        "Cyber": ["Data breach", "Cyber attack", "Business interruption", "System restoration", "Legal costs", "Notification costs", "Credit monitoring", "Ransomware"],
        "Watercraft": ["Hull damage", "Third party liability", "Personal accident", "Salvage costs", "Wreck removal", "Pollution liability", "Medical expenses"],
        "Personal Legal Liability": ["Legal costs", "Damages awarded", "Defense costs", "Bail bonds", "Court costs", "Settlement costs"],
        "Plant All risk": ["Construction plant", "Contractors equipment", "Hired in plant", "Transit", "Testing", "Commissioning", "Maintenance"],
        "Contractor All Risk": ["Contract works", "Plant and equipment", "Third party liability", "Professional indemnity", "Delay in start-up", "Testing", "Maintenance"],
        "Hospitality": ["Public liability", "Product liability", "Liquor liability", "Employment practices", "Food safety", "Guest property", "Business interruption"],
        
        # Additional Sections
        "Business interruption": ["Loss of gross profit", "Increased cost of working", "Claims preparation", "Accountants fees", "Loss of rent", "Debtors", "Book debts"],
        "Electronic equipment": ["Computers", "Servers", "Networking equipment", "Software", "Data", "Peripherals", "Mobile devices", "IoT devices"],
        "Theft": ["Burglary", "Robbery", "Employee dishonesty", "Money", "Securities", "Stock", "Equipment", "Contents"],
        "Money": ["Cash", "Cheques", "Credit cards", "Bank notes", "Coins", "Postal orders", "Gift vouchers", "Travellers cheques"],
        "Glass": ["Windows", "Doors", "Skylights", "Shop fronts", "Display cases", "Mirrors", "Signs", "Fittings"],
        "Fidelity guarantee": ["Employee dishonesty", "Fraud", "Theft", "Embezzlement", "Forgery", "Computer fraud", "Funds transfer fraud"],
        "Goods in transit": ["Road transport", "Rail transport", "Air transport", "Sea transport", "Temporary storage", "Loading/unloading", "Packing materials"],
        "Accidental damage": ["Impact damage", "Falling objects", "Collision", "Spillage", "Breakage", "Vandalism", "Natural disasters"],
        "Employers' liability": ["Workplace accidents", "Occupational diseases", "Medical expenses", "Rehabilitation", "Legal costs", "Compensation"],
        "Umbrella liability": ["Excess liability", "Aggregate limits", "Worldwide coverage", "Additional insureds", "Defense costs", "Settlement costs"],
        "Assist/Value services/ VAS": ["Emergency assistance", "Legal helpline", "Medical assistance", "Travel assistance", "Home assistance", "24/7 support"],
        "Intermediary fee": ["Brokerage", "Administration fees", "Policy fees", "Service charges", "Documentation fees", "Processing fees"]
    }

# Create global settings instance
settings = Settings() 