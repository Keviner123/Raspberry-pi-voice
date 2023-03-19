import threading
import pygame

class SoundFilePlayer:

    def __init__(self):
        pygame.mixer.init()

    def PlayMp3(self, filelocation: str):
        def play_mp3():
            pygame.mixer.music.load(filelocation)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.quit()

        thread = threading.Thread(target=play_mp3)
        thread.start()