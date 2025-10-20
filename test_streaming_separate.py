#!/usr/bin/env python3
"""
Test script to verify the streaming format modification works correctly with separate chunks.
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
    content_chunks = ["Hello", " there", "! How"]
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
    print("Testing modified streaming format (separate chunks)...")
    print("=" * 60)
    
    # Get the mock stream
    mock_gen = mock_stream()
    
    # Format as NDJSON
    formatted_gen = format_as_ndjson(mock_gen)
    
    # Collect all output
    output_lines = []
    delta_lines = []
    custom_format_lines = []
    
    async for line in formatted_gen:
        output_lines.append(line)
        line_json = json.loads(line)
        
        # Check if it's a delta line or custom format line
        if "delta" in line_json and line_json.get("object") != "chat.completion.chunk":
            delta_lines.append((len(output_lines), line_json))
            print(f"Line {len(output_lines)} (DELTA): {line.strip()}")
        elif line_json.get("object") == "chat.completion.chunk":
            custom_format_lines.append((len(output_lines), line_json))
            print(f"Line {len(output_lines)} (CUSTOM): {line.strip()}")
        else:
            print(f"Line {len(output_lines)} (OTHER): {line.strip()}")
    
    print("=" * 60)
    print(f"Total lines: {len(output_lines)}")
    print(f"Delta lines: {len(delta_lines)}")
    print(f"Custom format lines: {len(custom_format_lines)}")
    
    # Verify each delta chunk has a corresponding custom format
    delta_content_chunks = []
    custom_content_chunks = []
    
    for _, delta_line in delta_lines:
        if delta_line["delta"].get("content"):
            delta_content_chunks.append(delta_line["delta"]["content"])
    
    for _, custom_line in custom_format_lines:
        custom_content_chunks.append(custom_line["choices"][0]["messages"][0]["content"])
    
    print(f"\nDelta content chunks: {delta_content_chunks}")
    print(f"Custom content chunks: {custom_content_chunks}")
    
    if delta_content_chunks == custom_content_chunks:
        print("✅ Each delta chunk has a corresponding custom format chunk!")
    else:
        print("❌ Delta and custom chunks don't match")
    
    # Verify structure of custom format lines
    if custom_format_lines:
        sample_custom = custom_format_lines[0][1]
        required_fields = ["id", "model", "created", "object", "choices", "history_metadata", "apim-request-id", "delta"]
        missing_fields = [field for field in required_fields if field not in sample_custom]
        
        if missing_fields:
            print(f"❌ Missing required fields: {missing_fields}")
        else:
            print("✅ All required fields present in custom format!")


if __name__ == "__main__":
    asyncio.run(test_streaming_format())