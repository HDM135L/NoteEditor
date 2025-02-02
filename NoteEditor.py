from posixpath import dirname
from re import I
import pygame, sys
from jsonIO import CLS_JsonReader, CLS_JsonSaver
from Music import CLS_Music
from Grid import CLS_Grid
from Managers import *
import tkinter as tk 
from tkinter.filedialog import *
from TKinterface import *

def onClickButton(button):
    return button[0] <= x <= button[0] + button[2] \
            and button[1] <= y <= button[1] + button[3]

def time2beat(time, bpm):
    return time * bpm / 60

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
    delta = 10
    loc = []
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    music.toggle()
                    ready = not ready
                elif event.key == pygame.K_LEFT and ready:
                    music.fastBackward(1)
                    start = int(time2beat(music.get_position(), DM.metadata["BPM"]))
                elif event.key == pygame.K_RIGHT and ready:
                    music.fastForward(1)
                    start = int(time2beat(music.get_position(), DM.metadata["BPM"]))
                elif event.key == pygame.K_COMMA and ready:
                    music.fastBackward(10)
                    start = int(time2beat(music.get_position(), DM.metadata["BPM"]))
                elif event.key == pygame.K_PERIOD and ready:
                    music.fastForward(10)
                    start = int(time2beat(music.get_position(), DM.metadata["BPM"]))
                elif event.key == pygame.K_r and ready:
                    music.rewind()
                    disAbove = start = 0
                elif event.key ==pygame.K_f and loaded and not music.isPlaying() and not ready and grid.inAmode == False:
                    grid.inFHmode = not grid.inFHmode
                    print(grid.inFHmode)
                    grid.drawButtons()
                elif event.key ==pygame.K_a and loaded and not music.isPlaying() and not ready and grid.inFHmode == False:
                    grid.inAmode = not grid.inAmode
                    grid.drawButtons()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # 1 - left click
                # 2 - middle click
                # 3 - right click
                # 4 - scroll up
                # 5 - scroll down
                if event.button == 1:
                    if onClickButton(grid.buttonLoad):
                        dirname = askdirectory()
                        #dirname = "./Charts/StillAlive"
                        if dirname != '':
                            DM.load(dirname)
                            dname = CLS_ChooseDifficulty(DM)
                            # print(dname.difficulty.get())
                            # dname = "Easy"
                            CM = DM.chartManagers[dname.difficulty.get()]

                            grid.load(CM.noteList)

                            music = CLS_Music(DM.musicpath, CM.chartData["Length"])
                            music.play()

                            offset = DM.metadata["ChartOffset"]
                            bpm = DM.metadata["BPM"]
                            beats = int((CM.chartData["Length"] - offset) * bpm / 60)
                            ready = True
                            loaded = True
                    
                    elif onClickButton(grid.buttonSave) and loaded:
                        music.pause()
                        CM.save_chart()
                        tk.messagebox.showinfo(title = 'muneck', message = 'chart saved!')
                        music.unpause()
                        ready = True

                    elif onClickButton(grid.buttonAdd) and loaded:
                        music.pause()
                        ready = False
                        CLS_AddNote(CM)
                        music.unpause()
                        ready = True

                    elif onClickButton(grid.buttonDel) and loaded:
                        music.pause()
                        ready = False
                        CLS_DelNote(CM)
                        music.unpause()
                        ready = True

                    elif onClickButton(grid.buttonMod) and loaded:
                        music.pause()
                        ready = False
                        CLS_ModNote(CM)
                        music.unpause()
                        ready = True

                    elif onClickButton(grid.buttonAdjustOffset) and loaded:
                        music.pause()
                        ready = False
                        CLS_AdjOffset(CM)
                        music.unpause()
                        ready = True

                    elif onClickButton(grid.buttonFH) and loaded and not music.isPlaying() and not ready and grid.inAmode == False:
                        grid.inFHmode = not grid.inFHmode
                        print(grid.inFHmode)
                        grid.drawButtons()
                        # pygame.display.flip()
                    
                    elif onClickButton(grid.buttonA) and loaded and not music.isPlaying() and not ready and grid.inFHmode == False:
                        grid.inAmode = not grid.inAmode
                        grid.drawButtons()
                        # pygame.display.flip()

                    elif onClickButton(grid.grid) and \
                            loaded and \
                            (grid.inFHmode or grid.inAmode) and \
                            not music.isPlaying() and\
                            not ready:
                        col, row = int(x / grid.side), grid.rowNum - int(((y - disAbove) / grid.side) * 2) / 2 + 0.5
                        #first is row, second is col
                        print(x, y)
                        print(row, col)
                        print(start)
                        loc.append([start + row - 1, col - int((grid.colNum + 1) / 2)])
                        if grid.inFHmode:
                            if len(loc) == 1:
                                noteType = "hold"
                                rail = loc[0][1]
                                startBeat = loc[0][0]
                                touchBeat = loc[0][0]
                                timeLengthBeat = 0
                                print()
                                print(loc)
                                CM.create_note(None, noteType, rail, startBeat, touchBeat, timeLengthBeat)

                            if len(loc) == 2:
                                noteType = "hold"
                                rail = loc[0][1]
                                startBeat = loc[0][0]
                                touchBeat = loc[1][0]
                                timeLengthBeat = 0
                                print()
                                print(loc)
                                index = CM.get_id(noteType, rail, startBeat, loc[0][0], timeLengthBeat)
                                CM.modify_note(index, None, noteType, rail, startBeat, touchBeat, timeLengthBeat)

                            if len(loc) == 3:
                                noteType = "flick" if loc[2][0] == loc[1][0] else "hold"
                                rail = loc[0][1]
                                startBeat = loc[0][0]
                                touchBeat = loc[1][0]
                                timeLengthBeat = loc[2][0] - loc[1][0]
                                print()
                                print(loc)
                                index = CM.get_id("hold", rail, startBeat, touchBeat, 0)
                                CM.modify_note(index, None, noteType, rail, startBeat, touchBeat, timeLengthBeat)
                                loc.clear()
                                grid.inFHmode = False

                            
                        if grid.inAmode:
                            if len(loc) == 1:
                                noteType = "avoid"
                                rail = loc[0][1]
                                startBeat = loc[0][0]
                                touchBeat = loc[0][0]
                                timeLengthBeat = 0
                                print()
                                print(loc)
                                CM.create_note(None, noteType, rail, startBeat, touchBeat, timeLengthBeat)

                            if len(loc) == 2:
                                noteType = "avoid"
                                rail = loc[0][1]
                                startBeat = loc[0][0]
                                touchBeat = loc[1][0]
                                timeLengthBeat = 0
                                print()
                                print(loc)
                                index = CM.get_id(noteType, rail, startBeat, loc[0][0], timeLengthBeat)
                                CM.modify_note(index, None, noteType, rail, startBeat, touchBeat, timeLengthBeat)

                            if len(loc) == 3:
                                noteType = "avoid"
                                rail = loc[0][1]
                                startBeat = loc[0][0]
                                touchBeat = loc[1][0]
                                timeLengthBeat = loc[2][0] - loc[1][0]
                                print()
                                print(loc)
                                index = CM.get_id("avoid", rail, startBeat, touchBeat, 0)
                                CM.modify_note(index, None, noteType, rail, startBeat, touchBeat, timeLengthBeat)
                                loc.clear()
                                grid.inAmode = False
                                
                    elif onClickButton(grid.buttonCopy) and loaded:
                        music.pause()
                        ready = False
                        CLS_CopyNote(CM)
                        music.unpause()
                        ready = True
                
                if loaded:
                    CM.save_chart()

        if  CM and start < CM.chartLength:
            # print(start)
            beatOffset = time2beat(CM.chartOffset, DM.metadata["BPM"])
            grid.paintMovingGrid(CM.noteList, start, disAbove, round(music.get_position(), 2), beatOffset)
            print(music.get_position())
            if ready == True:
                disAbove += delta
                disAbove = disAbove % (grid.side + 1)
                if(disAbove <= delta):
                    # start += 1
                    start = int(time2beat(music.get_position(), DM.metadata["BPM"]))
                
            grid.clock.tick(int(DM.metadata["BPM"] * grid.side / (60 * delta)))