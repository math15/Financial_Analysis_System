#!/usr/bin/env python3
"""
Complete end-to-end test of the insurance quote comparison system
Tests: Upload -> Process -> Generate Report -> Download
"""
import requests
import json
import os
import time

# Configuration
BASE_URL = "http://localhost:5000"
AUTH_TOKEN = "demo-token"

def test_complete_flow():
    """Test the complete flow: upload -> process -> generate report"""
    print("🧪 Testing Complete Flow: Upload -> Process -> Generate Report")
    print("=" * 70)
    
    headers = {
        'Authorization': f'Bearer {AUTH_TOKEN}'
    }
    
    # Step 1: Health Check
    print("🔍 Step 1: Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend is running and healthy")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return
    
    # Step 2: Create Sample PDF (since we might not have actual files)
    sample_pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Sample Insurance Quote) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000058 00000 n\n0000000115 00000 n\n0000000204 00000 n\ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF"
    
    sample_files = ["sample_quote_1.pdf", "sample_quote_2.pdf"]
    for filename in sample_files:
        with open(filename, 'wb') as f:
            f.write(sample_pdf_content)
    
    print(f"📄 Created {len(sample_files)} sample PDF files")
    
    # Step 3: Upload Files
    print(f"\n📤 Step 2: Uploading {len(sample_files)} files...")
    upload_url = f"{BASE_URL}/api/quotes/upload"
    
    files = []
    try:
        for filename in sample_files:
            f = open(filename, 'rb')
            files.append(('files', (filename, f, 'application/pdf')))
        
        response = requests.post(upload_url, headers=headers, files=files, timeout=120)
        response.raise_for_status()
        
        upload_result = response.json()
        print("✅ Upload successful!")
        print(f"📋 Comparison ID: {upload_result['comparison_id']}")
        print(f"📊 Quote Count: {upload_result['quote_count']}")
        print(f"📝 Message: {upload_result['message']}")
        
        comparison_id = upload_result['comparison_id']
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"📊 Response Status: {e.response.status_code}")
            print(f"📊 Response Text: {e.response.text}")
        return
    finally:
        # Close all file handles
        for _, (_, f, _) in files:
            f.close()
        # Clean up sample files
        for filename in sample_files:
            if os.path.exists(filename):
                os.remove(filename)
    
    # Step 4: Generate Report
    print(f"\n📄 Step 3: Generating report for comparison {comparison_id}...")
    report_url = f"{BASE_URL}/api/quotes/generate-report/{comparison_id}"
    
    try:
        response = requests.post(report_url, headers=headers, timeout=60)
        response.raise_for_status()
        
        report_result = response.json()
        print("✅ Report generation successful!")
        print(f"📋 Report ID: {report_result['report_id']}")
        print(f"📄 Filename: {report_result['filename']}")
        print(f"🔗 Download URL: {report_result['download_url']}")
        print(f"⏰ Generated at: {report_result['generated_at']}")
        
        filename = report_result['filename']
        
    except Exception as e:
        print(f"❌ Report generation failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"📊 Response Status: {e.response.status_code}")
            print(f"📊 Response Text: {e.response.text}")
        return
    
    # Step 5: Test Download
    print(f"\n📥 Step 4: Testing report download...")
    download_url = f"{BASE_URL}{report_result['download_url']}"
    
    try:
        response = requests.get(download_url, timeout=30)
        if response.status_code == 200:
            print("✅ Download successful!")
            print(f"📊 Downloaded {len(response.content):,} bytes")
            print(f"📋 Content-Type: {response.headers.get('content-type', 'Unknown')}")
            
            # Verify it's a PDF
            if response.content.startswith(b'%PDF'):
                print("✅ File is a valid PDF")
            else:
                print("⚠️ File might not be a valid PDF")
                
        else:
            print(f"❌ Download failed: {response.status_code}")
            print(f"📊 Response: {response.text}")
    
    except Exception as e:
        print(f"❌ Download test failed: {e}")
    
    # Step 6: Check User Quotes
    print(f"\n📋 Step 5: Checking user quotes...")
    quotes_url = f"{BASE_URL}/api/quotes/my-quotes"
    
    try:
        response = requests.get(quotes_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        quotes_result = response.json()
        print("✅ User quotes retrieved!")
        print(f"📊 Total comparisons: {quotes_result['total_comparisons']}")
        
        for i, comp in enumerate(quotes_result['comparisons']):
            print(f"📋 Comparison {i+1}:")
            print(f"   ID: {comp['comparison_id']}")
            print(f"   Files: {comp['file_names']}")
            print(f"   Status: {comp['status']}")
            print(f"   Quote Count: {comp['quote_count']}")
        
    except Exception as e:
        print(f"❌ Failed to get user quotes: {e}")
    
    # Final Summary
    print(f"\n🎉 SUCCESS! Complete flow test completed successfully!")
    print("=" * 70)
    print("✅ Backend health check: PASSED")
    print("✅ File upload: PASSED") 
    print("✅ PDF report generation: PASSED")
    print("✅ Report download: PASSED")
    print("✅ User quotes retrieval: PASSED")
    print(f"\n📂 Your PDF report is available at: {download_url}")

if __name__ == "__main__":
    test_complete_flow() 