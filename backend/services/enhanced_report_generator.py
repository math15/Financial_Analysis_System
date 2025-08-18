import os
import time
import re
from typing import List, Dict
from weasyprint import HTML, CSS
from config import settings

class EnhancedReportGenerator:
    """Enhanced service for generating comprehensive PDF reports with detailed analysis"""
    
    def __init__(self):
        self.reports_dir = settings.REPORTS_DIR
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Enhanced Insurance Policy Sections - Complete Commercial Coverage (from main.py)
        self.POLICY_SECTIONS = [
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
    
    def generate_pdf_report(self, quote_data: List[Dict], comparison_id: str) -> str:
        """Generate a comprehensive PDF report from quote comparison data"""
        try:
            # Clean all text data first to avoid Unicode issues
            cleaned_data = self._clean_all_data_for_pdf(quote_data)
            
            # Generate enhanced HTML content
            html_content = self._create_detailed_pdf_html(cleaned_data)
            
            # Create filename
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = f"insurance_comparison_report_{comparison_id}_{timestamp}.pdf"
            file_path = os.path.join(self.reports_dir, filename)
            
            # Generate PDF using WeasyPrint
            self._generate_pdf_from_html(html_content, file_path)
            
            print(f"✅ Enhanced PDF report generated successfully: {file_path}")
            return file_path
            
        except Exception as e:
            print(f"❌ Error generating enhanced PDF report: {e}")
            raise
    
    def _create_detailed_pdf_html(self, data: List[Dict]) -> str:
        """Create PDF report that exactly matches the professional template structure from main.py"""

        generation_date = time.strftime('%B %d, %Y')
        generation_time = time.strftime('%I:%M %p')

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

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Commercial Insurance Quote Comparison Report</title>
            <style>
                @page {{
                    margin: 2cm 1.5cm;
                    size: A4;
                    @top-center {{
                        content: "Commercial Insurance Quote Comparison Report";
                        font-size: 10px;
                        color: #666;
                    }}
                    @bottom-center {{
                        content: "Page " counter(page) " of " counter(pages);
                        font-size: 10px;
                        color: #666;
                    }}
                }}

                body {{ 
                    font-family: 'DejaVu Sans', Arial, sans-serif; 
                    margin: 0; 
                    padding: 0; 
                    font-size: 11px;
                    line-height: 1.3;
                    color: #333;
                    background: white;
                }}

                .container {{ 
                    max-width: 100%; 
                    margin: 0 auto; 
                    padding: 20px; 
                }}

                .header {{ 
                    text-align: center; 
                    margin-bottom: 30px; 
                    padding-bottom: 20px; 
                    border-bottom: 3px solid #2c5aa0; 
                }}

                .header h1 {{ 
                    font-size: 24px; 
                    color: #2c5aa0; 
                    margin: 0 0 15px 0; 
                    font-weight: bold; 
                }}

                .header-info {{ 
                    display: flex; 
                    justify-content: space-between; 
                    font-size: 10px; 
                    color: #666; 
                    margin-top: 15px; 
                }}

                .client-info {{ 
                    background: #f8f9fa; 
                    padding: 15px; 
                    border-radius: 8px; 
                    margin: 20px 0; 
                    border-left: 4px solid #2c5aa0; 
                }}

                .client-info h3 {{ 
                    margin: 0 0 10px 0; 
                    color: #2c5aa0; 
                    font-size: 14px; 
                }}

                .section-title {{ 
                    background: #2c5aa0; 
                    color: white; 
                    padding: 12px 20px; 
                    font-size: 13px; 
                    font-weight: bold; 
                    text-transform: uppercase; 
                    margin: 25px 0 15px 0; 
                    border-radius: 5px; 
                    letter-spacing: 0.5px; 
                }}

                .comparison-table {{ 
                    width: 100%; 
                    border-collapse: collapse; 
                    margin: 15px 0; 
                    font-size: 10px; 
                    background: white; 
                    border-radius: 5px; 
                    overflow: hidden; 
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                }}

                .comparison-table th {{ 
                    background: #34495e; 
                    color: white; 
                    padding: 12px 8px; 
                    text-align: center; 
                    font-weight: bold; 
                    font-size: 10px; 
                }}

                .comparison-table td {{ 
                    border: 1px solid #ddd; 
                    padding: 10px 8px; 
                    text-align: center; 
                    font-size: 9px; 
                }}

                .section-name {{ 
                    text-align: left; 
                    font-weight: bold; 
                    background: #ecf0f1; 
                    padding-left: 15px; 
                }}

                .included {{ 
                    background: #d5f4e6; 
                    color: #2d8f47; 
                    font-weight: bold; 
                }}

                .not-included {{ 
                    background: #fce4e4; 
                    color: #d32f2f; 
                    font-weight: bold; 
                }}

                .premium-table {{ 
                    width: 100%; 
                    border-collapse: collapse; 
                    margin: 15px 0; 
                    background: white; 
                    border-radius: 5px; 
                    overflow: hidden; 
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                }}

                .premium-table th {{ 
                    background: #e74c3c; 
                    color: white; 
                    padding: 15px; 
                    text-align: center; 
                    font-weight: bold; 
                    font-size: 12px; 
                }}

                .premium-table td {{ 
                    border: 1px solid #ddd; 
                    padding: 15px; 
                    text-align: center; 
                    font-size: 14px; 
                    font-weight: bold; 
                    color: #e74c3c; 
                }}

                .breakdown-table {{ 
                    width: 100%; 
                    border-collapse: collapse; 
                    margin: 15px 0; 
                    font-size: 9px; 
                    background: white; 
                }}

                .breakdown-table th {{ 
                    background: #3498db; 
                    color: white; 
                    padding: 10px 6px; 
                    text-align: center; 
                    font-weight: bold; 
                    font-size: 9px; 
                    border: 1px solid #2980b9; 
                }}

                .breakdown-table td {{ 
                    border: 1px solid #bdc3c7; 
                    padding: 8px 6px; 
                    text-align: center; 
                    font-size: 8px; 
                    background: #fdfdfd; 
                }}

                .detail-breakdown {{ 
                    margin: 20px 0; 
                    page-break-inside: avoid; 
                }}

                .no-cover-list {{ 
                    background: #fff3cd; 
                    border: 1px solid #ffeaa7; 
                    border-radius: 5px; 
                    padding: 15px; 
                    margin: 15px 0; 
                }}

                .no-cover-list ul {{ 
                    margin: 0; 
                    padding-left: 20px; 
                }}

                .no-cover-list li {{ 
                    margin: 5px 0; 
                    color: #856404; 
                }}

                .page-break {{ 
                    page-break-before: always; 
                }}

                .footer-info {{ 
                    background: #ecf0f1; 
                    padding: 15px; 
                    border-radius: 5px; 
                    margin-top: 30px; 
                    text-align: center; 
                    font-size: 10px; 
                    color: #7f8c8d; 
                }}

                .summary-stats {{ 
                    display: flex; 
                    justify-content: space-around; 
                    background: #f8f9fa; 
                    padding: 20px; 
                    border-radius: 8px; 
                    margin: 20px 0; 
                    border: 1px solid #dee2e6; 
                }}

                .stat-item {{ 
                    text-align: center; 
                }}

                .stat-value {{ 
                    font-size: 18px; 
                    font-weight: bold; 
                    color: #2c5aa0; 
                    margin-bottom: 5px; 
                }}

                .stat-label {{ 
                    font-size: 11px; 
                    color: #666; 
                    text-transform: uppercase; 
                }}

                .risk-address {{ 
                    background: #e8f4f8; 
                    padding: 12px; 
                    border-radius: 5px; 
                    margin: 10px 0; 
                    border-left: 4px solid #3498db; 
                }}

                /* Enhanced styles for better readability */
                .vendor-highlight {{ 
                    font-weight: bold; 
                    color: #2c5aa0; 
                }}

                .amount-highlight {{ 
                    font-weight: bold; 
                    color: #e74c3c; 
                }}

                .note {{ 
                    background: #f0f8ff; 
                    border-left: 4px solid #3498db; 
                    padding: 10px; 
                    margin: 15px 0; 
                    font-size: 10px; 
                    color: #2c3e50; 
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Commercial Insurance Quote Comparison Report</h1>
                    <div class="header-info">
                        <div>Generated on: {generation_date} at {generation_time}</div>
                        <div>Total Quotes Analyzed: {len(data)}</div>
                    </div>
                </div>
        """

        # Client Information Section
        if data:
            first_quote = data[0]
            html += f"""
                <div class="client-info">
                    <h3>Client Information</h3>
                    <div><strong>Business Name:</strong> {first_quote.get('client_details', 'Not specified')}</div>
                    <div class="risk-address">
                        <strong>Risk Address:</strong> {first_quote.get('risk_address', 'Not specified')}
                    </div>
                </div>
            """

        # Summary Statistics
        total_premiums = []
        for quote in data:
            premium_str = quote.get('total_premium', 'R0')
            amount = re.sub(r'[^\d.]', '', premium_str)
            if amount:
                try:
                    total_premiums.append(float(amount))
                except ValueError:
                    pass

        if total_premiums:
            lowest_premium = min(total_premiums)
            highest_premium = max(total_premiums)
            avg_premium = sum(total_premiums) / len(total_premiums)
            potential_savings = highest_premium - lowest_premium

            html += f"""
                <div class="summary-stats">
                    <div class="stat-item">
                        <div class="stat-value">R{lowest_premium:,.0f}</div>
                        <div class="stat-label">Lowest Premium</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">R{highest_premium:,.0f}</div>
                        <div class="stat-label">Highest Premium</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">R{avg_premium:,.0f}</div>
                        <div class="stat-label">Average Premium</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">R{potential_savings:,.0f}</div>
                        <div class="stat-label">Potential Savings</div>
                    </div>
                </div>
            """

        # Enhanced Policy Sections Comparison Table
        html += f"""
            <div class="section-title">Policy Sections Comparison</div>
            <table class="comparison-table">
                <thead>
                    <tr>
                        <th style="width: 200px;">Policy Sections</th>
        """

        for i, quote in enumerate(data):
            html += f'<th style="min-width: 80px;">Quote {i+1}<br><span style="font-size: 9px;">{quote["vendor"]}</span></th>'
            html += f'<th style="min-width: 100px;">Sum Insured</th>'
            html += f'<th style="min-width: 80px;">Premium</th>'

        html += """
                    </tr>
                </thead>
                <tbody>
        """

        for section in self.POLICY_SECTIONS:
            html += f'<tr><td class="section-name">{section}</td>'
            for quote in data:
                section_info = quote.get('policy_sections', {}).get(section, {})
                included = section_info.get('included', 'N')
                premium = section_info.get('premium', '-')
                sum_insured = section_info.get('sum_insured', '-')

                status_class = 'included' if included == 'Y' else 'not-included'

                html += f'<td class="{status_class}">{included}</td>'
                html += f'<td>{sum_insured}</td>'
                html += f'<td>{premium}</td>'
            html += '</tr>'

        html += """
                </tbody>
            </table>

            <div class="section-title">Total/Final/Debit order Premium incl. VAT</div>
            <table class="premium-table">
                <thead>
                    <tr>
        """

        for i, quote in enumerate(data):
            html += f'<th>Quote {i+1} - {quote["vendor"]}</th>'

        html += """
                    </tr>
                </thead>
                <tbody>
                    <tr>
        """

        for quote in data:
            html += f'<td style="font-size: 14px; font-weight: bold; color: #d32f2f;">{quote["total_premium"]}</td>'

        html += """
                    </tr>
                </tbody>
            </table>
        """

        # List Policy Main Sections with No Cover
        if no_cover_sections:
            html += f"""
            <div class="section-title">List only Policy Main Sections here if they have No Cover under ANY quote</div>
            <div class="no-cover-list">
                <ul>
            """
            for section in no_cover_sections:
                html += f'<li>{section}</li>'
            html += """
                </ul>
            </div>
            """

        # Detailed breakdowns for ALL policy sections
        html += '<div class="page-break"></div>'

        for section in self.POLICY_SECTIONS:
            # Check if any quote has coverage for this section
            has_coverage = any(quote.get('policy_sections', {}).get(section, {}).get('included', 'N') == 'Y' for quote in data)

            if has_coverage:
                html += f"""
                <div class="section-title">{section.upper()}</div>
                <div class="detail-breakdown">
                    <table class="breakdown-table">
                        <thead>
                            <tr>
                                <th>Insurance Company</th>
                                <th>Description, SUB-Sections &amp; Details</th>
                                <th>Sum Insured</th>
                                <th>Included YES/NO</th>
                                <th>Premium</th>
                                <th>Excess</th>
                            </tr>
                        </thead>
                        <tbody>
                """

                for quote in data:
                    section_info = quote.get('policy_sections', {}).get(section, {})
                    sub_sections = section_info.get('sub_sections', [])
                    detailed_items = section_info.get('detailed_items', [])
                    extensions = section_info.get('extensions', [])
                    
                    # Build comprehensive description with detailed breakdown
                    description_parts = []
                    
                    # Add sub-sections
                    if sub_sections:
                        description_parts.append(f"<strong>Sub-sections:</strong> {', '.join(sub_sections)}")
                    
                    # Add detailed items with their specific coverage
                    if detailed_items:
                        description_parts.append("<strong>Detailed Coverage:</strong>")
                        for item in detailed_items:
                            item_desc = item.get('description', 'N/A')
                            item_sum = item.get('sum_insured', 'N/A')
                            item_type = item.get('type', '')
                            if item_sum != 'N/A' and item_sum != 'As per policy wording':
                                description_parts.append(f"• {item_desc} ({item_sum})")
                            else:
                                description_parts.append(f"• {item_desc}")
                    
                    # Add extensions if available
                    if extensions:
                        description_parts.append("<strong>Extensions:</strong>")
                        for ext in extensions:
                            if isinstance(ext, dict):
                                ext_desc = ext.get('description', str(ext))
                            else:
                                ext_desc = str(ext)
                            description_parts.append(f"• {ext_desc}")
                    
                    # If no detailed data, use fallback
                    if not description_parts:
                        description_parts.append(f"{section} coverage as per policy wording")
                    
                    comprehensive_description = "<br>".join(description_parts)

                    html += f"""
                            <tr>
                                <td style="font-weight: bold;">{quote['vendor']}</td>
                                <td style="text-align: left; font-size: 9px; line-height: 1.3;">{self._clean_text_for_pdf(comprehensive_description)}</td>
                                <td>{section_info.get('sum_insured', '-')}</td>
                                <td class="{'included' if section_info.get('included') == 'Y' else 'not-included'}">{section_info.get('included', 'N')}</td>
                                <td>{section_info.get('premium', '-')}</td>
                                <td>{section_info.get('excess', 'Standard')}</td>
                            </tr>
                    """

                html += """
                        </tbody>
                    </table>
                </div>
                """

        # Contact Information Section
        html += f"""
            <div class="section-title">Contact Information</div>
            <table class="comparison-table">
                <thead>
                    <tr>
                        <th>Quote</th>
                        <th>Insurance Company</th>
                        <th>Phone Number</th>
                        <th>Email Address</th>
                        <th>Quote Reference</th>
                        <th>Quote Date</th>
                    </tr>
                </thead>
                <tbody>
        """

        for i, quote in enumerate(data):
            html += f"""
                    <tr>
                        <td><strong>Quote {i+1}</strong></td>
                        <td class="vendor-highlight">{quote.get('vendor', 'Unknown')}</td>
                        <td>{quote.get('contact_phone', 'N/A')}</td>
                        <td>{quote.get('contact_email', 'N/A')}</td>
                        <td>{quote.get('quote_reference', 'N/A')}</td>
                        <td>{quote.get('quote_date', 'N/A')}</td>
                    </tr>
            """

        html += """
                </tbody>
            </table>
        """

        # Footer Information
        html += f"""
            <div class="footer-info">
                <p><strong>Report Generated:</strong> {generation_date} at {generation_time}</p>
                <p>This report provides a comprehensive comparison of commercial insurance quotes based on extracted policy data.</p>
                <p>Please verify all details with the respective insurance providers before making final decisions.</p>
            </div>
        """

        html += """
            </div>
        </body>
        </html>
        """

        return html

    def _clean_text_for_pdf(self, text: str) -> str:
        """Clean text to avoid Unicode issues in PDF generation"""
        if not text:
            return ""
        
        # Replace common problematic Unicode characters
        replacements = {
            # Bullet points and symbols
            '•': '&#8226;',  # HTML entity for bullet
            '●': '&#9679;',  # black circle
            '○': '&#9675;',  # white circle
            '◦': '&#9702;',  # white bullet
            '▪': '&#9642;',  # black small square
            '▫': '&#9643;',  # white small square
            '►': '&#9658;',  # black right-pointing pointer
            '▲': '&#9650;',  # black up-pointing triangle
            '▼': '&#9660;',  # black down-pointing triangle
            
            # Dashes and hyphens
            '–': '&#8211;',  # en dash
            '—': '&#8212;',  # em dash
            '−': '&#8722;',  # minus sign
            '‒': '&#8210;',  # figure dash
            '―': '&#8213;',  # horizontal bar
            
            # Quotes
            '"': '&quot;',   # left double quote
            '"': '&quot;',   # right double quote
            ''': '&#8217;',  # left single quote
            ''': '&#8217;',  # right single quote
            '‚': '&#8218;',  # single low-9 quotation mark
            '„': '&#8222;',  # double low-9 quotation mark
            
            # Other common symbols
            '…': '&#8230;',  # ellipsis
            '©': '&#169;',   # copyright
            '®': '&#174;',   # registered
            '™': '&#8482;',  # trademark
            '§': '&#167;',   # section sign
            '¶': '&#182;',   # pilcrow sign
            '†': '&#8224;',  # dagger
            '‡': '&#8225;',  # double dagger
            '‰': '&#8240;',  # per mille sign
            '€': '&#8364;',  # euro sign
            '£': '&#163;',   # pound sign
            '¥': '&#165;',   # yen sign
            '¢': '&#162;',   # cent sign
            
            # Mathematical symbols
            '×': '&#215;',   # multiplication sign
            '÷': '&#247;',   # division sign
            '±': '&#177;',   # plus-minus sign
            '≠': '&#8800;',  # not equal to
            '≤': '&#8804;',  # less than or equal to
            '≥': '&#8805;',  # greater than or equal to
            '∞': '&#8734;',  # infinity
            '∑': '&#8721;',  # summation
            '∏': '&#8719;',  # product
            '∆': '&#8710;',  # increment
            '∇': '&#8711;',  # nabla
            '∂': '&#8706;',  # partial differential
            '∫': '&#8747;',  # integral
            
            # Arrows
            '→': '&#8594;',  # rightwards arrow
            '←': '&#8592;',  # leftwards arrow
            '↑': '&#8593;',  # upwards arrow
            '↓': '&#8595;',  # downwards arrow
            '↔': '&#8596;',  # left right arrow
            '⇒': '&#8658;',  # rightwards double arrow
            '⇐': '&#8656;',  # leftwards double arrow
            '⇔': '&#8660;',  # left right double arrow
            
            # Greek letters (common ones)
            'α': '&#945;',   # alpha
            'β': '&#946;',   # beta
            'γ': '&#947;',   # gamma
            'δ': '&#948;',   # delta
            'ε': '&#949;',   # epsilon
            'π': '&#960;',   # pi
            'σ': '&#963;',   # sigma
            'τ': '&#964;',   # tau
            'φ': '&#966;',   # phi
            'ω': '&#969;',   # omega
            'Α': '&#913;',   # Alpha
            'Β': '&#914;',   # Beta
            'Γ': '&#915;',   # Gamma
            'Δ': '&#916;',   # Delta
            'Π': '&#928;',   # Pi
            'Σ': '&#931;',   # Sigma
            'Ω': '&#937;',   # Omega
            
            # Special characters
            '°': '&#176;',   # degree sign
            '¼': '&#188;',   # vulgar fraction one quarter
            '½': '&#189;',   # vulgar fraction one half
            '¾': '&#190;',   # vulgar fraction three quarters
            '²': '&#178;',   # superscript two
            '³': '&#179;',   # superscript three
            '¹': '&#185;',   # superscript one
            'ª': '&#170;',   # feminine ordinal indicator
            'º': '&#186;',   # masculine ordinal indicator
            
            # Additional punctuation
            '‹': '&#8249;',  # single left-pointing angle quotation mark
            '›': '&#8250;',  # single right-pointing angle quotation mark
            '«': '&#171;',   # left-pointing double angle quotation mark
            '»': '&#187;',   # right-pointing double angle quotation mark
            '‾': '&#8254;',  # overline
            '‿': '&#8255;',  # undertie
            '⁀': '&#8256;',  # character tie
        }
        
        cleaned_text = text
        for char, replacement in replacements.items():
            cleaned_text = cleaned_text.replace(char, replacement)
        
        # Also handle any remaining non-ASCII characters by converting them to safe alternatives
        try:
            # Try to encode as ASCII and handle any remaining Unicode errors
            cleaned_text.encode('ascii')
        except UnicodeEncodeError:
            # If there are still Unicode characters, replace them with safe alternatives
            import unicodedata
            cleaned_text = unicodedata.normalize('NFKD', cleaned_text)
            cleaned_text = ''.join(char for char in cleaned_text if ord(char) < 128 or char in '&#;')
        
        return cleaned_text

    def _clean_all_data_for_pdf(self, data: List[Dict]) -> List[Dict]:
        """Clean all text data in the quote data structure to avoid Unicode issues"""
        cleaned_data = []
        
        for quote in data:
            cleaned_quote = {}
            
            # Clean all string fields in the main quote data
            for key, value in quote.items():
                if isinstance(value, str):
                    cleaned_quote[key] = self._clean_text_for_pdf(value)
                elif isinstance(value, dict) and key == 'policy_sections':
                    # Clean policy sections data
                    cleaned_sections = {}
                    for section_name, section_info in value.items():
                        cleaned_section = {}
                        for section_key, section_value in section_info.items():
                            if isinstance(section_value, str):
                                cleaned_section[section_key] = self._clean_text_for_pdf(section_value)
                            elif isinstance(section_value, list):
                                # Clean lists (sub_sections, detailed_items, extensions)
                                if section_key == 'sub_sections':
                                    cleaned_section[section_key] = [self._clean_text_for_pdf(item) for item in section_value]
                                elif section_key in ['detailed_items', 'extensions']:
                                    cleaned_list = []
                                    for item in section_value:
                                        if isinstance(item, dict):
                                            cleaned_item = {}
                                            for item_key, item_value in item.items():
                                                if isinstance(item_value, str):
                                                    cleaned_item[item_key] = self._clean_text_for_pdf(item_value)
                                                else:
                                                    cleaned_item[item_key] = item_value
                                            cleaned_list.append(cleaned_item)
                                        else:
                                            cleaned_list.append(self._clean_text_for_pdf(str(item)))
                                    cleaned_section[section_key] = cleaned_list
                                else:
                                    cleaned_section[section_key] = section_value
                            elif isinstance(section_value, dict):
                                # Clean nested dictionaries (deductibles)
                                cleaned_dict = {}
                                for nested_key, nested_value in section_value.items():
                                    if isinstance(nested_value, str):
                                        cleaned_dict[nested_key] = self._clean_text_for_pdf(nested_value)
                                    else:
                                        cleaned_dict[nested_key] = nested_value
                                cleaned_section[section_key] = cleaned_dict
                            else:
                                cleaned_section[section_key] = section_value
                        cleaned_sections[section_name] = cleaned_section
                    cleaned_quote[key] = cleaned_sections
                else:
                    cleaned_quote[key] = value
                    
            cleaned_data.append(cleaned_quote)
        
        return cleaned_data

    def _generate_pdf_from_html(self, html: str, output_path: str):
        """Generate PDF from HTML using WeasyPrint with simple Unicode-safe configuration"""
        try:
            # Try basic WeasyPrint generation first
            HTML(string=html).write_pdf(output_path)
            print(f"✅ Enhanced PDF report generated successfully: {output_path}")
        except Exception as e:
            print(f"❌ Error generating PDF: {e}")
            # Try alternative approach with basic CSS
            try:
                # Simple CSS without font configuration
                simple_css = CSS(string='''
                    body {
                        font-family: Arial, sans-serif;
                    }
                ''')
                
                HTML(string=html).write_pdf(
                    output_path,
                    stylesheets=[simple_css]
                )
                print(f"✅ PDF generated with fallback CSS: {output_path}")
            except Exception as fallback_error:
                print(f"❌ All PDF generation methods failed: {fallback_error}")
                raise

    def create_detailed_section_comparison(self, data: List[Dict], section_name: str) -> Dict:
        """Analyzes and compares details for a specific section across multiple quotes."""
        observations = []
        all_items = []
        all_extensions = []
        coverage_comparison = []
        key_differences = []

        for quote in data:
            section_info = quote.get('policy_sections', {}).get(section_name, {})
            all_items.extend(section_info.get('detailed_items', []))
            all_extensions.extend(section_info.get('extensions', []))

            # Track coverage differences
            coverage_comparison.append({
                "vendor": quote.get('vendor', 'Unknown'),
                "included": section_info.get('included', 'N'),
                "premium": section_info.get('premium', 'N/A'),
                "sum_insured": section_info.get('sum_insured', 'N/A'),
                "items_count": len(section_info.get('detailed_items', [])),
                "extensions_count": len(section_info.get('extensions', []))
            })

        # Enhanced observations
        covered_quotes = [c for c in coverage_comparison if c['included'] == 'Y']
        not_covered_quotes = [c for c in coverage_comparison if c['included'] == 'N']

        if covered_quotes and not_covered_quotes:
            observations.append(f"Coverage varies: {len(covered_quotes)} providers offer coverage, {len(not_covered_quotes)} exclude this section.")

        if all_items:
            unique_items = set(item.get('description', '') for item in all_items if item.get('description'))
            if len(unique_items) > 1:
                observations.append(f"Detailed breakdown available: {len(unique_items)} specific items identified across quotes.")

            # Check for high-value items
            high_value_items = [item for item in all_items if item.get('sum_insured') and 
                              float(re.sub(r'[^\d.]', '', item.get('sum_insured', '0'))) > 10000]
            if high_value_items:
                observations.append(f"{len(high_value_items)} high-value items (>R10,000) identified.")

        return {
            "observations": observations,
            "all_items": all_items,
            "all_extensions": all_extensions,
            "coverage_comparison": coverage_comparison,
            "key_differences": key_differences
        } 