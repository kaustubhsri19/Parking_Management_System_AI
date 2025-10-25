# AI Powered Voice-to-Query Parking Management System

A comprehensive parking management system that allows users to interact with the database using natural language voice commands. The system converts speech to text, processes natural language queries, and executes database operations on Supabase.

## 🚀 Features

- **Voice Recognition**: Real-time speech-to-text conversion using microphone input
- **Natural Language Processing**: Rule-based mapping of voice commands to SQL queries
- **Database Integration**: Seamless connection with Supabase for data operations
- **Text-to-Speech**: Audio feedback for query results
- **Web Interface**: Modern, responsive web interface with real-time updates
- **Scalable Architecture**: Easy to extend with new voice commands and features

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Voice Input   │───▶│  NLP Processing │───▶│  Database Query │
│   (Microphone)  │    │  (Rule-based)   │    │   (Supabase)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Speech-to-Text  │    │ Query Mapping   │    │ Query Execution │
│ (speech_recog)  │    │ (nlp_module)    │    │ (supabase_py)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Web Interface  │◀───│  Flask Backend  │◀───│  Query Results  │
│   (HTML/CSS)    │    │   (app.py)      │    │   (JSON)        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
AI BASED PARKING/
├── app.py                    # Main Flask application
├── voice_module.py           # Voice recognition functionality
├── nlp_module.py            # Natural language processing
├── supabase_module.py       # Database operations
├── requirements.txt         # Python dependencies
├── supabase_schema.sql      # Database schema
├── README.md               # This file
├── templates/
│   └── index.html          # Web interface template
└── static/
    └── style.css           # CSS styling
```

## 🛠️ Prerequisites

- Python 3.8 or higher
- Microphone access
- Supabase account
- Modern web browser with microphone support

## 📦 Installation

### 1. Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd AI-BASED-PARKING

# Or download and extract the project files
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Note**: On Windows, you might need to install PyAudio separately:
```bash
pip install pipwin
pipwin install pyaudio
```

### 3. Set Up Supabase

1. Go to [Supabase](https://supabase.com) and create a new project
2. In your Supabase dashboard, go to Settings > API
3. Copy your Project URL and anon/public key
4. Create a `.env` file in the project root:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

### 4. Set Up Database Schema

1. In your Supabase dashboard, go to SQL Editor
2. Copy and paste the contents of `supabase_schema.sql`
3. Run the SQL script to create tables and sample data

### 5. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## 🎤 Supported Voice Commands

### Parking Slot Management
- "Show available slots" - Display all available parking slots
- "Show all slots" - Display all parking slots regardless of status
- "Book slot 3" - Book parking slot number 3
- "Release slot 3" - Release parking slot number 3
- "Status of slot 3" - Check the status of slot 3

### Data Queries
- "Show vehicles" - Display all registered vehicles
- "Show users" - Display all registered users
- "Show parking logs" - Display parking transaction history

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

### Voice Recognition Settings

You can modify voice recognition settings in `voice_module.py`:

```python
# Adjust timeout and phrase limits
success, text = voice_recognizer.get_voice_input(
    timeout=5,        # Max time to wait for speech to start
    phrase_time_limit=10  # Max time to wait for phrase to complete
)
```

### Adding New Voice Commands

To add new voice commands, edit `nlp_module.py`:

```python
# Add new pattern in _initialize_patterns method
'custom_query': {
    'patterns': [
        r'your new pattern here',
        r'another pattern'
    ],
    'query_type': 'select',
    'table': 'your_table',
    'sql_template': "SELECT * FROM your_table WHERE condition",
    'description': 'Description of your command'
}
```

## 🚀 Usage

### 1. Access the Web Interface

Open your browser and navigate to `http://localhost:5000`

### 2. Test Microphone

Click "Test Microphone" to ensure your microphone is working properly

### 3. Use Voice Commands

1. Click "Click to Speak" button
2. Wait for the "Listening..." indicator
3. Speak your command clearly
4. Wait for the system to process and respond
5. View results in the interface
6. Click "Play Response" to hear the audio feedback

### 4. Example Workflow

1. Say: "Show available slots"
2. System displays available parking slots
3. Say: "Book slot 5"
4. System books slot 5 and confirms
5. Say: "Show parking logs"
6. System displays recent parking transactions

## 🗄️ Database Schema

### Tables

1. **users** - User information
   - user_id (UUID, Primary Key)
   - name, phone, email
   - created_at, updated_at

2. **vehicles** - Vehicle information
   - vehicle_id (UUID, Primary Key)
   - vehicle_no, vehicle_type
   - user_id (Foreign Key)
   - created_at, updated_at

3. **parking_slots** - Parking slot information
   - slot_id (Serial, Primary Key)
   - location, status, floor_no, slot_type
   - hourly_rate
   - created_at, updated_at

4. **parking_logs** - Parking transaction logs
   - log_id (UUID, Primary Key)
   - vehicle_id, slot_id (Foreign Keys)
   - entry_time, exit_time, total_amount
   - payment_status
   - created_at

### Views

- **available_slots_view** - Shows only available parking slots
- **current_parking_status** - Shows currently occupied slots with details

## 🔒 Security Considerations

1. **Environment Variables**: Never commit `.env` files to version control
2. **API Keys**: Use Supabase Row Level Security (RLS) for production
3. **Input Validation**: The system includes basic input validation
4. **HTTPS**: Use HTTPS in production for secure voice transmission

## 🐛 Troubleshooting

### Common Issues

1. **Microphone Not Working**
   - Check browser permissions for microphone access
   - Test microphone in other applications
   - Try different browsers

2. **PyAudio Installation Issues**
   - On Windows: Use `pipwin install pyaudio`
   - On macOS: Install portaudio first: `brew install portaudio`
   - On Linux: Install system dependencies: `sudo apt-get install python3-pyaudio`

3. **Supabase Connection Issues**
   - Verify your SUPABASE_URL and SUPABASE_KEY
   - Check if your Supabase project is active
   - Ensure database schema is properly set up

4. **Voice Recognition Not Working**
   - Check internet connection (Google Speech Recognition requires internet)
   - Speak clearly and at normal volume
   - Try different phrases or rephrase your command

### Debug Mode

Enable debug mode by setting `debug=True` in `app.py`:

```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

## 📈 Performance Optimization

1. **Database Indexing**: The schema includes optimized indexes
2. **Connection Pooling**: Supabase handles connection pooling automatically
3. **Caching**: Consider implementing Redis for frequently accessed data
4. **Voice Processing**: Adjust timeout values based on your needs

## 🔮 Future Enhancements

- [ ] Machine learning-based NLP for better command understanding
- [ ] Multi-language support
- [ ] Mobile app integration
- [ ] Real-time notifications
- [ ] Payment integration
- [ ] Advanced analytics dashboard
- [ ] Integration with IoT sensors
- [ ] Mobile app with push notifications

## 📝 API Endpoints

### Voice Processing
- `POST /voice_input` - Process voice input
- `POST /query` - Execute voice command query
- `POST /test_microphone` - Test microphone functionality

### Data Access
- `GET /supported_commands` - Get list of supported commands
- `GET /health` - Health check endpoint

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
1. Check the troubleshooting section
2. Review the Supabase documentation
3. Check Python speech recognition documentation
4. Create an issue in the repository

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Supabase](https://supabase.com/) - Database and backend services
- [SpeechRecognition](https://github.com/Uberi/speech_recognition) - Voice recognition
- [Google Text-to-Speech](https://gtts.readthedocs.io/) - Text-to-speech conversion

---

**Happy Parking! 🚗💨**
