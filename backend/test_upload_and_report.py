#!/usr/bin/env python3
"""
Test script to upload files and generate a report to verify the complete flow
"""
import requests
import json
import os
import time

# Configuration
BASE_URL = "http://localhost:5000"
AUTH_TOKEN = "demo-token"
TEST_FILES = [
    "../3 civil commercial.pdf",
    "test_sample.txt"  # We'll create this as a backup
]

def test_upload_and_report():
    """Test uploading files and generating a report"""
    print("🧪 Testing Upload and Report Generation")
    print("=" * 60)
    
    headers = {
        'Authorization': f'Bearer {AUTH_TOKEN}'
    }
    
    # Find available test files
    found_files = []
    for test_file in TEST_FILES:
        if os.path.exists(test_file):
            found_files.append(test_file)
            print(f"✅ Found test file: {test_file}")
        else:
            print(f"❌ Test file not found: {test_file}")
    
    if not found_files:
        print("❌ No test files found!")
        return
    
    # Step 1: Upload files
    print(f"\n📤 Step 1: Uploading {len(found_files)} files...")
    upload_url = f"{BASE_URL}/api/quotes/upload"
    
    files = []
    try:
        for file_path in found_files:
            f = open(file_path, 'rb')
            files.append(('files', f))
        
        response = requests.post(upload_url, headers=headers, files=files, timeout=60)
        response.raise_for_status()
        
        upload_result = response.json()
        print("✅ Upload successful!")
        print(f"📋 Comparison ID: {upload_result['comparison_id']}")
        print(f"📊 Quote Count: {upload_result['quote_count']}")
        
        comparison_id = upload_result['comparison_id']
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return
    finally:
        # Close all file handles
        for _, f in files:
            f.close()
    
    # Step 2: Generate report
    print(f"\n📄 Step 2: Generating report for comparison {comparison_id}...")
    report_url = f"{BASE_URL}/api/quotes/generate-report/{comparison_id}"
    
    try:
        response = requests.post(report_url, headers=headers, timeout=60)
        response.raise_for_status()
        
        report_result = response.json()
        print("✅ Report generation successful!")
        print(f"📋 Report ID: {report_result['report_id']}")
        print(f"📄 Filename: {report_result['filename']}")
        print(f"🔗 Download URL: {report_result['download_url']}")
        
        # Step 3: Check if file exists
        filename = report_result['filename']
        report_path = f"../reports/{filename}"
        
        if os.path.exists(report_path):
            print(f"✅ Report file exists: {report_path}")
            file_size = os.path.getsize(report_path)
            print(f"📊 File size: {file_size:,} bytes")
        else:
            print(f"❌ Report file not found: {report_path}")
            # List all files in reports directory
            reports_dir = "../reports"
            if os.path.exists(reports_dir):
                files_in_reports = os.listdir(reports_dir)
                print(f"📂 Files in reports directory: {files_in_reports}")
            else:
                print(f"📂 Reports directory does not exist: {reports_dir}")
        
        # Step 4: Test download URL
        print(f"\n📥 Step 3: Testing download URL...")
        download_url = f"{BASE_URL}{report_result['download_url']}"
        
        response = requests.get(download_url, headers=headers, timeout=30)
        if response.status_code == 200:
            print("✅ Download URL works!")
            print(f"📊 Downloaded {len(response.content):,} bytes")
            print(f"📋 Content-Type: {response.headers.get('content-type', 'Unknown')}")
        else:
            print(f"❌ Download failed: {response.status_code} - {response.text}")
        
    except Exception as e:
        print(f"❌ Report generation failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"📊 Response Status: {e.response.status_code}")
            print(f"📊 Response Text: {e.response.text}")
    
    # Step 4: List user quotes
    print(f"\n📋 Step 4: Checking user quotes...")
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
            print(f"   Created: {comp['created_at']}")
        
    except Exception as e:
        print(f"❌ Failed to get user quotes: {e}")

if __name__ == "__main__":
    test_upload_and_report() 