import pygame

class SoundFilePlayer:

    def __init__(self) -> None:
        pass

    def PlayMp3(self, filelocation: str):

        pygame.mixer.init()
        pygame.mixer.music.load(filelocation)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # wait for the music to finish playing

        pygame.quit()