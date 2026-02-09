import sounddevice as sd
import vosk
import json
import time
from datetime import datetime
from .config import MODEL_PATH
from .detector import KeywordDetector
from .audio import AudioInput

def main():
    keyword_detector = KeywordDetector(model_path=MODEL_PATH)
    audio_input = AudioInput()

    print("Listening for emergency keywords...")
    print(f"Keywords: {keyword_detector.keywords}")
    print("Speak into your microphone...\n")
    
    frame_count = 0
    for audio_data in audio_input.start():
        # Convert audio data to bytes for vosk
        audio_bytes = audio_data.tobytes()
        
        # Process the audio
        detected_keyword = keyword_detector.process_audio(audio_bytes)
        
        # Show periodic feedback every 10 frames (~5 seconds)
        frame_count += 1
        if frame_count % 10 == 0:
            volume = abs(audio_data).mean()
            print(f"\r[Audio level: {volume:5.0f}] Listening...", end="", flush=True)
        
        if detected_keyword:
            current_time = time.time()
            keyword_detector.detect_keyword(detected_keyword, current_time)
            
            if keyword_detector.alert_triggered:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"\n[{timestamp}] ⚠️  ALERT! Detected: '{detected_keyword}'\n")
                keyword_detector.alert_triggered = False

if __name__ == "__main__":
    main()