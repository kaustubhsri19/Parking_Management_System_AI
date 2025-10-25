"""
Simplified Flask application for AI Powered Voice-to-Query Parking Management System
This version works without PyAudio and SpeechRecognition dependencies
"""

from flask import Flask, render_template, request, jsonify
import os
import logging
from datetime import datetime
import json

# Import custom modules
from nlp_module import query_mapper, process_voice_command
from supabase_module import supabase_manager
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
    """Handle voice input from frontend (simulated)"""
    try:
        logger.info("Processing voice input request")
        
        # For demo purposes, return a sample voice command
        # In a real implementation, this would capture actual voice input
        sample_commands = [
            "show available slots",
            "book slot 3",
            "show vehicles",
            "show parking logs"
        ]
        
        # Simulate voice recognition by returning a random command
        import random
        text = random.choice(sample_commands)
        
        return jsonify({
            'success': True,
            'text': text,
            'timestamp': datetime.now().isoformat(),
            'note': 'This is a simulated voice input for demo purposes'
        })
            
    except Exception as e:
        logger.error(f"Error in voice input: {e}")
        return jsonify({
            'success': False,
            'error': f'Voice input error: {str(e)}',
            'timestamp': datetime.now().isoformat()
        })

@app.route('/query', methods=['POST'])
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
        
        # Map voice to SQL query
        query_info = process_voice_command(voice_text)
        
        if not query_info['success']:
            return jsonify({
                'success': False,
                'error': query_info.get('error', 'Unknown error'),
                'suggestions': query_info.get('suggestions', []),
                'timestamp': datetime.now().isoformat()
            })
        
        # Execute query on Supabase
        logger.info(f"Executing SQL: {query_info['sql_query']}")
        result = supabase_manager.execute_query(query_info['sql_query'])
        
        # Prepare response
        response = {
            'success': True,
            'voice_text': voice_text,
            'query_type': query_info['query_type'],
            'description': query_info['description'],
            'sql_query': query_info['sql_query'],
            'database_result': result,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add text-to-speech response
        response['tts_text'] = _generate_tts_response(query_info, result)
        
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
    """Test microphone functionality (simulated)"""
    try:
        return jsonify({
            'success': True,
            'microphone_working': True,
            'available_microphones': ['Simulated Microphone (Demo Mode)'],
            'note': 'This is a simulated microphone test for demo purposes',
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
    """Get list of supported voice commands"""
    try:
        commands = query_mapper.get_supported_commands()
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
            'voice_recognition': 'simulated',
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

if __name__ == '__main__':
    try:
        # Validate configuration
        config.validate_config()
        logger.info("Configuration validated successfully")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please check your environment variables and .env file")
        print("\n" + "="*60)
        print("❌ CONFIGURATION ERROR")
        print("="*60)
        print("Please update your .env file with your Supabase credentials:")
        print("1. SUPABASE_URL=https://your-project-id.supabase.co")
        print("2. SUPABASE_KEY=your-supabase-anon-key")
        print("\nThen run the application again.")
        print("="*60)
        exit(1)
    
    # Run the application
    print("\n" + "="*60)
    print("🚀 AI Powered Voice-to-Query Parking Management System")
    print("="*60)
    print(f"🌐 Starting server on {config.HOST}:{config.PORT}")
    print(f"🔧 Debug mode: {'ON' if config.DEBUG else 'OFF'}")
    print("\n📱 Open your browser and go to:")
    print(f"   http://localhost:{config.PORT}")
    print("\n🎤 Voice recognition is simulated for demo purposes")
    print("⏹️  Press Ctrl+C to stop the server")
    print("="*60)
    
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
