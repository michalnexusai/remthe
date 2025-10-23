#!/usr/bin/env python3
"""
Test script to verify commas are added between choices objects.
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
        first_choices_object = True
        
        async for event in r:
            yield json.dumps(event, ensure_ascii=False, cls=JSONEncoder) + "\n"
            
            # If this event has delta content, also yield the additional format
            if "delta" in event and event["delta"].get("content"):
                delta_content = event["delta"]["content"]
                completion_chunk = {
                    "id": f"chatcmpl-{uuid.uuid4().hex[:25]}",
                    "model": "gpt-4.1-mini-2025-04-14",
                    "created": int(time.time()),
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
                    "apim-request-id": f"chatcmpl-{uuid.uuid4().hex[:25]}",
                    "delta": {
                        "content": delta_content,
                        "role": None
                    }
                }
                
                # Add comma before choices objects (except the first one)
                if not first_choices_object:
                    yield ",\n"
                else:
                    first_choices_object = False
                    
                yield json.dumps(completion_chunk, ensure_ascii=False, cls=JSONEncoder) + "\n"
            
    except Exception as error:
        print(f"Exception while generating response stream: {error}")
        yield json.dumps({"error": str(error)}) + "\n"


async def mock_stream() -> AsyncGenerator[dict, None]:
    """Mock streaming response from the chat approach"""
    
    # Initial response with context (no content)
    yield {
        "delta": {"role": "assistant"}, 
        "context": {"some": "context"}, 
        "session_state": "test_session"
    }
    
    # Stream content chunks
    content_chunks = ["Hello", " there", "!"]
    for chunk in content_chunks:
        yield {
            "delta": {
                "content": chunk,
                "role": "assistant"
            }
        }


async def test_comma_format():
    """Test the comma formatting between choices objects"""
    print("Testing comma formatting between choices objects...")
    print("=" * 60)
    
    # Get the mock stream
    mock_gen = mock_stream()
    
    # Format as NDJSON
    formatted_gen = format_as_ndjson(mock_gen)
    
    # Collect all output
    output_lines = []
    async for line in formatted_gen:
        output_lines.append(line)
        print(f"Output: {repr(line)}")
    
    print("=" * 60)
    print(f"Total output segments: {len(output_lines)}")
    
    # Check for commas between choices objects
    comma_count = sum(1 for line in output_lines if line.strip() == ",")
    choices_count = 0
    
    for line in output_lines:
        line_content = line.rstrip('\n,')
        if line_content and not line_content == ",":
            try:
                parsed = json.loads(line_content)
                if "choices" in parsed:
                    choices_count += 1
            except json.JSONDecodeError:
                pass
    
    print(f"\nChoices objects found: {choices_count}")
    print(f"Commas found: {comma_count}")
    
    expected_commas = max(0, choices_count - 1)  # n-1 commas for n objects
    
    if comma_count == expected_commas:
        print(f"✅ Correct number of commas ({comma_count}) between {choices_count} choices objects")
    else:
        print(f"❌ Expected {expected_commas} commas but found {comma_count}")
    
    # Show the pattern
    print("\nPattern analysis:")
    for i, line in enumerate(output_lines):
        line_stripped = line.rstrip('\n')
        if line_stripped == ",":
            print(f"Line {i+1}: COMMA")
        elif "choices" in line_stripped:
            print(f"Line {i+1}: CHOICES OBJECT")
        elif "delta" in line_stripped:
            print(f"Line {i+1}: DELTA OBJECT")
        else:
            print(f"Line {i+1}: OTHER")


if __name__ == "__main__":
    asyncio.run(test_comma_format())