#!/usr/bin/env python3
"""
Test the cloud endpoint specifically for CHOICES object streaming analysis
"""

import asyncio
import aiohttp
import json

async def test_cloud_choices_streaming():
    """Test the cloud endpoint for choices object streaming"""
    print("🌐 CLOUD ENDPOINT CHOICES STREAMING TEST")
    print("=" * 60)
    
    # Test payload with old format (should work)
    payload = {
        "messages": [
            {
                "role": "user",
                "content": "Say hello briefly"
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
            print(f"📤 Payload: {json.dumps(payload, indent=2)}")
            
            async with session.post(url, json=payload) as response:
                print(f"\n📨 Response:")
                print(f"  Status: {response.status}")
                print(f"  Content-Type: {response.headers.get('content-type')}")
                
                if response.status != 200:
                    error_content = await response.text()
                    print(f"❌ Error: {error_content}")
                    return
                
                # Collect the full response
                content = await response.text()
                print(f"  Total size: {len(content)} chars")
                
                # Analyze the response
                await analyze_cloud_choices_response(content)
                
    except Exception as e:
        print(f"❌ Error: {e}")


async def analyze_cloud_choices_response(response_text: str):
    """Analyze the cloud response for choices objects"""
    print(f"\n🔍 CHOICES ANALYSIS FOR CLOUD RESPONSE:")
    print("=" * 50)
    
    # Split by newlines and filter empty lines
    lines = [line for line in response_text.split('\n') if line.strip()]
    print(f"📊 Basic stats:")
    print(f"  Total lines: {len(lines)}")
    
    # Categorize objects
    delta_objects = []
    choices_objects = []
    context_objects = []
    invalid_lines = []
    
    print(f"\n🔍 Line-by-line analysis:")
    for i, line in enumerate(lines):
        try:
            obj = json.loads(line)
            
            if "choices" in obj:
                choices_objects.append(obj)
                content = obj.get("delta", {}).get("content", "")
                content_preview = repr(content[:15]) if len(str(content)) > 15 else repr(content)
                print(f"  Line {i+1:2}: ✅ CHOICES | content: {content_preview}")
                
            elif "delta" in obj:
                delta_objects.append(obj)
                content = obj.get("delta", {}).get("content")
                
                # Check if this is a context object (has non-content fields)
                if "context" in obj and obj["context"]:
                    context_objects.append(obj)
                    print(f"  Line {i+1:2}: ✅ CONTEXT | has thoughts/data")
                else:
                    if content is not None:
                        content_preview = repr(content[:15]) if len(str(content)) > 15 else repr(content)
                    else:
                        content_preview = "None"
                    print(f"  Line {i+1:2}: ✅ DELTA   | content: {content_preview}")
            else:
                print(f"  Line {i+1:2}: ✅ OTHER   | keys: {list(obj.keys())}")
                
        except json.JSONDecodeError as e:
            invalid_lines.append((i+1, line, str(e)))
            print(f"  Line {i+1:2}: ❌ INVALID | {str(e)[:30]}")
    
    print(f"\n📈 SUMMARY:")
    print(f"  Delta objects: {len(delta_objects)}")
    print(f"  Context objects: {len(context_objects)}")
    print(f"  Choices objects: {len(choices_objects)}")
    print(f"  Invalid lines: {len(invalid_lines)}")
    print(f"  Total valid JSON: {len(delta_objects) + len(choices_objects)}")
    
    # Analyze choices objects specifically
    print(f"\n🎯 CHOICES OBJECTS ANALYSIS:")
    if choices_objects:
        print(f"  ✅ Found {len(choices_objects)} choices objects!")
        
        # Check metadata consistency
        first_choice = choices_objects[0]
        shared_id = first_choice.get("id", "")
        shared_created = first_choice.get("created", 0)
        shared_model = first_choice.get("model", "")
        
        print(f"  📋 Metadata:")
        print(f"    ID: {shared_id}")
        print(f"    Created: {shared_created}")
        print(f"    Model: {shared_model}")
        
        # Check consistency across all choices
        consistent_id = all(obj.get("id") == shared_id for obj in choices_objects)
        consistent_created = all(obj.get("created") == shared_created for obj in choices_objects)
        consistent_model = all(obj.get("model") == shared_model for obj in choices_objects)
        
        print(f"  📊 Consistency:")
        print(f"    ID consistent: {'✅' if consistent_id else '❌'}")
        print(f"    Created consistent: {'✅' if consistent_created else '❌'}")
        print(f"    Model consistent: {'✅' if consistent_model else '❌'}")
        
        # Analyze choices content
        print(f"  📋 Content analysis:")
        choices_content_parts = []
        for i, choice_obj in enumerate(choices_objects):
            delta_content = choice_obj.get("delta", {}).get("content", "")
            message_content = choice_obj.get("choices", [{}])[0].get("messages", [{}])[0].get("content", "")
            
            choices_content_parts.append(delta_content)
            content_match = delta_content == message_content
            
            print(f"    Choice {i+1}: delta='{delta_content}' | message='{message_content}' | match={'✅' if content_match else '❌'}")
        
        # Reconstruct message from choices
        choices_message = "".join(choices_content_parts)
        print(f"  💬 Reconstructed from choices: '{choices_message}'")
        
    else:
        print("  ❌ NO CHOICES OBJECTS FOUND!")
        print("     This suggests the cloud deployment doesn't have the latest changes yet.")
    
    # Analyze delta objects for comparison
    print(f"\n📋 DELTA OBJECTS ANALYSIS:")
    delta_content_parts = []
    non_empty_delta_content = []
    
    for obj in delta_objects:
        if "context" not in obj or not obj["context"]:  # Skip context objects
            content = obj.get("delta", {}).get("content")
            if content is not None:
                delta_content_parts.append(content)
                if content != "":
                    non_empty_delta_content.append(content)
    
    delta_message = "".join(delta_content_parts)
    print(f"  💬 Reconstructed from deltas: '{delta_message}'")
    print(f"  📊 Delta content pieces: {len(delta_content_parts)} total, {len(non_empty_delta_content)} non-empty")
    
    # Check ordering (deltas before choices)
    print(f"\n📋 ORDERING ANALYSIS:")
    if choices_objects:
        choices_start_line = None
        delta_after_choices = False
        
        for i, line in enumerate(lines):
            try:
                obj = json.loads(line)
                if "choices" in obj and choices_start_line is None:
                    choices_start_line = i + 1
                elif "choices" not in obj and "delta" in obj and choices_start_line is not None:
                    if "context" not in obj or not obj["context"]:  # Skip context objects
                        delta_after_choices = True
                        print(f"    ❌ Found delta object at line {i+1} after choices started at line {choices_start_line}")
                        break
            except:
                pass
        
        if not delta_after_choices:
            print("    ✅ Correct ordering: All delta objects before choices objects")
        
        # Compare expected vs actual choices count
        expected_choices = len(non_empty_delta_content)  # Assuming we don't want empty strings
        actual_choices = len(choices_objects)
        
        print(f"\n📊 CHOICES COUNT ANALYSIS:")
        print(f"  Expected choices (non-empty delta content): {expected_choices}")
        print(f"  Actual choices: {actual_choices}")
        if expected_choices == actual_choices:
            print("  ✅ Choices count matches expected")
        else:
            print("  ⚠️  Choices count differs - might include empty strings")
    
    # Final verdict
    print(f"\n🏆 FINAL VERDICT:")
    if choices_objects:
        criteria_met = 0
        total_criteria = 4
        
        if len(choices_objects) > 0:
            criteria_met += 1
            print("  ✅ Choices objects are being generated")
        
        if choices_objects and consistent_id and consistent_created:
            criteria_met += 1
            print("  ✅ Metadata is consistent across choices")
        else:
            print("  ❌ Metadata inconsistency detected")
        
        if delta_message and choices_objects:
            choices_message = "".join(obj.get("delta", {}).get("content", "") for obj in choices_objects)
            if delta_message == choices_message:
                criteria_met += 1
                print("  ✅ Messages from deltas and choices match")
            else:
                print("  ❌ Message reconstruction mismatch")
        
        if not delta_after_choices:
            criteria_met += 1
            print("  ✅ Proper ordering maintained")
        else:
            print("  ❌ Ordering issues detected")
        
        print(f"\n  📊 Score: {criteria_met}/{total_criteria} criteria met")
        
        if criteria_met == total_criteria:
            print("  🎉 CLOUD ENDPOINT HAS PERFECT CHOICES STREAMING!")
        elif criteria_met >= 3:
            print("  ✅ CLOUD ENDPOINT HAS GOOD CHOICES STREAMING!")
        else:
            print("  ⚠️  CLOUD ENDPOINT CHOICES STREAMING NEEDS WORK")
    else:
        print("  ❌ CLOUD ENDPOINT DOESN'T HAVE CHOICES STREAMING YET")
        print("     The deployment might not include the latest changes")


if __name__ == "__main__":
    asyncio.run(test_cloud_choices_streaming())