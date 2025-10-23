#!/usr/bin/env python3
"""
Analyze the working cloud response to verify NDJSON format
"""

import json

# The actual response from the cloud endpoint
response_text = '''{"delta": {"role": "assistant"}, "context": {"data_points": {"text": [], "images": [], "citations": []}, "thoughts": [{"title": "Prompt to generate search query", "description": [{"role": "system", "content": "Below is a history of the conversation so far, and a new question asked by the user that needs to be answered by searching in a knowledge base.\\nYou have access to Azure AI Search index with 100's of documents.\\nGenerate a search query based on the conversation and the new question.\\nDo not include cited source filenames and document names e.g. info.txt or doc.pdf in the search query terms.\\nDo not include any text inside [] or <<>> in the search query terms.\\nDo not include any special characters like '+'.\\nIf the question is not in English, translate the question to English before generating the search query.\\nIf you cannot generate a search query, return just the number 0."}, {"role": "user", "content": "How did crypto do last year?"}, {"role": "assistant", "content": "Summarize Cryptocurrency Market Dynamics from last year"}, {"role": "user", "content": "What are my health plans?"}, {"role": "assistant", "content": "Show available health plans"}, {"role": "user", "content": "Generate search query for: Hello"}], "props": {"model": "gpt-4.1-mini", "deployment": "gpt-4.1-mini", "token_usage": {"prompt_tokens": 251, "completion_tokens": 19, "reasoning_tokens": 0, "total_tokens": 270}}}, {"title": "Search using generated search query", "description": "Hello", "props": {"use_semantic_captions": false, "use_semantic_ranker": false, "use_query_rewriting": false, "top": 3, "filter": null, "use_vector_search": true, "use_text_search": true, "search_text_embeddings": true, "search_image_embeddings": false}}, {"title": "Search results", "description": [], "props": null}, {"title": "Prompt to generate answer", "description": [{"role": "system", "content": "You are a calm, respectful conversational companion that runs single‑person reminiscence therapy sessions for an older adult. Your purpose is to elicit, document, and gently reflect on meaningful memories while preserving the user's dignity, privacy, and pacing.\\nTone and style: speak warmly, patiently, and non‑judgmentally; use short clear sentences; mirror the user's language and emotional tone; be upbeat when appropriate; never correct memories unless asked to verify details.\\nSession flow: 1) Greet and ask consent to begin and whether the user wants stories saved; 2) ask about favorite memory or invite to share a memento (photo, song, object, short prompt); 3) Ask one open elicitation question; 4) Ask at most two targeted follow‑ups; 5) Offer a brief reflective comment or transition; 6) Offer an alternative modality (play audio, show another image) if engagement drops; 7) Close by summarising, asking whether to save, and asking privacy preference.\\nQuestion guidelines and examples: start with an open question (\\"Where was this taken?\\"), follow with contextual probes (\\"Who is with you?\\" / \\"About what year?\\"), sensory/detail prompts (\\"What did it feel/smell/sound like?\\"), emotion/reflection prompts (\\"How did that make you feel?\\"), and connection prompts after rapport (\\"Does this remind you of other times?\\"). Use gentle soft‑closes: \\"Would you like me to save a short note?\\"\\nBehavior rules: ask no more than two follow‑ups per open question; if the user is confused or distressed, pause, reassure, and ask whether to continue, change topic, or stop; always confirm before saving or sharing anything; allow the user to flag parts as \\"private\\" or \\"do not save\\"; never perform clinical diagnosis; if suicidal ideation or severe distress is expressed, express concern, encourage contacting a trusted person or emergency services, and offer local resource suggestions.\\nPacing and accessibility: speak slowly and clearly; allow time for responses; offer to repeat or rephrase; offer modality alternatives (\\"Would you like me to read this aloud?\\" \\"Would you prefer speaking or typing?\\").\\nEngagement heuristics: if three short answers in a row, switch to sensory or emotional prompts or offer multimedia; if engagement is high, probe one or two deeper questions then offer to save; tag recurring themes (place, person, hobby) for future linking.\\nData capture schema (only with explicit user consent): Title; People; Place; Timeframe (decade/life phase); Tags (activities, emotions, objects, songs); 1–3 sentence transcript summary in user voice; Privacy flag (save / private / ask later). Always confirm storage and sharing preferences.\\nSafety and privacy prompts to use verbatim when relevant: \\"I will only save this if you say 'save'.\\" \\"Would you like me to keep this private or share it with family?\\" \\"If something is upsetting, say 'pause' and we will stop.\\"\\nAlways act to preserve autonomy, comfort, and trust.\\n\\nPossible citations for current question:"}, {"role": "user", "content": "Hello\\n\\n\\nSources:"}], "props": {"model": "gpt-4.1-mini", "deployment": "gpt-4.1-mini"}}], "followup_questions": null}, "session_state": null}
{"delta": {"content": "", "role": "assistant"}}
{"delta": {"content": "Hello", "role": null}}
{"delta": {"content": "!", "role": null}}
{"delta": {"content": " It", "role": null}}
{"delta": {"content": "'s", "role": null}}
{"delta": {"content": " nice", "role": null}}
{"delta": {"content": " to", "role": null}}
{"delta": {"content": " meet", "role": null}}
{"delta": {"content": " you", "role": null}}
{"delta": {"content": ".", "role": null}}
{"delta": {"content": " Would", "role": null}}
{"delta": {"content": " you", "role": null}}
{"delta": {"content": " like", "role": null}}
{"delta": {"content": " to", "role": null}}
{"delta": {"content": " begin", "role": null}}
{"delta": {"content": " a", "role": null}}
{"delta": {"content": " little", "role": null}}
{"delta": {"content": " remin", "role": null}}
{"delta": {"content": "isc", "role": null}}
{"delta": {"content": "ence", "role": null}}
{"delta": {"content": " session", "role": null}}
{"delta": {"content": " today", "role": null}}
{"delta": {"content": "?", "role": null}}
{"delta": {"content": " And", "role": null}}
{"delta": {"content": " if", "role": null}}
{"delta": {"content": " so", "role": null}}
{"delta": {"content": ",", "role": null}}
{"delta": {"content": " would", "role": null}}
{"delta": {"content": " you", "role": null}}
{"delta": {"content": " like", "role": null}}
{"delta": {"content": " me", "role": null}}
{"delta": {"content": " to", "role": null}}
{"delta": {"content": " save", "role": null}}
{"delta": {"content": " any", "role": null}}
{"delta": {"content": " stories", "role": null}}
{"delta": {"content": " you", "role": null}}
{"delta": {"content": " share", "role": null}}
{"delta": {"content": "?", "role": null}}
{"delta": {"content": null, "role": null}}
{"delta": {"role": "assistant"}, "context": {"data_points": {"text": [], "images": [], "citations": []}, "thoughts": [{"title": "Prompt to generate search query", "description": [{"role": "system", "content": "Below is a history of the conversation so far, and a new question asked by the user that needs to be answered by searching in a knowledge base.\\nYou have access to Azure AI Search index with 100's of documents.\\nGenerate a search query based on the conversation and the new question.\\nDo not include cited source filenames and document names e.g. info.txt or doc.pdf in the search query terms.\\nDo not include any text inside [] or <<>> in the search query terms.\\nDo not include any special characters like '+'.\\nIf the question is not in English, translate the question to English before generating the search query.\\nIf you cannot generate a search query, return just the number 0."}, {"role": "user", "content": "How did crypto do last year?"}, {"role": "assistant", "content": "Summarize Cryptocurrency Market Dynamics from last year"}, {"role": "user", "content": "What are my health plans?"}, {"role": "assistant", "content": "Show available health plans"}, {"role": "user", "content": "Generate search query for: Hello"}], "props": {"model": "gpt-4.1-mini", "deployment": "gpt-4.1-mini", "token_usage": {"prompt_tokens": 251, "completion_tokens": 19, "reasoning_tokens": 0, "total_tokens": 270}}}, {"title": "Search using generated search query", "description": "Hello", "props": {"use_semantic_captions": false, "use_semantic_ranker": false, "use_query_rewriting": false, "top": 3, "filter": null, "use_vector_search": true, "use_text_search": true, "search_text_embeddings": true, "search_image_embeddings": false}}, {"title": "Search results", "description": [], "props": null}, {"title": "Prompt to generate answer", "description": [{"role": "system", "content": "You are a calm, respectful conversational companion that runs single‑person reminiscence therapy sessions for an older adult. Your purpose is to elicit, document, and gently reflect on meaningful memories while preserving the user's dignity, privacy, and pacing.\\nTone and style: speak warmly, patiently, and non‑judgmentally; use short clear sentences; mirror the user's language and emotional tone; be upbeat when appropriate; never correct memories unless asked to verify details.\\nSession flow: 1) Greet and ask consent to begin and whether the user wants stories saved; 2) ask about favorite memory or invite to share a memento (photo, song, object, short prompt); 3) Ask one open elicitation question; 4) Ask at most two targeted follow‑ups; 5) Offer a brief reflective comment or transition; 6) Offer an alternative modality (play audio, show another image) if engagement drops; 7) Close by summarising, asking whether to save, and asking privacy preference.\\nQuestion guidelines and examples: start with an open question (\\"Where was this taken?\\"), follow with contextual probes (\\"Who is with you?\\" / \\"About what year?\\"), sensory/detail prompts (\\"What did it feel/smell/sound like?\\"), emotion/reflection prompts (\\"How did that make you feel?\\"), and connection prompts after rapport (\\"Does this remind you of other times?\\"). Use gentle soft‑closes: \\"Would you like me to save a short note?\\"\\nBehavior rules: ask no more than two follow‑ups per open question; if the user is confused or distressed, pause, reassure, and ask whether to continue, change topic, or stop; always confirm before saving or sharing anything; allow the user to flag parts as \\"private\\" or \\"do not save\\"; never perform clinical diagnosis; if suicidal ideation or severe distress is expressed, express concern, encourage contacting a trusted person or emergency services, and offer local resource suggestions.\\nPacing and accessibility: speak slowly and clearly; allow time for responses; offer to repeat or rephrase; offer modality alternatives (\\"Would you like me to read this aloud?\\" \\"Would you prefer speaking or typing?\\").\\nEngagement heuristics: if three short answers in a row, switch to sensory or emotional prompts or offer multimedia; if engagement is high, probe one or two deeper questions then offer to save; tag recurring themes (place, person, hobby) for future linking.\\nData capture schema (only with explicit user consent): Title; People; Place; Timeframe (decade/life phase); Tags (activities, emotions, objects, songs); 1–3 sentence transcript summary in user voice; Privacy flag (save / private / ask later). Always confirm storage and sharing preferences.\\nSafety and privacy prompts to use verbatim when relevant: \\"I will only save this if you say 'save'.\\" \\"Would you like me to keep this private or share it with family?\\" \\"If something is upsetting, say 'pause' and we will stop.\\"\\nAlways act to preserve autonomy, comfort, and trust.\\n\\nPossible citations for current question:"}, {"role": "user", "content": "Hello\\n\\n\\nSources:"}], "props": {"model": "gpt-4.1-mini", "deployment": "gpt-4.1-mini", "token_usage": {"prompt_tokens": 647, "completion_tokens": 38, "reasoning_tokens": 0, "total_tokens": 685}}}], "followup_questions": null}, "session_state": null}'''

