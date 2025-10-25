"""
Working AI Powered Voice-to-Query Parking Management System
"""

from flask import Flask, render_template, request, jsonify
import os
import logging
from datetime import datetime
import json
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'demo-secret-key'

# Demo database data
DEMO_DATA = {
    'parking_slots': [
        {'slot_id': 1, 'location': 'A1', 'status': 'available', 'floor_no': 1, 'slot_type': 'standard'},
        {'slot_id': 2, 'location': 'A2', 'status': 'available', 'floor_no': 1, 'slot_type': 'standard'},
        {'slot_id': 3, 'location': 'A3', 'status': 'booked', 'floor_no': 1, 'slot_type': 'premium'},
        {'slot_id': 4, 'location': 'A4', 'status': 'available', 'floor_no': 1, 'slot_type': 'standard'},
        {'slot_id': 5, 'location': 'A5', 'status': 'available', 'floor_no': 1, 'slot_type': 'electric'},
        {'slot_id': 6, 'location': 'B1', 'status': 'available', 'floor_no': 2, 'slot_type': 'standard'},
        {'slot_id': 7, 'location': 'B2', 'status': 'available', 'floor_no': 2, 'slot_type': 'premium'},
        {'slot_id': 8, 'location': 'B3', 'status': 'available', 'floor_no': 2, 'slot_type': 'disabled'},
        {'slot_id': 9, 'location': 'B4', 'status': 'booked', 'floor_no': 2, 'slot_type': 'standard'},
        {'slot_id': 10, 'location': 'B5', 'status': 'available', 'floor_no': 2, 'slot_type': 'electric'},
    ],
    'vehicles': [
        {'vehicle_id': 1, 'vehicle_no': 'ABC-123', 'vehicle_type': 'car', 'user_id': 1},
        {'vehicle_id': 2, 'vehicle_no': 'XYZ-789', 'vehicle_type': 'motorcycle', 'user_id': 2},
        {'vehicle_id': 3, 'vehicle_no': 'DEF-456', 'vehicle_type': 'car', 'user_id': 3},
        {'vehicle_id': 4, 'vehicle_no': 'GHI-321', 'vehicle_type': 'truck', 'user_id': 4},
        {'vehicle_id': 5, 'vehicle_no': 'JKL-654', 'vehicle_type': 'van', 'user_id': 5},
    ],
    'users': [
        {'user_id': 1, 'name': 'John Doe', 'phone': '+1234567890', 'email': 'john.doe@email.com'},
        {'user_id': 2, 'name': 'Jane Smith', 'phone': '+1234567891', 'email': 'jane.smith@email.com'},
        {'user_id': 3, 'name': 'Bob Johnson', 'phone': '+1234567892', 'email': 'bob.johnson@email.com'},
        {'user_id': 4, 'name': 'Alice Brown', 'phone': '+1234567893', 'email': 'alice.brown@email.com'},
        {'user_id': 5, 'name': 'Charlie Wilson', 'phone': '+1234567894', 'email': 'charlie.wilson@email.com'},
    ],
    'parking_logs': [
        {'log_id': 1, 'vehicle_id': 1, 'slot_id': 3, 'entry_time': '2024-01-08T10:00:00Z', 'exit_time': '2024-01-08T12:30:00Z', 'total_amount': 7.50, 'payment_status': 'paid'},
        {'log_id': 2, 'vehicle_id': 2, 'slot_id': 4, 'entry_time': '2024-01-08T11:00:00Z', 'exit_time': None, 'total_amount': 0.00, 'payment_status': 'pending'},
        {'log_id': 3, 'vehicle_id': 3, 'slot_id': 9, 'entry_time': '2024-01-08T09:00:00Z', 'exit_time': '2024-01-08T11:00:00Z', 'total_amount': 10.00, 'payment_status': 'paid'},
    ]
}

def execute_demo_query(query_type, sql_query, parameters=None):
    """Execute demo queries on in-memory data"""
    try:
        if 'parking_slots' in sql_query.lower():
            if 'status' in sql_query.lower() and 'available' in sql_query.lower():
                data = [slot for slot in DEMO_DATA['parking_slots'] if slot['status'] == 'available']
            else:
                data = DEMO_DATA['parking_slots']
            return {'success': True, 'data': data}
        
        elif 'vehicles' in sql_query.lower():
            return {'success': True, 'data': DEMO_DATA['vehicles']}
        
        elif 'users' in sql_query.lower():
            return {'success': True, 'data': DEMO_DATA['users']}
        
        elif 'parking_logs' in sql_query.lower():
            return {'success': True, 'data': DEMO_DATA['parking_logs']}
        
        elif 'update' in sql_query.lower() and 'parking_slots' in sql_query.lower():
            # Handle booking/releasing slots
            if parameters and 'slot_id' in parameters:
                slot_id = int(parameters['slot_id'])
                for slot in DEMO_DATA['parking_slots']:
                    if slot['slot_id'] == slot_id:
                        if 'booked' in sql_query.lower():
                            slot['status'] = 'booked'
                            return {'success': True, 'data': [slot], 'message': f'Slot {slot_id} booked successfully'}
                        elif 'available' in sql_query.lower():
                            slot['status'] = 'available'
                            return {'success': True, 'data': [slot], 'message': f'Slot {slot_id} released successfully'}
            return {'success': False, 'error': 'Could not process slot update'}
        
        else:
            return {'success': False, 'error': 'Query not supported in demo mode'}
            
    except Exception as e:
        return {'success': False, 'error': f'Demo query execution failed: {str(e)}'}

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
        sample_commands = [
            "show available slots",
            "book slot 3",
            "show vehicles",
            "show parking logs",
            "show all slots",
            "release slot 3",
            "status of slot 5"
        ]
        
        # Simulate voice recognition by returning a random command
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

