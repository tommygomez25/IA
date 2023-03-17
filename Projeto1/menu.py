import pygame
from settings import *
import pygame_menu

pygame.init()
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame_menu.font.FONT_FIRACODE_BOLD
mytheme = pygame_menu.themes.THEME_DARK.copy()


mytheme.background_color=BACKGROUND_COLOR
mytheme.cursor_color=(255,255,0)


mytheme.title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE
mytheme.title_offset=(40,20)
mytheme.title_font=font
mytheme.title_font_color=(0,0,0)
#mytheme.title_shadow=False
#mytheme.title_background_color=(255,255,0)


mytheme.widget_font_color=BLUE_PIECE_COLOR
mytheme.widget_font=font
mytheme.selection_color=RED_PIECE_COLOR

def set_difficulty(value, difficulty):
    
    pass

def start_the_game():
    play_menu()

def start_the_game():
    play_menu()

def start_menu():

    menu = pygame_menu.Menu('Black-hole Escape!', SCREEN_WIDTH, SCREEN_HEIGHT,
                       theme=mytheme)

    #menu.add.text_input('Name :', default='John Doe')
    menu.add.selector("Difficulty :", [('Easy', 1), ('Medium',2) ,('Hard', 3)], onchange=set_difficulty)
    menu.add.button('Play', start_the_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(surface)
    return

def play_menu():

    menu = pygame_menu.Menu('Black-hole Escape!', SCREEN_WIDTH, SCREEN_HEIGHT, theme=mytheme)

    #menu.add.text_input('Name :', default='John Doe')
    menu.add.selector('Difficulty :', [('Easy', 1), ('Medium',2) ,('Hard', 3)], onchange=set_difficulty)
    menu.add.button('Play', start_the_game)
    menu.add.button('Play', start_the_game)
    menu.add.button('Play', start_the_game)
    menu.add.button('Play', start_the_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    
    menu.mainloop(surface)
    return

start_menu()