import pygame

pygame.mixer.init()

def sound(audio_file):
  print("playing sound")
  pygame.mixer.music.load(f"{audio_file}.mp3")
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy():
      pygame.time.Clock().tick(10)

if __name__ == "__main__":
    sound()