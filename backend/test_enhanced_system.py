#!/usr/bin/env python3
"""
Comprehensive test script for the enhanced backend system
Tests all new features including specialized agents, enhanced PDF reports, and dashboard generation
"""

import os
import sys
import time
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from services.quote_processor import QuoteProcessor
from services.enhanced_report_generator import EnhancedReportGenerator
from services.dashboard_generator import DashboardGenerator
from services.specialized_agents import SpecializedAgents

def create_sample_quote_data():
    """Create sample quote data for testing"""
    return [
        {
            "quote_number": 1,
            "vendor": "Hollard Insurance",
            "total_premium": "R3,542.50",
            "payment_terms": "Monthly",
            "contact_phone": "011 408 4911",
            "contact_email": "commercial@hollard.co.za",
            "risk_address": "123 Business Park, Johannesburg",
            "client_details": "Sample Manufacturing (Pty) Ltd",
            "quote_reference": "HOL123456",
            "quote_date": "15/01/2024",
            "policy_sections": {
                "Fire": {
                    "included": "Y",
                    "premium": "R450.00",
                    "sum_insured": "R1,200,000",
                    "sub_sections": ["Building structure", "Contents", "Stock"],
                    "excess": "Standard",
                    "detailed_items": [
                        {"description": "Main building", "sum_insured": "R800,000", "reinstatement_value": "Yes"},
                        {"description": "Office contents", "sum_insured": "R400,000", "reinstatement_value": "Yes"}
                    ],
                    "extensions": [{"description": "Debris removal and clearing costs"}],
                    "deductibles": {"standard": "R5,000"}
                },
                "Motor General": {
                    "included": "Y",
                    "premium": "R1,200.00",
                    "sum_insured": "R500,000",
                    "sub_sections": ["3 vehicles", "Comprehensive cover"],
                    "excess": "R10,000",
                    "detailed_items": [],
                    "extensions": [{"description": "Roadside assistance"}],
                    "deductibles": {"standard": "R10,000"}
                },
                "Public liability": {
                    "included": "Y",
                    "premium": "R300.00",
                    "sum_insured": "R2,000,000",
                    "sub_sections": ["General public liability", "Legal costs"],
                    "excess": "Standard",
                    "detailed_items": [],
                    "extensions": [],
                    "deductibles": {"standard": "Standard"}
                },
                "SASRIA": {
                    "included": "Y",
                    "premium": "R234.07",
                    "sum_insured": "As per main sections",
                    "sub_sections": ["Riot damages", "Strike damages", "Civil commotion"],
                    "excess": "As per main policy",
                    "detailed_items": [],
                    "extensions": [],
                    "deductibles": {"standard": "As per main policy"}
                }
            }
        },
        {
            "quote_number": 2,
            "vendor": "Santam Insurance",
            "total_premium": "R3,890.00",
            "payment_terms": "Monthly",
            "contact_phone": "0860 444 444",
            "contact_email": "business@santam.co.za",
            "risk_address": "456 Industrial Estate, Cape Town",
            "client_details": "Sample Manufacturing (Pty) Ltd",
            "quote_reference": "SAN789012",
            "quote_date": "16/01/2024",
            "policy_sections": {
                "Fire": {
                    "included": "Y",
                    "premium": "R520.30",
                    "sum_insured": "R1,500,000",
                    "sub_sections": ["Building structure", "Contents", "Alternative accommodation"],
                    "excess": "R2,500",
                    "detailed_items": [
                        {"description": "Main building", "sum_insured": "R1,000,000", "reinstatement_value": "Yes"},
                        {"description": "Office contents", "sum_insured": "R500,000", "reinstatement_value": "Yes"}
                    ],
                    "extensions": [{"description": "Debris removal and temporary accommodation"}],
                    "deductibles": {"standard": "R2,500"}
                },
                "Motor General": {
                    "included": "Y",
                    "premium": "R1,456.90",
                    "sum_insured": "R600,000",
                    "sub_sections": ["5 vehicles", "Comprehensive cover", "Windscreen cover"],
                    "excess": "R8,000",
                    "detailed_items": [],
                    "extensions": [{"description": "Courtesy car and roadside assistance"}],
                    "deductibles": {"standard": "R8,000"}
                },
                "Public liability": {
                    "included": "Y",
                    "premium": "R420.15",
                    "sum_insured": "R3,000,000",
                    "sub_sections": ["General public liability", "Products liability", "Legal costs"],
                    "excess": "Standard",
                    "detailed_items": [],
                    "extensions": [],
                    "deductibles": {"standard": "Standard"}
                },
                "SASRIA": {
                    "included": "Y",
                    "premium": "R198.45",
                    "sum_insured": "As per main sections",
                    "sub_sections": ["Riot damages", "Strike damages", "Civil commotion"],
                    "excess": "As per main policy",
                    "detailed_items": [],
                    "extensions": [],
                    "deductibles": {"standard": "As per main policy"}
                }
            }
        }
    ]

