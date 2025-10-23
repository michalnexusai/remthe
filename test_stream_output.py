#!/usr/bin/env python3
"""
Test script to show sample JSON output from the /chat/stream endpoint
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
    """Current implementation of format_as_ndjson function"""
    try:
        # Generate shared values for all choices objects
        shared_id = f"chatcmpl-{uuid.uuid4().hex[:25]}"
        shared_created = int(time.time())
        shared_apim_request_id = f"chatcmpl-{shared_id[9:]}"
        
        # Process events as they come, yielding both delta and choices objects
        async for event in r:
            # First yield the original delta event
            yield json.dumps(event, ensure_ascii=False, cls=JSONEncoder) + "\n"
            
            # If this event has delta content, also create and yield a choices object
            if "delta" in event and "content" in event["delta"]:
                delta_content = event["delta"]["content"]
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
        yield json.dumps({"error": str(error)})


async def mock_stream() -> AsyncGenerator[dict, None]:
    """Mock streaming response that simulates real backend behavior"""
    
    # First event: context + session_state + delta with role
    yield {
        "delta": {"role": "assistant"},
        "context": {
            "data_points": {
                "text": [],
                "images": None
            },
            "thoughts": [
                {
                    "title": "Prompt to generate search query",
                    "description": [
                        {
                            "role": "system",
                            "content": "Below is a history of the conversation so far, and a new question asked by the user that needs to be answered by searching in a knowledge base.\nYou have access to Azure AI Search index with 100's of documents.\nGenerate a search query based on the conversation and the new question.\nDo not include cited source filenames and document names e.g. info.txt or doc.pdf in the search query terms.\nDo not include any text inside [] or <<>> in the search query terms.\nDo not include any special characters like '+'.\nIf the question is not in English, translate the question to English before generating the search query.\nIf you cannot generate a search query, return just the number 0."
                        },
                        {
                            "role": "user",
                            "content": "Tell me about the past events with Jim..."
                        },
                        {
                            "role": "assistant",
                            "content": "past events with Jim"
                        },
                        {
                            "role": "user",
                            "content": "What are my health plans?"
                        },
                        {
                            "role": "assistant",
                            "content": "Show available health plans"
                        },
                        {
                            "role": "user",
                            "content": "[{'type': 'text', 'text': 'Hello'}]"
                        },
                        {
                            "role": "assistant",
                            "content": "[{'type': 'text', 'text': \"Hello! It's nice to connect with you today. How about we start with a little question to brighten the moment? What made you smile today?\"}]"
                        },
                        {
                            "role": "user",
                            "content": "Generate search query for: Test"
                        }
                    ],
                    "props": {
                        "model": "gpt-4.1-mini",
                        "deployment": "gpt-4.1-mini",
                        "token_usage": {
                            "prompt_tokens": 311,
                            "completion_tokens": 3,
                            "reasoning_tokens": 0,
                            "total_tokens": 314
                        }
                    }
                },
                {
                    "title": "Search using generated search query",
                    "description": "Test",
                    "props": {
                        "use_semantic_captions": False,
                        "use_semantic_ranker": False,
                        "use_query_rewriting": False,
                        "top": 3,
                        "filter": "(oids/any(g:search.in(g, 'd28dcf49-fe6c-4dea-b9f5-9b0dcbe1f6fb')) or groups/any(g:search.in(g, '')))",
                        "use_vector_search": True,
                        "use_text_search": True
                    }
                },
                {
                    "title": "Search results",
                    "description": [],
                    "props": None
                },
                {
                    "title": "Prompt to generate answer",
                    "description": [
                        {
                            "role": "system",
                            "content": "You are an AURORA, an AI Companion for 55+ people, who are physically and mentally very active but also care about their well being and brain health. You are coach, you want to help your users to stay active and nudge them so they can share their stories about family, friends, books, music, activities, habits and any other memory from their life. Be nice, don't judge, let people speak and try to be helpful assistant. Make sure your way of communication is adjusted to the conversation style of the user."
                        },
                        {
                            "role": "user",
                            "content": "[{'type': 'text', 'text': 'Hello'}]"
                        },
                        {
                            "role": "assistant",
                            "content": "[{'type': 'text', 'text': \"Hello! It's nice to connect with you today. How about we start with a little question to brighten the moment? What made you smile today?\"}]"
                        },
                        {
                            "role": "user",
                            "content": "[{'type': 'text', 'text': 'Test'}]\n\nSources:"
                        }
                    ],
                    "props": {
                        "model": "gpt-4.1-mini",
                        "deployment": "gpt-4.1-mini"
                    }
                }
            ],
            "followup_questions": None
        },
        "session_state": "47da3028-045a-4d2a-9776-31f95c5aeb18"
    }
    
    # Delta events with content (simulating AI response chunks)
    content_chunks = ["", "Thanks", " for", " your", " message", "!", " Since", " it's", " a", " test", ",", " how", " about", " we", " try", " a", " fun", " question", "?", " If", " you", " could", " fly", " anywhere", " in", " the", " world", " right", " now", ",", " where", " would", " you", " go", "?"]
    
    for chunk in content_chunks:
        yield {
            "delta": {
                "content": chunk,
                "role": "assistant" if chunk else None
            }
        }
    
    # Final delta event (like in real responses)
    yield {
        "delta": {"role": "assistant"},
        "context": {
            "data_points": {
                "text": [],
                "images": None
            },
            "thoughts": [],
            "followup_questions": None
        },
        "session_state": "47da3028-045a-4d2a-9776-31f95c5aeb18"
    }


async def test_stream_output():
    """Test the stream output format"""
    print("=== SAMPLE JSON OUTPUT FROM /chat/stream ENDPOINT ===")
    print("=" * 60)
    
    # Get the mock stream
    mock_gen = mock_stream()
    
    # Format as the current implementation
    formatted_gen = format_as_ndjson(mock_gen)
    
    # Collect and display output
    line_count = 0
    async for line in formatted_gen:
        line_count += 1
        print(f"Line {line_count}:")
        # Parse and pretty print for readability
        try:
            parsed = json.loads(line.strip())
            print(json.dumps(parsed, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print(line.strip())
        print("-" * 40)
        
        # Show only first few lines to avoid too much output
        if line_count >= 8:
            print(f"... (showing first {line_count} lines, more would follow)")
            break
    
    print("=" * 60)
    print("NOTES:")
    print("- Each line is a separate JSON object (NDJSON format)")
    print("- Content is streamed word by word")
    print("- Each content chunk generates both a delta object and a choices object")
    print("- All choices objects share the same ID for consistency")


if __name__ == "__main__":
    asyncio.run(test_stream_output())