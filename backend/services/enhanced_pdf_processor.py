#!/usr/bin/env python3
"""
Enhanced Local PDF Processor for Insurance Documents
Provides high-quality text extraction and analysis without external APIs
"""

import re
import PyPDF2
import pdfplumber
from typing import Dict, List, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedPDFProcessor:
    """Enhanced local PDF processing with insurance-specific extraction"""
    
    def __init__(self):
        self.insurance_keywords = {
            'premium': ['premium', 'premium amount', 'total premium', 'annual premium'],
            'sum_insured': ['sum insured', 'coverage amount', 'limit of liability', 'policy limit'],
            'excess': ['excess', 'deductible', 'self-insured retention'],
            'policy_number': ['policy number', 'policy no', 'policy #', 'quote reference'],
            'vendor': ['insurance company', 'insurer', 'underwriter', 'carrier'],
            'contact': ['phone', 'email', 'contact', 'telephone', 'fax'],
            'address': ['address', 'risk address', 'premises', 'location'],
            'date': ['date', 'effective date', 'inception date', 'renewal date']
        }
    
    def extract_text_enhanced(self, file_path: str) -> str:
        """Enhanced text extraction using multiple methods"""
        try:
            # Try pdfplumber first (better for complex layouts)
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                
                if text.strip():
                    logger.info(f"✅ Successfully extracted text using pdfplumber")
                    return text
        except Exception as e:
            logger.warning(f"⚠️ pdfplumber failed: {e}")
        
        try:
            # Fallback to PyPDF2
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                
                if text.strip():
                    logger.info(f"✅ Successfully extracted text using PyPDF2")
                    return text
        except Exception as e:
            logger.warning(f"⚠️ PyPDF2 failed: {e}")
        
        logger.error(f"❌ All text extraction methods failed for {file_path}")
        return ""
    
    def extract_insurance_data(self, text: str) -> Dict[str, any]:
        """Extract insurance-specific data from text"""
        data = {
            'premium': self._extract_premium(text),
            'sum_insured': self._extract_sum_insured(text),
            'excess': self._extract_excess(text),
            'policy_number': self._extract_policy_number(text),
            'vendor': self._extract_vendor(text),
            'contact_info': self._extract_contact_info(text),
            'risk_address': self._extract_risk_address(text),
            'dates': self._extract_dates(text),
            'policy_sections': self._extract_policy_sections(text)
        }
        
        return data
    
    def _extract_premium(self, text: str) -> str:
        """Extract premium information"""
        patterns = [
            r'total premium[:\s]*([Rr]?\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'premium amount[:\s]*([Rr]?\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'annual premium[:\s]*([Rr]?\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'premium[:\s]*([Rr]?\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Not specified"
    
    def _extract_sum_insured(self, text: str) -> str:
        """Extract sum insured information"""
        patterns = [
            r'sum insured[:\s]*([Rr]?\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'coverage amount[:\s]*([Rr]?\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'limit of liability[:\s]*([Rr]?\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Not specified"
    
    def _extract_policy_number(self, text: str) -> str:
        """Extract policy number"""
        patterns = [
            r'policy number[:\s]*([A-Za-z0-9\-]+)',
            r'policy no[:\s]*([A-Za-z0-9\-]+)',
            r'quote reference[:\s]*([A-Za-z0-9\-]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Not specified"
    
    def _extract_vendor(self, text: str) -> str:
        """Extract insurance company/vendor"""
        # Common South African insurance companies
        companies = [
            'Santam', 'Old Mutual', 'Discovery', 'Momentum', 'Liberty', 'Metropolitan',
            'Guardian', 'Hollard', 'Auto & General', 'Outsurance', 'King Price',
            'MiWay', 'Dial Direct', 'Budget', '1st for Women', 'Telesure'
        ]
        
        for company in companies:
            if company.lower() in text.lower():
                return company
        
        return "Not specified"
    
    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information"""
        phone_pattern = r'(\+27|0)\s*\d{2}\s*\d{3}\s*\d{4}'
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        phone = re.search(phone_pattern, text)
        email = re.search(email_pattern, text)
        
        return {
            'phone': phone.group(0) if phone else "Not specified",
            'email': email.group(0) if email else "Not specified"
        }
    
    def _extract_risk_address(self, text: str) -> str:
        """Extract risk address"""
        # Look for address patterns
        address_patterns = [
            r'risk address[:\s]*(.+?)(?:\n|$)',
            r'premises[:\s]*(.+?)(?:\n|$)',
            r'location[:\s]*(.+?)(?:\n|$)'
        ]
        
        for pattern in address_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        
        return "Not specified"
    
    def _extract_dates(self, text: str) -> Dict[str, str]:
        """Extract relevant dates"""
        date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'
        dates = re.findall(date_pattern, text)
        
        return {
            'found_dates': dates[:3] if dates else [],  # Return first 3 dates found
            'count': len(dates)
        }
    
    def _extract_policy_sections(self, text: str) -> List[str]:
        """Extract policy sections mentioned"""
        sections = [
            'Fire', 'Theft', 'Public Liability', 'Motor', 'Buildings', 'Contents',
            'Business Interruption', 'Employers Liability', 'Professional Indemnity',
            'Cyber', 'Machinery Breakdown', 'Goods in Transit'
        ]
        
        found_sections = []
        for section in sections:
            if section.lower() in text.lower():
                found_sections.append(section)
        
        return found_sections
    
    def process_pdf_locally(self, file_path: str) -> Dict[str, any]:
        """Process PDF using local methods only"""
        logger.info(f"🔄 Processing PDF locally: {file_path}")
        
        # Extract text
        text = self.extract_text_enhanced(file_path)
        if not text:
            return {'error': 'Failed to extract text from PDF'}
        
        # Extract insurance data
        data = self.extract_insurance_data(text)
        
        # Add metadata
        data['processing_method'] = 'local_enhanced'
        data['text_length'] = len(text)
        data['extraction_success'] = True
        
        logger.info(f"✅ Local processing completed successfully")
        return data

# Create global instance
enhanced_processor = EnhancedPDFProcessor() 