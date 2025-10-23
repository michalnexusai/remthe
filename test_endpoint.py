#!/usr/bin/env python3
"""
Test the actual /chat/stream endpoint
"""

import asyncio
import aiohttp
import json

async def test_streaming_endpoint():
    """Test the actual streaming endpoint"""
    print("🌐 TESTING ACTUAL /chat/stream ENDPOINT")
    print("=" * 50)
    
    # Test payload
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
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    print(f"❌ HTTP {response.status}: {await response.text()}")
                    return
                
                print(f"✅ HTTP {response.status}")
                print(f"Content-Type: {response.headers.get('content-type')}")
                print("\n📡 STREAMING RESPONSE:")
                
                chunk_count = 0
                received_data = ""
                
                async for chunk in response.content.iter_chunked(1024):
                    chunk_count += 1
                    chunk_text = chunk.decode('utf-8')
                    received_data += chunk_text
                    
                    print(f"\nChunk {chunk_count}:")
                    print(f"  Size: {len(chunk_text)} chars")
                    print(f"  Ends with \\n: {chunk_text.endswith('\\n')}")
                    print(f"  Raw: {repr(chunk_text[:100])}")
                
                print(f"\n📊 SUMMARY:")
                print(f"  Total chunks: {chunk_count}")
                print(f"  Total size: {len(received_data)} chars")
                print(f"  Final ends with \\n: {received_data.endswith('\\n')}")
                
                # Try to parse as NDJSON
                print(f"\n🔍 NDJSON PARSING:")
                lines = [line for line in received_data.split('\\n') if line.strip()]
                print(f"  Total lines: {len(lines)}")
                
                valid_count = 0
                for i, line in enumerate(lines[:5]):  # Check first 5
                    try:
                        obj = json.loads(line)
                        valid_count += 1
                        obj_type = "CHOICES" if "choices" in obj else "DELTA"
                        print(f"  Line {i+1}: ✅ Valid {obj_type}")
                    except json.JSONDecodeError as e:
                        print(f"  Line {i+1}: ❌ {e}")
                        print(f"    Content: {repr(line[:50])}")
                
                if len(lines) > 5:
                    print(f"  ... checking remaining {len(lines)-5} lines")
                    for line in lines[5:]:
                        try:
                            json.loads(line)
                            valid_count += 1
                        except:
                            pass
                
                print(f"  Valid JSON lines: {valid_count}/{len(lines)}")
                
                if valid_count == len(lines):
                    print("  🎉 ALL LINES ARE VALID JSON - PERFECT NDJSON!")
                else:
                    print("  ❌ SOME LINES ARE INVALID")
                
    except aiohttp.ClientConnectorError:
        print("❌ Cannot connect to the cloud endpoint")
        print("   Check if the service is running and accessible")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_streaming_endpoint())