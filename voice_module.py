"""
Voice recognition module
Handles speech-to-text conversion using microphone input
"""

import speech_recognition as sr
import pyaudio
import io
import wave
from typing import Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceRecognizer:
    def __init__(self):
        """Initialize the voice recognizer"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            logger.info("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            logger.info("Ambient noise adjustment complete")
    
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
            
        except sr.WaitTimeoutError:
            logger.warning("No speech detected within timeout period")
            return False, "No speech detected. Please try again."
            
        except sr.UnknownValueError:
            logger.warning("Could not understand the audio")
            return False, "Could not understand the audio. Please try again."
            
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            return False, f"Speech recognition service error: {str(e)}"
            
        except Exception as e:
            logger.error(f"Unexpected error during voice recognition: {e}")
            return False, f"Unexpected error: {str(e)}"
    
    def test_microphone(self) -> bool:
        """
        Test if microphone is working properly
        
        Returns:
            bool: True if microphone is working, False otherwise
        """
        try:
            with self.microphone as source:
                # Quick test to see if we can access the microphone
                test_audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=1)
                return True
        except Exception as e:
            logger.error(f"Microphone test failed: {e}")
            return False
    
    def get_available_microphones(self) -> list:
        """
        Get list of available microphones
        
        Returns:
            list: List of microphone names
        """
        try:
            mic_list = sr.Microphone.list_microphone_names()
            return mic_list
        except Exception as e:
            logger.error(f"Failed to get microphone list: {e}")
            return []

# Global instance
voice_recognizer = VoiceRecognizer()

def get_voice_input() -> str:
    """
    Simple function to get voice input
    Returns the recognized text or error message
    """
    success, text = voice_recognizer.get_voice_input()
    return text
