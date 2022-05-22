import pygame

def sortKey(dict):
    return dict["StartTime"]

class CLS_Grid(object):
    def __init__(self, content):
        self.content = content
        self.content["NoteList"].sort(key = sortKey)
        pygame.init()
        self.screen = pygame.display.set_mode([770, 950])
        self.screen.fill([255, 255, 255])
        self.side = 110 #self.side length of a square

    def drawTimeNum(self, start):
        font = pygame.font.Font(None, 50)
        for i in range(start, start + 8):
            surf = font.render(str(i), 1, [0, 0, 0])
            self.screen.blit(surf, [self.side * 6 + 10, self.side * (start + 8 - i) - 15])

    def clean(self):
        self.screen.fill([255, 255, 255])
        for x in range(1, 6):
            for y in range(1, 8):
                square = [x*self.side, y*self.side, self.side, self.side]
                pygame.draw.rect(self.screen, [0, 0, 0], square, 2)

        #draw a big rect to make the line width outside the same
        pygame.draw.rect(
            self.screen, 
            [0, 0, 0],
            [self.side, self.side, self.side * 5, self.side * 7], 
            4
            )

    def draw(self):
        for dict in self.content["NoteList"]:
            self.drawImpl(
                dict["Type"], 
                dict["Rail"], 
                int(dict["StartTime"]) - int(dict["DelayTime"]), 
                int(dict["StartTime"]), 
                int(dict["Length"]) + int(dict["StartTime"])
                )
        pygame.display.flip()


    def paint(self, start, notes):
        self.clean()
        self.drawTimeNum(start)
        for dict in notes:
            if int(dict["StartTime"]) >= start or \
                (int(dict["Length"]) + int(dict["StartTime"])) <= start + 7 or \
                (int(dict["StartTime"]) < start and int(dict["Length"]) > 7):
                self.drawImpl(
                    dict["Type"], 
                    dict["Rail"], 
                    int(dict["StartTime"]) - int(dict["DelayTime"]) - start, 
                    int(dict["StartTime"]) - start, 
                    int(dict["Length"]) + int(dict["StartTime"]) - start
                    )
        pygame.display.flip()

    # "Type" = noteType
    # "Rail" = lane
    # int("StartTime") - int("DelayTime") = appearTime 
    # int("StartTime") = touchLineTime
    # int("Length") + int("StartTime") = allThroughLineTime
    def drawImpl(self, noteType, lane, appearTime, touchLineTime, allThroughLineTime): 
        color = {'flick' : [237, 28, 36], 'hold' : [255, 174, 201], 'avoid' : [181, 230, 29]}
        length = {
            'flick' : 10, 
            'hold' : (allThroughLineTime - touchLineTime) * self.side, 
            'avoid' : (allThroughLineTime - touchLineTime) * self.side
            }
        adj ={'flick' : -5, 'hold' : 0, 'avoid' : 0}
        pygame.draw.rect(
            self.screen, 
            color[noteType], 
            [
                (lane + 3) * self.side, 
                (8 - allThroughLineTime) * self.side + adj[noteType], 
                self.side, 
                length[noteType]
            ], 
            0
            )
        pygame.draw.rect(
            self.screen, 
            [195, 195, 195], 
            [
                (lane + 3) * self.side + 0.5 * self.side - 5, 
                (8 - touchLineTime) * self.side - adj[noteType], 
                10, 
                (touchLineTime - appearTime) * self.side + adj[noteType]
            ], 
            0
            )
        pygame.draw.rect(
            self.screen, 
            [195, 195, 195], 
            [
                (lane + 3) * self.side + 10, 
                (8 - appearTime) * self.side - 6, 
                self.side - 20, 
                6
            ], 
            0
            )
