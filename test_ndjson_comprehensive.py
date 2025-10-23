#!/usr/bin/env python3
"""
Comprehensive test to verify NDJSON format and streaming behavior
"""

import asyncio
import json
import time
import uuid
from typing import AsyncGenerator
import re


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
    """Mock stream that simulates real backend data"""
    
    # First event with context
    yield {
        "delta": {"role": "assistant"},
        "context": {
            "data_points": {"text": [], "images": [], "citations": []},
            "thoughts": [
                {
                    "title": "Prompt to generate search query",
                    "description": [
                        {"role": "system", "content": "Test system prompt"},
                        {"role": "user", "content": "Test user message"}
                    ],
                    "props": {"model": "gpt-4.1-mini", "deployment": "gpt-4.1-mini"}
                }
            ],
            "followup_questions": None
        },
        "session_state": None
    }
    
    # Delta events with content
    content_chunks = ["", "Hello", "!", " World", "?", None]
    for chunk in content_chunks:
        yield {
            "delta": {
                "content": chunk,
                "role": "assistant" if chunk and chunk != "" else None
            }
        }
    
    # Final event with context
    yield {
        "delta": {"role": "assistant"},
        "context": {
            "data_points": {"text": [], "images": [], "citations": []},
            "thoughts": [],
            "followup_questions": None
        },
        "session_state": None
    }


def validate_ndjson(text: str) -> dict:
    """Validate NDJSON format and return analysis"""
    result = {
        "is_valid_ndjson": True,
        "errors": [],
        "line_count": 0,
        "delta_objects": 0,
        "choices_objects": 0,
        "newline_issues": [],
        "json_parse_errors": []
    }
    
    # Check for basic newline structure
    if not text.endswith('\n'):
        result["errors"].append("Text doesn't end with newline")
    
    # Split by newlines and analyze each line
    lines = text.split('\n')
    result["line_count"] = len([line for line in lines if line.strip()])
    
    for i, line in enumerate(lines):
        if not line.strip():  # Skip empty lines
            continue
            
        # Check if line is valid JSON
        try:
            obj = json.loads(line)
            
            # Count object types
            if "delta" in obj and "choices" not in obj:
                result["delta_objects"] += 1
            elif "choices" in obj:
                result["choices_objects"] += 1
                
        except json.JSONDecodeError as e:
            result["is_valid_ndjson"] = False
            result["json_parse_errors"].append(f"Line {i+1}: {str(e)}")
    
    # Check for concatenation issues (}{ pattern)
    concatenation_pattern = r'}\s*{'
    matches = re.findall(concatenation_pattern, text)
    if matches:
        result["is_valid_ndjson"] = False
        result["errors"].append(f"Found {len(matches)} object concatenations (}}{{)")
        result["newline_issues"] = matches
    
    return result


