"""
Setup script for AI Powered Voice-to-Query Parking Management System
Helps users set up the project with proper configuration
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def create_env_file():
    """Create .env file from sample"""
    env_file = Path(".env")
    sample_file = Path("env_sample.txt")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if sample_file.exists():
        try:
            shutil.copy(sample_file, env_file)
            print("✅ Created .env file from sample")
            print("⚠️  Please edit .env file with your Supabase credentials")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("❌ Sample environment file not found")
        return False

def check_microphone():
    """Check if microphone is available"""
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        device_count = p.get_device_count()
        p.terminate()
        
        if device_count > 0:
            print("✅ Microphone devices detected")
            return True
        else:
            print("⚠️  No microphone devices detected")
            return False
    except ImportError:
        print("❌ PyAudio not installed - microphone check skipped")
        return False
    except Exception as e:
        print(f"⚠️  Microphone check failed: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['templates', 'static', 'logs']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Directory '{directory}' ready")

def display_next_steps():
    """Display next steps for the user"""
    print("\n" + "="*60)
    print("🎉 Setup completed successfully!")
    print("="*60)
    print("\n📋 Next steps:")
    print("1. Edit .env file with your Supabase credentials:")
    print("   - SUPABASE_URL: Your Supabase project URL")
    print("   - SUPABASE_KEY: Your Supabase anon key")
    print("\n2. Set up your Supabase database:")
    print("   - Go to your Supabase dashboard")
    print("   - Open SQL Editor")
    print("   - Run the SQL script from supabase_schema.sql")
    print("\n3. Run the application:")
    print("   python app.py")
    print("\n4. Open your browser and go to:")
    print("   http://localhost:5000")
    print("\n📚 For detailed instructions, see README.md")
    print("="*60)

def main():
    """Main setup function"""
    print("🚀 AI Powered Voice-to-Query Parking Management System Setup")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        print("\n❌ Setup failed during package installation")
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        print("\n❌ Setup failed during environment file creation")
        sys.exit(1)
    
    # Check microphone
    check_microphone()
    
    # Display next steps
    display_next_steps()

if __name__ == "__main__":
    main()
