import pygame, sys
from jsonIO import CLS_JsonReader, CLS_JsonSaver
from Music import CLS_Music
from Grid import CLS_Grid

#bound = "l" or "r"
def binarySearch(list, target, bound):
    left = 0
    right = len(list)
    while(left < right):
        mid = int(left + (right - left) / 2)
        if list[mid] < target:
            left = mid + 1
        elif list[mid] > target:
            right = mid
        else:
            if bound == "l":
                right = mid
            else:
                left = mid + 1
    if bound == "l":
        return left
    else: 
        return left - 1


if __name__ == '__main__':
    metapath = "C:\wjy\code\PYTHON\MUNECK_editor\chart5.json"
    loader = CLS_JsonReader(metapath)
    content = loader.get_content()

    grid = CLS_Grid(content)
    grid.clean()

    music = CLS_Music("C:\wjy\music\Kankitsu - Chronomia.mp3")
    music.play()

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
        grid.paint(int(pygame.mixer.music.get_pos() / 1000), content["NoteList"])
        pygame.time.delay(1000)

                
            
            