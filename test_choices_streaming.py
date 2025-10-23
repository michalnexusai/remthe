#!/usr/bin/env python3
"""
Test specifically focused on CHOICES object streaming analysis
"""

import asyncio
import json
import time
import uuid
from typing import AsyncGenerator


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        return super().default(o)


async def format_as_ndjson(r: AsyncGenerator[dict, None]) -> AsyncGenerator[str, None]:
    """Current implementation with CHOICES objects - copied from app.py"""
    try:
        all_events = []
        content_chunks = []
        
        # Collect all events first
        async for event in r:
            all_events.append(event)
            
            # If this event has delta content (not None), collect it for choices objects
            if "delta" in event and "content" in event["delta"] and event["delta"]["content"] is not None:
                delta_content = event["delta"]["content"]
                content_chunks.append(delta_content)
        
        # Generate shared values for all choices objects
        shared_id = f"chatcmpl-{uuid.uuid4().hex[:25]}"
        shared_created = int(time.time())
        shared_apim_request_id = f"chatcmpl-{shared_id[9:]}"
        
        # First, yield all the original delta events
        for event in all_events:
            yield json.dumps(event, ensure_ascii=False, cls=JSONEncoder) + "\n"
        
        # Then yield all the choices objects at the end
        for delta_content in content_chunks:
            completion_chunk = {
                "id": shared_id,
                "model": "gpt-4.1-mini-2025-04-14",
                "created": shared_created,
                "object": "chat.completion.chunk",
                "choices": [
                    {
                        "messages": [
                            {
                                "role": "assistant",
                                "content": delta_content
                            }
                        ]
                    }
                ],
                "history_metadata": {},
                "apim-request-id": shared_apim_request_id,
                "delta": {
                    "content": delta_content,
                    "role": "assistant" if delta_content else None
                }
            }
            yield json.dumps(completion_chunk, ensure_ascii=False, cls=JSONEncoder) + "\n"
            
    except Exception as error:
        print(f"Exception while generating response stream: {error}")
        yield json.dumps({"error": str(error)}) + "\n"


async def mock_stream_with_content() -> AsyncGenerator[dict, None]:
    """Mock stream that produces content chunks for choices analysis"""
    
    # First event with context (no content)
    yield {
        "delta": {"role": "assistant"},
        "context": {
            "data_points": {"text": [], "images": [], "citations": []},
            "thoughts": [
                {
                    "title": "Search and Answer",
                    "description": "Generated response for user query",
                    "props": {"model": "gpt-4.1-mini"}
                }
            ],
            "followup_questions": None
        },
        "session_state": None
    }
    
    # Content chunks - these should generate choices objects
    content_chunks = ["Hello", "!", " How", " can", " I", " help", " you", " today", "?"]
    for chunk in content_chunks:
        yield {
            "delta": {
                "content": chunk,
                "role": "assistant"
            }
        }
    
    # Empty content chunk (should not generate choices object)
    yield {
        "delta": {
            "content": "",
            "role": "assistant"
        }
    }
    
    # Null content chunk (should not generate choices object)
    yield {
        "delta": {
            "content": None,
            "role": "assistant"
        }
    }
    
    # Final event with context (no content)
    yield {
        "delta": {"role": "assistant"},
        "context": {
            "data_points": {"text": [], "images": [], "citations": []},
            "thoughts": [],
            "followup_questions": None
        },
        "session_state": None
    }


