import os
import time
from typing import List, Dict
from weasyprint import HTML
from config import settings
from .fpdf_report_generator import FPDFReportGenerator

class ReportGenerator:
    """Service for generating PDF reports with WeasyPrint fallback to FPDF"""
    
    def __init__(self):
        self.reports_dir = settings.REPORTS_DIR
        self.fpdf_generator = FPDFReportGenerator()
    
    def generate_pdf_report(self, quote_data: List[Dict], comparison_id: str) -> str:
        """Generate a PDF report from quote comparison data"""
        try:
            # Try WeasyPrint first
            return self._generate_with_weasyprint(quote_data, comparison_id)
        except Exception as e:
            print(f"❌ WeasyPrint failed: {e}")
            print("🔄 Using FPDF2 fallback...")
            # Use FPDF2 as fallback
            return self.fpdf_generator.generate_pdf_report(quote_data, comparison_id)
    
    def _generate_with_weasyprint(self, quote_data: List[Dict], comparison_id: str) -> str:
        """Generate PDF using WeasyPrint (original method)"""
        # Generate HTML content
        html_content = self._create_detailed_pdf_html(quote_data)
        
        # Create filename
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        filename = f"insurance_comparison_report_{comparison_id}_{timestamp}.pdf"
        file_path = os.path.join(self.reports_dir, filename)
        
        # Generate PDF
        self._generate_pdf_from_html(html_content, file_path)
        
        return file_path
    
    def _create_detailed_pdf_html(self, data: List[Dict]) -> str:
        """Create detailed HTML for PDF report"""
        generation_date = time.strftime('%B %d, %Y')
        generation_time = time.strftime('%I:%M %p')
        
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
                    @bottom-center {{
                        content: "Page " counter(page) " of " counter(pages);
                        font-size: 10px;
                        color: #666;
                    }}
                }}

                body {{ 
                    font-family: 'Arial', sans-serif; 
                    margin: 0; 
                    padding: 0; 
                    font-size: 11px;
                    line-height: 1.3;
                    color: #333;
                }}

                .header {{
                    text-align: center;
                    border-bottom: 2px solid #000;
                    padding-bottom: 15px;
                    margin-bottom: 20px;
                }}

                .header h1 {{
                    font-size: 20px;
                    font-weight: bold;
                    color: #000;
                    margin: 0 0 8px 0;
                    text-transform: uppercase;
                }}

                .section-title {{
                    background: #000;
                    color: white;
                    padding: 8px 15px;
                    font-weight: bold;
                    text-transform: uppercase;
                    margin: 15px 0 8px 0;
                    font-size: 12px;
                }}

                .client-info {{
                    border: 1px solid #000;
                    padding: 15px;
                    margin: 15px 0;
                }}

                .client-info h3 {{
                    margin: 0 0 10px 0;
                    color: #000;
                    font-size: 13px;
                    text-transform: uppercase;
                    font-weight: bold;
                }}

                .main-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 10px 0;
                    font-size: 9px;
                }}

                .main-table th {{
                    background: #f0f0f0;
                    border: 1px solid #000;
                    padding: 6px 4px;
                    text-align: center;
                    font-weight: bold;
                    font-size: 8px;
                }}

                .main-table td {{
                    border: 1px solid #000;
                    padding: 4px 3px;
                    text-align: center;
                    font-size: 8px;
                }}

                .section-name {{
                    text-align: left;
                    font-weight: bold;
                    padding-left: 8px;
                    background: #f8f8f8;
                }}

                .included {{
                    background: #e8f5e8;
                    color: #000;
                    font-weight: bold;
                }}

                .not-included {{
                    background: #ffeaea;
                    color: #000;
                    font-weight: bold;
                }}

                .premium-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 10px 0;
                    font-size: 10px;
                }}

                .premium-table th {{
                    background: #000;
                    color: white;
                    border: 1px solid #000;
                    padding: 8px;
                    text-align: center;
                    font-weight: bold;
                }}

                .premium-table td {{
                    border: 1px solid #000;
                    padding: 8px;
                    text-align: center;
                    font-weight: bold;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Commercial Insurance Quote Comparison Report</h1>
                <div style="font-size: 12px; margin-top: 8px;">Analysis Date: {generation_date}</div>
            </div>

            <div class="client-info">
                <h3>Client Details</h3>
                <table style="width: 100%; font-size: 10px; border: none;">
                    <tr>
                        <td style="border: none; padding: 2px;"><strong>Business Name:</strong></td>
                        <td style="border: none; padding: 2px;">{data[0].get('client_details', 'Not specified') if data else 'Multiple Clients'}</td>
                    </tr>
                    <tr>
                        <td style="border: none; padding: 2px;"><strong>Risk Address:</strong></td>
                        <td style="border: none; padding: 2px;">{data[0].get('risk_address', 'Not specified') if data else 'Various Addresses'}</td>
                    </tr>
                    <tr>
                        <td style="border: none; padding: 2px;"><strong>Report Date:</strong></td>
                        <td style="border: none; padding: 2px;">{generation_date}</td>
                    </tr>
                    <tr>
                        <td style="border: none; padding: 2px;"><strong>Number of Quotes:</strong></td>
                        <td style="border: none; padding: 2px;">{len(data)}</td>
                    </tr>
                </table>
            </div>

            <div class="section-title">Summary of Premiums</div>
            <table class="premium-table">
                <thead>
                    <tr>
        """
        
        for i, quote in enumerate(data):
            html += f'<th>Quote {i+1}<br>{quote["vendor"]}</th>'

        html += """
                    </tr>
                </thead>
                <tbody>
                    <tr>
        """

        for quote in data:
            html += f'<td>{quote["total_premium"]}</td>'

        html += """
                    </tr>
                </tbody>
            </table>

            <div class="section-title">Policy Sections Comparison</div>
            <table class="main-table">
                <thead>
                    <tr>
                        <th rowspan="2" style="width: 200px;">Policy Section</th>
        """

        for i, quote in enumerate(data):
            html += f'<th colspan="3">Quote {i+1} - {quote["vendor"]}</th>'

        html += '</tr><tr>'

        for quote in data:
            html += '<th>Included<br>(Y/N)</th><th>Premium<br>incl VAT</th><th>Sum Insured<br>incl VAT</th>'

        html += """
                    </tr>
                </thead>
                <tbody>
        """

        # Add policy sections
        policy_sections = settings.POLICY_SECTIONS
        for section in policy_sections:
            html += f'<tr><td class="section-name">{section}</td>'
            for quote in data:
                section_info = quote.get('policy_sections', {}).get(section, {})
                included = section_info.get('included', 'N')
                premium = section_info.get('premium', '-')
                sum_insured = section_info.get('sum_insured', '-')

                status_class = 'included' if included == 'Y' else 'not-included'

                html += f'<td class="{status_class}">{included}</td>'
                html += f'<td>{premium}</td>'
                html += f'<td>{sum_insured}</td>'
            html += '</tr>'

        html += """
                </tbody>
            </table>

            <div class="section-title">Total/Final Premium incl. VAT</div>
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

        html += f"""
                    </tr>
                </tbody>
            </table>

            <div style="margin-top: 20px; padding: 10px; border: 1px solid #000; font-size: 8px;">
                <p style="text-align: center; margin: 0; font-weight: bold;">
                    <strong>Report Generated:</strong> {generation_date} at {generation_time} | 
                    <strong>System:</strong> Commercial Insurance Comparison Platform v2.0<br>
                    <strong>Disclaimer:</strong> This report is for comparison purposes only. All terms and conditions should be verified with individual insurance providers.
                </p>
            </div>
        </body>
        </html>
        """

        return html
    
    def _generate_pdf_from_html(self, html: str, output_path: str):
        """Generate PDF from HTML using WeasyPrint"""
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Generate PDF with simpler method that should work with newer WeasyPrint versions
            doc = HTML(string=html)
            doc.write_pdf(output_path)
            
            print(f"✅ PDF generated successfully: {output_path}")
            
        except Exception as e:
            print(f"❌ Error generating PDF: {e}")
            # Try alternative method with explicit target
            try:
                HTML(string=html).write_pdf(target=output_path)
                print(f"✅ PDF generated with alternative method: {output_path}")
            except Exception as e2:
                print(f"❌ Alternative method also failed: {e2}")
                raise 