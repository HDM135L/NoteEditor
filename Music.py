import pygame

class CLS_Music(object):

    def __init__(self, path):
        pygame.mixer.init()
        #pygame.time.delay(1000)
        pygame.mixer.music.load(path)
    
    def play(self):
        pygame.mixer.music.play()

    def toggle(self):
        self.playing = pygame.mixer.music.get_busy()
        if self.playing:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

