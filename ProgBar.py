from Music import *
import sys

class ProgBar(object):

    def __init__(self, plots, screen, length):
        self.plots = plots
        self.screen = screen
        self.length = length

    def write(self, str):
        font = pygame.font.Font(None, 50)
        surf = font.render(str, 1, [0, 0, 0])
        self.screen.blit(surf, [10, 250])

    def clean(self):
        self.screen.fill([255, 255, 255])
        pygame.draw.lines(self.screen, [0, 0, 0], False, self.plots, 2)

    def drawProgBar(self, curTime):
        self.clean()
        self.write(str(curTime))
        curPos = (curTime * 700) / self.length + 50
        pygame.draw.circle(self.screen, [0, 0, 0], [curPos, 151], 5, 0)
        pygame.display.flip()


# length = 149

# pygame.init()
# screen = pygame.display.set_mode([800, 300])
# clean()
# pygame.display.flip()

# music = CLS_Music("C:\\wjy\\music\\Kankitsu - Chronomia.mp3", length)
# music.play()

# while 1:
#     #write(str(pygame.mixer.music.get_pos()))
#     drawProgBar(music.get_position())
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_SPACE:
#                 music.toggle()
#             elif event.key == pygame.K_LEFT:
#                 music.fastBackward()
#                 # if (pos - 10) < 0:
#                 #     music.set_position(0)
#                 #     print(music.get_position())
#                 # else:
#                 #     music.set_position(pos - 10)
#                 #music.play()
#             elif event.key == pygame.K_RIGHT:
#                 music.fastForward()
#                 # if (pos + 10) > length:
#                 #     music.set_position(length)
#                 # else:
#                 #     music.set_position(pos + 10)
#                 #music.play()
    