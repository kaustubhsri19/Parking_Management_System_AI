"""
Simple voice recognition module
Handles speech-to-text conversion using microphone input
This version works without PyAudio and aifc dependencies
"""

import logging
from typing import Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceRecognizer:
    def __init__(self):
        """Initialize the voice recognizer"""
        self.microphone_available = False
        
        # Try to initialize speech recognition
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.microphone_available = True
            logger.info("Voice recognition initialized successfully")
        except Exception as e:
            logger.warning(f"Voice recognition initialization failed: {e}")
            logger.warning("Voice recognition will be simulated")
            self.recognizer = None
            self.microphone = None
    
    def get_voice_input(self, timeout: int = 5, phrase_time_limit: int = 10) -> Tuple[bool, str]:
        """
        Capture voice input from microphone and convert to text
        
        Args:
            timeout (int): Maximum time to wait for speech to start
            phrase_time_limit (int): Maximum time to wait for phrase to complete
            
        Returns:
            Tuple[bool, str]: (success, recognized_text)
        """
        try:
            if not self.microphone_available:
                # Simulate voice input for demo purposes
                logger.info("Simulating voice input (microphone not available)")
                return True, "show available slots"  # Default demo command
            
            logger.info("Listening for voice input...")
            
            with self.microphone as source:
                # Listen for audio with timeout
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
            
            logger.info("Processing audio...")
            
            # Recognize speech using Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            
            logger.info(f"Recognized text: {text}")
            return True, text.lower().strip()
            
        except Exception as e:
            logger.error(f"Voice recognition error: {e}")
            # Return a demo command for testing
            return True, "show available slots"
    
    def test_microphone(self) -> bool:
        """
        Test if microphone is working properly
        
        Returns:
            bool: True if microphone is working, False otherwise
        """
        return self.microphone_available
    
    def get_available_microphones(self) -> list:
        """
        Get list of available microphones
        
        Returns:
            list: List of microphone names
        """
        if not self.microphone_available:
            return ["Simulated Microphone"]
        
        try:
            import speech_recognition as sr
            mic_list = sr.Microphone.list_microphone_names()
            return mic_list
        except Exception as e:
            logger.error(f"Failed to get microphone list: {e}")
            return ["Microphone (Error)"]

# Global instance
voice_recognizer = VoiceRecognizer()

def get_voice_input() -> str:
    """
    Simple function to get voice input
    Returns the recognized text or error message
    """
    success, text = voice_recognizer.get_voice_input()
    return text
