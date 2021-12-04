"""
---------------other Classes (Imports) & stuff-----------------------------
"""
#hii
from matrixGui import NeoMatrixGui
gui = NeoMatrixGui(15,30)

from pynput import keyboard
import random
import time

"""
---------------variables---------------------------------------------------
"""

debugMode = True
guiMode= True

pixelBoard = [[0 for i in range(30)] for j in range(15)]

game_board_xLength = 13
game_board_yLength = 24
game_board_xPos = 2
game_board_yPos = 4
game_board = [[0 for i in range(game_board_yLength)] for j in range(game_board_xLength)]

game_run = True
game_notPaused = True
game_speed = 1.0
game_lines = 0
game_score = 0

tetromino = [[0 for i in range(4)] for j in range(4)]
tetromino_number = 0
nextTetromino = [[0 for i in range(4)] for j in range(4)]
nextTetromino_number = 0

tetromino_startPos = 6
tetromino_xPos = 0
tetromino_yPos = 0

out = []
def get_color(x):
    TetrominoColors = [0 for i in range(9)]

    TetrominoColors[0]=(0,0,0)
    TetrominoColors[1]=(255,0,0)
    TetrominoColors[2]=(0,0,255)
    TetrominoColors[3]=(255,125,0)
    TetrominoColors[4]=(255,0,255)
    TetrominoColors[5]=(255,255,0)
    TetrominoColors[6]=(0,255,255)
    TetrominoColors[7]=(0,255,0)

    return TetrominoColors[x]


def get_tetromino(x):
    Tetrominos = [[[0 for i in range(4)] for j in range(4)] for k in range(8)]
    
    #L
    Tetrominos[1][0][1]=1
    Tetrominos[1][1][1]=1
    Tetrominos[1][2][1]=1
    Tetrominos[1][0][2]=1
    
    #Lr
    Tetrominos[2][0][1]=2
    Tetrominos[2][1][1]=2
    Tetrominos[2][2][1]=2
    Tetrominos[2][2][2]=2
    
    #Z
    Tetrominos[3][0][1]=3
    Tetrominos[3][1][1]=3
    Tetrominos[3][1][2]=3
    Tetrominos[3][2][2]=3
    
    #Zr
    Tetrominos[4][0][2]=4
    Tetrominos[4][1][2]=4
    Tetrominos[4][1][1]=4
    Tetrominos[4][2][1]=4
    
    #Square
    Tetrominos[5][1][1]=5
    Tetrominos[5][1][2]=5
    Tetrominos[5][2][1]=5
    Tetrominos[5][2][2]=5
    
    #Bar
    Tetrominos[6][0][1]=6
    Tetrominos[6][1][1]=6
    Tetrominos[6][2][1]=6
    Tetrominos[6][3][1]=6
    
    #T
    Tetrominos[7][0][1]=7
    Tetrominos[7][1][1]=7
    Tetrominos[7][1][2]=7
    Tetrominos[7][2][1]=7

    return Tetrominos[x],x


"""
---------------methods-----------------------------------------------------
"""

def sync_pixelBoard():
    for x in range(game_board_xLength):
        for y in range(game_board_yLength):
            pixelBoard[game_board_xPos+x][game_board_yPos+y] = game_board[x][y]
    
def print_pixelBoard():
    for y in range(30):
        for x in range(15):
           print(str(pixelBoard[x][y]) + " ",end="") 
        print("")
        
def print_array(xD: int, yD: int, inp: []):
    for y in range(yD):
        for x in range(xD):
           print(str(inp[x][y]) + " ",end="") 
        print("")

def print_tetromino():
    for y in range(4):
        for x in range(4):
           print(str(tetromino[x][y]) + " ",end="") 
        print("")

def gui_rewrite():
    global out
    sync_pixelBoard()
    gui.fill_all((0,0,0))
    out = [[(0, 0, 0) for j in range(30)] for i in range(15)]
    MatrixPositive = [[0 for i in range(30)] for j in range(15)]
    for x in range(15):
        for y in range(30):
            if(pixelBoard[x][y] < 0):
                MatrixPositive[x][y] = pixelBoard[x][y]*(-1)
            else:
                MatrixPositive[x][y] = pixelBoard[x][y]
        
    for x in range(15):
        for y in range(30):
            out[x][y]=get_color(MatrixPositive[x][y])
    
    for x in range(15):
        for y in range(30):
            if(MatrixPositive[x][y]) == 0:
                out[x][y] = (0,0,0)
    if debugMode:
        print("")
        print_array(15,30,MatrixPositive)
        """
        print("")
        print_array(15,30,out)
        print("")
        """
         
"""
!!!
"""
               
def game_refresh():
    sync_pixelBoard()
    if guiMode:
       gui_rewrite()
       for x in range(15):
        for y in range(30):
            if(pixelBoard[x][y]) == 0:
                out[x][y] = (0,0,0)
        print("")
        print_array(15,30,out)
        print("")
        
        gui.set_matrix(out)
        gui.submit_all() 
    else:
        print_pixelBoard()
        print("")
    

def set_speed(s):
    global speedF
    speedF = s/1000


def tetromino_fix():
    for x in range(game_board_xLength):
        for y in range(game_board_yLength):
            if game_board[x][y] > 0:
                game_board[x][y] = game_board[x][y]*(-1)
                
def tetromino_rewrite():
    for x in range(game_board_xLength):
        for y in range(game_board_yLength):
            if game_board[x][y] > 0:
                game_board[x][y] = 0
    for x in range(4):
        for y in range(4):
            game_board[tetromino_xPos + x][tetromino_yPos + y] = tetromino[x][y]
            