async def test_ndjson_format():
    """Comprehensive test of NDJSON format"""
    print("🧪 COMPREHENSIVE NDJSON FORMAT TEST")
    print("=" * 60)
    
    # Generate the formatted output
    mock_gen = mock_stream()
    formatted_gen = format_as_ndjson(mock_gen)
    
    # Collect all chunks individually
    chunks = []
    async for chunk in formatted_gen:
        chunks.append(chunk)
    
    # Join all chunks to get the full output
    full_output = "".join(chunks)
    
    print("📊 CHUNK ANALYSIS:")
    print(f"  Total chunks generated: {len(chunks)}")
    print(f"  Total characters: {len(full_output)}")
    print(f"  Chunks ending with \\n: {sum(1 for chunk in chunks if chunk.endswith('\\n'))}")
    
    print("\n🔍 INDIVIDUAL CHUNKS:")
    for i, chunk in enumerate(chunks[:5]):  # Show first 5 chunks
        chunk_repr = repr(chunk)
        if len(chunk_repr) > 100:
            chunk_repr = chunk_repr[:97] + "..."
        print(f"  Chunk {i+1}: {chunk_repr}")
    if len(chunks) > 5:
        print(f"  ... and {len(chunks) - 5} more chunks")
    
    print(f"\n📝 FULL OUTPUT (first 500 chars):")
    print(repr(full_output[:500]))
    if len(full_output) > 500:
        print("...")
    
    print(f"\n✅ NDJSON VALIDATION:")
    validation = validate_ndjson(full_output)
    
    print(f"  Valid NDJSON: {validation['is_valid_ndjson']}")
    print(f"  Total lines: {validation['line_count']}")
    print(f"  Delta objects: {validation['delta_objects']}")
    print(f"  Choices objects: {validation['choices_objects']}")
    
    if validation["errors"]:
        print("  ❌ Errors found:")
        for error in validation["errors"]:
            print(f"    - {error}")
    
    if validation["json_parse_errors"]:
        print("  ❌ JSON Parse Errors:")
        for error in validation["json_parse_errors"]:
            print(f"    - {error}")
    
    if validation["newline_issues"]:
        print("  ❌ Concatenation Issues:")
        for issue in validation["newline_issues"][:3]:  # Show first 3
            print(f"    - Found: {repr(issue)}")
    
    print(f"\n🎯 EXPECTED vs ACTUAL:")
    expected_lines = validation['delta_objects'] + validation['choices_objects']
    print(f"  Expected total objects: {expected_lines}")
    print(f"  Actual lines with content: {validation['line_count']}")
    print(f"  Match: {expected_lines == validation['line_count']}")
    
    # Test if we can parse each line individually
    print(f"\n🔧 LINE-BY-LINE PARSING:")
    lines = [line for line in full_output.split('\n') if line.strip()]
    parse_success = 0
    for i, line in enumerate(lines):
        try:
            json.loads(line)
            parse_success += 1
        except:
            print(f"  ❌ Line {i+1} failed to parse")
            if i < 3:  # Show first 3 failures
                print(f"    Content: {repr(line[:100])}")
    
    print(f"  Successfully parsed: {parse_success}/{len(lines)} lines")
    
    # Final verdict
    print(f"\n🏆 FINAL VERDICT:")
    if validation['is_valid_ndjson'] and parse_success == len(lines):
        print("  ✅ PERFECT: Output is valid NDJSON format!")
    elif validation['is_valid_ndjson']:
        print("  ⚠️  MOSTLY GOOD: Valid structure but some parsing issues")
    else:
        print("  ❌ FAILED: Output is NOT valid NDJSON format")
        print("     The main issue appears to be object concatenation")
        print("     This suggests newlines are being lost somewhere in the pipeline")
    
    return validation


async def test_streaming_simulation():
    """Test what happens when we simulate actual streaming"""
    print("\n" + "=" * 60)
    print("🌊 STREAMING SIMULATION TEST")
    print("=" * 60)
    
    # Simulate streaming by processing chunks as they arrive
    mock_gen = mock_stream()
    formatted_gen = format_as_ndjson(mock_gen)
    
    received_data = ""
    chunk_count = 0
    
    print("📡 Simulating streaming reception:")
    async for chunk in formatted_gen:
        chunk_count += 1
        received_data += chunk
        print(f"  Received chunk {chunk_count}: {len(chunk)} chars, ends_with_newline: {chunk.endswith('\\n')}")
        
        # Try to parse complete objects from received data so far
        lines = received_data.split('\n')
        complete_lines = lines[:-1] if not received_data.endswith('\n') else lines
        
        parseable_objects = 0
        for line in complete_lines:
            if line.strip():
                try:
                    json.loads(line)
                    parseable_objects += 1
                except:
                    pass
        
        print(f"    Parseable objects so far: {parseable_objects}")
    
    print(f"\n📈 STREAMING SUMMARY:")
    print(f"  Total chunks received: {chunk_count}")
    print(f"  Final data length: {len(received_data)}")
    print(f"  Ends with newline: {received_data.endswith('\\n')}")


if __name__ == "__main__":
    async def main():
        await test_ndjson_format()
        await test_streaming_simulation()
    
    asyncio.run(main())