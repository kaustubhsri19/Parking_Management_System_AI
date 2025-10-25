"""
Test script to verify Supabase connection
"""

from supabase import create_client, Client

# Your Supabase credentials
url = 'https://rsmqxmslaxwczzpzcopn.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJzbXF4bXNsYXh3Y3p6cHpjb3BuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk4OTY3OTEsImV4cCI6MjA3NTQ3Mjc5MX0.YepGyn-qTfayEMLwpiBFV1TJaOP64SXzPb9cVg_t8q8'

try:
    print("🔍 Testing Supabase connection...")
    
    # Create Supabase client
    supabase: Client = create_client(url, key)
    print("✅ Supabase client created successfully")
    
    # Test connection by trying to access a table
    print("🔍 Testing database access...")
    
    # Try to get parking slots
    result = supabase.table('parking_slots').select('*').limit(1).execute()
    print("✅ Database connection successful!")
    print(f"📊 Found {len(result.data)} parking slots")
    
    # Try to get users
    result = supabase.table('users').select('*').limit(1).execute()
    print(f"📊 Found {len(result.data)} users")
    
    # Try to get vehicles
    result = supabase.table('vehicles').select('*').limit(1).execute()
    print(f"📊 Found {len(result.data)} vehicles")
    
    print("\n🎉 SUCCESS! Your Supabase connection is working perfectly!")
    print("You can now run the main application.")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    print("\n🔧 Troubleshooting:")
    print("1. Make sure you've run the SQL schema in Supabase SQL Editor")
    print("2. Check that your Supabase project is active")
    print("3. Verify your credentials are correct")
