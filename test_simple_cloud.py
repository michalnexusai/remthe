#!/usr/bin/env python3
"""
Simple test to check cloud endpoint status and response
"""

import asyncio
import aiohttp
import json

async def test_simple_request():
    """Test a simple request to see what's happening"""
    print("🔍 SIMPLE CLOUD ENDPOINT TEST")
    print("=" * 50)
    
    # Simpler test payload
    payload = {
        "messages": [
            {
                "role": "user", 
                "content": "Hello"
            }
        ]
    }
    
    url = "https://capps-backend-sh6xxeyvkvn66.ambitioushill-723781d2.westus2.azurecontainerapps.io/chat/stream"
    
    try:
        async with aiohttp.ClientSession() as session:
            print(f"🌐 Testing URL: {url}")
            print(f"📤 Payload: {json.dumps(payload, indent=2)}")
            
            async with session.post(url, json=payload) as response:
                print(f"\n📨 Response:")
                print(f"  Status: {response.status}")
                print(f"  Headers: {dict(response.headers)}")
                
                content = await response.text()
                print(f"\n📄 Content ({len(content)} chars):")
                print(repr(content))
                
                if content:
                    print(f"\n📄 Formatted Content:")
                    print(content)
                
    except Exception as e:
        print(f"❌ Error: {e}")

async def test_with_new_format():
    """Test with the new array format"""
    print("\n" + "=" * 50)
    print("🔍 TESTING WITH NEW ARRAY FORMAT")
    print("=" * 50)
    
    # Test with new array format
    payload = {
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": "Hello"}]
            }
        ],
        "context": {
            "overrides": {
                "use_oid_security_filter": False,
                "use_groups_security_filter": False
            }
        }
    }
    
    url = "https://capps-backend-sh6xxeyvkvn66.ambitioushill-723781d2.westus2.azurecontainerapps.io/chat/stream"
    
    try:
        async with aiohttp.ClientSession() as session:
            print(f"🌐 Testing URL: {url}")
            print(f"📤 Payload: {json.dumps(payload, indent=2)}")
            
            async with session.post(url, json=payload) as response:
                print(f"\n📨 Response:")
                print(f"  Status: {response.status}")
                print(f"  Headers: {dict(response.headers)}")
                
                content = await response.text()
                print(f"\n📄 Content ({len(content)} chars):")
                print(repr(content))
                
                if content:
                    print(f"\n📄 Formatted Content:")
                    print(content)
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    async def main():
        await test_simple_request()
        await test_with_new_format()
    
    asyncio.run(main())