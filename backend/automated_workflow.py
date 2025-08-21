#!/usr/bin/env python3
"""
Automated Insurance Quote Comparison Workflow
Handles the complete pipeline: PDF → JSON → OpenRouter Category Analysis → Final Report

Usage:
  python automated_workflow.py quote1.pdf quote2.pdf [quote3.pdf]

Environment:
  OPENROUTER_API_KEY    – Required for OpenRouter Kimi K2 analysis
  LLM_API_KEY           – Optional for LLMWhisperer text extraction

Output:
  - quoteA.json, quoteB.json, quoteC.json (intermediate JSON files)
  - backend/reports/agents/*.md (category analysis files)
  - backend/reports/agents_index.md (index of all analyses)
  - final_comparison_report.md (consolidated report)
"""
import sys
import os
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime

def run_command(cmd: list, description: str) -> bool:
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent)
        if result.returncode != 0:
            print(f"❌ {description} failed:")
            print(result.stderr)
            return False
        print(f"✅ {description} completed")
        return True
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

async def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python automated_workflow.py quote1.pdf quote2.pdf [quote3.pdf]")
        print("Automated workflow: PDF → JSON → OpenRouter Analysis → Final Report")
        print("Supports 2-3 quotes for comparison")
        sys.exit(1)
    
    pdf_files = sys.argv[1:]
    quotes_count = len(pdf_files)
    
    if quotes_count < 2:
        print("❌ At least 2 quotes are required for comparison")
        sys.exit(1)
    
    print("=" * 60)
    print("🚀 AUTOMATED INSURANCE QUOTE COMPARISON WORKFLOW")
    print("=" * 60)
    print(f"Processing {quotes_count} quote(s): {', '.join(pdf_files)}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check environment
    if not os.getenv('OPENROUTER_API_KEY'):
        print("❌ OPENROUTER_API_KEY not found in environment")
        print("Please set: export OPENROUTER_API_KEY=sk-or-v1-...")
        sys.exit(1)
    
    # Validate PDF files
    for pdf_file in pdf_files:
        if not Path(pdf_file).exists():
            print(f"❌ File not found: {pdf_file}")
            sys.exit(1)
    
    print("✅ Environment and files validated")
    print()
    
    # Step 1: Convert PDFs to JSON
    print("📄 STEP 1: PDF to JSON Conversion")
    print("-" * 30)
    cmd = ["python", "pdf_to_json_converter.py"] + pdf_files
    if not run_command(cmd, "Converting PDFs to JSON format"):
        sys.exit(1)
    print()
    
    # Step 2: Run Category Agents Analysis
    print("🤖 STEP 2: OpenRouter Category Agents Analysis")
    print("-" * 45)
    
    json_files = ["quoteA.json", "quoteB.json"]
    if quotes_count >= 3:
        json_files.append("quoteC.json")
    
    # Verify JSON files exist
    for json_file in json_files:
        if not Path(json_file).exists():
            print(f"❌ JSON file not found: {json_file}")
            sys.exit(1)
    
    cmd = ["python", "category_agents.py"] + json_files
    if not run_command(cmd, "Running OpenRouter category analysis"):
        sys.exit(1)
    print()
    
    # Step 3: Generate Final Consolidated Report
    print("📊 STEP 3: Final Report Generation")
    print("-" * 35)
    
    # Read all agent outputs and create consolidated report
    reports_dir = Path("reports/agents")
    if not reports_dir.exists():
        print("❌ Agent reports directory not found")
        sys.exit(1)
    
    # Create consolidated report
    final_report = []
    final_report.append(f"# Insurance Quote Comparison Report ({quotes_count} Quotes)")
    final_report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    final_report.append(f"Source PDFs: {', '.join(pdf_files)}")
    final_report.append("")
    final_report.append("## Executive Summary")
    final_report.append("")
    final_report.append("This report provides a comprehensive comparison of insurance quotes using AI-powered category analysis.")
    final_report.append("Each section has been analyzed by specialized agents using OpenRouter's Kimi K2 model.")
    final_report.append("")
    final_report.append("## Table of Contents")
    final_report.append("")
    
    # Add table of contents
    from category_agents import CATEGORIES
    for i, category in enumerate(CATEGORIES, 1):
        safe_name = category.lower().replace(' ', '-').replace('/', '-').replace("'", "")
        final_report.append(f"{i}. [{category}](#{safe_name})")
    
    final_report.append("")
    final_report.append("---")
    final_report.append("")
    
    # Add each category analysis
    category_count = 0
    for category in CATEGORIES:
        safe_filename = category.lower().replace(' ', '_').replace('/', '_').replace("'", "")
        agent_file = reports_dir / f"{safe_filename}.md"
        
        if agent_file.exists():
            content = agent_file.read_text(encoding='utf-8')
            final_report.append(content)
            final_report.append("")
            final_report.append("---")
            final_report.append("")
            category_count += 1
    
    # Write final report
    final_report_path = Path("final_comparison_report.md")
    final_report_path.write_text("\n".join(final_report), encoding='utf-8')
    
    print(f"✅ Final report generated: {final_report_path}")
    print(f"   Categories analyzed: {category_count}")
    print()
    
    # Step 4: Summary and Next Steps
    print("🎉 WORKFLOW COMPLETED SUCCESSFULLY!")
    print("=" * 40)
    print("📁 Generated Files:")
    print(f"   • JSON Files: {', '.join(json_files)}")
    print(f"   • Agent Reports: reports/agents/*.md ({category_count} files)")
    print(f"   • Final Report: {final_report_path}")
    print()
    print("📖 Next Steps:")
    print(f"   • Review the final report: {final_report_path}")
    print("   • Check individual category analyses in reports/agents/")
    print("   • Use the data for client presentations or further analysis")
    print()
    print(f"⏱️  Total processing time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    asyncio.run(main()) 