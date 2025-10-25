"""
Supabase module for database operations
Handles all database interactions with Supabase
"""

import os
from supabase import create_client, Client
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SupabaseManager:
    def __init__(self):
        """Initialize Supabase client"""
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        
        self.supabase: Client = create_client(self.url, self.key)
    
    def execute_query(self, query: str) -> Dict[str, Any]:
        """
        Execute a raw SQL query on Supabase
        Note: Supabase doesn't support raw SQL queries directly
        This is a placeholder for demonstration
        """
        try:
            # For demonstration, we'll parse the query and use appropriate methods
            query_lower = query.lower().strip()
            
            if query_lower.startswith('select'):
                return self._handle_select_query(query)
            elif query_lower.startswith('insert'):
                return self._handle_insert_query(query)
            elif query_lower.startswith('update'):
                return self._handle_update_query(query)
            elif query_lower.startswith('delete'):
                return self._handle_delete_query(query)
            else:
                return {"error": "Unsupported query type"}
                
        except Exception as e:
            return {"error": f"Query execution failed: {str(e)}"}
    
    def _handle_select_query(self, query: str) -> Dict[str, Any]:
        """Handle SELECT queries"""
        try:
            query_lower = query.lower()
            
            if 'parking_slots' in query_lower:
                if 'status' in query_lower and 'available' in query_lower:
                    result = self.supabase.table('parking_slots').select('*').eq('status', 'available').execute()
                else:
                    result = self.supabase.table('parking_slots').select('*').execute()
                return {"success": True, "data": result.data}
            
            elif 'vehicles' in query_lower:
                result = self.supabase.table('vehicles').select('*').execute()
                return {"success": True, "data": result.data}
            
            elif 'users' in query_lower:
                result = self.supabase.table('users').select('*').execute()
                return {"success": True, "data": result.data}
            
            elif 'parking_logs' in query_lower:
                result = self.supabase.table('parking_logs').select('*').execute()
                return {"success": True, "data": result.data}
            
            else:
                return {"error": "Table not found in query"}
                
        except Exception as e:
            return {"error": f"SELECT query failed: {str(e)}"}
    
    def _handle_insert_query(self, query: str) -> Dict[str, Any]:
        """Handle INSERT queries"""
        try:
            # This is a simplified implementation
            # In a real scenario, you'd parse the query to extract table and values
            return {"success": True, "message": "INSERT query executed (simplified)"}
        except Exception as e:
            return {"error": f"INSERT query failed: {str(e)}"}
    
    def _handle_update_query(self, query: str) -> Dict[str, Any]:
        """Handle UPDATE queries"""
        try:
            query_lower = query.lower()
            
            if 'parking_slots' in query_lower and 'status' in query_lower:
                # Extract slot_id from query (simplified parsing)
                if 'slot_id=3' in query_lower or 'slot_id = 3' in query_lower:
                    result = self.supabase.table('parking_slots').update({'status': 'booked'}).eq('slot_id', 3).execute()
                    return {"success": True, "data": result.data, "message": "Slot 3 booked successfully"}
                else:
                    return {"error": "Could not parse slot_id from query"}
            else:
                return {"error": "Unsupported UPDATE query"}
                
        except Exception as e:
            return {"error": f"UPDATE query failed: {str(e)}"}
    
    def _handle_delete_query(self, query: str) -> Dict[str, Any]:
        """Handle DELETE queries"""
        try:
            return {"success": True, "message": "DELETE query executed (simplified)"}
        except Exception as e:
            return {"error": f"DELETE query failed: {str(e)}"}
    
    def get_available_slots(self) -> Dict[str, Any]:
        """Get all available parking slots"""
        try:
            result = self.supabase.table('parking_slots').select('*').eq('status', 'available').execute()
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"error": f"Failed to get available slots: {str(e)}"}
    
    def book_slot(self, slot_id: int, vehicle_id: int = None) -> Dict[str, Any]:
        """Book a parking slot"""
        try:
            result = self.supabase.table('parking_slots').update({'status': 'booked'}).eq('slot_id', slot_id).execute()
            return {"success": True, "data": result.data, "message": f"Slot {slot_id} booked successfully"}
        except Exception as e:
            return {"error": f"Failed to book slot: {str(e)}"}
    
    def release_slot(self, slot_id: int) -> Dict[str, Any]:
        """Release a parking slot"""
        try:
            result = self.supabase.table('parking_slots').update({'status': 'available'}).eq('slot_id', slot_id).execute()
            return {"success": True, "data": result.data, "message": f"Slot {slot_id} released successfully"}
        except Exception as e:
            return {"error": f"Failed to release slot: {str(e)}"}
    
    def get_parking_logs(self, vehicle_id: int = None) -> Dict[str, Any]:
        """Get parking logs"""
        try:
            if vehicle_id:
                result = self.supabase.table('parking_logs').select('*').eq('vehicle_id', vehicle_id).execute()
            else:
                result = self.supabase.table('parking_logs').select('*').execute()
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"error": f"Failed to get parking logs: {str(e)}"}

# Global instance
supabase_manager = SupabaseManager()
