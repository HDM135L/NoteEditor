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

CM = None

if __name__ == '__main__':
    ready = False

    DM = CLS_DataManager()

    grid = CLS_Grid()
    grid.__init__()
    grid.clean()
    # grid.drawButtons()
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
                elif event.key == pygame.K_LEFT:
                    music.fastBackward()
                    start = int(music.get_position())
                elif event.key == pygame.K_RIGHT:
                    music.fastForward()
                    start = int(music.get_position())
                elif event.key == pygame.K_r:
                    music.rewind()
                    disAbove = start = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if onClickButton(grid.buttonLoad):
                    dirname = askdirectory()
                    #dirname = "./Charts/StillAlive"
                    DM.load(dirname)
                    CM = DM.chartManagers["Easy"]

                    grid.load(CM.chartData)

                    music = CLS_Music(DM.musicpath, CM.chartData["Length"])
                    music.play()

                    offset = DM.metadata["ChartOffset"]
                    bpm = DM.metadata["BPM"]
                    beats = int((CM.chartData["Length"] - offset) * bpm / 60)
                    ready = True
                    
                elif onClickButton(grid.buttonSave):
                    music.stop()
                    # filename = asksaveasfilename(defaultextension='.json')
                    CM.save_chart()
                    tk.messagebox.showinfo(title = 'muneck', message = 'chart saved!')
                    music.rewind()
                    disAbove = start = 0

                elif onClickButton(grid.buttonAdd):
                    music.stop()
                    CLS_AddNote(CM)
                    music.rewind()
                    disAbove = start = 0
                elif onClickButton(grid.buttonDel):
                    music.stop()
                    CLS_DelNote(CM)
                    music.rewind()
                    disAbove = start = 0
                elif onClickButton(grid.buttonMod):
                    music.stop()
                    CLS_ModNote(CM)
                    music.rewind()
                    disAbove = start = 0
        if ready == True:
            grid.paintMovingGrid(CM.noteList, bpm, start, disAbove)
            disAbove += delta
            disAbove = disAbove % (grid.side + 1)
            if(disAbove == 0 and start + 1 <= CM.chartData["Length"]):
                start += 1
            grid.clock.tick(bpm)
            if 0 < grid.clock.get_fps() < bpm:
                delta = round(bpm / grid.clock.get_fps())


                
            
            