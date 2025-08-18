#!/usr/bin/env python3
"""
Enhanced PDF Report Generator using FPDF2
Comprehensive Commercial Insurance Comparison Report Generator
Based on professional industry standards
"""
import os
import time
import re
from typing import List, Dict
from fpdf import FPDF
from config import settings

class FPDFReportGenerator:
    """Service for generating comprehensive PDF reports using FPDF2"""
    
    def __init__(self):
        self.reports_dir = settings.REPORTS_DIR
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Enhanced Insurance Policy Sections - Complete Commercial Coverage
        self.POLICY_SECTIONS = [
            # Core Commercial Sections
            "Fire", "Buildings combined", "Office contents", "Business interruption",
            "General", "Theft", "Money", "Glass", "Fidelity guarantee", "Goods in transit",
            "Business all risks", "Accidental damage", "Public liability", "Employers' liability",
            "Stated benefits", "Group personal accident", "Motor personal accident",
            "Motor General", "Motor Specific/Specified", "Motor Fleet", "Electronic equipment",
            "Umbrella liability", "Assist/Value services/ VAS", "SASRIA", "Intermediary fee",
            
            # Additional Commercial Insurance Sections
            "Accounts receivable", "Motor Industry Risks", "Houseowners", "Machinery Breakdown",
            "Householders", "Personal, All Risks", "Watercraft", "Personal Legal Liability",
            "Deterioration of Stock", "Personal Umbrella Liability", "Greens and Irrigation Systems",
            "Commercial Umbrella Liability", "Professional Indemnity", "Cyber", 
            "Community & Sectional Title", "Plant All risk", "Contractor All Risk", "Hospitality"
        ]
    
    def generate_pdf_report(self, quote_data: List[Dict], comparison_id: str) -> str:
        """Generate a comprehensive PDF report from quote comparison data"""
        # Create filename
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        filename = f"insurance_comparison_report_{comparison_id}_{timestamp}.pdf"
        file_path = os.path.join(self.reports_dir, filename)
        
        # Generate comprehensive PDF
        pdf = self._create_comprehensive_pdf(quote_data)
        pdf.output(file_path)
        
        print(f"✅ Comprehensive PDF report generated successfully: {file_path}")
        return file_path
    
    def _create_comprehensive_pdf(self, data: List[Dict]) -> FPDF:
        """Create comprehensive PDF document with detailed insurance comparison"""
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Add first page
        pdf.add_page()
        
        # Header
        self._add_header(pdf)
        
        # Client information
        self._add_client_info(pdf, data)
        
        # Premium summary
        self._add_premium_summary(pdf, data)
        
        # Sum Insured / Limit table
        self._add_sum_insured_table(pdf, data)
        
        # Monthly Premium table
        self._add_monthly_premium_table(pdf, data)
        
        # Summary of Main Sections
        self._add_main_sections_summary(pdf, data)
        
        # Total/Final Premium table
        self._add_total_premium_table(pdf, data)
        
        # List sections with no cover
        self._add_no_cover_sections(pdf, data)
        
        # Page break for detailed breakdowns
        pdf.add_page()
        
        # Detailed breakdowns for each section
        self._add_detailed_section_breakdowns(pdf, data)
        
        # SASRIA special section
        self._add_sasria_section(pdf, data)
        
        # Professional Indemnity section
        self._add_professional_indemnity_section(pdf)
        
        # Cyber Insurance section
        self._add_cyber_insurance_section(pdf)
        
        # Machinery Breakdown section
        self._add_machinery_breakdown_section(pdf)
        
        # Footer
        self._add_footer(pdf)
        
        return pdf
    
    def _add_header(self, pdf: FPDF):
        """Add professional header to PDF"""
        pdf.set_font("Arial", "B", 18)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 12, "COMMERCIAL INSURANCE QUOTE COMPARISON REPORT", ln=True, align="C")
        
        # Date
        generation_date = time.strftime('%B %d, %Y')
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 8, f"Analysis Date: {generation_date}", ln=True, align="C")
        
        # Line separator
        pdf.ln(5)
        pdf.set_line_width(0.5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(8)
    
    def _add_client_info(self, pdf: FPDF, data: List[Dict]):
        """Add client information section"""
        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 8, "CLIENT DETAILS", ln=True, fill=True)
        pdf.ln(2)
        
        pdf.set_font("Arial", "", 10)
        
        # Client details
        if data:
            client_name = data[0].get('client_details', 'Not specified')
            risk_address = data[0].get('risk_address', 'Not specified')
        else:
            client_name = "Multiple Clients"
            risk_address = "Various Addresses"
        
        pdf.cell(45, 6, "Business Name:", border=0)
        pdf.cell(0, 6, client_name, ln=True, border=0)
        
        pdf.cell(45, 6, "Risk Address:", border=0)
        pdf.cell(0, 6, risk_address, ln=True, border=0)
        
        pdf.cell(45, 6, "Report Date:", border=0)
        pdf.cell(0, 6, time.strftime('%B %d, %Y'), ln=True, border=0)
        
        pdf.cell(45, 6, "Number of Quotes:", border=0)
        pdf.cell(0, 6, str(len(data)), ln=True, border=0)
        
        pdf.ln(5)
    
    def _add_premium_summary(self, pdf: FPDF, data: List[Dict]):
        """Add summary of premiums table"""
        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 8, "SUMMARY OF PREMIUMS", ln=True, fill=True)
        pdf.ln(2)
        
        # Create premium summary table
        col_width = 190 / len(data) if data else 190
        
        # Header row
        pdf.set_font("Arial", "B", 9)
        for i, quote in enumerate(data):
            pdf.cell(col_width, 8, f"Quote {i+1}\n{quote.get('vendor', 'Unknown')[:20]}", border=1, align='C')
        pdf.ln()
        
        # Premium values row
        pdf.set_font("Arial", "B", 10)
        for quote in data:
            premium = quote.get('total_premium', 'N/A')
            pdf.cell(col_width, 8, str(premium), border=1, align='C')
        pdf.ln()
        
        pdf.ln(5)
    
    def _add_sum_insured_table(self, pdf: FPDF, data: List[Dict]):
        """Add Sum Insured / Limit table"""
        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 8, "SUM INSURED / LIMIT INCL. VAT", ln=True, fill=True)
        pdf.ln(2)
        
        self._create_policy_sections_table(pdf, data, "sum_insured")
        pdf.ln(5)
    
    def _add_monthly_premium_table(self, pdf: FPDF, data: List[Dict]):
        """Add Monthly Premium table"""
        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 8, "MONTHLY PREMIUM INCL. VAT", ln=True, fill=True)
        pdf.ln(2)
        
        self._create_policy_sections_table(pdf, data, "premium")
        pdf.ln(5)
    
    def _add_main_sections_summary(self, pdf: FPDF, data: List[Dict]):
        """Add Summary of Main Sections table"""
        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 8, "SUMMARY OF MAIN SECTIONS", ln=True, fill=True)
        pdf.ln(2)
        
        # Create comprehensive summary table
        col_width = (190 - 50) / (len(data) * 3) if data else 47  # 50 for section name, rest divided by quotes * 3 columns
        
        # Header row 1
        pdf.set_font("Arial", "B", 8)
        pdf.cell(50, 8, "Policy Section", border=1, align='C')
        for i, quote in enumerate(data):
            pdf.cell(col_width * 3, 8, f"Quote {i+1} - {quote.get('vendor', 'Unknown')[:15]}", border=1, align='C')
        pdf.ln()
        
        # Header row 2
        pdf.set_font("Arial", "B", 7)
        pdf.cell(50, 6, "", border=0)
        for _ in data:
            pdf.cell(col_width, 6, "Section\nApplicable\n(Y/N)", border=1, align='C')
            pdf.cell(col_width, 6, "Sum Insured/\nLimit incl VAT", border=1, align='C')
            pdf.cell(col_width, 6, "Monthly\nPremium\nincl VAT", border=1, align='C')
        pdf.ln()
        
        # Data rows
        pdf.set_font("Arial", "", 8)
        for section in self.POLICY_SECTIONS:
            # Check if we need a new page
            if pdf.get_y() > 250:
                pdf.add_page()
                pdf.set_font("Arial", "B", 8)
                pdf.cell(50, 6, "Policy Section", border=1, align='C')
                for _ in data:
                    pdf.cell(col_width, 6, "Section\nApplicable\n(Y/N)", border=1, align='C')
                    pdf.cell(col_width, 6, "Sum Insured/\nLimit incl VAT", border=1, align='C')
                    pdf.cell(col_width, 6, "Monthly\nPremium\nincl VAT", border=1, align='C')
                pdf.ln()
                pdf.set_font("Arial", "", 8)
            
            pdf.cell(50, 6, section, border=1, align='L')
            
            for quote in data:
                section_info = quote.get('policy_sections', {}).get(section, {})
                included = section_info.get('included', 'N')
                premium = section_info.get('premium', '-')
                sum_insured = section_info.get('sum_insured', '-')
                
                # Section applicable
                pdf.cell(col_width, 6, included, border=1, align='C')
                # Sum insured
                pdf.cell(col_width, 6, str(sum_insured), border=1, align='C')
                # Premium
                pdf.cell(col_width, 6, str(premium), border=1, align='C')
            
            pdf.ln()
        
        pdf.ln(5)
    
    def _add_total_premium_table(self, pdf: FPDF, data: List[Dict]):
        """Add Total/Final Premium table"""
        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 8, "TOTAL/FINAL/DEBIT ORDER PREMIUM INCL. VAT", ln=True, fill=True)
        pdf.ln(2)
        
        # Create total premium table
        col_width = 190 / len(data) if data else 190
        
        # Header row
        pdf.set_font("Arial", "B", 9)
        for i, quote in enumerate(data):
            pdf.cell(col_width, 8, f"Quote {i+1} - {quote.get('vendor', 'Unknown')[:20]}", border=1, align='C')
        pdf.ln()
        
        # Premium values row
        pdf.set_font("Arial", "B", 12)
        for quote in data:
            premium = quote.get('total_premium', 'N/A')
            pdf.cell(col_width, 10, str(premium), border=1, align='C')
        pdf.ln()
        
        pdf.ln(5)
    
    def _add_no_cover_sections(self, pdf: FPDF, data: List[Dict]):
        """Add sections with no cover"""
        # Find sections with no coverage across all quotes
        no_cover_sections = []
        for section in self.POLICY_SECTIONS:
            has_coverage = False
            for quote in data:
                section_info = quote.get('policy_sections', {}).get(section, {})
                if section_info.get('included', 'N') == 'Y':
                    has_coverage = True
                    break
            if not has_coverage:
                no_cover_sections.append(section)
        
        if no_cover_sections:
            pdf.set_font("Arial", "B", 12)
            pdf.set_fill_color(240, 240, 240)
            pdf.cell(0, 8, "LIST ONLY POLICY MAIN SECTIONS HERE IF THEY HAVE NO COVER UNDER ANY QUOTE", ln=True, fill=True)
            pdf.ln(2)
            
            pdf.set_font("Arial", "", 10)
            for section in no_cover_sections:
                pdf.cell(0, 6, f"- {section}", ln=True, border=0)
            
            pdf.ln(5)
    
    def _add_detailed_section_breakdowns(self, pdf: FPDF, data: List[Dict]):
        """Add detailed breakdowns for each section"""
        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 8, "DETAILED BREAKDOWN OF POLICY SECTIONS", ln=True, fill=True)
        pdf.ln(2)
        
        for section in self.POLICY_SECTIONS:
            # Check if any quote has coverage for this section
            has_coverage = any(quote.get('policy_sections', {}).get(section, {}).get('included', 'N') == 'Y' for quote in data)
            
            if has_coverage:
                # Check if we need a new page
                if pdf.get_y() > 200:
                    pdf.add_page()
                
                pdf.set_font("Arial", "B", 11)
                pdf.set_fill_color(220, 220, 220)
                pdf.cell(0, 8, section.upper(), ln=True, fill=True)
                pdf.ln(2)
                
                # Create detailed breakdown table
                self._create_detailed_breakdown_table(pdf, data, section)
                pdf.ln(5)
    
    def _add_sasria_section(self, pdf: FPDF, data: List[Dict]):
        """Add SASRIA special section"""
        if pdf.get_y() > 200:
            pdf.add_page()
        
        pdf.set_font("Arial", "B", 11)
        pdf.set_fill_color(220, 220, 220)
        pdf.cell(0, 8, "SASRIA", ln=True, fill=True)
        pdf.ln(2)
        
        # Create SASRIA table
        col_width = (190 - 50) / 5  # 50 for company, rest divided by 5 columns
        
        # Header
        pdf.set_font("Arial", "B", 8)
        pdf.cell(50, 8, "Insurance Company", border=1, align='C')
        pdf.cell(col_width, 8, "SASRIA Coverage\nDetails", border=1, align='C')
        pdf.cell(col_width, 8, "Sum Insured", border=1, align='C')
        pdf.cell(col_width, 8, "Applicable", border=1, align='C')
        pdf.cell(col_width, 8, "Premium", border=1, align='C')
        pdf.cell(col_width, 8, "Excess", border=1, align='C')
        pdf.ln()
        
        # Data rows
        pdf.set_font("Arial", "", 8)
        for quote in data:
            sasria_info = quote.get('policy_sections', {}).get('SASRIA', {})
            pdf.cell(50, 8, quote.get('vendor', 'Unknown')[:20], border=1, align='C')
            pdf.cell(col_width, 8, "Special Risk Insurance\nAssociation Coverage", border=1, align='C')
            pdf.cell(col_width, 8, sasria_info.get('sum_insured', 'As per main\nsections'), border=1, align='C')
            pdf.cell(col_width, 8, sasria_info.get('included', 'N'), border=1, align='C')
            pdf.cell(col_width, 8, sasria_info.get('premium', '-'), border=1, align='C')
            pdf.cell(col_width, 8, sasria_info.get('excess', 'As per main\npolicy'), border=1, align='C')
            pdf.ln()
        
        pdf.ln(5)
    
    def _add_professional_indemnity_section(self, pdf: FPDF):
        """Add Professional Indemnity section"""
        if pdf.get_y() > 200:
            pdf.add_page()
        
        pdf.set_font("Arial", "B", 11)
        pdf.set_fill_color(220, 220, 220)
        pdf.cell(0, 8, "PROFESSIONAL INDEMNITY", ln=True, fill=True)
        pdf.ln(2)
        
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 8, "Policy Terms and Conditions", ln=True, border=0)
        pdf.ln(2)
        
        pdf.set_font("Arial", "", 9)
        terms = [
            "Policy Period: 12 months from commencement date unless otherwise stated",
            "Payment Terms: Monthly premium debit order or annual payment options available",
            "Renewal: Subject to annual review and acceptance by insurers",
            "Claims Procedure: All claims must be reported within 30 days of occurrence",
            "Risk Address: Coverage applies to the specified risk address only"
        ]
        
        for term in terms:
            pdf.cell(0, 6, f"- {term}", ln=True, border=0)
        
        pdf.ln(5)
    
    def _add_cyber_insurance_section(self, pdf: FPDF):
        """Add Cyber Insurance section"""
        if pdf.get_y() > 200:
            pdf.add_page()
        
        pdf.set_font("Arial", "B", 11)
        pdf.set_fill_color(220, 220, 220)
        pdf.cell(0, 8, "CYBER INSURANCE", ln=True, fill=True)
        pdf.ln(2)
        
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 8, "Policy Terms and Conditions", ln=True, border=0)
        pdf.ln(2)
        
        pdf.set_font("Arial", "", 9)
        terms = [
            "Policy Period: 12 months from commencement date unless otherwise stated",
            "Payment Terms: Monthly premium debit order or annual payment options available",
            "Renewal: Subject to annual review and acceptance by insurers",
            "Claims Procedure: All claims must be reported within 30 days of occurrence",
            "Risk Address: Coverage applies to the specified risk address only"
        ]
        
        for term in terms:
            pdf.cell(0, 6, f"- {term}", ln=True, border=0)
        
        pdf.ln(5)
    
    def _add_machinery_breakdown_section(self, pdf: FPDF):
        """Add Machinery Breakdown section"""
        if pdf.get_y() > 200:
            pdf.add_page()
        
        pdf.set_font("Arial", "B", 11)
        pdf.set_fill_color(220, 220, 220)
        pdf.cell(0, 8, "MACHINERY BREAKDOWN", ln=True, fill=True)
        pdf.ln(2)
        
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 8, "Policy Terms and Conditions", ln=True, border=0)
        pdf.ln(2)
        
        pdf.set_font("Arial", "", 9)
        terms = [
            "Policy Period: 12 months from commencement date unless otherwise stated",
            "Payment Terms: Monthly premium debit order or annual payment options available",
            "Renewal: Subject to annual review and acceptance by insurers",
            "Claims Procedure: All claims must be reported within 30 days of occurrence",
            "Risk Address: Coverage applies to the specified risk address only"
        ]
        
        for term in terms:
            pdf.cell(0, 6, f"- {term}", ln=True, border=0)
        
        pdf.ln(5)
    
    def _create_policy_sections_table(self, pdf: FPDF, data: List[Dict], field_type: str):
        """Create table for policy sections with specified field type"""
        col_width = (190 - 50) / len(data) if data else 140  # 50 for section name
        
        # Header row
        pdf.set_font("Arial", "B", 9)
        pdf.cell(50, 8, "Policy Section", border=1, align='C')
        for i, quote in enumerate(data):
            pdf.cell(col_width, 8, f"Quote {i+1}\n{quote.get('vendor', 'Unknown')[:15]}", border=1, align='C')
        pdf.ln()
        
        # Data rows
        pdf.set_font("Arial", "", 8)
        for section in self.POLICY_SECTIONS:
            # Check if we need a new page
            if pdf.get_y() > 250:
                pdf.add_page()
                pdf.set_font("Arial", "B", 9)
                pdf.cell(50, 8, "Policy Section", border=1, align='C')
                for i, quote in enumerate(data):
                    pdf.cell(col_width, 8, f"Quote {i+1}\n{quote.get('vendor', 'Unknown')[:15]}", border=1, align='C')
                pdf.ln()
                pdf.set_font("Arial", "", 8)
            
            pdf.cell(50, 6, section, border=1, align='L')
            
            for quote in data:
                section_info = quote.get('policy_sections', {}).get(section, {})
                value = section_info.get(field_type, '-')
                pdf.cell(col_width, 6, str(value), border=1, align='C')
            
            pdf.ln()
    
    def _create_detailed_breakdown_table(self, pdf: FPDF, data: List[Dict], section: str):
        """Create detailed breakdown table for a specific section"""
        col_width = (190 - 50) / 5  # 50 for company, rest divided by 5 columns
        
        # Header
        pdf.set_font("Arial", "B", 8)
        pdf.cell(50, 8, "Insurance\nCompany", border=1, align='C')
        pdf.cell(col_width, 8, "Description, SUB-\nSections & Details", border=1, align='C')
        pdf.cell(col_width, 8, "Sum\nInsured", border=1, align='C')
        pdf.cell(col_width, 8, "Included\nYES/NO", border=1, align='C')
        pdf.cell(col_width, 8, "Premium", border=1, align='C')
        pdf.cell(col_width, 8, "Excess", border=1, align='C')
        pdf.ln()
        
        # Data rows
        pdf.set_font("Arial", "", 7)
        for quote in data:
            section_info = quote.get('policy_sections', {}).get(section, {})
            sub_sections = section_info.get('sub_sections', [])
            sub_sections_text = ', '.join(sub_sections) if sub_sections else f"{section} coverage as per policy wording"
            
            # Truncate text if too long
            if len(sub_sections_text) > 25:
                sub_sections_text = sub_sections_text[:22] + "..."
            
            pdf.cell(50, 8, quote.get('vendor', 'Unknown')[:20], border=1, align='C')
            pdf.cell(col_width, 8, sub_sections_text, border=1, align='C')
            pdf.cell(col_width, 8, str(section_info.get('sum_insured', '-')), border=1, align='C')
            pdf.cell(col_width, 8, section_info.get('included', 'N'), border=1, align='C')
            pdf.cell(col_width, 8, str(section_info.get('premium', '-')), border=1, align='C')
            pdf.cell(col_width, 8, str(section_info.get('excess', 'Standard')), border=1, align='C')
            pdf.ln()
    
    def _add_footer(self, pdf: FPDF):
        """Add professional footer to PDF"""
        pdf.ln(10)
        pdf.set_line_width(0.5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        pdf.set_font("Arial", "", 8)
        generation_date = time.strftime('%B %d, %Y')
        generation_time = time.strftime('%I:%M %p')
        
        footer_text = f"Report Generated: {generation_date} at {generation_time} | System: Commercial Insurance Comparison Platform v2.0"
        pdf.cell(0, 6, footer_text, ln=True, align='C')
        
        disclaimer = "Disclaimer: This report is for comparison purposes only. All terms and conditions should be verified with individual insurance providers."
        pdf.cell(0, 6, disclaimer, ln=True, align='C') 