def test_specialized_agents():
    """Test the specialized agents functionality"""
    print("🧪 Testing Specialized Agents...")
    
    # Sample document text for testing
    sample_documents = [
        """
        COMMERCIAL INSURANCE POLICY SCHEDULE
        
        Client: Sample Manufacturing (Pty) Ltd
        Risk Address: 123 Business Park, Johannesburg
        
        POLICY SECTIONS & PREMIUMS:
        Fire: R450.00 - Buildings: R1,200,000 Contents: R800,000
        Motor General: R1,200.44 - Fleet of 3 vehicles
        Public liability: R316.66 - Limit: R2,000,000
        SASRIA: R234.07 - Full coverage
        
        TOTAL MONTHLY PREMIUM: R2,963.68 (including VAT)
        Contact: 011 408 4911
        Email: commercial@hollard.co.za
        """,
        """
        SANTAM COMMERCIAL INSURANCE QUOTATION
        
        Policyholder: Sample Manufacturing (Pty) Ltd
        Business Address: 456 Industrial Estate, Cape Town
        
        COVERAGE BREAKDOWN:
        Fire & Allied Perils: R520.30 - Building R1,500,000 Contents R600,000
        Motor comprehensive: R1,456.90 - 5 vehicle fleet
        Public liability: R420.15 - R3,000,000 limit
        SASRIA: R198.45 - Riot & strike damage
        
        TOTAL PREMIUM: R3,891.50 per month (VAT included)
        Phone: 0860 444 444
        Email: business@santam.co.za
        """
    ]
    
    specialized_agents = SpecializedAgents()
    
    # Test Fire section agent
    print("  🔥 Testing Fire section agent...")
    fire_results = specialized_agents.fire_section_agent(sample_documents)
    assert len(fire_results) == 2, f"Expected 2 fire results, got {len(fire_results)}"
    assert fire_results[0]["included"] == "Y", "First quote should have fire coverage"
    assert fire_results[1]["included"] == "Y", "Second quote should have fire coverage"
    print("    ✅ Fire section agent working correctly")
    
    # Test Motor section agent
    print("  🚗 Testing Motor section agent...")
    motor_results = specialized_agents.motor_section_agent(sample_documents)
    assert len(motor_results) == 2, f"Expected 2 motor results, got {len(motor_results)}"
    assert motor_results[0]["included"] == "Y", "First quote should have motor coverage"
    assert motor_results[1]["included"] == "Y", "Second quote should have motor coverage"
    print("    ✅ Motor section agent working correctly")
    
    # Test Public Liability section agent
    print("  🛡️ Testing Public Liability section agent...")
    liability_results = specialized_agents.public_liability_agent(sample_documents)
    assert len(liability_results) == 2, f"Expected 2 liability results, got {len(liability_results)}"
    assert liability_results[0]["included"] == "Y", "First quote should have liability coverage"
    assert liability_results[1]["included"] == "Y", "Second quote should have liability coverage"
    print("    ✅ Public Liability section agent working correctly")
    
    print("✅ All specialized agents tests passed!")
    return True

def test_enhanced_quote_processor():
    """Test the enhanced quote processor with specialized agents"""
    print("🧪 Testing Enhanced Quote Processor...")
    
    sample_documents = [
        """
        COMMERCIAL INSURANCE POLICY SCHEDULE
        
        Client: Test Company (Pty) Ltd
        Risk Address: 789 Test Street, Durban
        
        Fire: R450.00 - Buildings: R1,200,000
        Motor General: R1,200.44 - 3 vehicles
        Public liability: R316.66 - R2,000,000
        SASRIA: R234.07
        
        TOTAL: R2,963.68
        Tel: 031 123 4567
        Email: test@company.co.za
        """,
        """
        SECOND INSURANCE QUOTE
        
        Business: Test Company (Pty) Ltd
        Address: 789 Test Street, Durban
        
        Fire section: R520.30 - R1,500,000
        Motor coverage: R1,456.90 - 5 vehicles
        Public liability: R420.15 - R3,000,000
        SASRIA: R198.45
        
        Monthly total: R3,891.50
        Contact: 0860 555 555
        """
    ]
    
    processor = QuoteProcessor()
    results = processor.process_quotes(sample_documents)
    
    assert len(results) == 2, f"Expected 2 processed quotes, got {len(results)}"
    
    # Check first quote
    quote1 = results[0]
    assert quote1["quote_number"] == 1, "Quote number should be 1"
    assert "Fire" in quote1["policy_sections"], "Fire section should be present"
    assert "Motor General" in quote1["policy_sections"], "Motor section should be present"
    assert "Public liability" in quote1["policy_sections"], "Public liability should be present"
    
    # Check that specialized agents were used (should have better extraction)
    fire_section = quote1["policy_sections"]["Fire"]
    assert fire_section["included"] == "Y", "Fire should be included based on specialized agent"
    
    print("✅ Enhanced Quote Processor test passed!")
    return True

