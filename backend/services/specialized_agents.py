import re
import time
from typing import Dict, List
from config import settings

class SpecializedAgents:
    """Specialized agents for detailed insurance section extraction from main.py"""
    
    def __init__(self):
        self.policy_sections = settings.POLICY_SECTIONS
        self.section_subsections = settings.SECTION_SUBSECTIONS

    def fire_section_agent(self, documents: List[str]) -> List[Dict]:
        """Specialized agent focused ONLY on Fire section extraction"""
        results = []

        for i, doc in enumerate(documents):
            fire_data = self._extract_fire_section_specialized(doc, i + 1)
            results.append(fire_data)

        return results

    def _extract_fire_section_specialized(self, text: str, quote_num: int) -> Dict:
        """Specialized extraction for Fire section only"""

        fire_patterns = {
            "premium": [
                r"Fire\s*[:\-]?\s*.*?(?:Premium|Monthly)\s*.*?R\s?([\d,.\s]+)",
                r"Fire\s+(?:Insurance|Cover|Section)\s*.*?Premium\s*.*?R\s?([\d,.\s]+)",
                r"(?:Fire|Fire\s+&\s+Allied\s+Perils)\s*.*?Monthly\s*.*?R\s?([\d,.\s]+)",
                r"Fire\s*[:\-]?\s*R\s?([\d,.\s]+)(?=\s*(?:per\s+month|monthly|pm))",
                r"(?:Fire\s+section|Fire\s+cover)\s*[:\-]?\s*.*?R\s?([\d,.\s]+)",
                # Enhanced patterns for better detection
                r"FIRE\s*.*?R\s?([\d,.\s]+)",
                r"Fire\s+and\s+Allied\s+Perils\s*.*?R\s?([\d,.\s]+)"
            ],
            "sum_insured": [
                r"Fire\s*.*?(?:Building|Structure)\s*[:\-]?\s*R\s?([\d,.\s]{6,})",
                r"Fire\s*.*?(?:Contents|Stock)\s*[:\-]?\s*R\s?([\d,.\s]{6,})",
                r"Fire\s*.*?(?:Sum\s+Insured|Limit|Value)\s*[:\-]?\s*R\s?([\d,.\s]{6,})",
                r"(?:Building|Property)\s+value\s*.*?Fire\s*.*?R\s?([\d,.\s]{6,})",
                # Enhanced patterns
                r"Fire\s+section\s*.*?(?:building|structure|property)\s*[:\-]?\s*R\s?([\d,.\s]{6,})",
                r"Main\s+building\s*.*?Fire\s*.*?R\s?([\d,.\s]{6,})"
            ],
            "buildings": [
                r"Fire\s*.*?Building\s*[:\-]?\s*R\s?([\d,.\s]{6,})",
                r"Main\s+building\s*.*?R\s?([\d,.\s]{6,})",
                r"Building\s+structure\s*.*?R\s?([\d,.\s]{6,})",
                r"Property\s+value\s*.*?R\s?([\d,.\s]{6,})"
            ],
            "contents": [
                r"Fire\s*.*?Contents\s*[:\-]?\s*R\s?([\d,.\s]{6,})",
                r"Fire\s*.*?Stock\s*[:\-]?\s*R\s?([\d,.\s]{6,})",
                r"Contents\s+cover\s*.*?R\s?([\d,.\s]{6,})"
            ],
            "excess": [
                r"Fire\s*.*?(?:Excess|Deductible)\s*[:\-]?\s*R\s?([\d,.\s]+)",
                r"Fire\s*.*?(\d+)%\s+of\s+claim",
                r"Excess\s*.*?Fire\s*.*?R\s?([\d,.\s]+)"
            ]
        }

        result = {
            "quote_number": quote_num,
            "section": "Fire",
            "included": "N",
            "premium": "N/A",
            "sum_insured": "N/A",
            "buildings_cover": "N/A",
            "contents_cover": "N/A",
            "stock_cover": "N/A",
            "excess": "Standard",
            "sub_sections": []
        }

        # Enhanced detection logic
        fire_indicators = [
            r"\bFire\b",
            r"Fire\s+Insurance",
            r"Fire\s+Cover",
            r"Fire\s+Section", 
            r"Fire\s+&\s+Allied\s+Perils",
            r"FIRE\s+SECTION"
        ]
        
        has_fire_section = any(re.search(pattern, text, re.I) for pattern in fire_indicators)
        
        if has_fire_section:
            result["included"] = "Y"

            # Extract premium with enhanced validation
            for pattern in fire_patterns["premium"]:
                matches = re.finditer(pattern, text, re.I)
                for match in matches:
                    amount_str = match.group(1)
                    amount = re.sub(r'[^\d.]', '', amount_str)
                    if amount and len(amount) >= 2:
                        try:
                            float_amount = float(amount)
                            # More realistic premium range for fire insurance
                            if 50 <= float_amount <= 15000:
                                result["premium"] = f"R{float_amount:,.2f}".rstrip('0').rstrip('.')
                                break
                        except ValueError:
                            continue
                if result["premium"] != "N/A":
                    break

            # Extract sum insured with better validation
            for pattern in fire_patterns["sum_insured"]:
                matches = re.finditer(pattern, text, re.I)
                for match in matches:
                    amount_str = match.group(1)
                    amount = re.sub(r'[^\d.]', '', amount_str)
                    if amount and len(amount) >= 5:
                        try:
                            float_amount = float(amount)
                            if float_amount >= 100000:  # Minimum realistic sum insured
                                result["sum_insured"] = f"R{float_amount:,.0f}"
                                break
                        except ValueError:
                            continue
                if result["sum_insured"] != "N/A":
                    break

            # Extract building cover with context validation
            for pattern in fire_patterns["buildings"]:
                matches = re.finditer(pattern, text, re.I)
                for match in matches:
                    # Get context around the match to validate
                    context_start = max(0, match.start() - 50)
                    context_end = min(len(text), match.end() + 50)
                    context = text[context_start:context_end]
                    
                    amount_str = match.group(1)
                    amount = re.sub(r'[^\d.]', '', amount_str)
                    if amount and len(amount) >= 5:
                        try:
                            float_amount = float(amount)
                            if float_amount >= 100000:
                                result["buildings_cover"] = f"R{float_amount:,.0f}"
                                result["sub_sections"].append("Building structure")
                                break
                        except ValueError:
                            continue
                if result["buildings_cover"] != "N/A":
                    break

            # Extract contents cover
            for pattern in fire_patterns["contents"]:
                matches = re.finditer(pattern, text, re.I)
                for match in matches:
                    amount_str = match.group(1)
                    amount = re.sub(r'[^\d.]', '', amount_str)
                    if amount and len(amount) >= 4:
                        try:
                            float_amount = float(amount)
                            if float_amount >= 10000:
                                result["contents_cover"] = f"R{float_amount:,.0f}"
                                result["sub_sections"].append("Contents")
                                break
                        except ValueError:
                            continue
                if result["contents_cover"] != "N/A":
                    break

            # Extract excess with better patterns
            for pattern in fire_patterns["excess"]:
                match = re.search(pattern, text, re.I)
                if match:
                    if "%" in pattern:
                        result["excess"] = f"{match.group(1)}% of claim"
                    else:
                        amount = re.sub(r'[^\d.]', '', match.group(1))
                        if amount:
                            try:
                                float_amount = float(amount)
                                result["excess"] = f"R{float_amount:,.0f}"
                            except ValueError:
                                pass
                    break

            # Enhanced sub-section detection
            subsection_patterns = {
                "Building structure": [r"building\s+structure", r"main\s+building", r"property\s+structure"],
                "Contents": [r"\bcontents\b", r"office\s+contents", r"business\s+contents"],
                "Stock": [r"\bstock\b", r"stock\s+in\s+trade", r"trading\s+stock"],
                "Loss of rent": [r"loss\s+of\s+rent", r"rent\s+loss", r"rental\s+income"],
                "Debris removal": [r"debris\s+removal", r"clearing\s+costs", r"removal\s+costs"],
                "Alternative accommodation": [r"alternative\s+accommodation", r"temporary\s+accommodation"]
            }
            
            for subsection, patterns in subsection_patterns.items():
                if any(re.search(pattern, text, re.I) for pattern in patterns):
                    if subsection not in result["sub_sections"]:
                        result["sub_sections"].append(subsection)

        return result

    def motor_section_agent(self, documents: List[str]) -> List[Dict]:
        """Specialized agent focused ONLY on Motor section extraction"""
        results = []

        for i, doc in enumerate(documents):
            motor_data = self._extract_motor_section_specialized(doc, i + 1)
            results.append(motor_data)

        return results

    def _extract_motor_section_specialized(self, text: str, quote_num: int) -> Dict:
        """Specialized extraction for Motor section only"""

        motor_patterns = {
            "premium": [
                r"Motor\s+General\s*.*?R\s?([\d,.\s]+)",
                r"Motor\s*.*?(?:Premium|Monthly)\s*.*?R\s?([\d,.\s]+)",
                r"Vehicle\s*.*?(?:Insurance|Cover)\s*.*?R\s?([\d,.\s]+)"
            ],
            "vehicles": [
                r"(\d+)\s+vehicles?",
                r"Fleet\s+of\s+(\d+)",
                r"Motor\s*.*?(\d+)\s*vehicles?"
            ],
            "cover_type": [
                r"(?:Comprehensive|Third\s+party|Fire\s+&\s+theft)",
                r"Motor\s*.*?(Comprehensive|Third\s+party|Fire\s+&\s+theft)"
            ]
        }

        result = {
            "quote_number": quote_num,
            "section": "Motor General",
            "included": "N",
            "premium": "N/A",
            "vehicle_count": "0",
            "cover_type": "Not specified",
            "sub_sections": []
        }

        if re.search(r"\bMotor\b", text, re.I):
            result["included"] = "Y"

            # Extract premium
            for pattern in motor_patterns["premium"]:
                match = re.search(pattern, text, re.I)
                if match:
                    amount = re.sub(r'[^\d.]', '', match.group(1))
                    if amount and 50 <= float(amount) <= 20000:
                        result["premium"] = f"R{amount}"
                        break

            # Extract vehicle count
            for pattern in motor_patterns["vehicles"]:
                match = re.search(pattern, text, re.I)
                if match:
                    result["vehicle_count"] = match.group(1)
                    result["sub_sections"].append(f"{match.group(1)} vehicles")
                    break

        return result

    def public_liability_agent(self, documents: List[str]) -> List[Dict]:
        """Specialized agent focused ONLY on Public Liability section"""
        results = []

        for i, doc in enumerate(documents):
            liability_data = self._extract_public_liability_specialized(doc, i + 1)
            results.append(liability_data)

        return results

    def _extract_public_liability_specialized(self, text: str, quote_num: int) -> Dict:
        """Specialized extraction for Public Liability section only"""

        liability_patterns = {
            "premium": [
                r"Public\s+liability\s*.*?R\s?([\d,.\s]+)",
                r"Public\s+Liability\s*.*?Premium\s*.*?R\s?([\d,.\s]+)",
                r"Liability\s*.*?R\s?([\d,.\s]+)"
            ],
            "limit": [
                r"Public\s+liability\s*.*?Limit\s*.*?R\s?([\d,.\s]{6,})",
                r"Public\s+liability\s*.*?R\s?([\d,.\s]{6,})",
                r"Liability\s+limit\s*.*?R\s?([\d,.\s]{6,})"
            ]
        }

        result = {
            "quote_number": quote_num,
            "section": "Public liability",
            "included": "N",
            "premium": "N/A",
            "limit": "N/A",
            "sub_sections": []
        }

        if re.search(r"Public\s+liability", text, re.I):
            result["included"] = "Y"

            # Extract premium
            for pattern in liability_patterns["premium"]:
                match = re.search(pattern, text, re.I)
                if match:
                    amount = re.sub(r'[^\d.]', '', match.group(1))
                    if amount and 50 <= float(amount) <= 5000:
                        result["premium"] = f"R{amount}"
                        break

            # Extract limit
            for pattern in liability_patterns["limit"]:
                match = re.search(pattern, text, re.I)
                if match:
                    amount = re.sub(r'[^\d.]', '', match.group(1))
                    if amount and float(amount) >= 100000:
                        result["limit"] = f"R{amount}"
                        result["sub_sections"].append(f"Limit: {result['limit']}")
                        break

        return result

    def buildings_combined_agent(self, documents: List[str]) -> List[Dict]:
        """Specialized agent for Buildings Combined section"""
        results = []

        for i, doc in enumerate(documents):
            buildings_data = self._extract_buildings_combined_specialized(doc, i + 1)
            results.append(buildings_data)

        return results

    def _extract_buildings_combined_specialized(self, text: str, quote_num: int) -> Dict:
        """Specialized extraction for Buildings Combined section"""

        buildings_patterns = {
            "premium": [
                r"Buildings?\s+combined\s*.*?R\s?([\d,.\s]+)",
                r"Buildings?\s+Combined\s*.*?Premium\s*.*?R\s?([\d,.\s]+)",
                r"Combined\s+buildings?\s*.*?R\s?([\d,.\s]+)"
            ],
            "sum_insured": [
                r"Buildings?\s+combined\s*.*?(?:Sum\s+Insured|Limit)\s*.*?R\s?([\d,.\s]{6,})",
                r"Buildings?\s+combined\s*.*?R\s?([\d,.\s]{6,})",
                r"Combined\s+limit\s*.*?R\s?([\d,.\s]{6,})"
            ]
        }

        result = {
            "quote_number": quote_num,
            "section": "Buildings combined",
            "included": "N",
            "premium": "N/A",
            "sum_insured": "N/A",
            "sub_sections": []
        }

        if re.search(r"Buildings?\s+combined", text, re.I):
            result["included"] = "Y"

            for pattern in buildings_patterns["premium"]:
                match = re.search(pattern, text, re.I)
                if match:
                    amount = re.sub(r'[^\d.]', '', match.group(1))
                    if amount and 50 <= float(amount) <= 15000:
                        result["premium"] = f"R{amount}"
                        break

            for pattern in buildings_patterns["sum_insured"]:
                match = re.search(pattern, text, re.I)
                if match:
                    amount = re.sub(r'[^\d.]', '', match.group(1))
                    if amount and float(amount) >= 100000:
                        result["sum_insured"] = f"R{amount}"
                        break

            # Add sub-sections
            if "main building" in text.lower():
                result["sub_sections"].append("Main building")
            if "outbuilding" in text.lower():
                result["sub_sections"].append("Outbuildings")
            if "boundary" in text.lower():
                result["sub_sections"].append("Boundary walls")

        return result

    def office_contents_agent(self, documents: List[str]) -> List[Dict]:
        """Specialized agent for Office Contents section"""
        results = []

        for i, doc in enumerate(documents):
            contents_data = self._extract_office_contents_specialized(doc, i + 1)
            results.append(contents_data)

        return results

    def _extract_office_contents_specialized(self, text: str, quote_num: int) -> Dict:
        """Specialized extraction for Office Contents section"""

        contents_patterns = {
            "premium": [
                r"Office\s+contents\s*.*?R\s?([\d,.\s]+)",
                r"Contents\s*.*?Premium\s*.*?R\s?([\d,.\s]+)",
                r"Office\s+equipment\s*.*?R\s?([\d,.\s]+)"
            ],
            "sum_insured": [
                r"Office\s+contents\s*.*?(?:Sum\s+Insured|Limit)\s*.*?R\s?([\d,.\s]{5,})",
                r"Contents\s*.*?R\s?([\d,.\s]{5,})",
                r"Office\s+equipment\s*.*?R\s?([\d,.\s]{5,})"
            ]
        }

        result = {
            "quote_number": quote_num,
            "section": "Office contents",
            "included": "N",
            "premium": "N/A",
            "sum_insured": "N/A",
            "sub_sections": []
        }

        if re.search(r"Office\s+contents", text, re.I):
            result["included"] = "Y"

            for pattern in contents_patterns["premium"]:
                match = re.search(pattern, text, re.I)
                if match:
                    amount = re.sub(r'[^\d.]', '', match.group(1))
                    if amount and 20 <= float(amount) <= 5000:
                        result["premium"] = f"R{amount}"
                        break

            for pattern in contents_patterns["sum_insured"]:
                match = re.search(pattern, text, re.I)
                if match:
                    amount = re.sub(r'[^\d.]', '', match.group(1))
                    if amount and float(amount) >= 10000:
                        result["sum_insured"] = f"R{amount}"
                        break

            # Add sub-sections
            if "furniture" in text.lower():
                result["sub_sections"].append("Furniture & fittings")
            if "computer" in text.lower():
                result["sub_sections"].append("Computer equipment")

        return result

    def sasria_agent(self, documents: List[str]) -> List[Dict]:
        """Specialized agent for SASRIA section"""
        results = []

        for i, doc in enumerate(documents):
            sasria_data = self._extract_sasria_specialized(doc, i + 1)
            results.append(sasria_data)

        return results

    def _extract_sasria_specialized(self, text: str, quote_num: int) -> Dict:
        """Specialized extraction for SASRIA section"""

        sasria_patterns = {
            "premium": [
                r"SASRIA\s*.*?R\s?([\d,.\s]+)",
                r"Special\s+Risk\s*.*?R\s?([\d,.\s]+)",
                r"Riot\s*.*?R\s?([\d,.\s]+)"
            ]
        }

        result = {
            "quote_number": quote_num,
            "section": "SASRIA",
            "included": "N",
            "premium": "N/A",
            "sum_insured": "As per main sections",
            "sub_sections": ["Riot damages", "Strike damages", "Civil commotion"]
        }

        if re.search(r"SASRIA", text, re.I):
            result["included"] = "Y"

            for pattern in sasria_patterns["premium"]:
                match = re.search(pattern, text, re.I)
                if match:
                    amount = re.sub(r'[^\d.]', '', match.group(1))
                    if amount and 20 <= float(amount) <= 3000:
                        result["premium"] = f"R{amount}"
                        break

        return result

    # Create mapping for all specialized agents
    def get_section_agents(self):
        return {
            "Fire": self.fire_section_agent,
            "Motor General": self.motor_section_agent,
            "Public liability": self.public_liability_agent,
            "Buildings combined": self.buildings_combined_agent,
            "Office contents": self.office_contents_agent,
            "SASRIA": self.sasria_agent
        } 