#!/usr/bin/env python3
"""
Test script to verify the new JSON array format.
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
    """Modified format_as_ndjson function to test"""
    try:
        all_events = []
        choices_objects = []
        
        # Collect all events first
        async for event in r:
            all_events.append(event)
            
            # If this event has delta content, create a choices object
            if "delta" in event and event["delta"].get("content"):
                delta_content = event["delta"]["content"]
                choices_objects.append(delta_content)
        
        # Start the JSON array
        yield "[\n"
        
        # First, yield all the original delta events
        for i, event in enumerate(all_events):
            if i > 0:
                yield ",\n"
            yield json.dumps(event, ensure_ascii=False, cls=JSONEncoder)
        
        # Generate shared values for all choices objects
        shared_id = f"chatcmpl-{uuid.uuid4().hex[:25]}"
        shared_created = int(time.time())
        shared_apim_request_id = f"chatcmpl-{uuid.uuid4().hex[:25]}"
        
        # Then yield all the choices objects
        for delta_content in choices_objects:
            yield ",\n"
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
                    "role": None
                }
            }
            yield json.dumps(completion_chunk, ensure_ascii=False, cls=JSONEncoder)
        
        # Close the JSON array
        yield "\n]"
            
    except Exception as error:
        print(f"Exception while generating response stream: {error}")
        yield json.dumps({"error": str(error)})


async def mock_stream() -> AsyncGenerator[dict, None]:
    """Mock streaming response from the chat approach"""
    
    # Initial response with context
    yield {
        "delta": {"role": "assistant"}, 
        "context": {"some": "context"}, 
        "session_state": "test_session"
    }
    
    # Stream content chunks
    content_chunks = ["Hello", "!", " World"]
    for chunk in content_chunks:
        yield {
            "delta": {
                "content": chunk,
                "role": "assistant"
            }
        }
    
    # Final event
    yield {
        "delta": {"role": "assistant"},
        "context": {"final": "context"}
    }


async def test_array_format():
    """Test the new JSON array format"""
    print("Testing JSON array format...")
    print("=" * 50)
    
    # Get the mock stream
    mock_gen = mock_stream()
    
    # Format as JSON array
    formatted_gen = format_as_ndjson(mock_gen)
    
    # Collect all output
    full_output = ""
    async for chunk in formatted_gen:
        full_output += chunk
    
    print("Raw output:")
    print(full_output)
    print("=" * 50)
    
    # Try to parse as JSON
    try:
        parsed_array = json.loads(full_output)
        print(f"✅ Successfully parsed as JSON array with {len(parsed_array)} items")
        
        # Analyze the structure
        delta_objects = []
        choices_objects = []
        
        for i, item in enumerate(parsed_array):
            if "choices" in item:
                choices_objects.append(i)
                print(f"Item {i}: CHOICES OBJECT (content: '{item['choices'][0]['messages'][0]['content']}')")
            elif "delta" in item:
                delta_objects.append(i)
                content = item["delta"].get("content", "")
                if content:
                    print(f"Item {i}: DELTA OBJECT (content: '{content}')")
                else:
                    print(f"Item {i}: DELTA OBJECT (no content)")
        
        print(f"\nDelta objects at positions: {delta_objects}")
        print(f"Choices objects at positions: {choices_objects}")
        
        # Check if delta objects come first
        if delta_objects and choices_objects:
            if max(delta_objects) < min(choices_objects):
                print("✅ All delta objects come before choices objects")
            else:
                print("❌ Delta and choices objects are mixed")
        
        # Check if all choices objects have same ID
        if len(choices_objects) > 1:
            ids = [parsed_array[i]["id"] for i in choices_objects]
            created_times = [parsed_array[i]["created"] for i in choices_objects]
            apim_ids = [parsed_array[i]["apim-request-id"] for i in choices_objects]
            
            if len(set(ids)) == 1:
                print("✅ All choices objects have the same ID")
            else:
                print("❌ Choices objects have different IDs")
                
            if len(set(created_times)) == 1:
                print("✅ All choices objects have the same created timestamp")
            else:
                print("❌ Choices objects have different created timestamps")
                
            if len(set(apim_ids)) == 1:
                print("✅ All choices objects have the same apim-request-id")
            else:
                print("❌ Choices objects have different apim-request-ids")
        
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse as JSON: {e}")


if __name__ == "__main__":
    asyncio.run(test_array_format())