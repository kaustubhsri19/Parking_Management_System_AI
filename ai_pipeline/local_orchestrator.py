"""
Local ML orchestrator using GPU-accelerated Whisper (STT) and a fine-tuned
DistilBERT classifier to map text to intents, then route to Supabase actions.
"""

import re
import time
from datetime import datetime
from typing import Dict, Any

import torch
from transformers import pipeline

# Ensure GPU usage when available
DEVICE_INDEX = 0 if torch.cuda.is_available() else -1

# Lazy-load pipelines (created on first use to reduce startup time)
_stt_pipe = None
_clf_pipe = None

# Label mapping (0..9)
LABEL_TO_INTENT = {
    0: {
        'key': 'get_available_slots',
        'description': 'Show all available parking slots',
        'sql': "SELECT * FROM parking_slots WHERE status='available'",
        'needs_slot_id': False,
    },
    1: {
        'key': 'get_filled_slots',
        'description': 'Show all booked (filled) parking slots',
        'sql': "SELECT * FROM parking_slots WHERE status='booked'",
        'needs_slot_id': False,
    },
    2: {
        'key': 'book_specific_slot',
        'description': 'Book a specific parking slot by its ID',
        'sql': "UPDATE parking_slots SET status='booked' WHERE slot_id={slot_id} AND status='available'",
        'needs_slot_id': True,
    },
    3: {
        'key': 'book_any_slot',
        'description': 'Book the next available parking slot',
        'sql': "UPDATE parking_slots SET status='booked' WHERE slot_id = (SELECT slot_id FROM parking_slots WHERE status='available' LIMIT 1)",
        'needs_slot_id': False,
    },
    4: {
        'key': 'release_specific_slot',
        'description': 'Release a specific parking slot by its ID',
        'sql': "UPDATE parking_slots SET status='available' WHERE slot_id={slot_id}",
        'needs_slot_id': True,
    },
    5: {
        'key': 'get_specific_slot_status',
        'description': 'Check status of a specific slot by its ID',
        'sql': "SELECT * FROM parking_slots WHERE slot_id={slot_id}",
        'needs_slot_id': True,
    },
    6: {
        'key': 'get_all_slots',
        'description': 'Show a list of all parking slots',
        'sql': "SELECT * FROM parking_slots",
        'needs_slot_id': False,
    },
    7: {
        'key': 'get_available_count',
        'description': 'Count the number of available slots',
        'sql': "SELECT COUNT(*) FROM parking_slots WHERE status='available'",
        'needs_slot_id': False,
    },
    8: {
        'key': 'get_filled_count',
        'description': 'Count the number of booked (filled) slots',
        'sql': "SELECT COUNT(*) FROM parking_slots WHERE status='booked'",
        'needs_slot_id': False,
    },
    9: {
        'key': 'release_all_slots',
        'description': 'Release all booked parking slots',
        'sql': "UPDATE parking_slots SET status='available' WHERE status='booked'",
        'needs_slot_id': False,
    },
    10: {
        'key': 'book_all_slots',
        'description': 'Book all available parking slots',
        'sql': "UPDATE parking_slots SET status='booked' WHERE status='available'",
        'needs_slot_id': False,
    },
    11: {
        'key': 'set_maintenance',
        'description': 'Set a specific slot to maintenance mode',
        'sql': "UPDATE parking_slots SET status='maintenance' WHERE slot_id={slot_id}",
        'needs_slot_id': True,
    },
    12: {
        'key': 'get_maintenance_slots',
        'description': 'Show all slots in maintenance mode',
        'sql': "SELECT * FROM parking_slots WHERE status='maintenance'",
        'needs_slot_id': False,
    },
    13: {
        'key': 'fallback',
        'description': 'Out-of-scope request, do nothing',
        'sql': None,
        'needs_slot_id': False,
    },
}

def _load_stt_pipeline():
    global _stt_pipe
    if _stt_pipe is None:
        _stt_pipe = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-base",
            device=DEVICE_INDEX,
        )
    return _stt_pipe


def _load_classifier_pipeline():
    global _clf_pipe
    if _clf_pipe is None:
        _clf_pipe = pipeline(
            "text-classification",
            model="ai_pipeline/models/parking_intent_model",
            device=DEVICE_INDEX,
        )
    return _clf_pipe


