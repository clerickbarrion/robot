import pygame

pygame.mixer.init()

def sound(now):
  print("playing sound")
  pygame.mixer.music.load(f"{now}.mp3")
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy():
      pygame.time.Clock().tick(10)

if __name__ == "__main__":
    sound()