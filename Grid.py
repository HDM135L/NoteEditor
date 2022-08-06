import pygame

def sortKey(note):
    return note.touchBeat

class CLS_Grid(object):
    def __init__(self):
        self.side = 110 #self.side length of a square
        self.rowNum = 7 #number of rows in a page
        self.colNum = 5 #number of columns in a page
        pygame.init()
        self.screen = pygame.display.set_mode([self.side * (self.colNum + 9), self.side * (self.rowNum + 2)])
        self.screen.fill([255, 255, 255])
        self.clock = pygame.time.Clock()
        self.buttonLoad = [self.side * (self.colNum + 2), self.side, self.side * 2, self.side]
        self.buttonSave = [self.side * (self.colNum + 2), self.side * 4, self.side * 2, self.side]
        self.buttonAdd = [self.side * (self.colNum + 5), self.side, self.side * 2, self.side]
        self.buttonDel = [self.side * (self.colNum + 5), self.side * 4, self.side * 2, self.side]
        self.buttonMod = [self.side * (self.colNum + 5), self.side * 7, self.side * 2, self.side]
        self.buttonAdjustOffset = [self.side * (self.colNum + 2), self.side * 7, self.side * 2, self.side]
        self.buttonFH = [self.side * (self.colNum + 2), self.side * 2.5, self.side + 10, self.side]
        self.buttonA = [self.side * (self.colNum + 3.5) + 10, self.side * 2.5, self.side, self.side]
        self.buttonCopy = [self.side * (self.colNum + 2), self.side * 5.5, self.side * 2, self.side]
        self.font1 = pygame.font.Font(None, self.side * 5 // 11)
        self.font2 = pygame.font.Font(None, self.side * 10 // 11)
        self.inFHmode = False
        self.inAmode = False
        self.grid = [self.side, self.side, self.side * self.colNum, self.side * self.rowNum]
        self.lineColor = {0 : [0, 0, 0], 1 : [41, 50, 225], 2 : [0, 0, 0], 3 : [41, 50, 225]}
        self.lineWidth = {0 : 10, 1 : 2, 2 : 5, 3 : 2}
        self.copyright = "note editor made by Jerry Wen"
        

    def load(self, content):
        self.content = content
        self.content.sort(key = sortKey)

    def drawBeatNum(self, start, disAbove, now):
        for i in range(start, start + self.rowNum):
            s = str(i / 4 + 1)
            surf = self.font1.render(s, 1, [0, 0, 0])
            self.screen.blit(
                surf, 
                [
                    self.side * (self.colNum + 1) + 10, 
                    self.side * (start + self.rowNum - i) - 15 + disAbove
                ]
            )
        cur = round((start + disAbove / 110), 2)
        surf1 = self.font1.render(str(cur) + "beats", 1, [0, 237, 232])
        self.screen.blit(surf1, [self.side * (self.colNum + 1) + 60, self.side * self.rowNum - 20])
        surf2 = self.font1.render(str(now) + "s", 1, [0, 237, 232])
        self.screen.blit(surf2, [self.side * (self.colNum + 1) + 60, self.side * self.rowNum + 20])
        
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
        #f/h, meaning flick or hold
        pygame.draw.rect(
            self.screen, 
            [204, 204, 204] if self.inFHmode else [255, 174, 201],
            self.buttonFH, 
            0
        )
        #a, meaning avoid
        pygame.draw.rect(
            self.screen, 
            [204, 204, 204] if self.inAmode else [181, 230, 29],
            self.buttonA, 
            0
        )
        #copy
        pygame.draw.rect(
            self.screen, 
            [237, 125, 49],
            self.buttonCopy, 
            0
        )
        adj = self.side * 4 / 11
        self.write(self.font2, "load", [0, 0, 0], [self.buttonLoad[0] + adj, self.buttonLoad[1] + adj * 0.5])
        self.write(self.font2,"save", [0, 0, 0], [self.buttonSave[0] + adj, self.buttonSave[1] + adj * 0.5])
        self.write(self.font2,"add", [0, 0, 0], [self.buttonAdd[0] + adj * 1.125, self.buttonAdd[1] + adj * 0.5])
        self.write(self.font2,"del", [0, 0, 0], [self.buttonDel[0] + adj * 1.125, self.buttonDel[1] + adj * 0.5])
        self.write(self.font2,"mod", [0, 0, 0], [self.buttonMod[0] + adj * 1.125, self.buttonMod[1] + adj * 0.5])
        self.write(self.font1,"adjust offset", [0, 0, 0], [self.buttonAdjustOffset[0] + adj * 0.25, self.buttonAdjustOffset[1] + adj])
        self.write(self.font2,"F/H", [0, 0, 0], [self.buttonFH[0] + adj * 0.125, self.buttonFH[1] + adj * 0.5])
        self.write(self.font2,"A", [0, 0, 0], [self.buttonA[0] + adj * 0.75, self.buttonA[1] +  adj * 0.5])   
        self.write(self.font2, "copy", [0, 0, 0], [self.buttonCopy[0] + adj, self.buttonCopy[1] + adj * 0.5]) 
        self.write(self.font1, self.copyright, [0, 0, 0], [self.side * (self.colNum + 3), self.side * 8.5])

    def drawBlankSpace(self):
        pygame.draw.rect(
            self.screen, 
            [255, 255, 255],
            [0, 0, self.side * (self.colNum + 2), self.side], 
            0
            )
        pygame.draw.rect(
            self.screen, 
            [255, 255, 255],
            [0, self.side * (self.rowNum + 1), self.side * (self.colNum + 2), self.side], 
            0
            )
        pygame.draw.line(
            self.screen, 
            [0, 237, 232], 
            [self.side - 30, self.side * self.rowNum - 5], 
            [self.side * (self.colNum + 1) + 30, self.side * self.rowNum - 5],
            7
            )
        
    def drawGrid(self, start, disAbove):
        for x in range(1, self.colNum + 1):
            for y in range(0, self.rowNum + 1):
                square = [x*self.side, y*self.side + disAbove, self.side, self.side]
                pygame.draw.rect(self.screen, [0, 0, 0], square, 2)

        for i in range(1, self.rowNum * 2 + 2, 2):
            pygame.draw.line(
                self.screen, 
                [0, 0, 0], 
                [self.side, i * self.side / 2 + disAbove],
                [self.side * (self.colNum + 1), i * self.side / 2 + disAbove]
                )

        for i in range(start, start + self.rowNum):
            pygame.draw.line(
                self.screen,
                self.lineColor[i % 4],
                [
                    self.side, 
                    self.side * (start + self.rowNum - i) + disAbove
                ],
                [
                    self.side * (self.colNum + 1), 
                    self.side * (start + self.rowNum - i) + disAbove
                ],
                self.lineWidth[i % 4]
            )

        #draw a big rect to make the line width outside the same
        pygame.draw.rect(
            self.screen, 
            [0, 0, 0],
            [self.side, disAbove, self.side * self.colNum, self.side * (self.rowNum + 1)], 
            4
            )

    def paintMovingGrid(self, notes, start, disAbove, now, offset):
        self.clean()
        self.drawGrid(start, disAbove)
        self.drawBeatNum(start, disAbove, now)
        self.paint(start, notes, disAbove, offset)
        self.drawBlankSpace()
        pygame.display.flip()
            

    def paint(self, start, notes, disAbove, offset):
        for i in range(len(notes)):
            if int(notes[i].touchBeat) >= start or \
                (int(notes[i].timeLengthBeat) + int(notes[i].touchBeat)) <= (start + self.colNum + 1) or \
                (int(notes[i].touchBeat) < start and int(notes[i].timeLengthBeat) > (self.colNum + 1)):
                self.drawImpl(
                    notes[i].type, 
                    notes[i].rail, 
                    round(notes[i].spawnBeat, 2) - start, 
                    round(notes[i].touchBeat, 2)- start, 
                    round((notes[i].timeLengthBeat + notes[i].touchBeat), 2) - start,
                    disAbove - int(offset * self.side),
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
            'flick' : self.side / 11, 
            'hold' : (allThroughLineTime - touchLineTime) * self.side, 
            'avoid' : (allThroughLineTime - touchLineTime) * self.side
            }
        noteLocAdj ={'flick' : - self.side / 11, 'hold' : 0, 'avoid' : 0}
        numLocAdj = {
            'flick' : [self.side / 22, - self.side * 7 / 22], 
            'hold' : [self.side / 11, self.side / 11], 
            'avoid' : [self.side / 11, self.side / 11]
            }
        #->  []
        #    |
        #   --
        pygame.draw.rect(
            self.screen, 
            color[noteType], 
            [
                (lane + int((self.colNum + 1) / 2)) * self.side, 
                (self.rowNum - allThroughLineTime) * self.side + noteLocAdj[noteType] + disAbove, 
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
                (lane + int((self.colNum + 1) / 2)) * self.side + 0.5 * self.side - 5, 
                (self.rowNum - touchLineTime) * self.side + noteLocAdj[noteType] + disAbove, 
                self.side / 11, 
                (touchLineTime - appearTime) * self.side - noteLocAdj[noteType]
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
                (lane + int((self.colNum + 1) / 2)) * self.side + 10, 
                (self.rowNum - appearTime) * self.side - 6 + disAbove, 
                self.side - 20, 
                self.side * 3 / 55
            ], 
            0
            )
        #the serial number of the notes, the "id"
        self.write(
            self.font1, 
            str(num), 
            [193, 126, 39], 
            [
                (lane + int((self.colNum + 1) / 2)) * self.side + numLocAdj[noteType][0], 
                (self.rowNum - allThroughLineTime) * self.side + numLocAdj[noteType][1] + disAbove
            ]
            )
