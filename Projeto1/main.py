import pygame
from settings import *
import game
from state import State
import ai
import pygame_menu
from copy import deepcopy
import time

player1 = ai.execute_human_move
player2 = ai.execute_human_move

def set_player(value, p):
    global player1, player2
    if p == 2:
        player2 = value
    else:
        player1 = value
    return


def start_game():
    global player1, player2
    if player1 == "Computer":
        player1 = ai.execute_monte_carlo_move()
    if player2 == "Computer":
        player2 = ai.execute_monte_carlo_move()

    new_game = game.Game(State(), player1, player2)
    winner = new_game.loop()
    display_winner(winner)


def create_theme():

    mytheme = pygame_menu.themes.THEME_DARK.copy()
    font = pygame_menu.font.FONT_FIRACODE_BOLD

    mytheme.background_color = BACKGROUND_COLOR
    mytheme.cursor_color = (255, 255, 0)

    mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    mytheme.title_offset = (150, 20)
    mytheme.title_font = font
    mytheme.title_font_size = 50
    mytheme.title_font_color = (0, 0, 0)
    # mytheme.title_shadow=False
    # mytheme.title_background_color=(255,255,0)

    mytheme.widget_font_size = 32
    mytheme.widget_selection_effect = pygame_menu.widgets.HighlightSelection(
        border_width=5, margin_x=0, margin_y=0
    )
    mytheme.widget_background_color = WHITE
    mytheme.widget_font_color = BLUE_PIECE_COLOR
    mytheme.widget_font = font
    mytheme.widget_padding = 30
    mytheme.widget_margin = (10, 10)
    mytheme.selection_color = RED_PIECE_COLOR

    return mytheme


def start_menu():

    menu = pygame_menu.Menu(
        "Black-hole Escape!", SCREEN_WIDTH, SCREEN_HEIGHT, theme=create_theme()
    )
    menu.add.button("Play", player_menu)
    menu.add.button("Rules", rules)
    menu.add.button("Quit", pygame_menu.events.EXIT)

    menu.mainloop(surface)
    return


def player_menu():
    global player1, player2
    player1 = ai.execute_human_move
    player2 = ai.execute_human_move
    players = [("Human", ai.execute_human_move), ("Computer", "Computer")]
    menu = pygame_menu.Menu(
        "Select Players", SCREEN_WIDTH, SCREEN_HEIGHT, theme=create_theme()
    )
    menu.add.button("Start Game", difficulty_menu)
    menu.add.selector(
        "Player1 (Red):", players, onchange=lambda value, _: set_player(value[0][1], 1)
    )
    menu.add.selector(
        "Player2 (Blue):", players, onchange=lambda value, _: set_player(value[0][1], 2)
    )
    menu.add.button("Back", start_menu)
    menu.add.button("Quit", pygame_menu.events.EXIT)

    menu.mainloop(surface)
    return


def difficulty_menu():
    global player1, player2
    if(player1 == player2 and player1 == ai.execute_human_move): start_game()

    difficulty = [
        ("Easy", ai.execute_monte_carlo_move()),
        ("Medium", ai.execute_monte_carlo_move()),
        ("Hard", ai.execute_monte_carlo_move()),
    ]
    menu = pygame_menu.Menu(
        "Select difficulty", SCREEN_WIDTH, SCREEN_HEIGHT, theme=create_theme()
    )
    menu.add.button("Start Game", start_game)
    if player1 == "Computer":
        player1 = ai.execute_monte_carlo_move()
        menu.add.selector(
            "Player1 Difficulty :",
            difficulty,
            onchange=lambda value, _: set_player(value[0][1], 1),
        )
    if player2 == "Computer":
        player2 = ai.execute_monte_carlo_move()
        menu.add.selector(
            "Player2 Difficulty :",
            difficulty,
            onchange=lambda value, _: set_player(value[0][1], 2),
        )
    menu.add.button("Back", player_menu)
    menu.add.button("Quit", pygame_menu.events.EXIT)

    menu.mainloop(surface)
    return

def rules():

    menu = pygame_menu.Menu(
        "Black-hole Escape!", SCREEN_WIDTH, SCREEN_HEIGHT, theme=create_theme()
    )

    menu.add.label(
    "Rules:",
    max_char=90,
    font_size=36,
    font_color=RED_PIECE_COLOR,
    align=pygame_menu.locals.ALIGN_CENTER,
    background_color=pygame.Color(255,255,255,0),
    ).translate(0,-20)
    
    menu.add.label(
        RULES,
        max_char=90,
        font_size=14,
        font_color=BLACK_HOLE_COLOR,
        margin=(0, 5),
        padding=(0,0,10,0),
        align=pygame_menu.locals.ALIGN_CENTER,
        background_color=pygame.Color(255,255,255,0),
    )
    menu.add.button("Back to menu", start_menu, margin=(0,-500)).translate(0, 25)
    menu.mainloop(surface)
    return

def display_winner(winner):

    congrats_msg = "Player " + str(winner) + " Won!"

    menu = pygame_menu.Menu(
        "Black-hole Escape!", SCREEN_WIDTH, SCREEN_HEIGHT, theme=create_theme()
    )
    menu.add.label(
        congrats_msg,
        max_char=-1,
        font_size=60,
        font_color=GREEN,
        margin=(0, 120),
        align=pygame_menu.locals.ALIGN_CENTER,
        wordwrap=False,
        background_color=BACKGROUND_COLOR,
    )
    menu.add.button("Play again", start_game)
    menu.add.button("Back to menu", start_menu)
    menu.mainloop(surface)


pygame.init()
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Black Hole Escape")
start_menu()
