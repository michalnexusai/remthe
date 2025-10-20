#!/usr/bin/env python3
"""
Test script to verify the streaming format modification works correctly with all chunks.
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
        collected_content = ""
        all_delta_chunks = []
        last_event = None
        
        async for event in r:
            yield json.dumps(event, ensure_ascii=False, cls=JSONEncoder) + "\n"
            
            # Track content for final response
            if "delta" in event and event["delta"].get("content"):
                delta_content = event["delta"]["content"]
                collected_content += delta_content
                all_delta_chunks.append(delta_content)  # Store all delta content chunks
            last_event = event
        
        # Add the additional JSON format at the end with all chunks
        if all_delta_chunks or last_event:
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
                                "content": collected_content or "Hello"
                            }
                        ]
                    }
                ],
                "history_metadata": {},
                "apim-request-id": f"chatcmpl-{uuid.uuid4().hex[:25]}",
                "delta": {
                    "content": collected_content or "Hello",
                    "role": None
                }
            }
            yield json.dumps(completion_chunk, ensure_ascii=False, cls=JSONEncoder) + "\n"
            
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
    content_chunks = ["Hello", " there", "! How", " can I", " help you", " today?"]
    for chunk in content_chunks:
        yield {
            "delta": {
                "content": chunk,
                "role": "assistant"
            }
        }
    
    # Final chunk (often empty)
    yield {
        "delta": {"role": "assistant"},
        "context": {"some": "final_context"}
    }


async def test_streaming_format():
    """Test the modified streaming format"""
    print("Testing modified streaming format (all chunks accumulated)...")
    print("=" * 60)
    
    # Get the mock stream
    mock_gen = mock_stream()
    
    # Format as NDJSON
    formatted_gen = format_as_ndjson(mock_gen)
    
    # Collect all output
    output_lines = []
    async for line in formatted_gen:
        output_lines.append(line)
        print(f"Line {len(output_lines)}: {line.strip()}")
    
    print("=" * 60)
    print(f"Total lines output: {len(output_lines)}")
    
    # Verify the last line is our custom format
    if output_lines:
        try:
            last_line_json = json.loads(output_lines[-1])
            print("\nLast line (custom format) parsed successfully:")
            print(json.dumps(last_line_json, indent=2))
            
            # Check that content contains all chunks
            content = last_line_json["choices"][0]["messages"][0]["content"]
            delta_content = last_line_json["delta"]["content"]
            
            print(f"\n📝 Content field: '{content}'")
            print(f"📝 Delta content field: '{delta_content}'")
            
            expected_full_content = "Hello there! How can I help you today?"
            
            if content == delta_content:
                print("✅ Content and delta content match!")
            else:
                print("❌ Content and delta content don't match")
                
            if content == expected_full_content:
                print("✅ Content correctly shows ALL accumulated chunks!")
            else:
                print(f"❌ Expected '{expected_full_content}' but got '{content}'")
                
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing last line as JSON: {e}")


if __name__ == "__main__":
    asyncio.run(test_streaming_format())