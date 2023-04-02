import pygame
import settings
import game
from state import State
import ai
import pygame_menu
from copy import deepcopy
import time
from piece import Piece

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
        player1 = ai.execute_ai_move(ai.eval_mixed,5)
    if player2 == "Computer":
        player2 = ai.execute_ai_move(ai.eval_mixed,5)

    new_game = game.Game(State(), player1, player2)
    winner = new_game.loop()
    display_winner(winner)


def create_theme():

    mytheme = pygame_menu.themes.THEME_DARK.copy()
    font = pygame_menu.font.FONT_FIRACODE_BOLD

    mytheme.background_color = settings.BACKGROUND_COLOR
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
    mytheme.widget_background_color = settings.WHITE
    mytheme.widget_font_color = settings.BLUE_PIECE_COLOR
    mytheme.widget_font = font
    mytheme.widget_padding = 30
    mytheme.widget_margin = (10, 10)
    mytheme.selection_color = settings.RED_PIECE_COLOR

    return mytheme


def start_menu():

    menu = pygame_menu.Menu(
        "Black-hole Escape!", settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, theme=create_theme()
    )
    menu.add.button("Play", player_menu)
    menu.add.button("Settings", settings_menu)
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
        "Select Players", settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, theme=create_theme()
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
        ("Easy", ai.execute_ai_move(ai.eval_mixed,5)),
        ("Medium", ai.execute_ai_move(ai.eval_mixed2,7)),
        ("Hard", ai.execute_monte_carlo_move()),
    ]
    menu = pygame_menu.Menu(
        "Select difficulty", settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, theme=create_theme()
    )
    menu.add.button("Start Game", start_game)
    if player1 == "Computer":
        menu.add.selector(
            "Player1 Difficulty :",
            difficulty,
            onchange=lambda value, _: set_player(value[0][1], 1),
        )
    if player2 == "Computer":
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
        "Black-hole Escape!", settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, theme=create_theme()
    )

    menu.add.label(
    "Rules:",
    max_char=90,
    font_size=36,
    font_color=settings.RED_PIECE_COLOR,
    align=pygame_menu.locals.ALIGN_CENTER,
    background_color=pygame.Color(255,255,255,0),
    ).translate(0,-20)
    
    menu.add.label(
        settings.RULES,
        max_char=90,
        font_size=14,
        font_color=settings.BLACK_HOLE_COLOR,
        margin=(0, 5),
        padding=(0,0,10,0),
        align=pygame_menu.locals.ALIGN_CENTER,
        background_color=pygame.Color(255,255,255,0),
    )
    menu.add.button("Back to menu", start_menu, margin=(0,-500)).translate(0, 25)
    menu.mainloop(surface)
    return

def settings_menu():
    if settings.Game_size == 5:
        sizes = [("5x5",5),("7x7",7),("9x9",9)]
    elif settings.Game_size == 7:
        sizes = [("7x7",7),("9x9",9),("5x5",5)]
    elif settings.Game_size == 9:
        sizes = [("9x9",9),("5x5",5),("7x7",7)]

    menu = pygame_menu.Menu(
        "Black-hole Escape!", settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, theme=create_theme()
    )
    menu.add.selector(
        "Board Size:",
        sizes,
        onchange=lambda _, val: settings.set_game_size(val),
        )
    menu.add.button("Back to menu", start_menu, margin=(0,-500)).translate(0, 25)
    menu.mainloop(surface)
    return

def display_winner(winner):

    congrats_msg = "Player " + str(winner) + " Won!"

    menu = pygame_menu.Menu(
        "Black-hole Escape!", settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, theme=create_theme()
    )
    menu.add.label(
        congrats_msg,
        max_char=-1,
        font_size=60,
        font_color=settings.GREEN,
        margin=(0, 120),
        align=pygame_menu.locals.ALIGN_CENTER,
        wordwrap=False,
        background_color=settings.BACKGROUND_COLOR,
    )
    menu.add.button("Play again", start_game)
    menu.add.button("Back to menu", start_menu)
    menu.mainloop(surface)

game_pieces = [
    Piece(2,2,settings.BLACK_HOLE_COLOR, 0),
    Piece(0,0,settings.RED_PIECE_COLOR, 1),
    Piece(1,1,settings.RED_PIECE_COLOR,  1), 
    Piece(3,2,settings.RED_PIECE_COLOR, 1),
    Piece(3,1,settings.RED_PIECE_COLOR, 1), 
    Piece(0,4,settings.BLUE_PIECE_COLOR, 2),
    Piece(1,2,settings.BLUE_PIECE_COLOR, 2),
    Piece(4,4,settings.BLUE_PIECE_COLOR, 2),
    Piece(3,3,settings.BLUE_PIECE_COLOR, 2),
]

if __name__ == "__main__":
    #pygame.init()
    #surface = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    #pygame.display.set_caption("Black Hole Escape")
    #start_menu()
    g = game.Game(State(game_pieces), ai.execute_ai_move(ai.eval_mixed3, 4), ai.execute_ai_move(ai.eval_mixed4, 4))
    g.run_n_matches(10)
