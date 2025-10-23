#!/usr/bin/env python3
"""
Test cloud endpoint for both choices streaming AND array format preprocessing
"""

import asyncio
import aiohttp
import json

async def test_cloud_array_format():
    """Test if the cloud endpoint supports the new array format"""
    print("🔍 TESTING CLOUD ENDPOINT ARRAY FORMAT SUPPORT")
    print("=" * 60)
    
    # Test payload with NEW array format
    payload = {
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": "Say hello briefly"}]
            }
        ],
        "context": {
            "overrides": {
                "use_oid_security_filter": False,
                "use_groups_security_filter": False
            }
        }
    }
    
    url = "https://capps-backend-l4laiw3is6k5y.greenpebble-5418c67f.westus2.azurecontainerapps.io/chat/stream"
    
    try:
        async with aiohttp.ClientSession() as session:
            print(f"🌐 Testing URL: {url}")
            print(f"📤 New Array Format Payload:")
            print(json.dumps(payload, indent=2))
            
            async with session.post(url, json=payload) as response:
                print(f"\n📨 Response:")
                print(f"  Status: {response.status}")
                print(f"  Content-Type: {response.headers.get('content-type')}")
                
                content = await response.text()
                print(f"  Response size: {len(content)} chars")
                
                if response.status == 200:
                    print("  ✅ Array format accepted!")
                    
                    # Quick analysis
                    lines = [line for line in content.split('\n') if line.strip()]
                    choices_count = 0
                    delta_count = 0
                    
                    for line in lines:
                        try:
                            obj = json.loads(line)
                            if "choices" in obj:
                                choices_count += 1
                            elif "delta" in obj:
                                delta_count += 1
                        except:
                            pass
                    
                    print(f"  📊 Quick analysis:")
                    print(f"    Delta objects: {delta_count}")
                    print(f"    Choices objects: {choices_count}")
                    
                    if choices_count > 0:
                        print("  🎉 NEW FEATURES DEPLOYED: Array format + Choices streaming!")
                    else:
                        print("  ✅ Array format works, but no choices streaming yet")
                else:
                    print("  ❌ Array format failed!")
                    print(f"  Error: {content}")
                
    except Exception as e:
        print(f"❌ Error: {e}")


async def test_deployment_status():
    """Check what features are currently deployed"""
    print("\n" + "=" * 60)
    print("🚀 DEPLOYMENT STATUS CHECK")
    print("=" * 60)
    
    print("Testing multiple scenarios to determine what's deployed...")
    
    # Test 1: Old format (should always work)
    print("\n📋 Test 1: Old format (baseline)")
    old_payload = {
        "messages": [{"role": "user", "content": "Hi"}]
    }
    
    # Test 2: New array format  
    print("\n📋 Test 2: New array format (preprocessing)")
    new_payload = {
        "messages": [{"role": "user", "content": [{"type": "text", "text": "Hi"}]}]
    }
    
    url = "https://capps-backend-l4laiw3is6k5y.greenpebble-5418c67f.westus2.azurecontainerapps.io/chat/stream"
    
    results = {}
    
    for test_name, payload in [("old_format", old_payload), ("new_format", new_payload)]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    content = await response.text()
                    
                    if response.status == 200:
                        # Count choices objects
                        lines = [line for line in content.split('\n') if line.strip()]
                        choices_count = sum(1 for line in lines 
                                          if line.strip() and "choices" in json.loads(line))
                        
                        results[test_name] = {
                            "status": "success",
                            "choices_count": choices_count,
                            "total_lines": len(lines)
                        }
                        print(f"  ✅ {test_name}: Success, {choices_count} choices objects")
                    else:
                        results[test_name] = {"status": "failed", "error": content[:100]}
                        print(f"  ❌ {test_name}: Failed")
                        
        except Exception as e:
            results[test_name] = {"status": "error", "error": str(e)}
            print(f"  ❌ {test_name}: Error - {e}")
    
    print(f"\n🎯 DEPLOYMENT STATUS SUMMARY:")
    
    old_works = results.get("old_format", {}).get("status") == "success"
    new_works = results.get("new_format", {}).get("status") == "success"
    choices_available = any(r.get("choices_count", 0) > 0 for r in results.values() if isinstance(r, dict))
    
    print(f"  Old format support: {'✅' if old_works else '❌'}")
    print(f"  New array format support: {'✅' if new_works else '❌'}")
    print(f"  Choices streaming: {'✅' if choices_available else '❌'}")
    
    if old_works and new_works and choices_available:
        print(f"\n  🎉 FULLY DEPLOYED: All features are live!")
    elif old_works and new_works:
        print(f"\n  ✅ PARTIALLY DEPLOYED: Array preprocessing is live, choices streaming pending")
    elif old_works:
        print(f"\n  ⚠️  OLD DEPLOYMENT: Only original functionality available")
    else:
        print(f"\n  ❌ DEPLOYMENT ISSUES: Basic functionality not working")


if __name__ == "__main__":
    async def main():
        await test_cloud_array_format()
        await test_deployment_status()
    
    asyncio.run(main())