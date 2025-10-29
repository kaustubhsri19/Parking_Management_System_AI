# 🚗 AI Powered Voice-to-Query Parking Management System

A comprehensive, production-ready AI-powered parking management system that allows users to interact with the database using natural language voice commands. The system uses a fine-tuned DistilBERT classifier for intent recognition, browser-based speech recognition, and Supabase for database operations.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Supabase](https://img.shields.io/badge/Supabase-Database-orange.svg)](https://supabase.com/)
[![AI](https://img.shields.io/badge/AI-DistilBERT-purple.svg)](https://huggingface.co/distilbert-base-uncased)

---

## 🎯 Features

### Core Capabilities

- **🎤 Voice Recognition**: Browser-based Web Speech API for real-time speech-to-text
- **🤖 AI-Powered NLP**: Fine-tuned DistilBERT classifier with 14 intents (1,267 training examples)
- **💾 Database Integration**: Seamless Supabase integration with optimized queries
- **🔊 Text-to-Speech**: Browser-based audio feedback for query results
- **🌐 Modern Web Interface**: Responsive UI with real-time updates
- **📊 Bulk Operations**: Release all, book all, maintenance management
- **🔧 Maintenance Mode**: Mark slots for maintenance with dedicated status
- **📈 Scalable Architecture**: Easy to extend with new intents and features

### Supported Operations

- Query available/booked/all parking slots
- Book/release specific slots
- Bulk operations (book all, release all)
- Maintenance management (set/view maintenance slots)
- View vehicles, users, and parking logs
- Check specific slot status
- Count available/booked slots

---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Browser)                    │
│  - Web Speech API (STT)                                 │
│  - Speech Synthesis API (TTS)                           │
│  - JavaScript UI (templates/index.html)                 │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/JSON
┌────────────────────▼────────────────────────────────────┐
│                  Flask Backend (app.py)                  │
│  - Route handling (/query, /text_query, /stt_query)    │
│  - Request/response processing                          │
│  - Error handling & logging                             │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│          AI Pipeline (local_orchestrator.py)            │
│  - DistilBERT classifier (14 intents, GPU-accelerated) │
│  - Intent → SQL mapping                                 │
│  - Slot ID extraction (regex-based)                     │
│  - Query parameter building                             │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│        Database Layer (supabase_module.py)              │
│  - Query execution with error handling                  │
│  - Result formatting & ordering                         │
│  - Connection management                                │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Supabase Database                       │
│  - parking_slots (15 slots with status tracking)       │
│  - vehicles, users, parking_logs                        │
│  - Optimized indexes & views                            │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```text
Parking_Management_System_AI/
├── ai_pipeline/                      # AI/ML Pipeline
│   ├── data/
│   │   └── intents.csv              # Training data (1,267 examples, 14 intents)
│   ├── models/
│   │   └── parking_intent_model/    # Trained DistilBERT model
│   ├── local_orchestrator.py        # Intent classification & routing
│   └── train_classifier.py          # Model training script
├── templates/
│   └── index.html                   # Web UI with browser STT/TTS
├── static/
│   └── style.css                    # Modern responsive styling
├── app.py                           # Main Flask application
├── run.py                           # Application entry point
├── config.py                        # Configuration management
├── supabase_module.py               # Database operations
├── supabase_schema.sql              # Database schema & sample data
├── requirements.txt                 # All Python dependencies (includes CUDA PyTorch)
├── .env                             # Environment variables (gitignored)
├── env_sample.txt                   # Environment template
├── setup.py                         # Setup script
└── README.md                        # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Supabase account (free tier works)
- Modern web browser (Chrome/Firefox/Edge)
- CUDA-capable GPU (optional, for faster training)

### 1. Clone & Setup Virtual Environment

```bash
# Clone or download the project
cd Parking_Management_System_AI

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all dependencies (includes CUDA 12.4+ PyTorch, compatible with CUDA 12.8)
pip install -r requirements.txt

# Note: If you have a different CUDA version or want CPU-only:
# Edit requirements.txt line 19 to change the --extra-index-url
# - CUDA 11.8: https://download.pytorch.org/whl/cu118
# - CUDA 12.1: https://download.pytorch.org/whl/cu121
# - CUDA 12.4+: https://download.pytorch.org/whl/cu124 (default - works with 12.8)
# - CPU only:  https://download.pytorch.org/whl/cpu
```

### 3. Set Up Supabase

#### 3.1 Create Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Sign up/login and click "New Project"
3. Fill in project details and wait 2-3 minutes

#### 3.2 Get Credentials

1. Go to **Settings** → **API**
2. Copy:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **anon/public key** (JWT token starting with `eyJ...`)

#### 3.3 Set Up Database

1. Go to **SQL Editor** in Supabase dashboard
2. Open `supabase_schema.sql` from the project
3. Copy all SQL content and paste into SQL Editor
4. Click **Run** (Ctrl+Enter)
5. Verify tables in **Table Editor**: `users`, `vehicles`, `parking_slots`, `parking_logs`

### 4. Configure Environment

```bash
# Copy sample environment file
# Windows:
copy env_sample.txt .env
# macOS/Linux:
cp env_sample.txt .env
```

Edit `.env` file with your Supabase credentials:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-here

FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
SECRET_KEY=your-secret-key-change-in-production
```

### 5. Train the AI Model (First Time Only)

```bash
# Train the DistilBERT classifier
python ai_pipeline/train_classifier.py

# This will:
# - Load 1,267 training examples
# - Fine-tune DistilBERT for 50 epochs
# - Save model to ai_pipeline/models/parking_intent_model/
# - Takes ~5-10 minutes on GPU, ~30-60 minutes on CPU
```

### 6. Run the Application

```bash
# Option 1: Using run.py (recommended)
python run.py

# Option 2: Direct run
python app.py
```

### 7. Access the Application

1. Open browser: `http://localhost:5000`
2. Allow microphone access when prompted
3. Click "Test Microphone" to verify setup
4. Try voice commands or use text input

---

## 🎤 Supported Voice Commands

### Basic Slot Operations

| Command | Description | Intent Label |
|---------|-------------|--------------|
| "show available slots" | Display all available slots | 0: get_available_slots |
| "show booked slots" | Display all booked slots | 1: get_filled_slots |
| "show all slots" | Display all parking slots | 6: get_all_slots |
| "book slot 5" | Book specific slot | 2: book_specific_slot |
| "book any slot" | Book next available | 3: book_any_slot |
| "release slot 5" | Release specific slot | 4: release_specific_slot |
| "remove slot 5" | Release specific slot (alias) | 4: release_specific_slot |
| "empty slot 5" | Release specific slot (alias) | 4: release_specific_slot |
| "vacate slot 5" | Release specific slot (alias) | 4: release_specific_slot |
| "slot 5 status" | Check slot status | 5: get_specific_slot_status |

### Bulk Operations (NEW!)

| Command | Description | Intent Label |
|---------|-------------|--------------|
| "release all slots" | Release all booked slots | 9: release_all_slots |
| "vacate everything" | Release all booked slots | 9: release_all_slots |
| "clear the lot" | Release all booked slots | 9: release_all_slots |
| "book all slots" | Book all available slots | 10: book_all_slots |
| "fill everything" | Book all available slots | 10: book_all_slots |
| "close all slots" | Book all available slots | 10: book_all_slots |

### Maintenance Management (NEW!)

| Command | Description | Intent Label |
|---------|-------------|--------------|
| "set slot 5 to maintenance" | Mark slot for maintenance | 11: set_maintenance |
| "maintenance slot 3" | Mark slot for maintenance | 11: set_maintenance |
| "disable slot 7" | Mark slot for maintenance | 11: set_maintenance |
| "show maintenance slots" | List all maintenance slots | 12: get_maintenance_slots |
| "which slots need maintenance" | List all maintenance slots | 12: get_maintenance_slots |

### Counting & Analytics

| Command | Description | Intent Label |
|---------|-------------|--------------|
| "how many available" | Count available slots | 7: get_available_count |
| "how many booked" | Count booked slots | 8: get_filled_count |

### Data Queries

- "show vehicles" - Display all registered vehicles
- "show users" - Display all users
- "show parking logs" - Display transaction history

---

## 🔧 Configuration

### Environment Variables

```env
# Supabase Configuration (Required)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key

# Flask Configuration
FLASK_ENV=development              # development or production
FLASK_DEBUG=True                   # True for dev, False for prod
FLASK_HOST=0.0.0.0                # Listen on all interfaces
FLASK_PORT=5000                    # Application port
SECRET_KEY=change-this-in-prod     # Flask secret key

# Logging
LOG_LEVEL=INFO                     # DEBUG, INFO, WARNING, ERROR
LOG_FILE=app.log                   # Log file path
```

### Adding New Voice Commands

**Step 1: Add training examples** to `ai_pipeline/data/intents.csv`:

```csv
your new command here, 14
another variation, 14
```

**Step 2: Add intent mapping** in `ai_pipeline/local_orchestrator.py`:

```python
14: {
    'key': 'your_new_intent',
    'description': 'Description of your intent',
    'sql': "SELECT * FROM your_table WHERE condition",
    'needs_slot_id': False,  # or True if slot ID required
}
```

**Step 3: Update NUM_LABELS** in `ai_pipeline/train_classifier.py`:

```python
NUM_LABELS = 15  # Increment for new intent
```

**Step 4: Retrain the model**:

```bash
python ai_pipeline/train_classifier.py
```

**Step 5: Update frontend** in `templates/index.html` (if needed):

```javascript
// Add to summaryFromResult() and displayQueryResults()
```

---

## 🗄️ Database Schema

### Tables

#### 1. users

```sql
- user_id (UUID, Primary Key)
- name (VARCHAR)
- phone (VARCHAR)
- email (VARCHAR)
- created_at, updated_at (TIMESTAMP)
```

#### 2. vehicles

```sql
- vehicle_id (UUID, Primary Key)
- vehicle_no (VARCHAR, Unique)
- vehicle_type (VARCHAR)
- user_id (UUID, Foreign Key → users)
- created_at, updated_at (TIMESTAMP)
```

#### 3. parking_slots

```sql
- slot_id (SERIAL, Primary Key)
- location (VARCHAR)
- status (VARCHAR) -- 'available', 'booked', 'maintenance'
- floor_no (INTEGER)
- slot_type (VARCHAR) -- 'standard', 'premium', 'electric', 'disabled'
- hourly_rate (DECIMAL)
- created_at, updated_at (TIMESTAMP)
```

#### 4. parking_logs

```sql
- log_id (UUID, Primary Key)
- vehicle_id (UUID, Foreign Key → vehicles)
- slot_id (INTEGER, Foreign Key → parking_slots)
- entry_time (TIMESTAMP)
- exit_time (TIMESTAMP, Nullable)
- total_amount (DECIMAL)
- payment_status (VARCHAR)
- created_at (TIMESTAMP)
```

### Views

- **available_slots_view**: Filtered view of available slots
- **current_parking_status**: Real-time occupancy with vehicle details

---

## 🧪 Testing

### Test Voice Commands

```bash
# In browser at http://localhost:5000
1. Click "Test Microphone"
2. Click "Click to Speak"
3. Try: "show available slots"
4. Try: "book slot 3"
5. Try: "release all slots"
6. Try: "set slot 5 to maintenance"
```

### Test Text Input

Use the chat interface to test without voice:

- Type commands in the text box
- Click "Ask" or press Enter
- View results in real-time

### Verify Database

Check Supabase dashboard → Table Editor to see data changes

---

## 🐛 Troubleshooting

### Model Training Issues

**Issue**: CUDA out of memory

```bash
# Solution: Reduce batch size in train_classifier.py
per_device_train_batch_size=8  # Reduce from 16
```

### Microphone Issues

**Issue**: Microphone not working

- Allow microphone access in browser settings
- Try different browser (Chrome recommended)
- Check system microphone permissions
- Use text input as fallback

**Issue**: "Web Speech API not available"

- Use Chrome, Firefox, or Edge (Safari has limited support)
- Ensure HTTPS in production (required for Web Speech API)
- Use text input as alternative

### Supabase Connection

**Issue**: Connection refused

- Verify `.env` has correct `SUPABASE_URL` and `SUPABASE_KEY`
- Check Supabase project is active
- Verify database schema was created

**Issue**: Query fails

- Check table names match schema
- Verify Row Level Security (RLS) policies if enabled
- Check Supabase logs for errors

### Application Errors

**Issue**: Port 5000 already in use

```bash
# Change port in .env
FLASK_PORT=5001
```

**Issue**: Module not found

```bash
# Ensure venv is activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📈 Performance Optimization

### Database

- ✅ Optimized indexes on frequently queried columns
- ✅ Ordered results by `slot_id` for consistent display
- ✅ Efficient query patterns with minimal joins
- ✅ Connection pooling via Supabase

### AI Model

- ✅ GPU acceleration (CUDA) when available
- ✅ Efficient DistilBERT (66M parameters vs BERT's 110M)
- ✅ Cached model loading (loaded once on startup)
- ✅ Fast inference (~50ms per query on GPU)

### Frontend

- ✅ Browser-based STT/TTS (no server overhead)
- ✅ Async JavaScript for non-blocking UI
- ✅ Efficient DOM updates
- ✅ Responsive design with minimal CSS

---

## 🔒 Security Considerations

1. **Environment Variables**: Never commit `.env` to version control
2. **API Keys**: Use Supabase Row Level Security (RLS) in production
3. **Input Validation**: All inputs are validated before processing
4. **HTTPS**: Required for Web Speech API in production
5. **Secret Key**: Change `SECRET_KEY` in production
6. **SQL Injection**: Parameterized queries prevent SQL injection
7. **Error Messages**: No sensitive data in error responses

---

## 🚀 Deployment

### Development

```bash
python run.py
```

### Production

**Step 1: Update environment**:

```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=strong-random-key-here
```

**Step 2: Use production WSGI server**:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Step 3: Enable HTTPS** (required for Web Speech API):

- Use reverse proxy (nginx, Apache)
- Configure SSL certificates (Let's Encrypt)

**Step 4: Set up logging**:

- Configure log rotation
- Monitor error logs
- Set up alerts

---

## 📊 AI Model Details

### Training Dataset

- **Total Examples**: 1,267
- **Intents**: 14 (0-13, where 13 is fallback)
- **Distribution**:
  - get_available_slots: ~94 examples
  - get_filled_slots: ~95 examples
  - book_specific_slot: ~93 examples
  - book_any_slot: ~57 examples
  - release_specific_slot: ~177 examples (includes new variations)
  - get_specific_slot_status: ~77 examples
  - get_all_slots: ~95 examples
  - get_available_count: ~94 examples
  - get_filled_count: ~95 examples
  - release_all_slots: ~80 examples
  - book_all_slots: ~75 examples
  - set_maintenance: ~100 examples
  - get_maintenance_slots: ~92 examples
  - fallback: ~93 examples

### Model Architecture

- **Base Model**: DistilBERT (distilbert-base-uncased)
- **Parameters**: 66 million
- **Fine-tuning**: 50 epochs
- **Batch Size**: 16 (train), 64 (eval)
- **Max Sequence Length**: 64 tokens
- **Optimizer**: AdamW
- **Device**: CUDA (GPU) or CPU

### Performance

- **Accuracy**: ~98% on test set
- **Inference Time**: ~50ms on GPU, ~200ms on CPU
- **Model Size**: ~250 MB

---

## 🔮 Future Enhancements

- [ ] Multi-language support (Spanish, French, etc.)
- [ ] Mobile app (React Native/Flutter)
- [ ] Real-time notifications (WebSockets)
- [ ] Payment integration (Stripe/PayPal)
- [ ] Advanced analytics dashboard
- [ ] IoT sensor integration (occupancy detection)
- [ ] License plate recognition (OCR)
- [ ] Reservation system (advance booking)
- [ ] Dynamic pricing based on demand
- [ ] Admin panel for management

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Supabase](https://supabase.com/) - Database and backend services
- [Hugging Face Transformers](https://huggingface.co/transformers/) - DistilBERT model
- [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API) - Browser STT/TTS
- [PyTorch](https://pytorch.org/) - Deep learning framework

---

## 📞 Support

For support and questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review [Supabase documentation](https://supabase.com/docs)
3. Check [Transformers documentation](https://huggingface.co/docs/transformers)
4. Create an issue in the repository

---

## Happy Parking! 🚗💨

### Built with ❤️ using AI and modern web technologies
