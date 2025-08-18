#!/usr/bin/env python3
"""
LLM Integration Service for Insurance Quote Analysis
Supports multiple LLM providers for comprehensive insurance data extraction
"""

import os
import json
import requests
from typing import Dict, List, Any, Optional
from config import settings

class LLMIntegrationService:
    """Service for integrating with various LLM providers for insurance analysis"""
    
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        
    def analyze_insurance_quote(self, text: str, quote_number: int) -> Dict[str, Any]:
        """
        Analyze insurance quote using LLM
        Falls back through different providers if one fails
        """
        
        # Try OpenAI GPT first
        if self.openai_api_key:
            try:
                return self._analyze_with_openai(text, quote_number)
            except Exception as e:
                print(f"⚠️ OpenAI analysis failed: {e}")
        
        # Try Anthropic Claude
        if self.anthropic_api_key:
            try:
                return self._analyze_with_anthropic(text, quote_number)
            except Exception as e:
                print(f"⚠️ Anthropic analysis failed: {e}")
        
        # Try Google Gemini
        if self.google_api_key:
            try:
                return self._analyze_with_google(text, quote_number)
            except Exception as e:
                print(f"⚠️ Google analysis failed: {e}")
        
        # Fallback to local analysis
        print("🔄 Using local pattern-based analysis as fallback")
        return self._analyze_locally(text, quote_number)
    
    def _analyze_with_openai(self, text: str, quote_number: int) -> Dict[str, Any]:
        """Analyze using OpenAI GPT"""
        
        prompt = self._create_analysis_prompt(text)
        
        headers = {
            'Authorization': f'Bearer {self.openai_api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "model": "gpt-4",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert insurance analyst. Analyze insurance quotes and extract comprehensive information in JSON format."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "temperature": 0.1,
            "max_tokens": 2000
        }
        
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Parse JSON response
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # Extract JSON from response if it's wrapped in text
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                else:
                    raise Exception("Invalid JSON response from OpenAI")
        else:
            raise Exception(f"OpenAI API error: {response.status_code}")
    
    def _analyze_with_anthropic(self, text: str, quote_number: int) -> Dict[str, Any]:
        """Analyze using Anthropic Claude"""
        
        prompt = self._create_analysis_prompt(text)
        
        headers = {
            'x-api-key': self.anthropic_api_key,
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
        
        payload = {
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 2000,
            "messages": [
                {
                    "role": "user",
                    "content": f"You are an expert insurance analyst. {prompt}"
                }
            ]
        }
        
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['content'][0]['text']
            
            # Parse JSON response
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                else:
                    raise Exception("Invalid JSON response from Anthropic")
        else:
            raise Exception(f"Anthropic API error: {response.status_code}")
    
    def _analyze_with_google(self, text: str, quote_number: int) -> Dict[str, Any]:
        """Analyze using Google Gemini"""
        
        prompt = self._create_analysis_prompt(text)
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.google_api_key}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"You are an expert insurance analyst. {prompt}"
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 2000
            }
        }
        
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            content = result['candidates'][0]['content']['parts'][0]['text']
            
            # Parse JSON response
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                else:
                    raise Exception("Invalid JSON response from Google")
        else:
            raise Exception(f"Google API error: {response.status_code}")
    
    def _create_analysis_prompt(self, text: str) -> str:
        """Create comprehensive analysis prompt for LLM"""
        
        return f"""
        Analyze this insurance quote document and extract comprehensive information.
        
        INSURANCE QUOTE TEXT:
        {text[:4000]}  # Limit text for LLM processing
        
        Please provide a JSON response with the following exact structure:
        {{
            "company_name": "Insurance company name",
            "policy_type": "Type of insurance policy (Commercial/Business/Professional/Motor/Home)",
            "total_premium": "Total premium amount with currency (e.g., R 1,234.56)",
            "policy_sections": {{
                "section_name": {{
                    "premium": "Premium amount (e.g., R 123.45)",
                    "sum_insured": "Sum insured amount (e.g., R 1,000,000)",
                    "coverage_details": ["List of specific coverage items"],
                    "deductibles": "Deductible amount (e.g., R 1,000)"
                }}
            }},
            "key_benefits": ["List of key benefits and inclusions"],
            "exclusions": ["List of policy exclusions"],
            "policy_period": "Policy period (e.g., 12 months)",
            "contact_info": {{
                "phone": "Contact phone number",
                "email": "Contact email address",
                "address": "Company address"
            }},
            "broker_details": {{
                "commission_rate": "Commission percentage or amount",
                "broker_name": "Broker or intermediary name"
            }},
            "special_conditions": ["Any special conditions or warranties"],
            "compliance_info": {{
                "fsp_number": "FSP registration number",
                "vat_number": "VAT registration number"
            }},
            "risk_factors": ["Identified risk factors"],
            "coverage_recommendations": ["Recommended additional coverage"]
        }}
        
        IMPORTANT INSTRUCTIONS:
        1. Extract ONLY information that is clearly present in the text
        2. Use "N/A" for missing information
        3. For premium amounts, include currency symbol (R for South African Rand)
        4. Be precise with numbers - extract exact amounts, not approximations
        5. Focus on commercial insurance sections like Buildings, Contents, Liability, etc.
        6. Identify specific coverage items like "Additional Claims Preparation Costs", "Debris Removal", etc.
        7. Extract actual deductible amounts for different types of claims
        8. Return valid JSON only - no additional text or explanations
        """
    
    def _analyze_locally(self, text: str, quote_number: int) -> Dict[str, Any]:
        """Local fallback analysis using pattern matching"""
        
        from .fpdf_report_generator import FPDFReportGenerator
        
        # Use the enhanced pattern matching from the PDF generator
        generator = FPDFReportGenerator()
        
        analysis = {
            "company_name": generator._extract_company_name_enhanced(text),
            "policy_type": generator._extract_policy_type(text),
            "total_premium": generator._extract_total_premium_enhanced(text),
            "policy_sections": generator._extract_policy_sections_enhanced(text),
            "key_benefits": generator._extract_key_benefits(text),
            "exclusions": generator._extract_exclusions(text),
            "policy_period": generator._extract_policy_period(text),
            "contact_info": generator._extract_contact_info(text),
            "broker_details": generator._extract_broker_details(text),
            "special_conditions": generator._extract_special_conditions(text),
            "compliance_info": generator._extract_compliance_info(text),
            "risk_factors": generator._extract_risk_factors(text),
            "coverage_recommendations": generator._generate_coverage_recommendations(text)
        }
        
        return analysis
    
    def extract_structured_data(self, text: str) -> Dict[str, Any]:
        """Extract structured data using LLM or fallback methods"""
        
        structured_prompt = f"""
        Extract structured financial and policy data from this insurance quote:
        
        {text[:3000]}
        
        Return JSON with this structure:
        {{
            "financial_summary": {{
                "total_premium": "Total premium amount",
                "monthly_premium": "Monthly premium if specified",
                "annual_premium": "Annual premium if specified",
                "taxes_and_fees": {{"VAT": "amount", "Admin Fee": "amount"}},
                "broker_commission": "Commission amount or percentage"
            }},
            "policy_terms": {{
                "effective_date": "Policy start date",
                "expiry_date": "Policy end date", 
                "renewal_terms": "Renewal conditions",
                "cancellation_terms": "Cancellation conditions"
            }},
            "coverage_matrix": {{
                "section_name": {{
                    "included": true/false,
                    "premium": "amount",
                    "details": ["coverage items"]
                }}
            }}
        }}
        """
        
        # Try LLM analysis first, fallback to local
        if self.openai_api_key or self.anthropic_api_key or self.google_api_key:
            try:
                return self._get_llm_response(structured_prompt)
            except Exception as e:
                print(f"⚠️ LLM structured analysis failed: {e}")
        
        # Local fallback
        from .fpdf_report_generator import FPDFReportGenerator
        generator = FPDFReportGenerator()
        
        return generator._extract_structured_data_with_llm(text)
    
    def assess_risks(self, text: str) -> Dict[str, Any]:
        """Assess risks using LLM analysis"""
        
        risk_prompt = f"""
        Assess the insurance coverage and risks based on this quote:
        
        {text[:3000]}
        
        Return JSON with risk assessment:
        {{
            "coverage_adequacy": "Comprehensive/Good/Basic/Limited",
            "premium_competitiveness": "Assessment of premium value",
            "deductible_impact": "Impact of deductibles on claims",
            "policy_limitations": ["List of identified limitations"],
            "recommended_additions": ["Recommended additional coverage"]
        }}
        """
        
        # Try LLM first, fallback to local
        if self.openai_api_key or self.anthropic_api_key or self.google_api_key:
            try:
                return self._get_llm_response(risk_prompt)
            except Exception as e:
                print(f"⚠️ LLM risk assessment failed: {e}")
        
        # Local fallback
        from .fpdf_report_generator import FPDFReportGenerator
        generator = FPDFReportGenerator()
        
        return generator._assess_risks_with_llm(text)
    
    def identify_coverage_gaps(self, text: str) -> List[str]:
        """Identify coverage gaps using LLM"""
        
        gap_prompt = f"""
        Identify potential coverage gaps in this insurance quote:
        
        {text[:3000]}
        
        Return JSON array of coverage gaps:
        ["gap1", "gap2", "gap3"]
        
        Focus on common commercial insurance gaps like:
        - Cyber liability
        - Business interruption  
        - Professional indemnity
        - Directors & Officers
        - Key person insurance
        """
        
        # Try LLM first, fallback to local
        if self.openai_api_key or self.anthropic_api_key or self.google_api_key:
            try:
                response = self._get_llm_response(gap_prompt)
                if isinstance(response, list):
                    return response
                elif isinstance(response, dict) and 'gaps' in response:
                    return response['gaps']
            except Exception as e:
                print(f"⚠️ LLM gap analysis failed: {e}")
        
        # Local fallback
        from .fpdf_report_generator import FPDFReportGenerator
        generator = FPDFReportGenerator()
        
        return generator._identify_coverage_gaps_with_llm(text)
    
    def _get_llm_response(self, prompt: str) -> Any:
        """Get response from available LLM provider"""
        
        # Try providers in order of preference
        if self.openai_api_key:
            return self._query_openai(prompt)
        elif self.anthropic_api_key:
            return self._query_anthropic(prompt)
        elif self.google_api_key:
            return self._query_google(prompt)
        else:
            raise Exception("No LLM API keys available")
    
    def _query_openai(self, prompt: str) -> Any:
        """Query OpenAI API"""
        headers = {
            'Authorization': f'Bearer {self.openai_api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 1500
        }
        
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            return json.loads(content)
        else:
            raise Exception(f"OpenAI API error: {response.status_code}")
    
    def _query_anthropic(self, prompt: str) -> Any:
        """Query Anthropic API"""
        headers = {
            'x-api-key': self.anthropic_api_key,
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
        
        payload = {
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 1500,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['content'][0]['text']
            return json.loads(content)
        else:
            raise Exception(f"Anthropic API error: {response.status_code}")
    
    def _query_google(self, prompt: str) -> Any:
        """Query Google Gemini API"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.google_api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 1500
            }
        }
        
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            content = result['candidates'][0]['content']['parts'][0]['text']
            return json.loads(content)
        else:
            raise Exception(f"Google API error: {response.status_code}") 