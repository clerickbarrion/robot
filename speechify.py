import pygame

class SpeechPlayer:
    def __init__(self):
        self.pygame = pygame
        self.pygame.mixer.init()

    def sound(self, audio_file):
        print("playing sound")
        self.pygame.mixer.music.load(f"{audio_file}.mp3")
        self.pygame.mixer.music.play()
        while self.pygame.mixer.music.get_busy():
            self.pygame.time.Clock().tick(10)

    def stream_sound(self, audio_stream, temp_file_path):
        """
        Play audio as it streams in from a file-like object or generator.
        audio_stream: generator yielding bytes
        temp_file_path: path to write the temporary audio file
        """
        with open(temp_file_path, 'wb') as f:
            for chunk in audio_stream:
                f.write(chunk)
                f.flush()
                if f.tell() > 1024 * 16:  # Start playback after some data is available
                    if not self.pygame.mixer.music.get_busy():
                        self.pygame.mixer.music.load(temp_file_path)
                        self.pygame.mixer.music.play()
        # Wait for playback to finish
        while self.pygame.mixer.music.get_busy():
            self.pygame.time.Clock().tick(10)

if __name__ == "__main__":
    player = SpeechPlayer()
    # Example usage: player.sound('audio/filename')
    # Uncomment and provide a valid audio file path to test
    # player.sound('audio/your_audio_file')