async def analyze_choices_streaming():
    """Analyze the choices object streaming specifically"""
    print("🎯 CHOICES OBJECT STREAMING ANALYSIS")
    print("=" * 60)
    
    # Generate the formatted output
    mock_gen = mock_stream_with_content()
    formatted_gen = format_as_ndjson(mock_gen)
    
    # Collect all chunks
    chunks = []
    async for chunk in formatted_gen:
        chunks.append(chunk)
    
    full_output = "".join(chunks)
    
    print("📊 BASIC ANALYSIS:")
    print(f"  Total chunks: {len(chunks)}")
    print(f"  Total characters: {len(full_output)}")
    
    # Parse and categorize each line
    lines = [line for line in full_output.split('\n') if line.strip()]
    print(f"  Total lines: {len(lines)}")
    
    delta_objects = []
    choices_objects = []
    other_objects = []
    
    print(f"\n🔍 OBJECT ANALYSIS:")
    for i, line in enumerate(lines):
        try:
            obj = json.loads(line)
            
            if "choices" in obj:
                choices_objects.append(obj)
                content = obj.get("delta", {}).get("content", "")
                print(f"  Line {i+1:2}: ✅ CHOICES | content: {repr(content[:20])}")
            elif "delta" in obj:
                delta_objects.append(obj)
                content = obj.get("delta", {}).get("content")
                if content is not None:
                    content_repr = repr(content) if len(str(content)) <= 10 else repr(content[:10]) + "..."
                else:
                    content_repr = "None"
                print(f"  Line {i+1:2}: ✅ DELTA   | content: {content_repr}")
            else:
                other_objects.append(obj)
                print(f"  Line {i+1:2}: ✅ OTHER   | keys: {list(obj.keys())}")
                
        except json.JSONDecodeError as e:
            print(f"  Line {i+1:2}: ❌ INVALID | {str(e)[:30]}")
    
    print(f"\n📈 SUMMARY:")
    print(f"  Delta objects: {len(delta_objects)}")
    print(f"  Choices objects: {len(choices_objects)}")
    print(f"  Other objects: {len(other_objects)}")
    print(f"  Total valid JSON: {len(delta_objects) + len(choices_objects) + len(other_objects)}")
    
    # Analyze choices objects specifically
    print(f"\n🎯 CHOICES OBJECTS DETAILED ANALYSIS:")
    if choices_objects:
        # Check if all choices objects have same ID/created time
        first_choice = choices_objects[0]
        shared_id = first_choice.get("id")
        shared_created = first_choice.get("created")
        shared_apim_id = first_choice.get("apim-request-id")
        
        print(f"  Shared ID: {shared_id}")
        print(f"  Shared created: {shared_created}")
        print(f"  Shared apim-request-id: {shared_apim_id}")
        
        consistent_ids = all(obj.get("id") == shared_id for obj in choices_objects)
        consistent_created = all(obj.get("created") == shared_created for obj in choices_objects)
        consistent_apim = all(obj.get("apim-request-id") == shared_apim_id for obj in choices_objects)
        
        print(f"  ID consistency: {'✅' if consistent_ids else '❌'}")
        print(f"  Created consistency: {'✅' if consistent_created else '❌'}")
        print(f"  Apim-request-id consistency: {'✅' if consistent_apim else '❌'}")
        
        print(f"\n  📋 Choices Content Analysis:")
        for i, choice_obj in enumerate(choices_objects):
            content = choice_obj.get("delta", {}).get("content", "")
            message_content = choice_obj.get("choices", [{}])[0].get("messages", [{}])[0].get("content", "")
            
            content_match = content == message_content
            print(f"    Choice {i+1}: delta.content={repr(content)} | message.content={repr(message_content)} | match={'✅' if content_match else '❌'}")
    else:
        print("  ❌ NO CHOICES OBJECTS FOUND!")
    
    # Check ordering: deltas first, then choices
    print(f"\n📋 ORDERING ANALYSIS:")
    found_choices = False
    ordering_correct = True
    
    for i, line in enumerate(lines):
        try:
            obj = json.loads(line)
            if "choices" in obj:
                found_choices = True
            elif "delta" in obj and found_choices:
                ordering_correct = False
                print(f"  ❌ Found delta object after choices object at line {i+1}")
                break
        except:
            pass
    
    if ordering_correct:
        print("  ✅ Correct ordering: All delta objects come before choices objects")
    else:
        print("  ❌ Incorrect ordering: Delta objects found after choices objects")
    
    # Reconstruct the full message
    print(f"\n💬 MESSAGE RECONSTRUCTION:")
    delta_content_parts = []
    for obj in delta_objects:
        content = obj.get("delta", {}).get("content")
        if content is not None and content != "":
            delta_content_parts.append(content)
    
    full_message = "".join(delta_content_parts)
    print(f"  From deltas: '{full_message}'")
    
    choices_content_parts = [obj.get("delta", {}).get("content", "") for obj in choices_objects]
    choices_message = "".join(choices_content_parts)
    print(f"  From choices: '{choices_message}'")
    print(f"  Messages match: {'✅' if full_message == choices_message else '❌'}")
    
    # Analyze what content should generate choices
    expected_choices_content = [content for content in delta_content_parts if content != ""]  # Non-empty content only
    actual_choices_content = [obj.get("delta", {}).get("content", "") for obj in choices_objects]
    
    print(f"\n📊 EXPECTED vs ACTUAL CHOICES:")
    print(f"  Expected choices count: {len(expected_choices_content)}")
    print(f"  Actual choices count: {len(actual_choices_content)}")
    print(f"  Expected content: {expected_choices_content}")
    print(f"  Actual content: {actual_choices_content}")
    
    # Final verdict
    print(f"\n🏆 CHOICES STREAMING VERDICT:")
    
    criteria_results = {
        "Has choices objects": len(choices_objects) > 0,
        "Correct choices count": len(choices_objects) == len(expected_choices_content),
        "Proper ordering": ordering_correct,
        "Consistent metadata": consistent_ids if choices_objects else False,
        "Content consistency": expected_choices_content == actual_choices_content if choices_objects else False
    }
    
    passed_criteria = sum(criteria_results.values())
    total_criteria = len(criteria_results)
    
    print(f"  Criteria passed: {passed_criteria}/{total_criteria}")
    
    for criterion, passed in criteria_results.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {criterion}")
    
    if passed_criteria == total_criteria:
        print(f"\n  🎉 PERFECT CHOICES STREAMING IMPLEMENTATION!")
        print("     All criteria met for choices object streaming!")
    else:
        print(f"\n  ⚠️  CHOICES STREAMING HAS ISSUES:")
        print("     Review the failed criteria above")


if __name__ == "__main__":
    asyncio.run(analyze_choices_streaming())