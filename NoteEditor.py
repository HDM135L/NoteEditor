from posixpath import dirname
import pygame, sys
from jsonIO import CLS_JsonReader, CLS_JsonSaver
from Music import CLS_Music
from Grid import CLS_Grid
from Managers import *
import tkinter as tk 
from tkinter.filedialog import *
from TKinterface import CLS_AddNote, CLS_DelNote, CLS_ModNote

def onClickButton(button):
    return button[0] <= x <= button[0] + button[2] \
            and button[1] <= y <= button[1] + button[3]

def time2beat(time, offset, bpm):
    return (time - offset) * bpm / 60

CM = None

if __name__ == '__main__':
    ready = False
    loaded = False

    DM = CLS_DataManager()

    grid = CLS_Grid()
    grid.__init__()
    grid.clean()
    pygame.display.flip()

    cur = 0
    start = 0
    disAbove = 0
    delta = 1
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    music.toggle()
                    ready = not ready
                elif event.key == pygame.K_LEFT and ready:
                    music.fastBackward()
                    start = int(time2beat(int(music.get_position()), DM.metadata["ChartOffset"], DM.metadata["BPM"]))
                elif event.key == pygame.K_RIGHT and ready:
                    music.fastForward()
                    start = int(time2beat(int(music.get_position()), DM.metadata["ChartOffset"], DM.metadata["BPM"]))
                elif event.key == pygame.K_r and ready:
                    music.rewind()
                    disAbove = start = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if onClickButton(grid.buttonLoad):
                    dirname = askdirectory()
                    #dirname = "./Charts/StillAlive"
                    try:
                        DM.load(dirname)
                        CM = DM.chartManagers["Easy"]

                        grid.load(CM.noteList)

                        music = CLS_Music(DM.musicpath, CM.chartData["Length"])
                        music.play()

                        offset = DM.metadata["ChartOffset"]
                        bpm = DM.metadata["BPM"]
                        beats = int((CM.chartData["Length"] - offset) * bpm / 60)
                        ready = True
                        loaded = True
                    except:
                        pass
                    
                elif onClickButton(grid.buttonSave) and loaded:
                    music.stop()
                    CM.save_chart()
                    tk.messagebox.showinfo(title = 'muneck', message = 'chart saved!')
                    music.rewind()
                    disAbove = start = 0

                elif onClickButton(grid.buttonAdd) and loaded:
                    music.stop()
                    ready = False
                    CLS_AddNote(CM)
                    music.rewind()
                    disAbove = start = 0
                    ready = True
                elif onClickButton(grid.buttonDel) and loaded:
                    music.stop()
                    ready = False
                    CLS_DelNote(CM)
                    music.rewind()
                    disAbove = start = 0
                    ready = True
                elif onClickButton(grid.buttonMod) and loaded:
                    music.stop()
                    ready = False
                    CLS_ModNote(CM)
                    music.rewind()
                    disAbove = start = 0
                    ready = True
        if ready == True:
            grid.paintMovingGrid(CM.noteList, bpm, start, disAbove)
            disAbove += delta
            disAbove = disAbove % (grid.side + 1)
            if(disAbove == 0 and start + 1 <= CM.chartLength):
                start += 1
            grid.clock.tick(bpm)


                
            
            