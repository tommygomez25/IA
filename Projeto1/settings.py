SCREEN_WIDTH =800
SCREEN_HEIGHT = 800
FPS = 60
BACKGROUND_COLOR = (255,221,121)
RED_PIECE_COLOR = (174,4,1)
BLUE_PIECE_COLOR = (4,2,168)
BLACK_HOLE_COLOR = (0,0,0)
WHITE = (255,255,255)
GREY = (128,128,128)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
Game_size = 5
Tile_size = (((SCREEN_HEIGHT+SCREEN_WIDTH)//2)//Game_size+2)

RULES= "This game is a two player game. Game is played on a 5x5 board. The middle square of the board is accepted as a black hole. \
The aim of the game is to land firs two of game pieces on this center hole. \
Each player has four space ships in his/her own color. At the beginning of the \
game players places their pieces on the board as seen in the game picture. \
Each piece can move horizontally or vertically. Diagonal moves are not allowed.\
The ships are in a weird dimension and their brake motors are not working. \
For this reason if a piece is moved, must move until stopped by an other piece or by the borders of the board. \
Players try to land their ships on the black hole. The ship landed on this square pass to another dimension and removed from the board. \
The ships can pass over the black hole, but for removing it must land on this square. The player who rescue first his/her two ships from this dimension win the game."

def set_game_size(val):
    global GAME_SIZE,TILE_SIZE
    GAME_SIZE = val
    TILE_SIZE = (((SCREEN_HEIGHT+SCREEN_WIDTH)//2)//GAME_SIZE+2)
    return
