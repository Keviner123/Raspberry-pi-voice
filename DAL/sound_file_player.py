import threading
import pygame

class SoundFilePlayer:

    def __init__(self):
        pass

    def play_mp3(self, filelocation):
        pygame.mixer.init()
        pygame.mixer.music.load(filelocation)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()

    def play_mp3_async(self, filelocation: str):
        thread = threading.Thread(target=self.play_mp3, args=(filelocation,))
        thread.start()