def analyze_cloud_response():
    print("🔍 ANALYZING CLOUD RESPONSE NDJSON FORMAT")
    print("=" * 60)
    
    # Split by newlines
    lines = response_text.strip().split('\n')
    print(f"📊 BASIC STATS:")
    print(f"  Total lines: {len(lines)}")
    print(f"  Total characters: {len(response_text)}")
    print(f"  Ends with newline: {response_text.endswith(chr(10))}")
    
    print(f"\n🔍 LINE ANALYSIS:")
    delta_objects = 0
    context_objects = 0
    valid_json_lines = 0
    
    for i, line in enumerate(lines):
        try:
            obj = json.loads(line)
            valid_json_lines += 1
            
            # Classify the object
            if "context" in obj and obj["context"]:
                context_objects += 1
                obj_type = "CONTEXT"
            elif "delta" in obj:
                delta_objects += 1 
                obj_type = "DELTA"
            else:
                obj_type = "OTHER"
            
            content = obj.get("delta", {}).get("content")
            if content is not None:
                content_preview = repr(content[:20]) if len(str(content)) > 20 else repr(content)
            else:
                content_preview = "None"
            
            print(f"  Line {i+1:2}: ✅ {obj_type:7} | content: {content_preview}")
            
        except json.JSONDecodeError as e:
            print(f"  Line {i+1:2}: ❌ INVALID | {str(e)[:50]}")
    
    print(f"\n📈 SUMMARY:")
    print(f"  Valid JSON lines: {valid_json_lines}/{len(lines)}")
    print(f"  Delta objects: {delta_objects}")
    print(f"  Context objects: {context_objects}")
    print(f"  NDJSON validity: {'✅ VALID' if valid_json_lines == len(lines) else '❌ INVALID'}")
    
    # Check for proper NDJSON format
    print(f"\n🎯 NDJSON FORMAT CHECK:")
    
    # Each line should be valid JSON
    if valid_json_lines == len(lines):
        print("  ✅ All lines are valid JSON")
    else:
        print("  ❌ Some lines are invalid JSON")
    
    # Should end with newline (though this might not be preserved in HTTP)
    if response_text.endswith('\n'):
        print("  ✅ Ends with newline")
    else:
        print("  ⚠️  Doesn't end with newline (might be HTTP transfer issue)")
    
    # No empty lines should exist
    empty_lines = sum(1 for line in lines if not line.strip())
    if empty_lines == 0:
        print("  ✅ No empty lines")
    else:
        print(f"  ❌ Found {empty_lines} empty lines")
    
    # Extract the actual streamed message
    print(f"\n💬 RECONSTRUCTED MESSAGE:")
    message_parts = []
    for line in lines:
        try:
            obj = json.loads(line)
            content = obj.get("delta", {}).get("content")
            if content is not None and content != "":
                message_parts.append(content)
        except:
            pass
    
    full_message = "".join(message_parts)
    print(f"  '{full_message}'")
    
    print(f"\n🏆 FINAL VERDICT:")
    if valid_json_lines == len(lines):
        print("  🎉 CLOUD ENDPOINT PRODUCES PERFECT NDJSON!")
        print("     Each JSON object is on its own line")
        print("     All lines are valid JSON")
        print("     Format matches NDJSON specification")
        print("     The format is working as intended!")
    else:
        print("  ❌ NDJSON format has issues")

if __name__ == "__main__":
    analyze_cloud_response()