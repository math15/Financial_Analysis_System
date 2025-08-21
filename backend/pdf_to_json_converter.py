#!/usr/bin/env python3
"""
PDF to JSON Converter for Category Agents
Extracts insurance quote data from PDFs and saves as JSON files.

Usage:
  python pdf_to_json_converter.py path/to/quote1.pdf path/to/quote2.pdf

Output:
  - quoteA.json (from first PDF)
  - quoteB.json (from second PDF)
"""
import sys
import json
from pathlib import Path
from services.pdf_extractor import PDFExtractor
from services.llm_integration import LLMIntegrationService
from services.fpdf_report_generator import FPDFReportGenerator

def extract_pdf_to_json(pdf_path: str, output_path: str) -> None:
    """Extract data from PDF and save as JSON with category structure."""
    print(f"Processing {pdf_path}...")
    
    # Initialize services
    pdf_extractor = PDFExtractor()
    llm_service = LLMIntegrationService()
    report_generator = FPDFReportGenerator()
    
    try:
        # Extract text from PDF
        extracted_text = pdf_extractor.extract_text(pdf_path)
        if not extracted_text:
            print(f"❌ Failed to extract text from {pdf_path}")
            return
        
        # Analyze with LLM
        llm_analysis = llm_service.analyze_insurance_quote(extracted_text, Path(pdf_path).name)
        
        # Extract structured data
        company_name = llm_analysis.get('company_name', 'Unknown Company')
        policy_sections = llm_analysis.get('policy_sections', {})
        quote_details = llm_analysis.get('quote_details', {})
        
        # Build category-based JSON structure
        json_data = {}
        
        # Add company and general info
        json_data['Company'] = company_name
        json_data['Total/Final/Debit order Premium incl. VAT'] = {
            'total_premium': quote_details.get('Total Premium', 'N/A'),
            'monthly_premium': quote_details.get('Monthly Premium', 'N/A'),
            'annual_premium': quote_details.get('Annual Premium', 'N/A')
        }
        
        # Add intermediary fee if found
        intermediary_fee = report_generator._extract_intermediary_fee(extracted_text)
        if intermediary_fee != 'N/A':
            json_data['Intermediary fee'] = {
                'fee': intermediary_fee,
                'description': 'Broker/intermediary fees'
            }
        
        # Map policy sections to categories
        category_mapping = {
            'Fire': ['fire', 'fire and allied perils'],
            'Buildings combined': ['buildings combined', 'buildings', 'building'],
            'Office contents': ['office contents', 'contents', 'office content'],
            'Business interruption': ['business interruption', 'loss of profits'],
            'General': ['general', 'general cover'],
            'Theft': ['theft', 'burglary', 'robbery'],
            'Money': ['money', 'cash', 'cheques'],
            'Glass': ['glass', 'windows', 'glazing'],
            'Fidelity guarantee': ['fidelity guarantee', 'fidelity', 'employee dishonesty'],
            'Goods in transit': ['goods in transit', 'transit', 'transportation'],
            'Business all risks': ['business all risks', 'all risks', 'all risk'],
            'Accidental damage': ['accidental damage', 'accidental'],
            'Public liability': ['public liability', 'liability'],
            "Employers' liability": ['employers liability', 'employers\' liability', 'workmen compensation'],
            'Stated benefits': ['stated benefits', 'benefits'],
            'Group personal accident': ['group personal accident', 'personal accident', 'group accident'],
            'Motor personal accident': ['motor personal accident', 'motor accident'],
            'Motor General': ['motor general', 'motor', 'vehicle'],
            'Motor Specific/Specified': ['motor specific', 'motor specified', 'specified vehicles'],
            'Motor Fleet': ['motor fleet', 'fleet'],
            'Electronic equipment': ['electronic equipment', 'computer equipment', 'electronics'],
            'Umbrella liability': ['umbrella liability', 'umbrella'],
            'Assist/Value services/  VAS': ['assist', 'value services', 'vas', 'assistance'],
            'SASRIA': ['sasria', 'riot', 'strike'],
            'Accounts receivable': ['accounts receivable', 'debtors'],
            'Motor Industry Risks': ['motor industry risks', 'motor trade'],
            'Houseowners': ['houseowners', 'homeowners'],
            'Machinery Breakdown': ['machinery breakdown', 'boiler', 'mechanical breakdown'],
            'Householders': ['householders', 'household'],
            'Personal, All Risks': ['personal all risks', 'personal property'],
            'Watercraft': ['watercraft', 'marine', 'boat'],
            'Personal Legal Liability': ['personal legal liability', 'legal liability'],
            'Deterioration of Stock': ['deterioration of stock', 'spoilage'],
            'Personal Umbrella Liability': ['personal umbrella liability'],
            'Greens and Irrigation Systems': ['greens and irrigation', 'irrigation'],
            'Commercial Umbrella Liability': ['commercial umbrella liability'],
            'Professional Indemnity': ['professional indemnity', 'errors and omissions'],
            'Cyber': ['cyber', 'cyber liability', 'data breach'],
            'Community & Sectional Title': ['community', 'sectional title'],
            'Plant All risk': ['plant all risk', 'contractors plant'],
            'Contractor All Risk': ['contractor all risk', 'construction'],
            'Hospitality': ['hospitality', 'hotel', 'restaurant']
        }
        
        # Match sections to categories
        for category, keywords in category_mapping.items():
            matched_section = None
            for section_key, section_data in policy_sections.items():
                section_lower = section_key.lower()
                if any(keyword in section_lower for keyword in keywords):
                    matched_section = section_data
                    break
            
            if matched_section and isinstance(matched_section, dict):
                json_data[category] = {
                    'premium': matched_section.get('premium', 'N/A'),
                    'sum_insured': matched_section.get('sum_insured', 'N/A'),
                    'coverage_details': matched_section.get('coverage_details', []),
                    'selected': matched_section.get('selected', False),
                    'deductible': matched_section.get('deductible', 'N/A')
                }
            else:
                # Check if section exists in text but wasn't parsed
                text_lower = extracted_text.lower()
                if any(keyword in text_lower for keyword in keywords):
                    json_data[category] = {
                        'premium': 'Found in text but not parsed',
                        'sum_insured': 'N/A',
                        'coverage_details': ['Section mentioned in document'],
                        'selected': True,
                        'deductible': 'N/A'
                    }
                else:
                    json_data[category] = {
                        'premium': 'N/A',
                        'sum_insured': 'N/A',
                        'coverage_details': ['Not covered'],
                        'selected': False,
                        'deductible': 'N/A'
                    }
        
        # Save JSON file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved {output_path}")
        print(f"   Company: {company_name}")
        print(f"   Categories: {len([k for k, v in json_data.items() if isinstance(v, dict) and v.get('selected', False)])}")
        
    except Exception as e:
        print(f"❌ Error processing {pdf_path}: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_json_converter.py quote1.pdf [quote2.pdf] [quote3.pdf]")
        print("Output: quoteA.json, quoteB.json, quoteC.json (max 3 quotes)")
        sys.exit(1)
    
    pdf_files = sys.argv[1:]
    output_names = ['quoteA.json', 'quoteB.json', 'quoteC.json']
    
    print(f"Converting {min(len(pdf_files), 3)} PDF(s) to JSON format for category agents...")
    print()
    
    for i, pdf_path in enumerate(pdf_files):
        if i >= len(output_names):
            print(f"⚠️  Skipping {pdf_path} - maximum 3 PDFs supported")
            continue
        
        if not Path(pdf_path).exists():
            print(f"❌ File not found: {pdf_path}")
            continue
        
        extract_pdf_to_json(pdf_path, output_names[i])
        print()
    
    print("Conversion complete! You can now run:")
    if len(pdf_files) >= 3:
        print("python category_agents.py quoteA.json quoteB.json quoteC.json")
    elif len(pdf_files) >= 2:
        print("python category_agents.py quoteA.json quoteB.json")
    else:
        print("python category_agents.py quoteA.json quoteA.json  # (compare with itself)")

if __name__ == '__main__':
    main() 