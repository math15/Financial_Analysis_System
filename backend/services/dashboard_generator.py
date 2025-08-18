import re
import time
from typing import List, Dict
from config import settings

class DashboardGenerator:
    """Enhanced dashboard generator for interactive HTML reports from main.py"""
    
    def __init__(self):
        self.policy_sections = settings.POLICY_SECTIONS
    
    def create_dashboard_html(self, data: List[Dict]) -> str:
        """Create comprehensive interactive dashboard HTML"""
        analysis_date = time.strftime('%B %d, %Y')
        num_quotes = len(data)

        # Calculate statistics
        total_premiums = []
        for quote in data:
            premium_str = quote.get('total_premium', 'N/A')
            if premium_str != 'N/A':
                amount = re.sub(r'[^\d.]', '', premium_str)
                if amount:
                    try:
                        total_premiums.append(float(amount))
                    except ValueError:
                        pass

        lowest_premium = min(total_premiums) if total_premiums else 0
        highest_premium = max(total_premiums) if total_premiums else 0
        avg_premium = sum(total_premiums) / len(total_premiums) if total_premiums else 0

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Insurance Quote Comparison Dashboard</title>
            <meta charset="UTF-8">
            <style>
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    margin: 0; 
                    padding: 20px; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    min-height: 100vh;
                }}
                .container {{ 
                    max-width: 1400px; 
                    margin: 0 auto; 
                    background: white; 
                    padding: 40px; 
                    border-radius: 15px; 
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2); 
                }}
                .header {{ 
                    text-align: center; 
                    margin-bottom: 40px; 
                    border-bottom: 3px solid #667eea; 
                    padding-bottom: 25px; 
                }}
                .header h1 {{ 
                    font-size: 32px; 
                    color: #333; 
                    margin: 0 0 10px 0; 
                    font-weight: 300; 
                }}
                .stats-grid {{ 
                    display: grid; 
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                    gap: 20px; 
                    margin: 30px 0; 
                }}
                .stat-card {{ 
                    background: linear-gradient(135deg, #667eea, #764ba2); 
                    color: white; 
                    padding: 25px; 
                    border-radius: 12px; 
                    text-align: center; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
                }}
                .stat-value {{ 
                    font-size: 28px; 
                    font-weight: bold; 
                    margin-bottom: 5px; 
                }}
                .stat-label {{ 
                    font-size: 14px; 
                    opacity: 0.9; 
                }}
                .section-title {{ 
                    background: #333; 
                    color: white; 
                    padding: 15px 25px; 
                    font-size: 18px; 
                    font-weight: bold; 
                    text-transform: uppercase; 
                    margin: 40px 0 20px 0; 
                    border-radius: 8px; 
                }}
                .premium-summary {{ 
                    display: grid; 
                    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); 
                    gap: 25px; 
                    margin: 25px 0; 
                }}
                .quote-card {{ 
                    border: 2px solid #667eea; 
                    padding: 25px; 
                    background: linear-gradient(145deg, #f8f9ff, #e8ecff); 
                    border-radius: 12px; 
                    position: relative; 
                    overflow: hidden; 
                }}
                .quote-card::before {{ 
                    content: ''; 
                    position: absolute; 
                    top: 0; 
                    left: 0; 
                    right: 0; 
                    height: 4px; 
                    background: linear-gradient(90deg, #667eea, #764ba2); 
                }}
                .quote-header {{ 
                    font-size: 20px; 
                    font-weight: bold; 
                    color: #333; 
                    margin-bottom: 15px; 
                    display: flex; 
                    align-items: center; 
                    gap: 10px; 
                }}
                .premium-amount {{ 
                    font-size: 28px; 
                    color: #d32f2f; 
                    font-weight: bold; 
                    margin: 15px 0; 
                    text-shadow: 1px 1px 2px rgba(0,0,0,0.1); 
                }}
                .comparison-table {{ 
                    width: 100%; 
                    border-collapse: collapse; 
                    margin: 25px 0; 
                    font-size: 13px; 
                    background: white; 
                    border-radius: 8px; 
                    overflow: hidden; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
                }}
                .comparison-table th {{ 
                    background: linear-gradient(135deg, #667eea, #764ba2); 
                    color: white; 
                    padding: 15px 10px; 
                    text-align: center; 
                    font-weight: bold; 
                    position: sticky; 
                    top: 0; 
                }}
                .comparison-table td {{ 
                    border: 1px solid #e0e0e0; 
                    padding: 12px 8px; 
                    text-align: center; 
                    transition: background-color 0.3s ease; 
                }}
                .comparison-table tr:hover {{ 
                    background-color: #f5f5f5; 
                }}
                .section-name {{ 
                    text-align: left; 
                    font-weight: bold; 
                    padding-left: 15px; 
                    background: #f8f9fa; 
                }}
                .included {{ 
                    background: #e8f5e8; 
                    color: #2e7d32; 
                    font-weight: bold; 
                }}
                .not-included {{ 
                    background: #ffeaea; 
                    color: #d32f2f; 
                    font-weight: bold; 
                }}
                .download-section {{ 
                    text-align: center; 
                    margin: 50px 0; 
                    padding: 40px; 
                    background: linear-gradient(135deg, #e3f2fd, #bbdefb); 
                    border: 2px solid #2196f3; 
                    border-radius: 15px; 
                }}
                .download-btn {{ 
                    background: linear-gradient(135deg, #2196f3, #1976d2); 
                    color: white; 
                    padding: 18px 35px; 
                    border: none; 
                    border-radius: 25px; 
                    font-size: 16px; 
                    cursor: pointer; 
                    text-transform: uppercase; 
                    font-weight: bold; 
                    letter-spacing: 1px; 
                    transition: all 0.3s ease; 
                    box-shadow: 0 4px 15px rgba(33, 150, 243, 0.3); 
                }}
                .download-btn:hover {{ 
                    transform: translateY(-2px); 
                    box-shadow: 0 6px 20px rgba(33, 150, 243, 0.4); 
                }}
                .info-badge {{ 
                    background: #667eea; 
                    color: white; 
                    padding: 5px 12px; 
                    border-radius: 20px; 
                    font-size: 12px; 
                    font-weight: bold; 
                }}

                /* Styles for detailed section comparison */
                .section-details {{
                    padding: 20px;
                    background-color: #fdfdfd;
                    border-top: 1px solid #eee;
                }}
                .section-details h4 {{
                    font-size: 16px;
                    margin-bottom: 15px;
                    color: #333;
                }}
                .section-details ul {{
                    list-style: disc;
                    margin-left: 20px;
                }}
                .section-details li {{
                    margin-bottom: 8px;
                    color: #555;
                }}
                .section-details table {{
                    font-size: 10px;
                    border-collapse: collapse;
                    margin-top: 10px;
                }}
                .section-details th, .section-details td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: center;
                }}
                .section-details th {{
                    background-color: #f0f0f0;
                    font-weight: bold;
                }}
                .section-details .items-row td {{
                    background-color: #fefefe;
                }}
                .section-details .items-row:hover td {{
                    background-color: #f5f5f5;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏢 Insurance Quote Comparison Dashboard</h1>
                    <p style="font-size: 16px; color: #666; margin: 10px 0;">Professional Commercial Insurance Analysis</p>
                    <div class="info-badge">Generated on {analysis_date}</div>
                </div>

                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">{num_quotes}</div>
                        <div class="stat-label">Quotes Analyzed</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">R{lowest_premium:,.0f}</div>
                        <div class="stat-label">Lowest Premium</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">R{highest_premium:,.0f}</div>
                        <div class="stat-label">Highest Premium</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">R{avg_premium:,.0f}</div>
                        <div class="stat-label">Average Premium</div>
                    </div>
                </div>

                <div class="section-title">📊 Summary of Premiums</div>
                <div class="premium-summary">
        """

        for i, quote in enumerate(data):
            savings = ""
            if total_premiums and quote.get('total_premium', 'N/A') != 'N/A':
                current_premium = float(re.sub(r'[^\d.]', '', quote['total_premium']))
                if current_premium == lowest_premium and len(total_premiums) > 1:
                    savings = f'<div style="color: #2e7d32; font-weight: bold; margin-top: 10px;">💰 BEST VALUE</div>'

            html += f"""
                <div class="quote-card">
                    <div class="quote-header">
                        <span>📋 Quote {i+1}</span>
                        <span style="color: #667eea;">{quote['vendor']}</span>
                    </div>
                    <div class="premium-amount">{quote['total_premium']}</div>
                    <div style="margin: 8px 0;"><strong>Payment:</strong> {quote.get('payment_terms', 'Monthly')}</div>
                    <div style="margin: 8px 0;"><strong>Contact:</strong> {quote.get('contact_phone', 'N/A')}</div>
                    <div style="margin: 8px 0;"><strong>Email:</strong> {quote.get('contact_email', 'N/A')}</div>
                    <div style="margin: 8px 0;"><strong>Reference:</strong> {quote.get('quote_reference', 'N/A')}</div>
                    {savings}
                </div>
            """

        html += f"""
                </div>

                <div class="section-title">📋 Detailed Policy Sections Comparison</div>
                <div style="overflow-x: auto;">
                    <table class="comparison-table">
                        <thead>
                            <tr>
                                <th style="width: 200px;">Policy Sections</th>
        """

        for i, quote in enumerate(data):
            html += f'<th style="min-width: 180px;">Quote {i+1}<br><span style="font-size: 12px;">{quote["vendor"]}</span></th>'

        html += """
                            </tr>
                        </thead>
                        <tbody>
        """

        for section in self.policy_sections:
            html += f'<tr><td class="section-name" onclick="toggleDetails(\'{section}\')" style="cursor: pointer;">{section} <span style="font-size: 10px;">▼</span></td>'
            for quote in data:
                section_info = quote.get('policy_sections', {}).get(section, {})
                status = section_info.get('included', 'N')
                premium = section_info.get('premium', 'N/A')
                sum_insured = section_info.get('sum_insured', '-')

                if status == 'Y':
                    cell_class = 'included'

                    # Enhanced display with items count
                    items_count = len(section_info.get('detailed_items', []))
                    extensions_count = len(section_info.get('extensions', []))

                    display_parts = [f"✅ YES", f"<small>{sum_insured}</small>", f"<strong>{premium}</strong>"]

                    if items_count > 0:
                        display_parts.append(f"<small>{items_count} items</small>")
                    if extensions_count > 0:
                        display_parts.append(f"<small>{extensions_count} ext.</small>")

                    display_text = "<br>".join(display_parts)
                else:
                    cell_class = 'not-included'
                    display_text = "❌ NO"

                html += f'<td class="{cell_class}">{display_text}</td>'
            html += '</tr>'

            # Add detailed row (initially hidden)
            html += f'<tr id="details-{section.replace(" ", "-")}" style="display: none; background: #f9f9f9;"><td colspan="{len(data)+1}" style="padding: 15px;"><div class="section-details">'

            # Add section comparison details
            section_comparison = self._create_detailed_section_comparison(data, section)

            html += f'<h4 style="margin: 0 0 10px 0; color: #333;">{section} - Detailed Analysis</h4>'

            if section_comparison["observations"]:
                html += '<div style="background: #e3f2fd; padding: 10px; border-radius: 5px; margin: 10px 0;"><strong>Key Observations:</strong><ul style="margin: 5px 0 0 20px;">'
                for obs in section_comparison["observations"]:
                    html += f'<li>{obs}</li>'
                html += '</ul></div>'

            # Add key differences table
            if section_comparison.get("key_differences"):
                html += '<div style="background: #fff3e0; padding: 10px; border-radius: 5px; margin: 10px 0;"><strong>Key Differences:</strong><ul style="margin: 5px 0 0 20px;">'
                for diff in section_comparison["key_differences"]:
                    html += f'<li>{diff}</li>'
                html += '</ul></div>'

            # Show detailed items if available
            any_items = any(q.get('policy_sections', {}).get(section, {}).get('detailed_items', []) for q in data)
            if any_items:
                html += '<table style="width: 100%; font-size: 10px; border-collapse: collapse; margin: 10px 0;"><thead><tr style="background: #333; color: white;"><th>Company</th><th>Items</th><th>Extensions</th><th>Deductibles</th></tr></thead><tbody>'
                for quote in data:
                    section_info = quote.get('policy_sections', {}).get(section, {})
                    items = section_info.get('detailed_items', [])
                    extensions = section_info.get('extensions', [])
                    deductibles = section_info.get('deductibles', {})

                    items_text = '; '.join([item.get('description', 'N/A') for item in items[:3]]) if items else 'None'
                    if len(items) > 3:
                        items_text += f' ... ({len(items)} total)'

                    ext_text = '; '.join([ext.get('description', 'N/A') for ext in extensions[:2]]) if extensions else 'None'

                    deduct_text = deductibles.get('standard', 'Standard') if isinstance(deductibles, dict) else 'Standard'

                    html += f'<tr><td style="border: 1px solid #ddd; padding: 5px; font-weight: bold;">{quote["vendor"]}</td><td style="border: 1px solid #ddd; padding: 5px;">{items_text}</td><td style="border: 1px solid #ddd; padding: 5px;">{ext_text}</td><td style="border: 1px solid #ddd; padding: 5px;">{deduct_text}</td></tr>'
                html += '</tbody></table>'

            html += '</div></td></tr>'

        html += f"""
                        </tbody>
                    </table>
                </div>

                <script>
                function toggleDetails(section) {{
                    const detailsRow = document.getElementById('details-' + section.replace(/ /g, '-'));
                    if (detailsRow.style.display === 'none') {{
                        detailsRow.style.display = 'table-row';
                    }} else {{
                        detailsRow.style.display = 'none';
                    }}
                }}
                </script>

                <div class="download-section">
                    <h3 style="margin-top: 0; font-size: 24px; color: #1976d2;">📄 Generate Professional Report</h3>
                    <p style="font-size: 16px; margin: 20px 0; line-height: 1.6;">
                        Download a comprehensive PDF report with detailed policy breakdowns, 
                        sub-sections analysis, and professional formatting that matches industry standards.
                    </p>
                    <button onclick="generateReport()" class="download-btn">
                        📥 Download Detailed PDF Report
                    </button>
                    <p style="font-size: 12px; color: #666; margin-top: 15px;">
                        Report includes: Premium comparisons &#8226; Policy details &#8226; Contact information &#8226; Sub-section analysis
                    </p>
                </div>
            </div>

            <script>
            function generateReport() {{
                // This would be implemented to call the backend PDF generation endpoint
                alert('PDF report generation feature will be implemented with backend integration');
            }}
            </script>
        </body>
        </html>
        """

        return html

    def _create_detailed_section_comparison(self, data: List[Dict], section_name: str) -> Dict:
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

        if all_extensions:
            unique_extensions = set(ext.get('description', '') for ext in all_extensions if ext.get('description'))
            if len(unique_extensions) > 1:
                observations.append(f"Policy extensions vary: {len(unique_extensions)} different coverage extensions found.")

        # Premium analysis
        premiums = []
        for c in covered_quotes:
            if c['premium'] != 'N/A':
                try:
                    amount = float(re.sub(r'[^\d.]', '', c['premium']))
                    premiums.append(amount)
                except:
                    pass

        if len(premiums) > 1:
            min_premium = min(premiums)
            max_premium = max(premiums)
            if (max_premium - min_premium) / min_premium > 0.2:  # >20% difference
                savings = max_premium - min_premium
                observations.append(f"Significant premium difference: R{savings:.2f} potential savings between highest and lowest.")

        # Sum insured analysis
        sum_insureds = []
        for c in covered_quotes:
            if c['sum_insured'] != 'N/A':
                try:
                    amount = float(re.sub(r'[^\d.]', '', c['sum_insured']))
                    sum_insureds.append(amount)
                except:
                    pass

        if len(sum_insureds) > 1:
            min_cover = min(sum_insureds)
            max_cover = max(sum_insureds)
            if max_cover > min_cover * 1.5:  # >50% difference
                observations.append(f"Coverage limits vary significantly: R{min_cover:,.0f} to R{max_cover:,.0f}")

        # Identify key differences between providers
        if len(coverage_comparison) >= 2:
            quote1, quote2 = coverage_comparison[0], coverage_comparison[1]

            if quote1['included'] != quote2['included']:
                key_differences.append(f"Coverage availability differs: {quote1['vendor']} ({quote1['included']}) vs {quote2['vendor']} ({quote2['included']})")

            if quote1['items_count'] != quote2['items_count']:
                key_differences.append(f"Item details: {quote1['vendor']} ({quote1['items_count']} items) vs {quote2['vendor']} ({quote2['items_count']} items)")

        return {
            "observations": observations,
            "all_items": all_items,
            "all_extensions": all_extensions,
            "coverage_comparison": coverage_comparison,
            "key_differences": key_differences
        } 