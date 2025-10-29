# 🚀 Setup Instructions - AI Parking Management System

## Complete Step-by-Step Guide to Run the Application

### Prerequisites
- Python 3.8 or higher installed
- Supabase account (free tier works)
- Microphone access (for voice commands)
- Modern web browser

---

## Step 1: Create Python Virtual Environment

### Windows:
```powershell
# Navigate to project directory
cd D:\Projects\Parking_Management_System_AI

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

### macOS/Linux:
```bash
# Navigate to project directory
cd /path/to/Parking_Management_System_AI

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

**✅ You should see `(venv)` prefix in your terminal when activated**

---

## Step 2: Install Python Dependencies

### Basic Installation:
```bash
# Make sure venv is activated (you should see (venv) prefix)
pip install --upgrade pip
pip install -r requirements.txt
```

### Windows - PyAudio Installation (if above fails):
```powershell
# If PyAudio installation fails on Windows, use pipwin:
pip install pipwin
pipwin install pyaudio
```

### macOS - PyAudio Installation (if needed):
```bash
# Install portaudio first
brew install portaudio

# Then install PyAudio
pip install pyaudio
```

### Linux - PyAudio Installation (if needed):
```bash
# Install system dependencies
sudo apt-get install portaudio19-dev python3-pyaudio

# Then install PyAudio
pip install pyaudio
```

**✅ Verify installation:**
```bash
python -c "import flask, supabase, speech_recognition; print('✅ All dependencies installed')"
```

---

## Step 3: Set Up Supabase Database

### 3.1 Create Supabase Project
1. Go to [https://supabase.com](https://supabase.com)
2. Sign up or log in
3. Click "New Project"
4. Fill in:
   - Project name: `parking-management` (or any name)
   - Database password: (choose a strong password)
   - Region: (select closest to you)
5. Click "Create new project"
6. Wait 2-3 minutes for project to be ready

### 3.2 Get Supabase Credentials
1. In your Supabase dashboard, go to **Settings** → **API**
2. Copy the following:
   - **Project URL** (looks like: `https://xxxxx.supabase.co`)
   - **anon/public key** (long JWT token starting with `eyJ...`)

### 3.3 Set Up Database Schema
1. In Supabase dashboard, go to **SQL Editor**
2. Click **New query**
3. Open the file `supabase_schema.sql` in your project
4. Copy ALL the SQL content
5. Paste it into the SQL Editor
6. Click **Run** (or press Ctrl+Enter)
7. ✅ You should see "Success. No rows returned" or similar success message
8. Verify tables were created by checking **Table Editor** - you should see:
   - `users`
   - `vehicles`
   - `parking_slots`
   - `parking_logs`

---

## Step 4: Configure Environment Variables

### 4.1 Create .env File
```bash
# Windows PowerShell:
Copy-Item env_sample.txt .env

# macOS/Linux:
cp env_sample.txt .env
```

### 4.2 Edit .env File
Open `.env` file in a text editor and update these values:

```env
# Replace with your actual Supabase credentials
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-starts-with-eyJ

# Flask Configuration (can keep defaults)
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
SECRET_KEY=your-secret-key-here-change-this-in-production

# Voice Recognition (can keep defaults)
VOICE_TIMEOUT=5
VOICE_PHRASE_LIMIT=10
VOICE_LANGUAGE=en-US

# Other settings can remain as default
```

**⚠️ Important:** Never commit `.env` file to version control (it should be in `.gitignore`)

---

## Step 5: Verify Setup (Optional but Recommended)

```bash
# Run setup script to verify everything is configured
python setup.py
```

This will:
- ✅ Check Python version
- ✅ Verify dependencies are installed
- ✅ Create .env file if missing
- ✅ Check microphone availability
- ✅ Create necessary directories

---

## Step 6: Run the Application

### Option 1: Using run.py (Recommended)
```bash
# Make sure venv is activated
python run.py
```

### Option 2: Direct run
```bash
python app.py
```

### Expected Output:
```
🚀 Starting AI Powered Voice-to-Query Parking Management System
======================================================================
🔍 Checking environment...
✅ Environment check passed
🔍 Checking dependencies...
✅ All dependencies are installed
🔍 Loading application...
✅ Application loaded successfully
🌐 Starting server on 0.0.0.0:5000
🔧 Debug mode: ON

📱 Open your browser and go to:
   http://localhost:5000

🎤 Make sure your microphone is enabled in your browser

⏹️  Press Ctrl+C to stop the server
======================================================================
 * Running on http://127.0.0.1:5000
```

---

## Step 7: Access the Application

1. **Open your web browser** (Chrome, Firefox, or Edge recommended)
2. **Navigate to:** `http://localhost:5000`
3. **Allow microphone access** when prompted by your browser
4. **Test the system:**
   - Click "Test Microphone" button
   - Click "Click to Speak" button
   - Try saying: **"Show available slots"**
   - Wait for processing and results

---

## 🎤 Testing Voice Commands

Try these commands:
1. **"Show available slots"** - Lists available parking slots
2. **"Book slot 3"** - Books slot number 3
3. **"Release slot 3"** - Releases slot number 3
4. **"Show all slots"** - Shows all parking slots
5. **"Show vehicles"** - Lists all vehicles
6. **"Show users"** - Lists all users
7. **"Show parking logs"** - Shows transaction history
8. **"Status of slot 5"** - Checks status of specific slot

---

## 🔧 Troubleshooting

### Issue: PyAudio installation fails on Windows
**Solution:**
```powershell
pip install pipwin
pipwin install pyaudio
```

### Issue: "ModuleNotFoundError" when running
**Solution:**
- Make sure virtual environment is activated (you see `(venv)` prefix)
- Reinstall dependencies: `pip install -r requirements.txt`

### Issue: Supabase connection error
**Solution:**
- Verify `.env` file exists and has correct `SUPABASE_URL` and `SUPABASE_KEY`
- Check Supabase dashboard - project should be active
- Verify database schema was created (check Table Editor)

### Issue: Microphone not working
**Solution:**
- Allow microphone access in browser settings
- Try different browser
- Check system microphone permissions
- Test microphone in system settings first

### Issue: Port 5000 already in use
**Solution:**
- Change port in `.env` file: `FLASK_PORT=5001`
- Or stop the process using port 5000

### Issue: Browser shows connection refused
**Solution:**
- Make sure application is still running in terminal
- Check if firewall is blocking the connection
- Try `http://127.0.0.1:5000` instead of `localhost`

---

## 📋 Quick Reference Commands

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Deactivate virtual environment
deactivate

# Install/update dependencies
pip install -r requirements.txt

# Run application
python run.py

# Or directly
python app.py

# Stop application
Press Ctrl+C in the terminal
```

---

## ✅ Verification Checklist

Before running, ensure:
- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed (check with `pip list`)
- [ ] `.env` file created from `env_sample.txt`
- [ ] Supabase credentials added to `.env`
- [ ] Supabase database schema created (run `supabase_schema.sql`)
- [ ] Microphone permissions granted in browser

---

## 🎉 Success Indicators

You'll know everything is working when:
1. ✅ Application starts without errors
2. ✅ Browser loads the web interface at `http://localhost:5000`
3. ✅ "Test Microphone" button works
4. ✅ Voice commands are recognized and processed
5. ✅ Database queries return results
6. ✅ Text-to-speech responses are heard

---

## 📞 Next Steps

After setup is complete:
1. Explore the web interface
2. Try different voice commands
3. Check the database in Supabase dashboard to see data changes
4. Customize voice commands by editing `nlp_module.py`
5. Read `README.md` for more detailed documentation

---

**Happy Coding! 🚀**

