#!/usr/bin/env python3
"""
Run script for AI Powered Voice-to-Query Parking Management System
Provides an easy way to start the application with proper error handling
"""

import sys
import os
import logging
from pathlib import Path

def check_environment():
    """Check if the environment is properly set up"""
    print("🔍 Checking environment...")
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found!")
        print("   Please run 'python setup.py' first or create .env file manually")
        return False
    
    # Check if required directories exist
    required_dirs = ['templates', 'static']
    for directory in required_dirs:
        if not Path(directory).exists():
            print(f"❌ Required directory '{directory}' not found!")
            return False
    
    print("✅ Environment check passed")
    return True

def check_dependencies():
    """Check if all dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_modules = [
        'flask',
        'speech_recognition',
        'pyaudio',
        'supabase',
        'gtts',
        'python-dotenv'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"❌ Missing dependencies: {', '.join(missing_modules)}")
        print("   Please run 'pip install -r requirements.txt'")
        return False
    
    print("✅ All dependencies are installed")
    return True

def main():
    """Main run function"""
    print("🚀 Starting AI Powered Voice-to-Query Parking Management System")
    print("="*70)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Import and run the application
    try:
        print("🔍 Loading application...")
        from app import app, config
        
        print("✅ Application loaded successfully")
        print(f"🌐 Starting server on {config.HOST}:{config.PORT}")
        print(f"🔧 Debug mode: {'ON' if config.DEBUG else 'OFF'}")
        print("\n📱 Open your browser and go to:")
        print(f"   http://localhost:{config.PORT}")
        print("\n🎤 Make sure your microphone is enabled in your browser")
        print("\n⏹️  Press Ctrl+C to stop the server")
        print("="*70)
        
        # Run the application
        app.run(
            debug=config.DEBUG,
            host=config.HOST,
            port=config.PORT,
            use_reloader=False  # Disable reloader to avoid issues with voice recognition
        )
        
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Failed to start application: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check your .env file configuration")
        print("3. Run the test script: python test_installation.py")
        print("4. Check the README.md for detailed setup instructions")
        sys.exit(1)

if __name__ == "__main__":
    main()
