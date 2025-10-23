#!/usr/bin/env python3
"""
Debug test to check if our NDJSON is actually correct
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
    """Exact copy of the current implementation"""
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


async def mock_stream() -> AsyncGenerator[dict, None]:
    """Simple mock stream"""
    
    yield {"delta": {"content": "Hello", "role": "assistant"}}
    yield {"delta": {"content": " World", "role": "assistant"}}


async def test_actual_ndjson():
    """Test if we're generating valid NDJSON"""
    print("🔍 NDJSON REALITY CHECK")
    print("=" * 50)
    
    # Generate the output
    mock_gen = mock_stream()
    formatted_gen = format_as_ndjson(mock_gen)
    
    chunks = []
    async for chunk in formatted_gen:
        chunks.append(chunk)
    
    full_output = "".join(chunks)
    
    print("📋 RAW OUTPUT:")
    print(repr(full_output))
    print()
    
    print("📋 FORMATTED OUTPUT:")
    print(full_output)
    print()
    
    print("🔍 INDIVIDUAL CHUNKS:")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}: {repr(chunk)}")
    print()
    
    # Try to parse each line
    lines = full_output.strip().split('\n')
    print(f"📊 PARSING {len(lines)} LINES:")
    
    for i, line in enumerate(lines):
        try:
            obj = json.loads(line)
            if "choices" in obj:
                obj_type = "CHOICES"
            else:
                obj_type = "DELTA"
            print(f"  Line {i+1}: ✅ Valid JSON ({obj_type})")
        except json.JSONDecodeError as e:
            print(f"  Line {i+1}: ❌ Invalid JSON - {e}")
            print(f"    Content: {repr(line)}")
    
    # Test if it's valid NDJSON by the standard definition
    print("\n✅ NDJSON VALIDITY:")
    valid_ndjson = True
    
    if not full_output.endswith('\n'):
        print("  ❌ Doesn't end with newline")
        valid_ndjson = False
    
    if '\n\n' in full_output:
        print("  ❌ Contains double newlines")
        valid_ndjson = False
    
    try:
        # Each line should be valid JSON
        for line in lines:
            json.loads(line)
        print("  ✅ All lines are valid JSON")
    except:
        print("  ❌ Some lines are not valid JSON")
        valid_ndjson = False
    
    if valid_ndjson:
        print("  🎉 OUTPUT IS VALID NDJSON!")
    else:
        print("  💥 OUTPUT IS NOT VALID NDJSON")


if __name__ == "__main__":
    asyncio.run(test_actual_ndjson())