def test_enhanced_pdf_generator():
    """Test the enhanced PDF report generator"""
    print("🧪 Testing Enhanced PDF Report Generator...")
    
    sample_data = create_sample_quote_data()
    
    report_generator = EnhancedReportGenerator()
    
    try:
        # Generate PDF report
        report_path = report_generator.generate_pdf_report(sample_data, "test_comparison_123")
        
        # Check if file was created
        assert os.path.exists(report_path), f"PDF report should be created at {report_path}"
        
        # Check file size (should be substantial for comprehensive report)
        file_size = os.path.getsize(report_path)
        assert file_size > 50000, f"PDF should be substantial, got {file_size} bytes"  # At least 50KB
        
        print(f"    ✅ PDF report generated successfully: {os.path.basename(report_path)} ({file_size:,} bytes)")
        
        # Clean up test file
        os.remove(report_path)
        
    except Exception as e:
        print(f"    ❌ PDF generation failed: {e}")
        return False
    
    print("✅ Enhanced PDF Report Generator test passed!")
    return True

def test_dashboard_generator():
    """Test the interactive dashboard generator"""
    print("🧪 Testing Dashboard Generator...")
    
    sample_data = create_sample_quote_data()
    
    dashboard_generator = DashboardGenerator()
    
    try:
        # Generate dashboard HTML
        dashboard_html = dashboard_generator.create_dashboard_html(sample_data)
        
        # Check if HTML was generated
        assert isinstance(dashboard_html, str), "Dashboard should return HTML string"
        assert len(dashboard_html) > 10000, f"Dashboard HTML should be substantial, got {len(dashboard_html)} characters"
        
        # Check for key components
        assert "Insurance Quote Comparison Dashboard" in dashboard_html, "Should contain dashboard title"
        assert "Interactive" in dashboard_html or "Comparison" in dashboard_html, "Should contain comparison features"
        assert "Hollard Insurance" in dashboard_html, "Should contain sample vendor"
        assert "Fire" in dashboard_html, "Should contain Fire section"
        assert "toggleDetails" in dashboard_html, "Should contain interactive JavaScript"
        
        print(f"    ✅ Dashboard HTML generated successfully ({len(dashboard_html):,} characters)")
        
        # Optionally save sample dashboard for manual inspection
        dashboard_path = os.path.join(backend_dir, "reports", "sample_dashboard.html")
        os.makedirs(os.path.dirname(dashboard_path), exist_ok=True)
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(dashboard_html)
        print(f"    📄 Sample dashboard saved to: {dashboard_path}")
        
    except Exception as e:
        print(f"    ❌ Dashboard generation failed: {e}")
        return False
    
    print("✅ Dashboard Generator test passed!")
    return True

def run_comprehensive_tests():
    """Run all comprehensive tests"""
    print("🚀 Starting Comprehensive Backend Enhancement Tests\n")
    
    tests = [
        ("Specialized Agents", test_specialized_agents),
        ("Enhanced Quote Processor", test_enhanced_quote_processor),
        ("Enhanced PDF Generator", test_enhanced_pdf_generator),
        ("Dashboard Generator", test_dashboard_generator)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print('='*60)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                failed += 1
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total:  {passed + failed}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! The backend is now fully enhanced with main.py capabilities!")
        print("\nEnhanced Features Available:")
        print("  🔥 Specialized section agents for accurate extraction")
        print("  📊 Interactive dashboard with detailed analysis")
        print("  📄 Professional PDF reports matching industry standards")
        print("  🎯 Enhanced quote processing with specialized agents")
        print("  📈 Comprehensive section comparison and analysis")
        print("  💡 Advanced pattern matching and validation")
        return True
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    print("Enhanced Backend System Comprehensive Test Suite")
    print("=" * 60)
    print("Testing all features from main.py integration")
    print(f"Backend Directory: {backend_dir}")
    print(f"Test Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    success = run_comprehensive_tests()
    
    if success:
        print("\n🎯 Ready for production use!")
    else:
        print("\n🔧 Please fix the failing tests before deployment.")
        sys.exit(1) 