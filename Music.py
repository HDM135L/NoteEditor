import pygame

class CLS_Music(object):

    def __init__(self, path, length):
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        self.start = 0
        self.length = length
    
    def play(self):
        pygame.mixer.music.play(0, self.start)

    def stop(self):
        pygame.mixer.music.stop()

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def toggle(self):
        self.playing = pygame.mixer.music.get_busy()
        if self.playing:
            self.pause()
        else:
            self.unpause()

    #get_position and set_position : in seconds
    def get_position(self):
        return (self.start + pygame.mixer.music.get_pos() / 1000)

    def set_position(self, pos):
        pygame.mixer.music.set_pos(pos)

    def fastForward(self, forwardTime = 10):
        self.start = self.get_position() + forwardTime
        if self.start > self.length: self.start = self.length
        self.play()

    def fastBackward(self, backwardTime = 10):
        self.start = self.get_position() - backwardTime
        if self.start < 0: self.start = 0
        self.play()

    def rewind(self):
        self.start = 0
        self.play()