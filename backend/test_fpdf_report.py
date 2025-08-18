#!/usr/bin/env python3
"""
Test script for FPDF report generation
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.fpdf_report_generator import FPDFReportGenerator
import time

def test_fpdf_report_generation():
    """Test FPDF report generation with sample data"""
    print("🧪 Testing FPDF Report Generation")
    print("=" * 45)
    
    # Create sample quote data
    sample_data = [
        {
            "quote_number": 1,
            "vendor": "Hollard Insurance",
            "total_premium": "R2,963.68",
            "payment_terms": "Monthly",
            "contact_phone": "011 408 4911",
            "contact_email": "commercial@hollard.co.za",
            "risk_address": "123 Business Street, Johannesburg",
            "client_details": "Sample Manufacturing (Pty) Ltd",
            "quote_reference": "HOL-2024-001",
            "quote_date": "14/08/2024",
            "policy_sections": {
                "Fire": {"included": "Y", "premium": "R450.00", "sum_insured": "R2,000,000"},
                "Buildings combined": {"included": "Y", "premium": "R971.45", "sum_insured": "R2,000,000"},
                "Office contents": {"included": "Y", "premium": "R118.11", "sum_insured": "R500,000"},
                "Motor General": {"included": "Y", "premium": "R812.44", "sum_insured": "Fleet of 3"},
                "Public liability": {"included": "Y", "premium": "R316.66", "sum_insured": "R2,000,000"},
                "SASRIA": {"included": "Y", "premium": "R234.07", "sum_insured": "Full coverage"},
                "Electronic equipment": {"included": "Y", "premium": "R89.50", "sum_insured": "R300,000"},
                "Theft": {"included": "N", "premium": "-", "sum_insured": "-"}
            }
        },
        {
            "quote_number": 2,
            "vendor": "Bytes Insurance",
            "total_premium": "R3,891.50",
            "payment_terms": "Monthly",
            "contact_phone": "0860 444 444",
            "contact_email": "business@bytes.co.za",
            "risk_address": "456 Commercial Avenue, Cape Town",
            "client_details": "Olijvenhof Owner Association",
            "quote_reference": "BYT-2024-002",
            "quote_date": "14/08/2024",
            "policy_sections": {
                "Fire": {"included": "Y", "premium": "R520.30", "sum_insured": "R2,100,000"},
                "Buildings combined": {"included": "Y", "premium": "R1,245.80", "sum_insured": "R2,200,000"},
                "Office contents": {"included": "Y", "premium": "R95.40", "sum_insured": "R450,000"},
                "Motor General": {"included": "Y", "premium": "R1,156.90", "sum_insured": "5 vehicle fleet"},
                "Public liability": {"included": "Y", "premium": "R420.15", "sum_insured": "R3,000,000"},
                "SASRIA": {"included": "Y", "premium": "R198.45", "sum_insured": "Full coverage"},
                "Electronic equipment": {"included": "Y", "premium": "R67.80", "sum_insured": "R250,000"},
                "Theft": {"included": "Y", "premium": "R45.30", "sum_insured": "R150,000"}
            }
        },
        {
            "quote_number": 3,
            "vendor": "Santam Commercial",
            "total_premium": "R2,745.20",
            "payment_terms": "Monthly",
            "contact_phone": "0860 444 555",
            "contact_email": "commercial@santam.co.za",
            "risk_address": "789 Industrial Park, Durban",
            "client_details": "Tech Solutions (Pty) Ltd",
            "quote_reference": "SAN-2024-003",
            "quote_date": "14/08/2024",
            "policy_sections": {
                "Fire": {"included": "Y", "premium": "R380.90", "sum_insured": "R1,800,000"},
                "Buildings combined": {"included": "Y", "premium": "R756.20", "sum_insured": "R1,900,000"},
                "Office contents": {"included": "Y", "premium": "R134.60", "sum_insured": "R550,000"},
                "Motor General": {"included": "Y", "premium": "R945.70", "sum_insured": "Commercial vehicles"},
                "Public liability": {"included": "Y", "premium": "R298.80", "sum_insured": "R1,500,000"},
                "SASRIA": {"included": "Y", "premium": "R167.30", "sum_insured": "Civil unrest"},
                "Electronic equipment": {"included": "N", "premium": "-", "sum_insured": "-"},
                "Theft": {"included": "Y", "premium": "R62.10", "sum_insured": "R200,000"}
            }
        }
    ]
    
    # Initialize FPDF report generator
    fpdf_generator = FPDFReportGenerator()
    
    try:
        # Generate PDF report
        print("📄 Generating FPDF report...")
        comparison_id = "fpdf-test-123"
        
        pdf_path = fpdf_generator.generate_pdf_report(sample_data, comparison_id)
        
        # Check if file was created
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print("✅ FPDF report generated successfully!")
            print(f"📂 File location: {pdf_path}")
            print(f"📊 File size: {file_size:,} bytes")
            
            # Show absolute path for easy access
            abs_path = os.path.abspath(pdf_path)
            print(f"🔗 Absolute path: {abs_path}")
            
            # List all files in reports directory
            reports_dir = "reports"
            if os.path.exists(reports_dir):
                files_in_reports = os.listdir(reports_dir)
                print(f"📂 All files in reports directory: {files_in_reports}")
            
        else:
            print("❌ PDF file was not created!")
            
    except Exception as e:
        print(f"❌ Error generating FPDF report: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_fpdf_report_generation() 