@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Live Parking Slot Visualization page"""
    return render_template('dashboard.html')

@app.route('/api/parking_slots', methods=['GET'])
def api_parking_slots():
    """Provide parking slots in a normalized shape for the dashboard
    Fields: slot_id, slot_number, status (available|occupied), vehicle_id
    """
    try:
        slots = []
        for s in DEMO_DATA.get('parking_slots', []):
            status = s.get('status', 'available').lower()
            norm_status = 'occupied' if status == 'booked' else 'available'
            vehicle_id = None
            if norm_status == 'occupied':
                # Demo: attach the first matching log vehicle if any
                vehicle_id = next((log['vehicle_id'] for log in DEMO_DATA.get('parking_logs', []) if log['slot_id'] == s['slot_id']), None)
            slots.append({
                'slot_id': s['slot_id'],
                'slot_number': s.get('location') or f"S{s['slot_id']}",
                'status': norm_status,
                'vehicle_id': vehicle_id
            })
        return jsonify({'success': True, 'data': slots, 'timestamp': datetime.now().isoformat()})
    except Exception as e:
        logger.error(f"Error fetching slots: {e}")
        return jsonify({'success': False, 'error': str(e), 'data': []}), 500

@app.route('/text_query', methods=['POST'])
def text_query():
    """Process typed query using same logic as voice queries"""
    return process_query()

@app.route('/voice_query', methods=['POST'])
def voice_query():
    """Alias endpoint for voice queries to maintain compatibility"""
    return process_query()

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
        
        # Simple query mapping
        if 'available slots' in voice_text.lower():
            query_type = 'available_slots'
            sql_query = "SELECT * FROM parking_slots WHERE status='available'"
            description = 'Show all available parking slots'
            result = execute_demo_query(query_type, sql_query)
        elif 'book slot' in voice_text.lower():
            slot_id = voice_text.split()[-1]
            query_type = 'book_slot'
            sql_query = f"UPDATE parking_slots SET status='booked' WHERE slot_id={slot_id}"
            description = f'Book parking slot {slot_id}'
            result = execute_demo_query(query_type, sql_query, {'slot_id': slot_id})
        elif 'show vehicles' in voice_text.lower():
            query_type = 'vehicles'
            sql_query = "SELECT * FROM vehicles"
            description = 'Show all vehicles'
            result = execute_demo_query(query_type, sql_query)
        elif 'show parking logs' in voice_text.lower():
            query_type = 'parking_logs'
            sql_query = "SELECT * FROM parking_logs"
            description = 'Show parking logs'
            result = execute_demo_query(query_type, sql_query)
        elif 'show all slots' in voice_text.lower():
            query_type = 'all_slots'
            sql_query = "SELECT * FROM parking_slots"
            description = 'Show all parking slots'
            result = execute_demo_query(query_type, sql_query)
        else:
            return jsonify({
                'success': False,
                'error': 'Command not recognized',
                'suggestions': ['show available slots', 'book slot 3', 'show vehicles', 'show parking logs'],
                'timestamp': datetime.now().isoformat()
            })
        
        # Prepare response
        response = {
            'success': True,
            'voice_text': voice_text,
            'query_type': query_type,
            'description': description,
            'sql_query': sql_query,
            'database_result': result,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add text-to-speech response
        if result.get('success'):
            data = result.get('data', [])
            count = len(data)
            response['tts_text'] = f"Found {count} results for {description}"
        else:
            response['tts_text'] = f"Error: {result.get('error', 'Unknown error')}"
        
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
        commands = {
            'available_slots': {
                'patterns': ['show available slots', 'available slots', 'free slots'],
                'description': 'Show all available parking slots'
            },
            'book_slot': {
                'patterns': ['book slot 3', 'reserve slot 3', 'occupy slot 3'],
                'description': 'Book a specific parking slot'
            },
            'vehicles': {
                'patterns': ['show vehicles', 'list vehicles'],
                'description': 'Show all registered vehicles'
            },
            'parking_logs': {
                'patterns': ['show parking logs', 'parking history'],
                'description': 'Show parking transaction history'
            }
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

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'database': 'demo_mode',
        'voice_recognition': 'simulated',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("\n" + "="*70)
    print("AI Powered Voice-to-Query Parking Management System - WORKING VERSION")
    print("="*70)
    print("Starting server on http://localhost:5002")
    print("Debug mode: ON")
    print("\nOpen your browser and go to: http://localhost:5002")
    print("Voice recognition is simulated for demo purposes")
    print("Using demo data (no Supabase required)")
    print("Press Ctrl+C to stop the server")
    print("="*70)
    
    app.run(debug=True, host='0.0.0.0', port=5002)
