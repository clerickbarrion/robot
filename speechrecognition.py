import sounddevice as sd
import numpy as np
import speech_recognition as sr
import chatbot
import speechify
from audiolist import get_first_input_device
from datetime import datetime
import serial
arduino = serial.Serial(port="COM3", baudrate=9600, timeout=1)


audio_buffer = []  # Initialize an empty audio buffer
audio = True

def audio_callback(indata, frames, time, status):
    global audio_buffer
    
    # Calculate the RMS (Root Mean Square) value
    rms = np.sqrt(np.mean(indata ** 2))
    print(rms)
    # Define a threshold value to detect audio
    threshold = 0.05
    
    if rms > threshold:
        print("Audio detected from the application!")
        
        audio_data = (indata * 32767).astype(np.int16)
        audio_buffer.append(audio_data)  # Append new audio data to buffer
    else:
        if len(audio_buffer) > 0:
            audio_data = (indata * 32767).astype(np.int16)
            audio_buffer.append(audio_data)
            process_audio_buffer()

def process_audio_buffer():
    global audio_buffer
    
    stacked_audio = np.concatenate(audio_buffer)
    
    recognizer = sr.Recognizer()
    audio_source = sr.AudioData(stacked_audio.tobytes(), sample_rate=sample_rate, sample_width=2)
    
    audio_file = f"audio/{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    try:
        text = recognizer.recognize_google(audio_source)
        print("Recognized text:", text)
        print(chatbot.send_message(text, audio_file, audio=audio, arduino=arduino))
        speechify.sound(audio_file)
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")

    audio_buffer = []

# Set the audio parameters
sample_rate = 48000#16000#
duration = 1.2  # Duration of each audio callback in seconds

# Start recording audio
def record():
    with sd.InputStream(device=get_first_input_device(), channels=1, callback=audio_callback,
                        samplerate=sample_rate, blocksize=int(sample_rate * duration)):
        print("Listening for audio...")
        input("Press Enter to stop...")

record()