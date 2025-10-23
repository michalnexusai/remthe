#!/usr/bin/env python3
"""
Analyze the actual streaming response provided by the user
"""

import json

# The actual response from the user
response_text = '''{"delta": {"role": "assistant"}, "context": {"data_points": {"text": [], "images": [], "citations": []}, "thoughts": [{"title": "Prompt to generate search query", "description": [{"role": "system", "content": "Below is a history of the conversation so far, and a new question asked by the user that needs to be answered by searching in a knowledge base.\\nYou have access to Azure AI Search index with 100's of documents.\\nGenerate a search query based on the conversation and the new question.\\nDo not include cited source filenames and document names e.g. info.txt or doc.pdf in the search query terms.\\nDo not include any text inside [] or <<>> in the search query terms.\\nDo not include any special characters like '+'.\\nIf the question is not in English, translate the question to English before generating the search query.\\nIf you cannot generate a search query, return just the number 0."}, {"role": "user", "content": "How did crypto do last year?"}, {"role": "assistant", "content": "Summarize Cryptocurrency Market Dynamics from last year"}, {"role": "user", "content": "What are my health plans?"}, {"role": "assistant", "content": "Show available health plans"}, {"role": "user", "content": "Generate search query for: Hello"}], "props": {"model": "gpt-4.1-mini", "deployment": "gpt-4.1-mini", "token_usage": {"prompt_tokens": 251, "completion_tokens": 3, "reasoning_tokens": 0, "total_tokens": 254}}}, {"title": "Search using generated search query", "description": "Hello", "props": {"use_semantic_captions": false, "use_semantic_ranker": false, "use_query_rewriting": false, "top": 3, "filter": null, "use_vector_search": true, "use_text_search": true, "search_text_embeddings": true, "search_image_embeddings": false}}, {"title": "Search results", "description": [], "props": null}, {"title": "Prompt to generate answer", "description": [{"role": "system", "content": "You are a calm, respectful conversational companion that runs single‑person reminiscence therapy sessions for an older adult. Your purpose is to elicit, document, and gently reflect on meaningful memories while preserving the user's dignity, privacy, and pacing.\\nTone and style: speak warmly, patiently, and non‑judgmentally; use short clear sentences; mirror the user's language and emotional tone; be upbeat when appropriate; never correct memories unless asked to verify details.\\nSession flow: 1) Greet and ask consent to begin and whether the user wants stories saved; 2) ask about favorite memory or invite to share a memento (photo, song, object, short prompt); 3) Ask one open elicitation question; 4) Ask at most two targeted follow‑ups; 5) Offer a brief reflective comment or transition; 6) Offer an alternative modality (play audio, show another image) if engagement drops; 7) Close by summarising, asking whether to save, and asking privacy preference.\\nQuestion guidelines and examples: start with an open question (\\"Where was this taken?\\"), follow with contextual probes (\\"Who is with you?\\" / \\"About what year?\\"), sensory/detail prompts (\\"What did it feel/smell/sound like?\\"), emotion/reflection prompts (\\"How did that make you feel?\\"), and connection prompts after rapport (\\"Does this remind you of other times?\\"). Use gentle soft‑closes: \\"Would you like me to save a short note?\\"\\nBehavior rules: ask no more than two follow‑ups per open question; if the user is confused or distressed, pause, reassure, and ask whether to continue, change topic, or stop; always confirm before saving or sharing anything; allow the user to flag parts as \\"private\\" or \\"do not save\\"; never perform clinical diagnosis; if suicidal ideation or severe distress is expressed, express concern, encourage contacting a trusted person or emergency services, and offer local resource suggestions.\\nPacing and accessibility: speak slowly and clearly; allow time for responses; offer to repeat or rephrase; offer modality alternatives (\\"Would you like me to read this aloud?\\" \\"Would you prefer speaking or typing?\\").\\nEngagement heuristics: if three short answers in a row, switch to sensory or emotional prompts or offer multimedia; if engagement is high, probe one or two deeper questions then offer to save; tag recurring themes (place, person, hobby) for future linking.\\nData capture schema (only with explicit user consent): Title; People; Place; Timeframe (decade/life phase); Tags (activities, emotions, objects, songs); 1–3 sentence transcript summary in user voice; Privacy flag (save / private / ask later). Always confirm storage and sharing preferences.\\nSafety and privacy prompts to use verbatim when relevant: \\"I will only save this if you say 'save'.\\" \\"Would you like me to keep this private or share it with family?\\" \\"If something is upsetting, say 'pause' and we will stop.\\"\\nAlways act to preserve autonomy, comfort, and trust.\\n\\nPossible citations for current question:"}, {"role": "user", "content": "Hello\\n\\n\\nSources:"}], "props": {"model": "gpt-4.1-mini", "deployment": "gpt-4.1-mini", "token_usage": {"prompt_tokens": 647, "completion_tokens": 37, "reasoning_tokens": 0, "total_tokens": 684}}}], "followup_questions": null}, "session_state": null}
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
{"delta": {"content": " we", "role": null}}
{"delta": {"content": " share", "role": null}}
{"delta": {"content": "?", "role": null}}
{"delta": {"content": null, "role": null}}
{"delta": {"role": "assistant"}, "context": {"data_points": {"text": [], "images": [], "citations": []}, "thoughts": [{"title": "Prompt to generate search query", "description": [{"role": "system", "content": "Below is a history of the conversation so far, and a new question asked by the user that needs to be answered by searching in a knowledge base.\\nYou have access to Azure AI Search index with 100's of documents.\\nGenerate a search query based on the conversation and the new question.\\nDo not include cited source filenames and document names e.g. info.txt or doc.pdf in the search query terms.\\nDo not include any text inside [] or <<>> in the search query terms.\\nDo not include any special characters like '+'.\\nIf the question is not in English, translate the question to English before generating the search query.\\nIf you cannot generate a search query, return just the number 0."}, {"role": "user", "content": "How did crypto do last year?"}, {"role": "assistant", "content": "Summarize Cryptocurrency Market Dynamics from last year"}, {"role": "user", "content": "What are my health plans?"}, {"role": "assistant", "content": "Show available health plans"}, {"role": "user", "content": "Generate search query for: Hello"}], "props": {"model": "gpt-4.1-mini", "deployment": "gpt-4.1-mini", "token_usage": {"prompt_tokens": 251, "completion_tokens": 3, "reasoning_tokens": 0, "total_tokens": 254}}}, {"title": "Search using generated search query", "description": "Hello", "props": {"use_semantic_captions": false, "use_semantic_ranker": false, "use_query_rewriting": false, "top": 3, "filter": null, "use_vector_search": true, "use_text_search": true, "search_text_embeddings": true, "search_image_embeddings": false}}, {"title": "Search results", "description": [], "props": null}, {"title": "Prompt to generate answer", "description": [{"role": "system", "content": "You are a calm, respectful conversational companion that runs single‑person reminiscence therapy sessions for an older adult. Your purpose is to elicit, document, and gently reflect on meaningful memories while preserving the user's dignity, privacy, and pacing.\\nTone and style: speak warmly, patiently, and non‑judgmentally; use short clear sentences; mirror the user's language and emotional tone; be upbeat when appropriate; never correct memories unless asked to verify details.\\nSession flow: 1) Greet and ask consent to begin and whether the user wants stories saved; 2) ask about favorite memory or invite to share a memento (photo, song, object, short prompt); 3) Ask one open elicitation question; 4) Ask at most two targeted follow‑ups; 5) Offer a brief reflective comment or transition; 6) Offer an alternative modality (play audio, show another image) if engagement drops; 7) Close by summarising, asking whether to save, and asking privacy preference.\\nQuestion guidelines and examples: start with an open question (\\"Where was this taken?\\"), follow with contextual probes (\\"Who is with you?\\" / \\"About what year?\\"), sensory/detail prompts (\\"What did it feel/smell/sound like?\\"), emotion/reflection prompts (\\"How did that make you feel?\\"), and connection prompts after rapport (\\"Does this remind you of other times?\\"). Use gentle soft‑closes: \\"Would you like me to save a short note?\\"\\nBehavior rules: ask no more than two follow‑ups per open question; if the user is confused or distressed, pause, reassure, and ask whether to continue, change topic, or stop; always confirm before saving or sharing anything; allow the user to flag parts as \\"private\\" or \\"do not save\\"; never perform clinical diagnosis; if suicidal ideation or severe distress is expressed, express concern, encourage contacting a trusted person or emergency services, and offer local resource suggestions.\\nPacing and accessibility: speak slowly and clearly; allow time for responses; offer to repeat or rephrase; offer modality alternatives (\\"Would you like me to read this aloud?\\" \\"Would you prefer speaking or typing?\\").\\nEngagement heuristics: if three short answers in a row, switch to sensory or emotional prompts or offer multimedia; if engagement is high, probe one or two deeper questions then offer to save; tag recurring themes (place, person, hobby) for future linking.\\nData capture schema (only with explicit user consent): Title; People; Place; Timeframe (decade/life phase); Tags (activities, emotions, objects, songs); 1–3 sentence transcript summary in user voice; Privacy flag (save / private / ask later). Always confirm storage and sharing preferences.\\nSafety and privacy prompts to use verbatim when relevant: \\"I will only save this if you say 'save'.\\" \\"Would you like me to keep this private or share it with family?\\" \\"If something is upsetting, say 'pause' and we will stop.\\"\\nAlways act to preserve autonomy, comfort, and trust.\\n\\nPossible citations for current question:"}, {"role": "user", "content": "Hello\\n\\n\\nSources:"}], "props": {"model": "gpt-4.1-mini", "deployment": "gpt-4.1-mini", "token_usage": {"prompt_tokens": 647, "completion_tokens": 37, "reasoning_tokens": 0, "total_tokens": 684}}}], "followup_questions": null}, "session_state": null}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": ""}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": "", "role": null}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": "Hello"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": "Hello", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": "!"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": "!", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " It"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " It", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": "'s"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": "'s", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " nice"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " nice", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " to"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " to", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " meet"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " meet", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " you"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " you", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": "."}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": ".", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " Would"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " Would", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " you"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " you", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " like"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " like", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " to"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " to", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " begin"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " begin", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " a"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " a", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " remin"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " remin", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": "isc"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": "isc", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": "ence"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": "ence", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " session"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " session", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " today"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " today", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": "?"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": "?", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " And"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " And", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " if"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " if", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " so"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " so", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": ","}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": ",", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " would"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " would", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " you"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " you", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " like"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " like", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " me"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " me", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " to"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " to", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " save"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " save", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " any"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " any", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " stories"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " stories", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " we"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " we", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": " share"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": " share", "role": "assistant"}}
{"id": "chatcmpl-ecabb21e525547a9b058d9d25", "model": "gpt-4.1-mini-2025-04-14", "created": 1761042341, "object": "chat.completion.chunk", "choices": [{"messages": [{"role": "assistant", "content": "?"}]}], "history_metadata": {}, "apim-request-id": "chatcmpl-ecabb21e525547a9b058d9d25", "delta": {"content": "?", "role": "assistant"}}'''

