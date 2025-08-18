#!/usr/bin/env python3
"""
Simple test script to verify the AI-Enhanced Insurance Quote Comparison System
"""

import requests
import json
import time
import os

def test_system():
    """Test the complete system"""
    base_url = "http://localhost:5000"
    
    print("🤖 Testing AI-Enhanced Insurance Quote Comparison System")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health Check: {health_data['status']}")
            print(f"   Services: {health_data['services']}")
        else:
            print(f"❌ Health Check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health Check error: {e}")
    
    # Test 2: Root Endpoint
    print("\n2. Testing Root Endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            root_data = response.json()
            print(f"✅ Root Endpoint: {root_data['message']}")
            print(f"   Version: {root_data['version']}")
            print(f"   Features: {len(root_data['features'])} features available")
        else:
            print(f"❌ Root Endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root Endpoint error: {e}")
    
    # Test 3: User Stats
    print("\n3. Testing User Stats...")
    try:
        headers = {"Authorization": "Bearer demo-token"}
        response = requests.get(f"{base_url}/api/quotes/stats", headers=headers)
        if response.status_code == 200:
            stats_data = response.json()
            print(f"✅ User Stats: {stats_data['total_quotes']} total quotes")
            print(f"   Completed: {stats_data['completed']}")
            print(f"   Average Premium: {stats_data['average_premium']}")
        else:
            print(f"❌ User Stats failed: {response.status_code}")
    except Exception as e:
        print(f"❌ User Stats error: {e}")
    
    # Test 4: User Quotes
    print("\n4. Testing User Quotes...")
    try:
        headers = {"Authorization": "Bearer demo-token"}
        response = requests.get(f"{base_url}/api/quotes/my-quotes", headers=headers)
        if response.status_code == 200:
            quotes_data = response.json()
            print(f"✅ User Quotes: {quotes_data['total_comparisons']} comparisons")
        else:
            print(f"❌ User Quotes failed: {response.status_code}")
    except Exception as e:
        print(f"❌ User Quotes error: {e}")
    
    # Test 5: LLMWhisperer Client Integration
    print("\n5. Testing LLMWhisperer Integration...")
    try:
        from backend.services.pdf_extractor import PDFExtractor
        extractor = PDFExtractor()
        
        if hasattr(extractor, 'client') and extractor.client:
            print("✅ LLMWhisperer Official Client initialized")
            print(f"   API Key configured: {'Yes' if extractor.api_key else 'No'}")
            print(f"   Base URL: {extractor.base_url}")
        else:
            print("⚠️ LLMWhisperer Client not initialized (will use fallback)")
            
    except ImportError as e:
        print(f"⚠️ LLMWhisperer client not installed: {e}")
        print("   Install with: pip install llmwhisperer-client")
    except Exception as e:
        print(f"❌ LLMWhisperer integration test failed: {e}")
    
    # Test 6: Environment Variables Check
    print("\n6. Testing Environment Configuration...")
    env_vars = {
        'LLM_API_KEY': 'LLMWhisperer API Key',
        'OPENAI_API_KEY': 'OpenAI API Key (optional)',
        'ANTHROPIC_API_KEY': 'Anthropic API Key (optional)',
        'GOOGLE_API_KEY': 'Google API Key (optional)'
    }
    
    for var, description in env_vars.items():
        value = os.getenv(var)
        if value:
            print(f"✅ {description}: {'*' * 10}{value[-4:] if len(value) > 4 else '****'}")
        else:
            status = "⚠️" if var == 'LLM_API_KEY' else "ℹ️"
            print(f"{status} {description}: Not configured")
    
    print("\n" + "=" * 60)
    print("🎉 System test completed!")
    print("\n📋 Next Steps:")
    print("1. Install LLMWhisperer client: pip install llmwhisperer-client")
    print("2. Set environment variables (especially LLM_API_KEY)")
    print("3. Start backend: cd backend && python main.py")
    print("4. Start frontend: npm run dev")
    print("5. Upload PDFs at: http://localhost:3000/upload-pdf")
    print("6. View reports at: http://localhost:3000/my-quotes")
    print("\n🔧 Configuration:")
    print("   - LLM_API_KEY: Required for LLMWhisperer")
    print("   - OPENAI_API_KEY: Optional for enhanced LLM analysis")
    print("   - ANTHROPIC_API_KEY: Optional for Claude analysis")
    print("   - GOOGLE_API_KEY: Optional for Gemini analysis")

def test_llmwhisperer_client():
    """Test LLMWhisperer client specifically"""
    print("\n🔍 Testing LLMWhisperer Client Specifically...")
    
    try:
        from unstract.llmwhisperer import LLMWhispererClientV2
        from unstract.llmwhisperer.client_v2 import LLMWhispererClientException
        
        api_key = os.getenv('LLM_API_KEY')
        if not api_key:
            print("⚠️ LLM_API_KEY not set - cannot test client")
            return
        
        client = LLMWhispererClientV2(api_key=api_key)
        
        # Test usage info
        try:
            usage_info = client.get_usage_info()
            print(f"✅ LLMWhisperer Client connected successfully")
            print(f"   Usage info retrieved: {len(str(usage_info))} characters")
        except LLMWhispererClientException as e:
            print(f"❌ LLMWhisperer API error: {e.message} (Status: {e.status_code})")
        except Exception as e:
            print(f"❌ LLMWhisperer client error: {e}")
            
    except ImportError:
        print("❌ LLMWhisperer client not installed")
        print("   Install with: pip install llmwhisperer-client")

if __name__ == "__main__":
    test_system()
    test_llmwhisperer_client() 