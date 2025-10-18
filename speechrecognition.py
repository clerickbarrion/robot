from chatbot import ChatBot
from speechify import SpeechPlayer
import sounddevice as sd
import numpy as np
import speech_recognition as sr
from audiolist import get_first_input_device
from datetime import datetime
import serial
import os

class SpeechRecognizer:
    def __init__(self):
        self.sd = sd
        self.np = np
        self.sr = sr
        self.get_first_input_device = get_first_input_device
        self.datetime = datetime
        self.serial = serial
        self.os = os
        self.arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=1)
        self.audio_buffer = []
        self.audio = True
        self.sample_rate = 48000
        self.duration = 0.5
        self.chatbot = ChatBot()
        self.speech_player = SpeechPlayer()

    def audio_callback(self, indata, frames, time, status):
        # Calculate the RMS (Root Mean Square) value
        rms = self.np.sqrt(self.np.mean(indata ** 2))
        print(rms)
        # Define a threshold value to detect audio
        threshold = 0.03
        if rms > threshold:
            print("Audio detected from the application!")
            audio_data = (indata * 32767).astype(self.np.int16)
            self.audio_buffer.append(audio_data)
        else:
            if len(self.audio_buffer) > 0:
                audio_data = (indata * 32767).astype(self.np.int16)
                self.audio_buffer.append(audio_data)
                self.process_audio_buffer()

    def process_audio_buffer(self):
        stacked_audio = self.np.concatenate(self.audio_buffer)
        recognizer = self.sr.Recognizer()
        audio_source = self.sr.AudioData(stacked_audio.tobytes(), sample_rate=self.sample_rate, sample_width=2)
        try:
            text = recognizer.recognize_google(audio_source)
            print("Recognized text:", text)
            self.chatbot.send_message(text, audio=self.audio, arduino=self.arduino)
        except self.sr.UnknownValueError:
            print("Speech recognition could not understand audio")
        self.audio_buffer = []

    def record(self):
        with self.sd.InputStream(device=self.get_first_input_device(), channels=1, callback=self.audio_callback,
                                 samplerate=self.sample_rate, blocksize=int(self.sample_rate * self.duration)):
            print("Listening for audio...")
            input("Press Enter to stop...")

if __name__ == "__main__":
    recognizer = SpeechRecognizer()
    recognizer.record()
