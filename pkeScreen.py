import os, sys
import math, time
import logging
import traceback
import pygame
from pygame.locals import *

#Screen size in pixels
screen_width = 320
screen_height = 240

#Crosshair Position
crosshair_pos = (200, 100)

#Functions to create resources
class Crosshair(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.position = position

    def update(self):
        pos = pygame.mouse.get_pos()
        #pos = crosshair_pos
        self.rect = self.image.get_rect()
        self.rect.center = pos

class BorderX(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.position = position

    def update(self):
        pos = pygame.mouse.get_pos()
        #pos = crosshair_pos
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.rect.top = 0

class BorderY(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.position = position

    def update(self):
        pos = pygame.mouse.get_pos()
        #pos = crosshair_pos
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.rect.left = 0

def main():
#Setup Logger
    logging.basicConfig(filename='debug.log',level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    try:
#Initialize PyGame
        pygame.init()
       # screen = pygame.display.set_mode((screen_width, screen_height))
        screen = pygame.display.set_mode((0,0))
        pygame.display.set_caption('PKE Screen')
        pygame.mouse.set_visible(0)
        font = pygame.font.SysFont('Lucida Console', 12, bold=False)

        pygame.mixer.music.load('PKE_Loop.wav')
        pygame.mixer.music.play(-1) #Plays loop forever

#Create Background
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((230, 230, 200))

#Display Background
        screen.blit(background, (0, 0))
        pygame.display.flip()

#Prepare Game Objects
        rect = screen.get_rect()
        lines = Crosshair('lines.png', rect.center)
        borderx = BorderX('borderx.png', rect.center)
        bordery = BorderY('bordery.png', rect.center)
        allsprites = pygame.sprite.RenderPlain(lines, borderx, bordery)

        #Sine Wave Parameters
        frequency = 5
        amplitude = 20 #In pixels
        speed = 3
        sin_offset = 70

#Main Loop
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    return
                elif event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    return

            #Update Sprites
            allsprites.update()

            #Calculate and Print Crosshair Coordinates (0,0 = middle of screen)
            #mouse_pos = pygame.mouse.get_pos()
            mouse_pos = crosshair_pos
            coordx = int(mouse_pos[0] - screen_width/2)
            coordy = int(screen_height - mouse_pos[1])
            coord_text = font.render('Position: (' + str(coordx) + ', ' + str(coordy) + ')', 1, (0, 0, 0))

            #Ghost Details
            class_text = font.render('Class: Unknown', 1, (0, 0, 0))

            #Set Background Color (must be done before drawing the sine wave)
            background.fill((230, 230, 200))

        #Calculate and Print Sine Wave
            for x in range(0, screen_width):
                y = int((screen_height/2) + amplitude * math.sin(frequency *((float(x)/320) * (2 * math.pi) + (speed*time.time())))) + sin_offset
                background.set_at((x, y), (0, 0, 0))

            #Draw Everything
            screen.blit(background, (0, 0))
            screen.blit(coord_text, (10, 5))
            screen.blit(class_text, (10, 20))
            allsprites.draw(screen)

            pygame.display.flip()

    except Exception as error:
        logger.exception(error)

#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
