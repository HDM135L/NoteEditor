import pygame

def sortKey(note):
    return note.touchBeat

class CLS_Grid(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([1540, 990])
        self.screen.fill([255, 255, 255])
        self.side = 110 #self.side length of a square
        self.clock = pygame.time.Clock()
        self.buttonLoad = [self.side * 7, self.side, self.side * 2, self.side]
        self.buttonSave = [self.side * 7, self.side * 4, self.side * 2, self.side]
        self.buttonAdd = [self.side * 10, self.side, self.side * 2, self.side]
        self.buttonDel = [self.side * 10, self.side * 4, self.side * 2, self.side]
        self.buttonMod = [self.side * 10, self.side * 7, self.side * 2, self.side]
        self.buttonAdjustOffset = [self.side * 7, self.side * 7, self.side * 2, self.side]
        self.font1 = pygame.font.Font(None, 50)
        self.font2 = pygame.font.Font(None, 100)

    def load(self, content):
        self.content = content
        self.content.sort(key = sortKey)

    def drawBeatNum(self, start, disAbove, now):
        for i in range(start, start + 7):
            s = str(i / 4 + 1)
            surf = self.font1.render(s, 1, [0, 0, 0])
            self.screen.blit(
                surf, 
                [
                    self.side * 6 + 10, 
                    self.side * (start + 7 - i) - 15 + disAbove
                ]
            )
        cur = round((start + 1 + disAbove / 110), 2)
        surf1 = self.font1.render(str(cur) + "beats", 1, [0, 237, 232])
        self.screen.blit(surf1, [self.side * 6 + 60, self.side * 7 - 20])
        surf2 = self.font1.render(str(now) + "s", 1, [0, 237, 232])
        self.screen.blit(surf2, [self.side * 6 + 60, self.side * 7 + 20])
        
    def write(self, font, content, color, pos):
        surf = font.render(content, 1, color)
        self.screen.blit(surf, pos)

    def clean(self):
        self.screen.fill([255, 255, 255])
        self.drawButtons()

    def drawButtons(self):
        #load
        pygame.draw.rect(
            self.screen, 
            [237, 125, 49],
            self.buttonLoad, 
            0
        )
        #save
        pygame.draw.rect(
            self.screen, 
            [237, 125, 49],
            self.buttonSave, 
            0
        )
        #add
        pygame.draw.rect(
            self.screen, 
            [237, 125, 49],
            self.buttonAdd, 
            0
        )
        #delete
        pygame.draw.rect(
            self.screen, 
            [237, 125, 49],
            self.buttonDel, 
            0
        )
        #modify
        pygame.draw.rect(
            self.screen, 
            [237, 125, 49],
            self.buttonMod, 
            0
        )      
        #change offset
        pygame.draw.rect(
            self.screen, 
            [237, 125, 49],
            self.buttonAdjustOffset, 
            0
        )  
        self.write(self.font2, "load", [0, 0, 0], [self.buttonLoad[0] + 40, self.buttonLoad[1] + 20])
        self.write(self.font2,"save", [0, 0, 0], [self.buttonSave[0] + 40, self.buttonSave[1] + 20])
        self.write(self.font2,"add", [0, 0, 0], [self.buttonAdd[0] + 45, self.buttonAdd[1] + 20])
        self.write(self.font2,"del", [0, 0, 0], [self.buttonDel[0] + 45, self.buttonDel[1] + 20])
        self.write(self.font2,"mod", [0, 0, 0], [self.buttonMod[0] + 45, self.buttonMod[1] + 20])
        self.write(self.font1,"adjust offset", [0, 0, 0], [self.buttonAdjustOffset[0] + 10, self.buttonAdjustOffset[1] + 40])      

    def drawBlankSpace(self):
        pygame.draw.rect(
            self.screen, 
            [255, 255, 255],
            [0, 0, self.side * 7, self.side], 
            0
            )
        pygame.draw.rect(
            self.screen, 
            [255, 255, 255],
            [0, self.side * 8, self.side * 7, self.side], 
            0
            )
        pygame.draw.line(
            self.screen, 
            [0, 237, 232], 
            [self.side - 30, self.side * 7 - 5], 
            [self.side * 6 + 30, self.side * 7 - 5],
            7
            )
        
    def drawGrid(self, disAbove):
        for x in range(1, 6):
            for y in range(0, 8):
                square = [x*self.side, y*self.side + disAbove, self.side, self.side]
                pygame.draw.rect(self.screen, [0, 0, 0], square, 2)

        #draw a big rect to make the line width outside the same
        pygame.draw.rect(
            self.screen, 
            [0, 0, 0],
            [self.side, disAbove, self.side * 5, self.side * 8], 
            4
            )

    def paintMovingGrid(self, notes, start, disAbove, now, offset):
        self.clean()
        self.drawGrid(disAbove)
        self.drawBeatNum(start, disAbove, now)
        self.paint(start, notes, disAbove, offset)
        self.drawBlankSpace()
        pygame.display.flip()
            

    def paint(self, start, notes, disAbove, offset):
        for i in range(len(notes)):
            if int(notes[i].touchBeat) >= start or \
                (int(notes[i].timeLengthBeat) + int(notes[i].touchBeat)) <= start + 6 or \
                (int(notes[i].touchBeat) < start and int(notes[i].timeLengthBeat) > 6):
                self.drawImpl(
                    notes[i].type, 
                    notes[i].rail, 
                    round(notes[i].spawnBeat, 2) - start, 
                    round(notes[i].touchBeat, 2)- start, 
                    round((notes[i].timeLengthBeat + notes[i].touchBeat), 2) - start,
                    disAbove - offset * self.side,
                    i + 1
                    )

    # "Type" = noteType
    # "Rail" = lane
    # int("StartTime") - int("DelayTime") = appearTime 
    # int("StartTime") = touchLineTime
    # int("Length") + int("StartTime") = allThroughLineTime
    def drawImpl(self, noteType, lane, appearTime, touchLineTime, allThroughLineTime, disAbove, num): 
        color = {'flick' : [237, 28, 36], 'hold' : [255, 174, 201], 'avoid' : [181, 230, 29]}
        length = {
            'flick' : 10, 
            'hold' : (allThroughLineTime - touchLineTime) * self.side, 
            'avoid' : (allThroughLineTime - touchLineTime) * self.side
            }
        noteLocAdj ={'flick' : 0, 'hold' : 0, 'avoid' : 0}
        numLocAdj = {
            'flick' : [5, -35], 
            'hold' : [10, 10], 
            'avoid' : [10, 10]
            }
        #->  []
        #    |
        #   --
        pygame.draw.rect(
            self.screen, 
            color[noteType], 
            [
                (lane + 3) * self.side, 
                (7 - allThroughLineTime) * self.side + noteLocAdj[noteType] + disAbove, 
                self.side, 
                length[noteType]
            ], 
            0
            )
        #    []
        #->  |
        #   --
        pygame.draw.rect(
            self.screen, 
            [195, 195, 195], 
            [
                (lane + 3) * self.side + 0.5 * self.side - 5, 
                (7 - touchLineTime) * self.side - noteLocAdj[noteType] + disAbove, 
                10, 
                (touchLineTime - appearTime) * self.side + noteLocAdj[noteType]
            ], 
            0
            )
        #    []
        #    |
        #-> --
        pygame.draw.rect(
            self.screen, 
            [195, 195, 195], 
            [
                (lane + 3) * self.side + 10, 
                (7 - appearTime) * self.side - 6 + disAbove, 
                self.side - 20, 
                6
            ], 
            0
            )
        #the serial number of the notes, the "id"
        self.write(
            self.font1, 
            str(num), 
            [193, 126, 39], 
            [
                (lane + 3) * self.side + numLocAdj[noteType][0], 
                (7 - allThroughLineTime) * self.side + numLocAdj[noteType][1] + disAbove
            ]
            )
