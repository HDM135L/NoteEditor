import pygame, sys
from jsonIO import CLS_JsonReader, CLS_JsonSaver
from Music import CLS_Music
from Grid import CLS_Grid
from Managers import *

if __name__ == '__main__':
    DM = CLS_DataManager("./Charts/StillAlive")
    CM = DM.chartManagers["Easy"]

    grid = CLS_Grid(CM.chartData)
    grid.clean()

    music = CLS_Music(DM.musicpath)
    music.play()

    offset = DM.metadata["ChartOffset"]
    bpm = DM.metadata["BPM"]
    beats = int((CM.chartData["Length"] - offset) * bpm / 60)

    cur = 0

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    music.toggle()
                # elif event.key == pygame.K_LEFT:
                #     pygame.mixer.music.set_pos(7)
                #     #music.play()
                # elif event.key == pygame.K_RIGHT:
                #     pygame.mixer.music.set_pos(20)
                #     #music.play()
        if cur <= beats and pygame.mixer.music.get_busy() == True:
            grid.paint(
                cur, 
                CM.noteList
                )
            cur += 1
        pygame.time.delay(int((offset + 1 / bpm * 60) * 1000))

                
            
            