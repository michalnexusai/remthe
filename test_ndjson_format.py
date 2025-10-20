#!/usr/bin/env python3
"""
Test script to verify the NDJSON format is properly formatted.
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
    content_chunks = ["Hello", "!"]
    for chunk in content_chunks:
        yield {
            "delta": {
                "content": chunk,
                "role": "assistant"
            }
        }


async def test_ndjson_format():
    """Test the NDJSON formatting"""
    print("Testing NDJSON format correctness...")
    print("=" * 50)
    
    # Get the mock stream
    mock_gen = mock_stream()
    
    # Format as NDJSON
    formatted_gen = format_as_ndjson(mock_gen)
    
    # Collect all output as raw strings
    output_lines = []
    raw_output = ""
    async for line in formatted_gen:
        output_lines.append(line)
        raw_output += line
        print(f"Line {len(output_lines)}: {repr(line)}")  # repr shows \n explicitly
    
    print("=" * 50)
    print(f"Total lines: {len(output_lines)}")
    print("\nRaw concatenated output:")
    print(repr(raw_output))
    
    print("\nTesting each line can be parsed as JSON:")
    for i, line in enumerate(output_lines):
        line_content = line.rstrip('\n')  # Remove trailing newline for parsing
        try:
            parsed = json.loads(line_content)
            print(f"✅ Line {i+1}: Valid JSON")
        except json.JSONDecodeError as e:
            print(f"❌ Line {i+1}: Invalid JSON - {e}")
            print(f"   Content: {repr(line_content)}")
    
    # Check for proper NDJSON format (each line ends with \n)
    proper_format = all(line.endswith('\n') for line in output_lines)
    if proper_format:
        print("✅ All lines properly end with newline (proper NDJSON format)")
    else:
        print("❌ Some lines don't end with newline")


if __name__ == "__main__":
    asyncio.run(test_ndjson_format())