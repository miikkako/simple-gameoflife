import pygame
from colors import *
from grid import *


clock = pygame.time.Clock()
screen_width = 960
screen_height = 600
separator_height = 100
screencolor = WHITE
livecolor = BLACK


class Message(object):

    def __init__(self, color, text, size, centerx, centery, font='comicsansms'):
        font = pygame.font.SysFont(font, size)
        self.size = size
        self.font = font
        self.color = color
        self.screen_text = font.render(text, True, color)
        self.pos = self.screen_text.get_rect()
        self.centerx = centerx
        self.centery = centery
        self.pos.center = (centerx, centery)

    def show(self, screen):
        screen.blit(self.screen_text, self.pos)

    def changetext(self, text):
        font = pygame.font.SysFont(self.font, self.size)
        self.screen_text = font.render(text, True, self.color)
        self.pos = self.screen_text.get_rect()
        self.pos.center = (self.centerx, self.centery)


def messagetoscreen(screen, color, text, size, centerx, centery):
    font = pygame.font.SysFont(None, size)
    screen_text = font.render(text, True, color)
    pos = screen_text.get_rect()
    pos.center = (centerx, centery)
    screen.blit(screen_text, pos)
    pygame.display.update()



def ismouseinrect(x, y, width, height):
    # x, y = top left corner of the rectangle
    mouse = pygame.mouse.get_pos()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        return True
    else:
        return False


def main():
    """ Program """

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height + separator_height))
    screen.fill(screencolor)

    
    gridheight = 50
    gridwidth = 50
    grid = Grid(gridheight, gridwidth)

    done = False
    loops = 0
    drawmode = False
    y_pos = 1
    x_pos = 1
    square = 10
    gridalteringspeed = 5
    drawposition_x = square
    drawposition_y = square
    textsize = 2 * square

    #define some texts
    stopmessage = Message(BRIGHTYELLOW, 'PAUSED (you can draw)', 3 * textsize, screen_width // 2, screen_height + separator_height//2)
    infomessage = Message(RED, '', textsize, screen_width // 2, screen_height + 2*square)
    texts = (
        Message(BLACK, 'Grid options: P (wider), O (narrower), L (taller), K (lower)  |  Arrowkeys: Move grid', 
            textsize, screen_width // 2, screen_height + 5*square),
        Message(BLACK, 'Game start/stop: D  |  Blank grid: B  |  Make gun: Q, W  |  Particles: - (smaller), + (bigger)', 
            textsize, screen_width // 2, screen_height + 8*square),
    )


    """---------- Loop starts ----------"""

    while not done:

        # if loops % 2 == 0:

        for event in pygame.event.get():
            # print(event)
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                quit()

            # events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PLUS:
                    square += 1
                if event.key == pygame.K_MINUS:
                    square -= 1
                if event.key == pygame.K_RIGHT:
                    drawposition_x += gridalteringspeed * square
                if event.key == pygame.K_LEFT:
                    drawposition_x -= gridalteringspeed * square
                if event.key == pygame.K_UP:
                    drawposition_y -= gridalteringspeed * square
                if event.key == pygame.K_DOWN:
                    drawposition_y += gridalteringspeed * square
                if event.key == pygame.K_d:
                    drawmode = not drawmode
                if event.key == pygame.K_b:
                    grid.blank()
                
                if event.key == pygame.K_p: # and drawposition_y + grid.width * square < screen_width - square:
                    grid.alterwidth('a', gridalteringspeed)
                if event.key == pygame.K_o: # and grid.width > 5:
                    grid.alterwidth('b', gridalteringspeed)
                if event.key == pygame.K_l: # and drawposition_x + grid.height * square < screen_height - square:
                    grid.alterheight('a', gridalteringspeed)
                if event.key == pygame.K_k: # and grid.height > 5:
                    grid.alterheight('b', gridalteringspeed)
                if event.key == pygame.K_q:
                    grid.makegun(mouse[1] // square - drawposition_y // square, mouse[0] // square - drawposition_x // square, 'southeast')
                if event.key == pygame.K_w:
                    grid.makegun(mouse[1] // square - drawposition_y // square, mouse[0] // square - drawposition_x // square, 'northwest')

            if event.type == pygame.MOUSEBUTTONDOWN:
                # turn clicked square live
                try:
                    grid.grid[mouse[1]//square-drawposition_y//square][mouse[0]//square-drawposition_x//square] = \
                        not grid.grid[mouse[1]//square-drawposition_y//square][mouse[0]//square-drawposition_x//square]
                except IndexError:
                    pass

        #clear screen
        screen.fill(screencolor)        

        # draw grid and its squares
        grid.draw(screen, square, drawposition_y, drawposition_x)

        # draw separator
        pygame.draw.rect(screen, GREY, (0, screen_height, screen_width, screen_height - separator_height))

        # basic screen messages:
        infotext = 'Grid height: ' + str(grid.height) + '  |  width: ' + str(grid.width) + '  |  square size: ' + str(square) + \
        '  |  Grid position (x, y): ' + str(drawposition_x // square) + ', ' + str(drawposition_y // square)
        infomessage = Message(infomessage.color, infotext, infomessage.size, infomessage.centerx, infomessage.centery)
        infomessage.show(screen)
        for text in texts:
            text.show(screen)

        # game mode
        if not drawmode:
            grid.handle()
        else:
            stopmessage.show(screen)

        
        
        # finally show everything that has been drawn
        pygame.display.update()


        # if loops > 100000:
        #     loops = 0
        # loops += 1

    """---------- Loop ends ----------"""



if __name__ == "__main__":
    count = 0
    while count < 100:
        main()
        count += 1
    pygame.quit()
    quit()


