import re
import time
from typing import List, Dict
from config import settings
from .specialized_agents import SpecializedAgents

class QuoteProcessor:
    """Service for processing and analyzing insurance quotes with specialized agents"""
    
    def __init__(self):
        self.policy_sections = settings.POLICY_SECTIONS
        self.section_subsections = settings.SECTION_SUBSECTIONS
        self.specialized_agents = SpecializedAgents()
    
    def process_quotes(self, documents: List[str]) -> List[Dict]:
        """Process multiple quote documents using specialized agents for enhanced accuracy"""
        results = []
        
        # Use specialized agents for key sections
        specialized_results = self._process_with_specialized_agents(documents)
        
        for i, doc in enumerate(documents):
            result = self._process_single_quote_enhanced(doc, i + 1, specialized_results)
            results.append(result)
        
        return results
    
    def _process_with_specialized_agents(self, documents: List[str]) -> Dict:
        """Process documents using specialized agents for key sections"""
        agent_methods = self.specialized_agents.get_section_agents()
        specialized_results = {}
        
        for section_name, agent_method in agent_methods.items():
            try:
                section_results = agent_method(documents)
                specialized_results[section_name] = section_results
            except Exception as e:
                print(f"❌ Error processing {section_name} with specialized agent: {e}")
                specialized_results[section_name] = []
        
        return specialized_results
    
    def _process_single_quote_enhanced(self, text: str, quote_number: int, specialized_results: Dict) -> Dict:
        """Process a single quote document with enhanced specialized extraction"""
        # Extract basic information
        basic_info = self._extract_basic_info(text)
        
        # Process policy sections with specialized agents where available
        policy_sections = {}
        
        for section in self.policy_sections:
            if section in specialized_results and quote_number-1 < len(specialized_results[section]):
                # Use specialized agent result
                specialized_data = specialized_results[section][quote_number-1]
                # Convert specialized format to standard format
                policy_sections[section] = self._convert_specialized_to_standard(specialized_data)
            else:
                # Use fallback extraction
                section_data = self._extract_section_details(text, section)
                policy_sections[section] = section_data
        
        return {
            "quote_number": quote_number,
            "vendor": basic_info.get("vendor", "Unknown Provider"),
            "total_premium": basic_info.get("total_premium", "N/A"),
            "payment_terms": basic_info.get("payment_terms", "Monthly"),
            "contact_phone": basic_info.get("contact_phone", "N/A"),
            "contact_email": basic_info.get("contact_email", "N/A"),
            "risk_address": basic_info.get("risk_address", "Not specified"),
            "client_details": basic_info.get("client_details", "Not specified"),
            "quote_reference": basic_info.get("quote_reference", "N/A"),
            "quote_date": basic_info.get("quote_date", time.strftime('%d/%m/%Y')),
            "policy_sections": policy_sections
        }
    
    def _convert_specialized_to_standard(self, specialized_data: Dict) -> Dict:
        """Convert specialized agent data to standard format with full detail preservation"""
        section = specialized_data.get("section", "Unknown")
        
        # Create detailed items array from specialized data
        detailed_items = []
        extensions = []
        
        # Extract detailed items based on section type
        if section == "Fire":
            if specialized_data.get("buildings_cover") != "N/A":
                detailed_items.append({
                    "description": "Building Structure Coverage",
                    "sum_insured": specialized_data.get("buildings_cover", "N/A"),
                    "type": "Building"
                })
            if specialized_data.get("contents_cover") != "N/A":
                detailed_items.append({
                    "description": "Contents Coverage", 
                    "sum_insured": specialized_data.get("contents_cover", "N/A"),
                    "type": "Contents"
                })
            if specialized_data.get("stock_cover") != "N/A":
                detailed_items.append({
                    "description": "Stock in Trade",
                    "sum_insured": specialized_data.get("stock_cover", "N/A"), 
                    "type": "Stock"
                })
                
        elif section == "Motor General":
            if specialized_data.get("vehicle_count", "0") != "0":
                detailed_items.append({
                    "description": f"Fleet Coverage - {specialized_data.get('vehicle_count', '0')} Vehicles",
                    "sum_insured": "As per schedule",
                    "type": "Vehicles"
                })
            if specialized_data.get("cover_type", "Not specified") != "Not specified":
                detailed_items.append({
                    "description": f"Cover Type: {specialized_data.get('cover_type', 'Comprehensive')}",
                    "sum_insured": "N/A",
                    "type": "Coverage Type"
                })
                
        elif section == "Buildings combined":
            if specialized_data.get("main_building") != "N/A":
                detailed_items.append({
                    "description": "Main Building Structure",
                    "sum_insured": specialized_data.get("main_building", "N/A"),
                    "type": "Building"
                })
            if specialized_data.get("outbuildings") != "N/A":
                detailed_items.append({
                    "description": "Outbuildings & Structures", 
                    "sum_insured": specialized_data.get("outbuildings", "N/A"),
                    "type": "Outbuildings"
                })
                
        elif section == "Office contents":
            if specialized_data.get("furniture_fittings") != "N/A":
                detailed_items.append({
                    "description": "Furniture & Fittings",
                    "sum_insured": specialized_data.get("furniture_fittings", "N/A"),
                    "type": "Furniture"
                })
            if specialized_data.get("office_equipment") != "N/A":
                detailed_items.append({
                    "description": "Office Equipment",
                    "sum_insured": specialized_data.get("office_equipment", "N/A"),
                    "type": "Equipment"
                })
                
        elif section == "Public liability":
            if specialized_data.get("general_liability") != "N/A":
                detailed_items.append({
                    "description": "General Public Liability",
                    "sum_insured": specialized_data.get("general_liability", "N/A"),
                    "type": "Liability"
                })
            if specialized_data.get("products_liability") != "N/A":
                detailed_items.append({
                    "description": "Products Liability",
                    "sum_insured": specialized_data.get("products_liability", "N/A"),
                    "type": "Products"
                })
                
        # Add sub_sections as detailed items if they exist
        sub_sections = specialized_data.get("sub_sections", [])
        for sub_section in sub_sections:
            detailed_items.append({
                "description": sub_section,
                "sum_insured": "As per policy wording",
                "type": "Sub-section"
            })
        
        # Add any specific extensions
        if specialized_data.get("extensions"):
            extensions = specialized_data.get("extensions", [])
        
        # Create comprehensive result
        return {
            "included": specialized_data.get("included", "N"),
            "premium": specialized_data.get("premium", "N/A"),
            "sum_insured": specialized_data.get("sum_insured", "N/A"),
            "sub_sections": sub_sections,
            "excess": specialized_data.get("excess", "Standard"),
            "detailed_items": detailed_items,  # Now populated with actual detailed data
            "extensions": extensions,
            "deductibles": {"standard": specialized_data.get("excess", "Standard")},
            # Preserve all specialized data for future use
            "specialized_data": specialized_data
        }
    
    def _extract_basic_info(self, text: str) -> Dict:
        """Extract basic information from quote text"""
        # Enhanced vendor extraction
        vendor_patterns = [
            r"(Hollard|Bryte|Sanlam|OUTsurance|Discovery|Momentum|King Price|Santam|Mutual & Federal|Old Mutual|Auto & General|Budget Insurance|1st for Women|Miway|Dial Direct|Absa|Standard Bank|FNB|Nedbank)",
            r"(?:Insurance\s+Company|Insurer)[:\s]*([A-Za-z\s&]+?)(?:\n|Limited|Ltd|\(Pty\))",
            r"(?:Provider|Underwriter)[:\s]*([A-Za-z\s&]+?)(?:\n|Limited|Ltd|\(Pty\))",
        ]

        vendor = "Unknown Provider"
        for pattern in vendor_patterns:
            matches = re.finditer(pattern, text, re.I | re.M)
            for match in matches:
                potential_vendor = match.group(1).strip()
                potential_vendor = re.sub(r'\s+', ' ', potential_vendor).title()
                
                if (len(potential_vendor) >= 4 and 
                    not any(word in potential_vendor.lower() for word in ['policy', 'quote', 'premium', 'section']) and
                    len(potential_vendor.split()) <= 4):
                    vendor = potential_vendor
                    break
            if vendor != "Unknown Provider":
                break

        # Enhanced total premium extraction
        total_patterns = [
            r"(?:Total|Final|Monthly|Debit\s+Order)\s+(?:Premium|Amount|Cost)\s*[:\-]?\s*R\s?([\d,.\s]+)",
            r"TOTAL\s+(?:PREMIUM|MONTHLY|COST)\s*[:\-]?\s*R\s?([\d,.\s]+)",
            r"(?:Monthly|Per\s+month)\s+(?:premium|payment|cost)\s*[:\-]?\s*R\s?([\d,.\s]+)",
        ]

        total_premium = "N/A"
        highest_amount = 0
        
        for pattern in total_patterns:
            matches = re.finditer(pattern, text, re.I)
            for match in matches:
                amount_str = match.group(1)
                amount = re.sub(r'[^\d.]', '', amount_str)
                if amount and len(amount) >= 3:
                    try:
                        float_amount = float(amount)
                        if 200 <= float_amount <= 100000 and float_amount > highest_amount:
                            highest_amount = float_amount
                            total_premium = f"R{float_amount:,.2f}".rstrip('0').rstrip('.')
                    except ValueError:
                        continue

        # Enhanced phone number extraction
        phone_patterns = [
            r"(?:Tel|Phone|Telephone|Call)[:\s]*(\+?27\s?[\d\s\-]{8,14})",
            r"(?:Tel|Phone|Telephone|Call)[:\s]*(0[\d\s\-]{8,12})",
            r"(011\s?[\d\s\-]{6,9})",  # Johannesburg
            r"(021\s?[\d\s\-]{6,9})",  # Cape Town
            r"(031\s?[\d\s\-]{6,9})"   # Durban
        ]
        
        contact_phone = "N/A"
        for pattern in phone_patterns:
            match = re.search(pattern, text, re.I)
            if match:
                phone_num = match.group(1).strip()
                phone_num = re.sub(r'[^\d+\s]', ' ', phone_num)
                phone_num = re.sub(r'\s+', ' ', phone_num).strip()
                if len(re.sub(r'[^\d]', '', phone_num)) >= 9:
                    contact_phone = phone_num
                    break

        # Enhanced email extraction
        email_patterns = [
            r"(?:Email|E-mail)[:\s]*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
            r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
        ]
        
        contact_email = "N/A"
        for pattern in email_patterns:
            match = re.search(pattern, text, re.I)
            if match:
                email_addr = match.group(1).strip().lower()
                if '@' in email_addr and '.' in email_addr and len(email_addr) > 5:
                    contact_email = email_addr
                    break

        # Extract other basic information
        risk_address = self._extract_risk_address(text)
        client_details = self._extract_client_details(text)
        quote_reference = self._extract_quote_reference(text)
        quote_date = self._extract_quote_date(text)
        payment_terms = self._extract_payment_terms(text)

        return {
            "vendor": vendor,
            "total_premium": total_premium,
            "contact_phone": contact_phone,
            "contact_email": contact_email,
            "risk_address": risk_address,
            "client_details": client_details,
            "quote_reference": quote_reference,
            "quote_date": quote_date,
            "payment_terms": payment_terms
        }
    
    def _extract_section_details(self, text: str, section_name: str) -> Dict:
        """Enhanced section extraction with comprehensive analysis from main.py"""
        
        # Get the raw section text
        section_text = self._extract_section_raw_text(text, section_name)
        
        # Enhanced patterns for better detection with case-insensitive and flexible matching
        escaped_section = re.escape(section_name)
        
        premium_patterns = [
            rf"{escaped_section}\s*[:\-]?\s*(?:Premium|Monthly|PM)?\s*[:\-]?\s*R\s?([\d,.\s]+)",
            rf"Premium\s*[:\-]?\s*{escaped_section}\s*[:\-]?\s*R\s?([\d,.\s]+)",
            rf"{escaped_section}\s*.*?(?:Monthly|per\s+month|PM)\s*[:\-]?\s*R\s?([\d,.\s]+)",
            rf"{escaped_section}\s*Section\s*[:\-]?\s*R\s?([\d,.\s]+)",
            # More flexible patterns
            rf"{escaped_section}(?:\s+Insurance|\s+Cover|\s+Section)?\s*[:\-]?\s*R\s?([\d,.\s]+)",
            rf"(?:Monthly\s+)?{escaped_section}\s*[:\-]?\s*R\s?([\d,.\s]+)"
        ]

        sum_insured_patterns = [
            rf"{escaped_section}\s*[:\-]?\s*.*?(?:Sum\s+Insured|Limit|Value|Cover)\s*[:\-]?\s*R\s?([\d,.\s]{{5,}})",
            rf"(?:Sum\s+Insured|Limit|Value|Cover)\s*[:\-]?\s*{escaped_section}\s*[:\-]?\s*R\s?([\d,.\s]{{5,}})",
            rf"{escaped_section}\s*[:\-]?\s*(?:Buildings?|Contents?|Property)\s*[:\-]?\s*R\s?([\d,.\s]{{5,}})",
            rf"{escaped_section}\s*.*?R\s?([\d,.\s]{{5,}})(?=\s*(?:limit|cover|insured))",  # Large amounts likely sum insured
            # Building and contents specific patterns
            rf"(?:Building|Property|Structure)\s*.*?{escaped_section}\s*[:\-]?\s*R\s?([\d,.\s]{{5,}})",
            rf"Contents\s*.*?{escaped_section}\s*[:\-]?\s*R\s?([\d,.\s]{{5,}})"
        ]

        included_patterns = [
            rf"{escaped_section}\s*[:\-]?\s*(?:Yes|Y|Included|✓|Covered|Available)",
            rf"{escaped_section}\s*[:\-]?\s*R\s?[\d,.\s]+",  # If has premium, likely included
            rf"{escaped_section}\s+Section\s*[:\-]?\s*(?:Yes|Y|Included)",
            rf"✓\s*{escaped_section}",
            rf"{escaped_section}\s*.*?(?:applicable|included|covered)"
        ]

        excluded_patterns = [
            rf"{escaped_section}\s*[:\-]?\s*(?:No|N|Not\s+included|✗|Excluded|Not\s+covered|N/A)",
            rf"✗\s*{escaped_section}",
            rf"{escaped_section}\s*.*?(?:excluded|not\s+applicable|not\s+covered)"
        ]

        premium = "N/A"
        included = "N"
        sum_insured = "N/A"
        detailed_items = []
        extensions = []
        deductibles = {}

        # Check if section is included with enhanced logic
        has_positive_indicators = False
        has_negative_indicators = False
        
        for pattern in included_patterns:
            if re.search(pattern, text, re.I):
                has_positive_indicators = True
                break

        for pattern in excluded_patterns:
            if re.search(pattern, text, re.I):
                has_negative_indicators = True
                break

        # Enhanced inclusion logic
        if has_positive_indicators and not has_negative_indicators:
            included = "Y"
        elif has_negative_indicators:
            included = "N"
        
        # Extract premium with enhanced validation
        for pattern in premium_patterns:
            matches = re.finditer(pattern, text, re.I)
            for match in matches:
                amount_str = match.group(1)
                amount = re.sub(r'[^\d.]', '', amount_str)
                if amount and len(amount) >= 2:
                    try:
                        float_amount = float(amount)
                        # Enhanced premium validation based on section type
                        min_premium, max_premium = self._get_premium_range(section_name)
                        if min_premium <= float_amount <= max_premium:
                            premium = f"R{float_amount:,.2f}".rstrip('0').rstrip('.')
                            included = "Y"  # If valid premium found, section is included
                            break
                    except ValueError:
                        continue
            if premium != "N/A":
                break

        # Extract sum insured with enhanced validation
        for pattern in sum_insured_patterns:
            matches = re.finditer(pattern, text, re.I)
            for match in matches:
                amount_str = match.group(1)
                amount = re.sub(r'[^\d.]', '', amount_str)
                if amount and len(amount) >= 4:
                    try:
                        float_amount = float(amount)
                        # Enhanced sum insured validation
                        min_sum = self._get_minimum_sum_insured(section_name)
                        if float_amount >= min_sum:
                            sum_insured = f"R{float_amount:,.0f}"
                            break
                    except ValueError:
                        continue
            if sum_insured != "N/A":
                break

        # Extract detailed items for specific sections with better patterns
        if section_name.lower() in ["business all risks", "all risks", "office contents", "electronic equipment", "personal, all risks"]:
            detailed_items = self._parse_all_risks_detailed(section_text if section_text else text)

        # Extract sub-sections with enhanced detection
        sub_sections = []
        if section_name in self.section_subsections:
            for subsection in self.section_subsections[section_name]:
                # Use flexible matching for sub-sections
                subsection_patterns = [
                    rf"\b{re.escape(subsection)}\b",
                    rf"{re.escape(subsection)}",
                    rf"{re.escape(subsection.replace(' ', r'\s+'))}"
                ]
                if any(re.search(pattern, text, re.I) for pattern in subsection_patterns):
                    sub_sections.append(subsection)

        # Enhanced detailed items extraction for applicable sections
        if section_text and section_name.lower() in ["business all risks", "all risks", "office contents", "electronic equipment", "buildings combined", "personal, all risks"]:
            items = self._parse_all_risks_detailed(section_text)
            if items:
                detailed_items.extend(items)
                # Add item descriptions as sub-sections for better visibility
                for item in items[:3]:  # Limit to first 3 items to avoid clutter
                    if item.get('description') and len(item['description']) < 50:
                        sub_sections.append(item['description'])

        # Extract extensions with better patterns
        extension_patterns = [
            r"(?:Includes?|Extensions?|Additional\s+cover|Also\s+covers?)[:\s]*((?:[^.\n]+\.?\s*){1,3})",
            r"(?:Cover\s+for|Covering|Extended\s+to)[:\s]*((?:[^.\n]+\.?\s*){1,3})",
            r"(?:Plus|Including)[:\s]*((?:[^.\n]+\.?\s*){1,2})"
        ]

        context_text = section_text if section_text else text
        for pattern in extension_patterns:
            for match in re.finditer(pattern, context_text, re.I):
                ext_text = match.group(1).strip()
                if 5 < len(ext_text) < 100:  # Reasonable length for extensions
                    extensions.append({"description": ext_text})

        # Extract deductibles/excess with enhanced patterns
        excess_patterns = [
            rf"{escaped_section}\s*.*?(?:Excess|Deductible)\s*[:\-]?\s*R\s?([\d,.\s]+)",
            r"(?:Standard\s+)?(?:Excess|Deductible)\s*[:\-]?\s*R\s?([\d,.\s]+)",
            r"(\d+)%\s+of\s+(?:claim|loss)",
            r"Minimum\s+(?:excess\s+)?R\s?([\d,.\s]+)",
            rf"(?:Excess|Deductible)\s*.*?{escaped_section}\s*[:\-]?\s*R\s?([\d,.\s]+)"
        ]

        excess = "Standard"
        for pattern in excess_patterns:
            match = re.search(pattern, text, re.I)
            if match:
                if "%" in pattern:
                    deductibles["percentage"] = f"{match.group(1)}% of claim"
                    excess = deductibles["percentage"]
                else:
                    amount = re.sub(r'[^\d.]', '', match.group(1))
                    if amount:
                        try:
                            float_amount = float(amount)
                            deductibles["standard"] = f"R{float_amount:,.0f}"
                            excess = deductibles["standard"]
                        except ValueError:
                            pass
                break

        return {
            "included": included,
            "premium": premium,
            "sum_insured": sum_insured,
            "sub_sections": sub_sections,
            "excess": excess,
            "detailed_items": detailed_items,
            "extensions": extensions,
            "deductibles": deductibles
        }

    def _extract_section_raw_text(self, full_text: str, section_name: str) -> str:
        """Extract the complete section text between headers"""
        # Create regex pattern outside f-string to avoid backslash issues
        spaced_section = section_name.replace(' ', r'\s*')
        section_patterns = [
            rf"(?:{re.escape(section_name)}|{spaced_section})\s*[:\-]*\s*(.*?)(?=(?:[A-Z][A-Z\s]+:|$))",
            rf"{re.escape(section_name)}\s*SECTION\s*(.*?)(?=(?:[A-Z]+\s+SECTION|$))",
            rf"{re.escape(section_name)}.*?\n(.*?)(?=\n[A-Z][A-Z\s]+:|$)"
        ]

        for pattern in section_patterns:
            match = re.search(pattern, full_text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        return ""

    def _parse_all_risks_detailed(self, section_text: str) -> List[Dict]:
        """Parse All Risks section with detailed item extraction"""
        items = []

        # Enhanced patterns for detailed items extraction
        item_patterns = [
            # Pattern 1: "Item 1: Intercom Camera, Computer Screen - R 24,000 - R 60.00"
            r"Item\s+\d+[:\s]*([^-\n]+?)\s*-\s*R\s?([\d,.\s]+)\s*-\s*R\s?([\d,.\s]+)",
            # Pattern 2: "Intercom Camera, Computer Screen - R 24,000"
            r"([A-Z][^,\n]*(?:Camera|Computer|Screen|Phone|Equipment|Machine|Gate|Garden|Motor|Apple|Samsung)[^,\n]*),?\s*(?:[^\d]*)?R?\s?([\d,\s]+)",
            # Pattern 3: "Apple iPhone 14 Pro Max 256 GB - R 15,000"
            r"([A-Z][a-z]+\s+[A-Z][a-z]+\s+\d+\s+(?:Pro|Max|Plus)?\s*\d*\s*GB?)\s*[^\d]*R?\s?([\d,\s]+)",
            # Pattern 4: "IMEI: 123456789012345 - R 12,000"
            r"(IMEI[:\s]*\d+[^\n]*)\s*R?\s?([\d,\s]+)",
            # Pattern 5: General equipment pattern
            r"([A-Z][a-z]+(?:\s+[a-z]+)*\s+(?:equipment|motors|receiver|beams|loop))\s*[^\d]*R?\s?([\d,\s]+)",
            # Pattern 6: Building components
            r"([A-Z][a-z]+\s+(?:building|structure|walls|roof|foundation|improvements))\s*[^\d]*R?\s?([\d,\s]+)"
        ]

        for pattern in item_patterns:
            for match in re.finditer(pattern, section_text, re.IGNORECASE):
                description = match.group(1).strip()
                value = re.sub(r'[^\d.]', '', match.group(2)) if len(match.groups()) >= 2 else "0"
                premium = re.sub(r'[^\d.]', '', match.group(3)) if len(match.groups()) >= 3 else "N/A"

                if value and len(value) > 2:
                    item_data = {
                        "description": description,
                        "sum_insured": f"R{value}",
                        "reinstatement_value": "Yes" if "reinstatement" in section_text.lower() else "No"
                    }
                    if premium != "N/A" and premium:
                        item_data["premium"] = f"R{premium}"
                    items.append(item_data)

        # Also extract sub-sections like "Main building", "Outbuildings", etc.
        subsection_patterns = [
            r"(Main\s+building|Outbuildings|Boundary\s+walls|Fixed\s+improvements|Furniture\s+&\s+fittings)",
            r"(Office\s+equipment|Computer\s+equipment|Personal\s+effects|Building\s+structure)",
            r"(Contents|Stock|Loss\s+of\s+rent|Debris\s+removal|Windscreen\s+cover)"
        ]

        for pattern in subsection_patterns:
            for match in re.finditer(pattern, section_text, re.IGNORECASE):
                subsection = match.group(1).strip()
                # Look for associated value
                context = section_text[max(0, match.start()-100):match.end()+100]
                value_match = re.search(r"R\s?([\d,.\s]+)", context)
                if value_match:
                    value = re.sub(r'[^\d.]', '', value_match.group(1))
                    if value and len(value) > 3:
                        items.append({
                            "description": subsection,
                            "sum_insured": f"R{value}",
                            "reinstatement_value": "As per policy"
                        })

        return items
    
    def _get_premium_range(self, section_name: str) -> tuple:
        """Get realistic premium range for different insurance sections"""
        premium_ranges = {
            "Fire": (50, 15000),
            "Buildings combined": (100, 20000),
            "Motor General": (500, 25000),
            "Public liability": (80, 8000),
            "Professional Indemnity": (200, 12000),
            "Cyber": (150, 10000),
            "Machinery Breakdown": (50, 5000),
            "Electronic equipment": (30, 3000),
            "SASRIA": (20, 2000),
            "Office contents": (40, 4000),
        }
        return premium_ranges.get(section_name, (20, 50000))
    
    def _get_minimum_sum_insured(self, section_name: str) -> float:
        """Get minimum realistic sum insured for different sections"""
        min_sums = {
            "Fire": 100000,
            "Buildings combined": 200000,
            "Motor General": 50000,
            "Public liability": 100000,
            "Professional Indemnity": 500000,
            "Cyber": 100000,
            "Machinery Breakdown": 50000,
            "Electronic equipment": 10000,
            "Office contents": 20000,
        }
        return min_sums.get(section_name, 10000)
    
    def _extract_risk_address(self, text: str) -> str:
        """Extract risk address from text"""
        address_patterns = [
            r"(?:Risk|Property|Business|Premises)\s+Address[:\s]*([A-Z0-9][^\n]{15,100})",
            r"(?:Situated|Located)\s+at[:\s]*([A-Z0-9][^\n]{15,100})",
            r"Address[:\s]*([0-9]+[^\n]{15,100})",
        ]

        for pattern in address_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                address = match.group(1).strip()
                address = re.sub(r'\s+', ' ', address)
                if len(address) > 15 and not any(word in address.lower() for word in ['telephone', 'email', 'contact']):
                    return address
        return "Address not specified"
    
    def _extract_client_details(self, text: str) -> str:
        """Extract client details from text"""
        client_patterns = [
            r"(?:Client|Business Name|Company|Policyholder|Insured)[:\s]*([A-Z][^\n]{10,100})",
            r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:\(Pty\)\s*Ltd|CC|Ltd|Limited|Inc))",
        ]

        for pattern in client_patterns:
            matches = re.finditer(pattern, text, re.MULTILINE)
            for match in matches:
                client_name = match.group(1).strip()
                client_name = re.sub(r'\s+', ' ', client_name)
                unwanted = ['policy', 'agrees', 'renew', 'telephone', 'premium']
                if len(client_name) > 8 and not any(word in client_name.lower() for word in unwanted):
                    return client_name
        return "Client details not specified"
    
    def _extract_quote_reference(self, text: str) -> str:
        """Extract quote reference from text"""
        ref_patterns = [
            r"(?:Quote|Reference|Policy)\s+(?:No|Number|Ref)[:\s]*([A-Z0-9\-/]+)",
            r"([A-Z]{2,}\d{4,})"
        ]

        for pattern in ref_patterns:
            match = re.search(pattern, text, re.I)
            if match:
                return match.group(1).strip()
        return "N/A"
    
    def _extract_quote_date(self, text: str) -> str:
        """Extract quote date from text"""
        date_patterns = [
            r"(?:Date|Quoted on)[:\s]*(\d{1,2}/\d{1,2}/\d{4})",
            r"(\d{1,2}\s+\w+\s+\d{4})"
        ]

        for pattern in date_patterns:
            match = re.search(pattern, text, re.I)
            if match:
                return match.group(1).strip()
        return time.strftime('%d/%m/%Y')
    
    def _extract_payment_terms(self, text: str) -> str:
        """Extract payment terms from text"""
        payment_patterns = [
            r"(monthly|annually|annual|per month|per year|quarterly)",
            r"payment[^\n]*?(monthly|annually|quarterly)"
        ]

        for pattern in payment_patterns:
            match = re.search(pattern, text, re.I)
            if match:
                return match.group(1).title()
        return "Monthly" 

    def parse_insurance_quote(self, text: str, quote_number: int) -> Dict:
        """Parse a single insurance quote document"""
        # Extract basic info
        basic_info = self._extract_basic_info(text)
        
        # Process with key sections only for faster API response
        key_sections = ["Fire", "Buildings combined", "Office contents", "Motor General", "Public liability", "SASRIA"]
        
        policy_sections = {}
        for section in self.policy_sections:
            section_data = self._extract_section_details(text, section)
            policy_sections[section] = section_data
        
        return {
            "quote_number": quote_number,
            "vendor": basic_info.get("vendor", "Unknown Provider"),
            "total_premium": basic_info.get("total_premium", "N/A"),
            "payment_terms": basic_info.get("payment_terms", "Monthly"),
            "contact_phone": basic_info.get("contact_phone", "N/A"),
            "contact_email": basic_info.get("contact_email", "N/A"),
            "risk_address": basic_info.get("risk_address", "Not specified"),
            "client_details": basic_info.get("client_details", "Not specified"),
            "quote_reference": basic_info.get("quote_reference", "N/A"),
            "quote_date": basic_info.get("quote_date", time.strftime('%d/%m/%Y')),
            "policy_sections": policy_sections
        } 