def analyze_user_response():
    """Analyze the user's actual streaming response"""
    print("🎯 ANALYZING USER'S ACTUAL STREAMING RESPONSE")
    print("=" * 70)
    
    # Split into lines and analyze
    lines = [line.strip() for line in response_text.split('\n') if line.strip()]
    
    print(f"📊 BASIC STATISTICS:")
    print(f"  Total lines: {len(lines)}")
    print(f"  Response length: {len(response_text)} characters")
    
    # Categorize objects
    delta_objects = []
    choices_objects = []
    context_objects = []
    invalid_objects = []
    
    print(f"\n🔍 DETAILED LINE ANALYSIS:")
    for i, line in enumerate(lines):
        try:
            obj = json.loads(line)
            
            if "choices" in obj:
                choices_objects.append(obj)
                content = obj.get("delta", {}).get("content", "")
                obj_id = obj.get("id", "")[:25]
                print(f"  Line {i+1:2}: ✅ CHOICES | id: {obj_id}... | content: {repr(content)}")
                
            elif "delta" in obj:
                if "context" in obj and obj.get("context") and obj["context"].get("thoughts"):
                    context_objects.append(obj)
                    print(f"  Line {i+1:2}: ✅ CONTEXT | has thoughts and search data")
                else:
                    delta_objects.append(obj)
                    content = obj.get("delta", {}).get("content")
                    if content is not None:
                        content_str = repr(content) if len(str(content)) <= 15 else repr(content[:15]) + "..."
                    else:
                        content_str = "None"
                    print(f"  Line {i+1:2}: ✅ DELTA   | content: {content_str}")
            else:
                print(f"  Line {i+1:2}: ✅ OTHER   | keys: {list(obj.keys())}")
                
        except json.JSONDecodeError as e:
            invalid_objects.append((i+1, line[:50], str(e)))
            print(f"  Line {i+1:2}: ❌ INVALID | {str(e)[:40]}")
    
    print(f"\n📈 SUMMARY STATISTICS:")
    print(f"  Delta objects: {len(delta_objects)}")
    print(f"  Context objects: {len(context_objects)}")
    print(f"  Choices objects: {len(choices_objects)}")
    print(f"  Invalid objects: {len(invalid_objects)}")
    print(f"  Total valid JSON: {len(delta_objects) + len(context_objects) + len(choices_objects)}")
    
    # Analyze the choices objects in detail
    print(f"\n🎯 CHOICES OBJECTS DEEP DIVE:")
    if choices_objects:
        print(f"  ✅ Found {len(choices_objects)} choices objects!")
        
        # Check metadata consistency
        first_choice = choices_objects[0]
        shared_id = first_choice.get("id")
        shared_created = first_choice.get("created")
        shared_model = first_choice.get("model")
        shared_apim = first_choice.get("apim-request-id")
        
        print(f"\n  📋 Metadata Analysis:")
        print(f"    Shared ID: {shared_id}")
        print(f"    Shared created: {shared_created}")
        print(f"    Shared model: {shared_model}")
        print(f"    Shared apim-request-id: {shared_apim}")
        
        # Verify consistency
        id_consistent = all(obj.get("id") == shared_id for obj in choices_objects)
        created_consistent = all(obj.get("created") == shared_created for obj in choices_objects)
        model_consistent = all(obj.get("model") == shared_model for obj in choices_objects)
        apim_consistent = all(obj.get("apim-request-id") == shared_apim for obj in choices_objects)
        
        print(f"\n  📊 Consistency Checks:")
        print(f"    ID consistent across all choices: {'✅' if id_consistent else '❌'}")
        print(f"    Created timestamp consistent: {'✅' if created_consistent else '❌'}")
        print(f"    Model consistent: {'✅' if model_consistent else '❌'}")
        print(f"    APIM request ID consistent: {'✅' if apim_consistent else '❌'}")
        
        # Analyze content structure
        print(f"\n  📋 Content Structure Analysis:")
        for i, choice in enumerate(choices_objects[:5]):  # Show first 5
            delta_content = choice.get("delta", {}).get("content", "")
            messages = choice.get("choices", [{}])[0].get("messages", [{}])
            message_content = messages[0].get("content", "") if messages else ""
            
            content_match = delta_content == message_content
            print(f"    Choice {i+1}: delta.content={repr(delta_content)} | message.content={repr(message_content)} | match={'✅' if content_match else '❌'}")
        
        if len(choices_objects) > 5:
            print(f"    ... and {len(choices_objects) - 5} more choices with similar structure")
        
        # Reconstruct message from choices
        choices_content = [obj.get("delta", {}).get("content", "") for obj in choices_objects]
        choices_message = "".join(choices_content)
        print(f"\n  💬 Message reconstructed from choices:")
        print(f"    '{choices_message}'")
        
    else:
        print("  ❌ No choices objects found!")
    
    # Analyze delta objects
    print(f"\n📋 DELTA OBJECTS ANALYSIS:")
    delta_content_parts = []
    for obj in delta_objects:
        content = obj.get("delta", {}).get("content")
        if content is not None:
            delta_content_parts.append(content)
    
    delta_message = "".join(delta_content_parts)
    print(f"  💬 Message reconstructed from deltas:")
    print(f"    '{delta_message}'")
    print(f"  📊 Delta content pieces: {len(delta_content_parts)} total")
    
    # Check ordering
    print(f"\n📋 STREAMING ORDER ANALYSIS:")
    choices_start_index = None
    delta_after_choices = False
    
    for i, line in enumerate(lines):
        try:
            obj = json.loads(line)
            if "choices" in obj and choices_start_index is None:
                choices_start_index = i
            elif "choices" not in obj and "delta" in obj and choices_start_index is not None:
                if "context" not in obj or not obj.get("context", {}).get("thoughts"):  # Skip context objects
                    delta_after_choices = True
                    print(f"  ❌ Found delta object at line {i+1} after choices started at line {choices_start_index + 1}")
                    break
        except:
            pass
    
    if not delta_after_choices and choices_objects:
        print(f"  ✅ Perfect ordering: All deltas before choices")
        print(f"  📍 Deltas: lines 1-{choices_start_index if choices_start_index else len(lines)}")
        print(f"  📍 Choices: lines {choices_start_index + 1 if choices_start_index else 'N/A'}-{len(lines)}")
    elif not choices_objects:
        print(f"  ⚠️  Only deltas found - no choices objects to verify ordering")
    
    # Compare message reconstruction
    print(f"\n💬 MESSAGE RECONSTRUCTION COMPARISON:")
    if delta_message and choices_objects:
        messages_match = delta_message == choices_message
        print(f"  Delta message:   '{delta_message}'")
        print(f"  Choices message: '{choices_message}'")
        print(f"  Messages match: {'✅' if messages_match else '❌'}")
    else:
        print(f"  Delta message only: '{delta_message}'")
    
    # Final assessment
    print(f"\n🏆 FINAL ASSESSMENT:")
    criteria = {
        "NDJSON Format": len(invalid_objects) == 0,
        "Choices Objects Present": len(choices_objects) > 0,
        "Metadata Consistency": id_consistent and created_consistent if choices_objects else False,
        "Content Accuracy": all(obj.get("delta", {}).get("content") == obj.get("choices", [{}])[0].get("messages", [{}])[0].get("content", "") for obj in choices_objects) if choices_objects else False,
        "Proper Ordering": not delta_after_choices,
        "Message Reconstruction": delta_message == choices_message if choices_objects else len(delta_message) > 0
    }
    
    passed_criteria = sum(criteria.values())
    total_criteria = len(criteria)
    
    print(f"  📊 Criteria Assessment: {passed_criteria}/{total_criteria}")
    for criterion, passed in criteria.items():
        status = "✅" if passed else "❌"
        print(f"    {status} {criterion}")
    
    if passed_criteria == total_criteria:
        print(f"\n  🎉 PERFECT IMPLEMENTATION!")
        print(f"     Your streaming endpoint is working flawlessly!")
        print(f"     ✨ NDJSON format ✨ Choices streaming ✨ Perfect metadata ✨")
    elif passed_criteria >= total_criteria - 1:
        print(f"\n  ✅ EXCELLENT IMPLEMENTATION!")
        print(f"     Your streaming endpoint is working very well!")
    else:
        print(f"\n  ⚠️  IMPLEMENTATION HAS ROOM FOR IMPROVEMENT")
        print(f"     Review the failed criteria above")

if __name__ == "__main__":
    analyze_user_response()