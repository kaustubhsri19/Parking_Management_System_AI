"""
NLP module for converting natural language to SQL queries
Uses rule-based approach to map voice commands to database operations
"""

import re
from typing import Dict, List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QueryMapper:
    def __init__(self):
        """Initialize the query mapper with predefined patterns"""
        self.patterns = self._initialize_patterns()
    
    def _initialize_patterns(self) -> Dict[str, Dict]:
        """Initialize pattern mappings for different query types"""
        return {
            # Available slots queries
            'available_slots': {
                'patterns': [
                    r'show available slots',
                    r'available slots',
                    r'free slots',
                    r'empty slots',
                    r'show free parking',
                    r'what slots are available',
                    r'list available parking'
                ],
                'query_type': 'select',
                'table': 'parking_slots',
                'sql_template': "SELECT * FROM parking_slots WHERE status='available'",
                'description': 'Show all available parking slots'
            },
            
            # Book slot queries
            'book_slot': {
                'patterns': [
                    r'book slot (\d+)',
                    r'reserve slot (\d+)',
                    r'occupy slot (\d+)',
                    r'park in slot (\d+)',
                    r'use slot (\d+)',
                    r'take slot (\d+)'
                ],
                'query_type': 'update',
                'table': 'parking_slots',
                'sql_template': "UPDATE parking_slots SET status='booked' WHERE slot_id={slot_id}",
                'description': 'Book a specific parking slot',
                'requires_params': ['slot_id']
            },
            
            # Release slot queries
            'release_slot': {
                'patterns': [
                    r'release slot (\d+)',
                    r'free slot (\d+)',
                    r'vacate slot (\d+)',
                    r'leave slot (\d+)',
                    r'empty slot (\d+)'
                ],
                'query_type': 'update',
                'table': 'parking_slots',
                'sql_template': "UPDATE parking_slots SET status='available' WHERE slot_id={slot_id}",
                'description': 'Release a parking slot',
                'requires_params': ['slot_id']
            },
            
            # Show all slots queries
            'all_slots': {
                'patterns': [
                    r'show all slots',
                    r'list all slots',
                    r'show parking slots',
                    r'display slots',
                    r'all parking slots'
                ],
                'query_type': 'select',
                'table': 'parking_slots',
                'sql_template': "SELECT * FROM parking_slots",
                'description': 'Show all parking slots'
            },
            
            # Vehicle queries
            'vehicles': {
                'patterns': [
                    r'show vehicles',
                    r'list vehicles',
                    r'show all vehicles',
                    r'registered vehicles'
                ],
                'query_type': 'select',
                'table': 'vehicles',
                'sql_template': "SELECT * FROM vehicles",
                'description': 'Show all registered vehicles'
            },
            
            # User queries
            'users': {
                'patterns': [
                    r'show users',
                    r'list users',
                    r'show all users',
                    r'registered users'
                ],
                'query_type': 'select',
                'table': 'users',
                'sql_template': "SELECT * FROM users",
                'description': 'Show all registered users'
            },
            
            # Parking logs queries
            'parking_logs': {
                'patterns': [
                    r'show parking logs',
                    r'parking history',
                    r'show logs',
                    r'parking records',
                    r'transaction history'
                ],
                'query_type': 'select',
                'table': 'parking_logs',
                'sql_template': "SELECT * FROM parking_logs",
                'description': 'Show parking transaction logs'
            },
            
            # Status queries
            'slot_status': {
                'patterns': [
                    r'status of slot (\d+)',
                    r'slot (\d+) status',
                    r'is slot (\d+) available',
                    r'check slot (\d+)'
                ],
                'query_type': 'select',
                'table': 'parking_slots',
                'sql_template': "SELECT * FROM parking_slots WHERE slot_id={slot_id}",
                'description': 'Check status of a specific slot',
                'requires_params': ['slot_id']
            }
        }
    
    def map_voice_to_query(self, voice_text: str) -> Dict[str, any]:
        """
        Map voice input to SQL query
        
        Args:
            voice_text (str): The recognized voice text
            
        Returns:
            Dict: Query information including SQL, type, and metadata
        """
        try:
            voice_text = voice_text.lower().strip()
            logger.info(f"Processing voice input: '{voice_text}'")
            
            # Try to match against all patterns
            for query_type, config in self.patterns.items():
                for pattern in config['patterns']:
                    match = re.search(pattern, voice_text, re.IGNORECASE)
                    if match:
                        logger.info(f"Matched pattern: {pattern}")
                        
                        # Extract parameters if needed
                        params = {}
                        if 'requires_params' in config:
                            for param in config['requires_params']:
                                if param == 'slot_id':
                                    params['slot_id'] = match.group(1)
                        
                        # Generate SQL query
                        sql_query = self._generate_sql(config, params)
                        
                        return {
                            'success': True,
                            'query_type': query_type,
                            'sql_query': sql_query,
                            'description': config['description'],
                            'table': config['table'],
                            'parameters': params,
                            'original_text': voice_text
                        }
            
            # No pattern matched
            return {
                'success': False,
                'error': 'No matching pattern found',
                'suggestions': self._get_suggestions(),
                'original_text': voice_text
            }
            
        except Exception as e:
            logger.error(f"Error mapping voice to query: {e}")
            return {
                'success': False,
                'error': f'Error processing voice input: {str(e)}',
                'original_text': voice_text
            }
    
    def _generate_sql(self, config: Dict, params: Dict) -> str:
        """Generate SQL query from template and parameters"""
        sql_template = config['sql_template']
        
        # Replace parameters in template
        for param_name, param_value in params.items():
            sql_template = sql_template.replace(f'{{{param_name}}}', str(param_value))
        
        return sql_template
    
    def _get_suggestions(self) -> List[str]:
        """Get list of supported voice commands"""
        suggestions = []
        for config in self.patterns.values():
            # Add first pattern as example
            if config['patterns']:
                suggestions.append(config['patterns'][0])
        return suggestions
    
    def add_custom_pattern(self, query_type: str, pattern: str, sql_template: str, description: str):
        """
        Add a custom pattern for voice-to-query mapping
        
        Args:
            query_type (str): Type of query (e.g., 'custom_query')
            pattern (str): Regex pattern to match
            sql_template (str): SQL template with placeholders
            description (str): Description of the query
        """
        if query_type not in self.patterns:
            self.patterns[query_type] = {
                'patterns': [],
                'query_type': 'custom',
                'table': 'unknown',
                'sql_template': sql_template,
                'description': description
            }
        
        self.patterns[query_type]['patterns'].append(pattern)
        logger.info(f"Added custom pattern: {pattern}")
    
    def get_supported_commands(self) -> Dict[str, List[str]]:
        """Get all supported voice commands organized by category"""
        commands = {}
        for query_type, config in self.patterns.items():
            commands[query_type] = {
                'patterns': config['patterns'],
                'description': config['description']
            }
        return commands

# Global instance
query_mapper = QueryMapper()

def process_voice_command(voice_text: str) -> Dict[str, any]:
    """
    Process voice command and return query information
    
    Args:
        voice_text (str): The recognized voice text
        
    Returns:
        Dict: Query information including SQL, type, and metadata
    """
    return query_mapper.map_voice_to_query(voice_text)
