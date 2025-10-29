"""
Flask application for AI Powered Voice-to-Query Parking Management System
Main application file with routes and voice processing
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import logging
from datetime import datetime
import json

# Import custom modules
# Remove rule-based voice module usage; frontend handles browser STT
from supabase_module import supabase_manager
from ai_pipeline.local_orchestrator import process_text_query, transcribe_audio_file, LABEL_TO_INTENT
from config import get_config

# Get configuration
config = get_config()

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def index():
    """Home page with voice recognition interface"""
    return render_template('index.html')

@app.route('/voice_input', methods=['POST'])
def voice_input():
    """Handle voice input from frontend (kept for compatibility)"""
    try:
        return jsonify({
            'success': False,
            'error': 'Browser speech recognition is recommended. For server-side STT, add /stt_query with audio upload.',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in voice input: {e}")
        return jsonify({
            'success': False,
            'error': f'Voice input error: {str(e)}',
            'timestamp': datetime.now().isoformat()
        })

@app.route('/query', methods=['POST'])
@app.route('/text_query', methods=['POST'])  # Alias for text-based queries
def process_query():
    """Process voice command and execute database query"""
    try:
        data = request.get_json()
        voice_text = data.get('text', '').strip()
        
        if not voice_text:
            return jsonify({
                'success': False,
                'error': 'No voice text provided',
                'timestamp': datetime.now().isoformat()
            })
        
        logger.info(f"Processing query for text: '{voice_text}'")
        
        # Route via ML orchestrator (classifier on GPU)
        response = process_text_query(voice_text)
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return jsonify({
            'success': False,
            'error': f'Query processing error: {str(e)}',
            'timestamp': datetime.now().isoformat()
        })

@app.route('/test_microphone', methods=['POST'])
def test_microphone():
    """Test microphone functionality (handled in browser)."""
    try:
        return jsonify({
            'success': True,
            'microphone_working': True,
            'available_microphones': ['Browser Microphone'],
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error testing microphone: {e}")
        return jsonify({
            'success': False,
            'error': f'Microphone test error: {str(e)}',
            'timestamp': datetime.now().isoformat()
        })

@app.route('/supported_commands', methods=['GET'])
def supported_commands():
    """Get list of supported intents from ML router"""
    try:
        commands = {}
        for _, meta in LABEL_TO_INTENT.items():
            if meta['key'] == 'fallback':
                continue
            commands[meta['key']] = {
                'description': meta['description'],
                'patterns': []
            }
        return jsonify({
            'success': True,
            'commands': commands,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting supported commands: {e}")
        return jsonify({
            'success': False,
            'error': f'Error getting commands: {str(e)}',
            'timestamp': datetime.now().isoformat()
        })

@app.route('/stt_query', methods=['POST'])
def stt_query():
    """Optional server-side STT + classify + route. Accepts multipart 'audio' or 'file'."""
    try:
        if 'audio' in request.files:
            f = request.files['audio']
        elif 'file' in request.files:
            f = request.files['file']
        else:
            return jsonify({'success': False, 'error': 'No audio file provided', 'timestamp': datetime.now().isoformat()})

        tmp_path = os.path.join('logs', f'upload_{int(time.time())}.wav')
        os.makedirs('logs', exist_ok=True)
        f.save(tmp_path)

        stt_res = transcribe_audio_file(tmp_path)
        if not stt_res.get('success'):
            return jsonify({'success': False, 'error': stt_res.get('error', 'STT failed'), 'timestamp': datetime.now().isoformat()})

        response = process_text_query(stt_res['text'])
        return jsonify(response)
    except Exception as e:
        logger.error(f"/stt_query error: {e}")
        return jsonify({'success': False, 'error': str(e), 'timestamp': datetime.now().isoformat()})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        db_test = supabase_manager.get_available_slots()
        db_healthy = db_test.get('success', False)
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected' if db_healthy else 'disconnected',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        })

def _generate_tts_response(query_info: dict, result: dict) -> str:
    """Generate text-to-speech response based on query and result"""
    try:
        query_type = query_info['query_type']
        description = query_info['description']
        
        if result.get('success'):
            if query_type == 'available_slots':
                data = result.get('data', [])
                count = len(data)
                return f"Found {count} available parking slots."
            
            elif query_type == 'booked_slots':
                data = result.get('data', [])
                count = len(data)
                return f"Found {count} booked parking slots."
            
            elif query_type == 'book_slot':
                slot_id = query_info.get('parameters', {}).get('slot_id', 'unknown')
                return f"Slot {slot_id} has been booked successfully."
            
            elif query_type == 'release_slot':
                slot_id = query_info.get('parameters', {}).get('slot_id', 'unknown')
                return f"Slot {slot_id} has been released successfully."
            
            elif query_type in ['all_slots', 'vehicles', 'users', 'parking_logs']:
                data = result.get('data', [])
                count = len(data)
                return f"Retrieved {count} records from {query_info['table']}."
            
            else:
                return f"Query executed successfully: {description}"
        
        else:
            error_msg = result.get('error', 'Unknown error')
            return f"Query failed: {error_msg}"
            
    except Exception as e:
        logger.error(f"Error generating TTS response: {e}")
        return "Query processed, but could not generate voice response."

# Error handlers to return JSON instead of HTML
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'timestamp': datetime.now().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'timestamp': datetime.now().isoformat()
    }), 500

if __name__ == '__main__':
    try:
        # Validate configuration
        config.validate_config()
        logger.info("Configuration validated successfully")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please check your environment variables and .env file")
        exit(1)
    
    # Run the application
    logger.info(f"Starting application on {config.HOST}:{config.PORT}")
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
