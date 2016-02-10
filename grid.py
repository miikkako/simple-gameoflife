import pygame
import guns
from gameoflife import livecolor, screencolor



class Grid(object):

    def __init__(self, ycount, xcount):
        grid = []
        for j in range(ycount):
            row = []
            for i in range(xcount):
                row.append(False)
            grid.append(row)
        self.grid = grid
        self.height = ycount
        self.width = xcount

    def countliveneighbours(self, y, x):
        count = 0

        try:
            if self.grid[y-1][x]: count += 1
        except IndexError:
            pass
        try:
            if self.grid[y-1][x+1]: count += 1
        except IndexError:
            pass
        try:
            if self.grid[y][x+1]: count += 1
        except IndexError:
            pass
        try:
            if self.grid[y+1][x+1]: count += 1
        except IndexError:
            pass
        try:
            if self.grid[y+1][x]: count += 1
        except IndexError:
            pass
        try:
            if self.grid[y+1][x-1]: count += 1
        except IndexError:
            pass
        try:
            if self.grid[y][x-1]: count += 1
        except IndexError:
            pass
        try:
            if self.grid[y-1][x-1]: count += 1
        except IndexError:
            pass

        return count

    def handle(self):

        tobekilled = []
        tobewaken = []
        tosurvive = []
        for j in range(self.height):
            for i in range(self.width): 
                live = self.countliveneighbours(j, i)
                if self.grid[j][i] and (live == 2 or live == 3):
                    tosurvive.append((j, i))
                elif self.grid[j][i] and (live < 2 or live > 3) and (j, i) not in tosurvive:
                    tobekilled.append((j, i))
                elif not self.grid[j][i] and live == 3:
                    tobewaken.append((j, i))

        for coord in tobekilled:
            self.grid[coord[0]][coord[1]] = False
        for coord in tobewaken:
            self.grid[coord[0]][coord[1]] = True

    def draw(self, screen, square, dmy, dmx):
        #draw live squares and grid borders
        for j in range(self.height):
            for i in range(self.width):
                try: 
                    if self.grid[j][i]:
                        pygame.draw.rect(screen, livecolor, (dmx+i*square, dmy+j*square, square, square))
                except IndexError:
                    pass
        pygame.draw.rect(screen, livecolor, (dmx, dmy+self.height*square, self.width*square, square))
        pygame.draw.rect(screen, livecolor, (dmx, dmy-square, self.width*square, square))
        pygame.draw.rect(screen, livecolor, (dmx+self.width*square, dmy, square, self.height*square))
        pygame.draw.rect(screen, livecolor, (dmx-square, dmy, square, self.height*square))


    def makegun(self, y, x, direction):
        if direction == 'southeast': gun = guns.southeastgun
        elif direction == 'northwest': gun = guns.northwestgun

        for j in range(len(gun)):
            for i in range(len(gun[0])):
                if gun[j][i] == 1:
                    try:
                        self.grid[y+j][x+i] = True
                    except IndexError:
                        pass


    def blank(self):

        for j in range(self.height):
            for i in range(self.width):
                self.grid[j][i] = False



    def alterwidth(self, param, alterspeed):
        if param == 'a':
            for a in self.grid:
                for x in range(alterspeed):
                    a.append(False)
            self.width += alterspeed
        elif param == 'b':
            for a in self.grid:
                for x in range(alterspeed):
                    a.pop()
            self.width -= alterspeed



    def alterheight(self, param, alterspeed):
        if param == 'a':
            
            for x in range(alterspeed):
                row = []
                for b in range(self.width):
                    row.append(False)
                self.grid.append(row)
            self.height += alterspeed
        elif param == 'b':
            for x in range(alterspeed):
                self.grid.pop()
            self.height -= alterspeed





