def transcribe_audio_file(audio_path: str) -> Dict[str, Any]:
    stt = _load_stt_pipeline()
    start = time.time()
    try:
        result = stt(audio_path)
        text = result.get('text', '').strip()
        return {
            'success': True,
            'text': text,
            'latency_ms': int((time.time() - start) * 1000),
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'STT failed: {str(e)}',
            'latency_ms': int((time.time() - start) * 1000),
        }


def _extract_slot_id(text: str) -> int:
    match = re.search(r"slot\s*(?:number\s*)?(\d+)", text)
    if match:
        return int(match.group(1))
    # fallback: any standalone number
    match = re.search(r"\b(\d+)\b", text)
    return int(match.group(1)) if match else -1


def classify_text(text: str) -> Dict[str, Any]:
    clf = _load_classifier_pipeline()
    result = clf(text)
    # Expecting like: [{'label': 'LABEL_3', 'score': 0.98}]
    label_str = result[0]['label']
    score = float(result[0]['score'])
    try:
        label_id = int(label_str.split('_')[-1])
    except Exception:
        label_id = 9  # fallback
    return {'label_id': label_id, 'score': score}


def _tts_text_for(intent_key: str, sql_result: Dict[str, Any], params: Dict[str, Any]) -> str:
    if not sql_result.get('success'):
        return f"Query failed: {sql_result.get('error', 'Unknown error')}"
    data = sql_result.get('data', []) if isinstance(sql_result, dict) else []
    count = len(data) if isinstance(data, list) else 0
    if intent_key == 'available_slots':
        return f"Found {count} available parking slots."
    if intent_key == 'booked_slots':
        return f"Found {count} booked parking slots."
    if intent_key == 'all_slots':
        return f"Retrieved {count} parking slots."
    if intent_key == 'book_slot':
        return f"Slot {params.get('slot_id', 'unknown')} has been booked successfully."
    if intent_key == 'release_slot':
        return f"Slot {params.get('slot_id', 'unknown')} has been released successfully."
    if intent_key in {'vehicles', 'users', 'parking_logs'}:
        entity = 'records'
        if intent_key == 'vehicles':
            entity = 'vehicles'
        elif intent_key == 'users':
            entity = 'users'
        elif intent_key == 'parking_logs':
            entity = 'parking logs'
        return f"Retrieved {count} {entity}."
    if intent_key == 'slot_status':
        return f"Returned status for slot {params.get('slot_id', 'unknown')}."
    return "Query executed successfully."


def process_text_query(text: str) -> Dict[str, Any]:
    """
    Full pipeline for text input: classify -> build SQL -> execute -> response.
    """
    from supabase_module import supabase_manager  # local import to avoid cycles

    classification = classify_text(text)
    label_id = classification['label_id']
    label_info = LABEL_TO_INTENT.get(label_id, LABEL_TO_INTENT[13])

    if label_info['key'] == 'fallback' or label_id == 13:
        return {
            'success': False,
            'error': 'Out-of-scope request. Supported queries: available slots, booked slots, all slots, book slot <n>, release slot <n>, vehicles, users, logs, slot status <n>.',
            'timestamp': datetime.now().isoformat(),
        }

    params: Dict[str, Any] = {}
    if label_info['needs_slot_id']:
        slot_id = _extract_slot_id(text)
        if slot_id <= 0:
            return {
                'success': False,
                'error': 'Missing or invalid slot number. Try like: "book slot 3".',
                'timestamp': datetime.now().isoformat(),
            }
        params['slot_id'] = slot_id

    sql_query = label_info['sql']
    if params:
        for k, v in params.items():
            sql_query = sql_query.replace(f"{{{k}}}", str(v))

    sql_result = supabase_manager.execute_query(sql_query)

    response: Dict[str, Any] = {
        'success': True if sql_result and sql_result.get('success') else False,
        'voice_text': text,
        'query_type': label_info['key'],
        'description': label_info['description'],
        'sql_query': sql_query,
        'database_result': sql_result,
        'timestamp': datetime.now().isoformat(),
    }

    response['tts_text'] = _tts_text_for(label_info['key'], sql_result, params)
    return response


