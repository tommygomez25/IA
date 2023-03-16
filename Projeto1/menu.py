import pygame
from settings import *
import pygame_menu

pygame.init()
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def set_difficulty(value, difficulty):
    # Do the job here !
    pass

def start_the_game():
    # Do the job here !
    pass


menu = pygame_menu.Menu('Black-hole Escape!', SCREEN_WIDTH, SCREEN_HEIGHT,
                       theme=pygame_menu.themes.THEME_DARK)

#menu.add.text_input('Name :', default='John Doe')
menu.add.selector('Difficulty :', [('Easy', 1), ('Medium',2) ,('Hard', 3)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)


menu.mainloop(surface)