def game_place_nextTetromino():
    global tetromino_xPos, tetromino_yPos
    global tetromino, nextTetromino
    global tetromino_number, nextTetromino_number
    
    tetromino = nextTetromino
    tetromino_number = nextTetromino_number
    
    Temp = get_tetromino(random.randint(1,7))
    nextTetromino = Temp[0]
    nextTetromino_number = Temp[1]
    
    tetromino_xPos = tetromino_startPos
    tetromino_yPos = 0
    tetromino_rewrite()
    
def game_start():
    global tetromino, nextTetromino
    global tetromino_number, nextTetromino_number
    global tetromino_xPos, tetromino_yPos
    
    Temp = get_tetromino(random.randint(1,7))
    tetromino = Temp[0]
    tetromino_number = Temp[1]
    
    Temp = get_tetromino(random.randint(1,7))
    nextTetromino = Temp[0]
    nextTetromino_number = Temp[1]
    
    tetromino_xPos = tetromino_startPos
    tetromino_yPos = 0
    tetromino_rewrite()
    
def cwRotation(inp: []):
    return list(reversed(list(zip(*inp))))
      
            
def ccwRotation(inp:[]):
    return list(zip(*inp[::-1])) 

def check_cwRotation():
    check = True
    test = cwRotation(tetromino)
    for x in range(4):
        for y in range(4):
            if test[x][y] > 0:
                if game_board[tetromino_xPos + x][tetromino_yPos + y] < 0:
                    check = False
    return check
            
def check_ccwRotation():
    check = True
    test = ccwRotation(tetromino)
    for x in range(4):
        for y in range(4):
            if test[x][y] > 0:
                if game_board[tetromino_xPos + x][tetromino_yPos + y] < 0:
                    check = False
    return check
          

def game_delete_fullRows():
    counter = 0
    for y in range(game_board_yLength):
        full = True
        for x in range(game_board_xLength):
            if game_board[x][y] == 0:
                full = False
        if(full==True):
            counter=+1
            for yN in range(y,game_board_yLength-1):
                for xN in range(game_board_xLength):
                    game_board[yN][xN] = game_board[yN+1][xN]
    return counter
    

def check_dMove():
    check = True
    points = [0 for x in range(4)]
    for x in range(4):
        for y in range(4):
            if(tetromino[x][y] > 0 and points[x] < y):
                points[x] = y
    for x in range(4):
        if game_board[tetromino_xPos + x][tetromino_yPos + points[x] + 1] < 0:
            check = False
    return check

def check_rMove():
    check = True
    points = [0 for y in range(4)]
    for y in range(4):
        for x in range(4):
            if(tetromino[x][y] > 0 and points[y] < x):
                points[y] = x
    for y in range(4):
        if game_board[tetromino_xPos + points[y] + 1][tetromino_yPos + y] < 0:
            check = False
    return check

def check_lMove():
    check = True
    points = [4 for y in range(4)]
    for y in range(4):
        for x in range(4):
            if(tetromino[x][y] > 0 and points[y] > x):
                points[y] = x
    for y in range(4):
        if game_board[tetromino_xPos + points[y] + 1][tetromino_yPos + y] < 0:
            check = False
    return check
    
"""
!!!
def landÃ­nganimation():
    #
"""

def landing():
    if game_delete_fullRows() == 4:
        #landinganimation
        if debugMode:
            print("wow")
    tetromino_fix()
    game_place_nextTetromino()

def input_action(a: str):
    global tetromino_xPos, tetromino_yPos, tetromino
    if a == "dMove":
        if check_dMove():
            tetromino_yPos = tetromino_yPos + 1
        else:
            print("check is dumb af")
            landing()
        
    if a == "rMove":
        if check_rMove():
            tetromino_xPos = tetromino_xPos + 1
        
    if a == "lMove":
        if check_lMove():
            tetromino_xPos = tetromino_xPos - 1
        
    if a == "cwRotation":
        if check_cwRotation():
            tetromino = cwRotation(tetromino)
            
    if a == "ccwRotation":
        if check_ccwRotation():
            tetromino = ccwRotation(tetromino)
    
    tetromino_rewrite()
    game_refresh()

"""
def randommove():
    # move randomly (for prototype w/o input)
"""

"""
---------------gameloop-----------------------------------------------------
"""

def on_press(key):
    global game_run
    """
    !!! pause mode
    """
    if key == keyboard.Key.esc:
        game_run = False
        # Stop listener
        return False   
        print("HEEEEEEYAAAAAAAHHEEEEEYAAAAAAAA")
    if key == keyboard.Key.right:
        input_action("cwRotation")
        
    if key == keyboard.Key.left:
        input_action("ccwRotation")
        
    if str(key) == ("a"):
        input_action("lMove")
        
    if str(key) == ("a"):
        input_action("dMove")
        
    if str(key) == ("d"):
        input_action("rMove")
        
    if debugMode :
        try:
            print('alphanumeric key {0} pressed'.format(key.char))
        except AttributeError:
            print('special key {0} pressed'.format(key))
        
def on_release(key):
    if False:
        print("hmmmmmmmmmmmm")
    
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
    

#-----------------------
game_start()


while(game_run):
    time.sleep(1)
    if(game_notPaused == True):
        input_action("dMove")
        if debugMode:
            #print_pixelBoard()
            print("drop")


"""

"""
