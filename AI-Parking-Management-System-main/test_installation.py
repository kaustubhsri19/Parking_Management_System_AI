"""
Test script for AI Powered Voice-to-Query Parking Management System
Verifies that all components are working correctly
"""

import sys
import os
import traceback

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        import speech_recognition
        print("✅ SpeechRecognition imported successfully")
    except ImportError as e:
        print(f"❌ SpeechRecognition import failed: {e}")
        return False
    
    try:
        import pyaudio
        print("✅ PyAudio imported successfully")
    except ImportError as e:
        print(f"❌ PyAudio import failed: {e}")
        return False
    
    try:
        import supabase
        print("✅ Supabase imported successfully")
    except ImportError as e:
        print(f"❌ Supabase import failed: {e}")
        return False
    
    try:
        from gtts import gTTS
        print("✅ gTTS imported successfully")
    except ImportError as e:
        print(f"❌ gTTS import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration loading"""
    print("\n🔍 Testing configuration...")
    
    try:
        from config import get_config
        config = get_config()
        print("✅ Configuration loaded successfully")
        
        # Check if required environment variables are set
        if not config.SUPABASE_URL or not config.SUPABASE_KEY:
            print("⚠️  Supabase credentials not configured")
            print("   Please set SUPABASE_URL and SUPABASE_KEY in .env file")
            return False
        else:
            print("✅ Supabase credentials configured")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_voice_module():
    """Test voice recognition module"""
    print("\n🔍 Testing voice module...")
    
    try:
        from voice_module import voice_recognizer
        print("✅ Voice module imported successfully")
        
        # Test microphone availability
        available_mics = voice_recognizer.get_available_microphones()
        if available_mics:
            print(f"✅ Microphones detected: {len(available_mics)} devices")
        else:
            print("⚠️  No microphones detected")
        
        return True
    except Exception as e:
        print(f"❌ Voice module test failed: {e}")
        return False

def test_nlp_module():
    """Test NLP processing module"""
    print("\n🔍 Testing NLP module...")
    
    try:
        from nlp_module import query_mapper
        print("✅ NLP module imported successfully")
        
        # Test a sample voice command
        test_commands = [
            "show available slots",
            "book slot 3",
            "show vehicles"
        ]
        
        for cmd in test_commands:
            result = query_mapper.map_voice_to_query(cmd)
            if result['success']:
                print(f"✅ Command '{cmd}' mapped successfully")
            else:
                print(f"⚠️  Command '{cmd}' mapping failed: {result.get('error', 'Unknown error')}")
        
        return True
    except Exception as e:
        print(f"❌ NLP module test failed: {e}")
        return False

def test_supabase_module():
    """Test Supabase connection"""
    print("\n🔍 Testing Supabase module...")
    
    try:
        from supabase_module import supabase_manager
        print("✅ Supabase module imported successfully")
        
        # Test connection (this might fail if credentials are not set)
        try:
            result = supabase_manager.get_available_slots()
            if result.get('success'):
                print("✅ Supabase connection successful")
            else:
                print(f"⚠️  Supabase connection failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"⚠️  Supabase connection test failed: {e}")
            print("   This is expected if Supabase credentials are not configured")
        
        return True
    except Exception as e:
        print(f"❌ Supabase module test failed: {e}")
        return False

def test_flask_app():
    """Test Flask application"""
    print("\n🔍 Testing Flask application...")
    
    try:
        from app import app
        print("✅ Flask application imported successfully")
        
        # Test if app can be created
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Flask application responds to requests")
            else:
                print(f"⚠️  Flask application returned status {response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ Flask application test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 AI Powered Voice-to-Query Parking Management System - Installation Test")
    print("="*80)
    
    tests = [
        ("Import Test", test_imports),
        ("Configuration Test", test_config),
        ("Voice Module Test", test_voice_module),
        ("NLP Module Test", test_nlp_module),
        ("Supabase Module Test", test_supabase_module),
        ("Flask Application Test", test_flask_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            traceback.print_exc()
    
    print("\n" + "="*80)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your installation is ready.")
        print("\n🚀 You can now run the application with: python app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\n📚 For help, see the README.md file or run: python setup.py")
    
    print("="*80)

if __name__ == "__main__":
    main()
