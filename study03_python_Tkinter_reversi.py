# ------------------------
# Import libraries and define constant .

import random
import time
import math
import tkinter
from tkinter import messagebox

SPACE = 0
BLACK = 1
WHITE = -1

BOARD_SQUARE = 8
BOARD_SQUARE_X = BOARD_SQUARE
BOARD_SQUARE_Y = BOARD_SQUARE

BOARD_PX_SIZE = 500
BOARD_SQUARE_PX_SIZE = BOARD_PX_SIZE / BOARD_SQUARE
GAP_PX_SIZE = 4

MOVEDIR = [[-1, -1], [-1, 0], [-1, 1],
           [ 0, -1],          [ 0, 1],
           [ 1, -1], [ 1, 0], [ 1, 1]]

GAME_WAIT = 0
GAME_ONGOING = 1
GAME_END = 2
HUMAN = 1
COMPUTER = 0

COLOR_PIECE_BLACK =  "#566573"
COLOR_PIECE_WHITE =  "#F8F9F9"
COLOR_BOARD = "#229954"
COLOR_BOARD_LINE = "#196F3D"


# ------------------------
# Class : Manage a coordinate of a target square.
class Position:
    
    def __init__(self):
        self.y = 0
        self.x = 0
    
    def __init__(self, y, x):
        self.y = y
        self.x = x
    
# ------------------------
## Class : Manage the board.
class Board:
    def __init__(self):
        self.turn = BLACK
        self.move_num = 1
        self.board = [[SPACE for i in range(BOARD_SQUARE_X)] for j in range(BOARD_SQUARE_Y)]
        #  ---- board
        # [[0, 0, 0, 0, 0, 0, 0, 0],
        #  [0, 0, 0, 0, 0, 0, 0, 0],
        #  [0, 0, 0, 0, 0, 0, 0, 0],
        #  [0, 0, 0, 0, 0, 0, 0, 0],
        #  [0, 0, 0, 0, 0, 0, 0, 0],
        #  [0, 0, 0, 0, 0, 0, 0, 0],
        #  [0, 0, 0, 0, 0, 0, 0, 0],
        #  [0, 0, 0, 0, 0, 0, 0, 0]]
    
    # Initialize the board. / 盤面を初期化
    def init_board(self):
        self.board = [[SPACE for i in range(BOARD_SQUARE_X)] for j in range(BOARD_SQUARE_Y)]
        self.board[3][3] = WHITE
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[4][4] = WHITE
        self.turn = BLACK  # turn / 手番
        self.move_num = 1  # number of moves in attack./ 手数
        #  ---- board
        # [[0, 0, 0, 0, 0, 0, 0, 0],
        #  [0, 0, 0, 0, 0, 0, 0, 0],
        #  [0, 0, 0, 0, 0, 0, 0, 0],
        #  [0, 0, 0, -1, 1, 0, 0, 0],
        #  [0, 0, 0, 1, -1, 0, 0, 0],
        #  [0, 0, 0, 0, 0, 0, 0, 0],
        #  [0, 0, 0, 0, 0, 0, 0, 0],
        #  [0, 0, 0, 0, 0, 0, 0, 0]]
        
    # Count black and white pieces. / 白と黒のピースの数を数える    
    def get_pieces(self):
        black_discs = 0
        white_discs = 0
        for y in range(BOARD_SQUARE_Y):
            for x in range(BOARD_SQUARE_X):
                disc = self.board[y][x]
                if disc == BLACK:
                    black_discs += 1
                elif disc == WHITE:
                    white_discs += 1
        return (black_discs, white_discs)

    # Can place a new piece or not? / ピースを配置できるかどうか    
    def is_movable(self, position):
        # Is the position ocupied or opened? / 配置位置が空いているか
        if self.board[position.y][position.x] != SPACE:
            return False
        # Can flipp white/black to black/white?
        # ピースを裏返すことが出来るか
        for dir in MOVEDIR:
            # Get coordinate around the original position.
            # 指定位置の周りの座標を取得            
            y = position.y + dir[0]
            x = position.x + dir[1]
            if self.is_inRange(x, y) and self.board[y][x] == -self.turn:
                y += dir[0]
                x += dir[1]
                while self.is_inRange(x, y) and self.board[y][x] == -self.turn:
                    y += dir[0]
                    x += dir[1]
                if self.is_inRange(x, y) and self.board[y][x] == self.turn:
                    return True
        return False

    # The position is in range? / 配置位置が範囲内か
    def is_inRange(self, x, y):
        if y >= 0 and x >= 0 and y < BOARD_SQUARE_Y and x < BOARD_SQUARE_X:
            return True
        else:
            return False
    
    # Get a list of squares which can put peice in. / ピースを置けるマスのリストを取得 
    def get_move_list(self):
        move_list = []
        for y in range(BOARD_SQUARE_Y):
            for x in range(BOARD_SQUARE_X):
                if self.board[y][x] == SPACE:
                    position = Position(y, x)
                    if self.is_movable(position):
                        move_list.append(position)
        return move_list
    
    # Move / ピースを置く
    def move(self, position):
        self.board[position.y][position.x] = self.turn

        for dir in MOVEDIR:
            y = position.y + dir[0]
            x = position.x + dir[1]
            if self.is_inRange(x, y) and self.board[y][x] == -self.turn:
                y += dir[0]
                x += dir[1]
                # Move strait as long as the opponent's piece continues.
                # 相手のピースが続いている限り直線的に移動            
                while self.is_inRange(x, y) and self.board[y][x] == -self.turn:
                    y += dir[0]
                    x += dir[1]
                # After moving in a straight line, check if my piece is at the end point.
                # 直線的に移動した後、終点に自分のピースがあるかをチェック
                if self.is_inRange(x, y) and self.board[y][x] == self.turn:
                    y -= dir[0]
                    x -= dir[1]
                    # In case of there is my own piece at the end, flap the opponent's piece upside down.
                    # 終点に自分のピースがある場合、戻りながら相手のピースを裏返す
                    while self.is_inRange(x, y) and self.board[y][x]==-self.turn:
                        self.board[y][x] = self.turn
                        y -= dir[0]
                        x -= dir[1]
        # Change the turn.
        self.turn = -self.turn
        # Incriment the number of moving
        self.move_num += 1
    
    # Passing
    def move_pass(self):
        self.turn = -self.turn
        
    # Judgement of the game end. / 対局終了の判定
    def is_game_end(self):
        # When reatching 60 move. / 60手に達した時
        if self.move_num == BOARD_SQUARE_X * BOARD_SQUARE_Y - 3:
            return True
        
        # When the number of my pieces or opponent's became 0./.自分か相手のピースの数が0になった時
        (black_discs, white_discs) = self.get_pieces()
        if black_discs == 0 or white_discs == 0:
            return True
        
        # There is no square to put a piece. / 黒白どちらも手がない場合
        move_list1 = self.get_move_list()
        if len(move_list1) == 0:
            self.move_pass()
            move_list2 = self.get_move_list()
            self.move_pass()
            if len(move_list2) == 0:
                return True
        
        return False
    
# ------------------------
## Class : Manage the game progress
class Game:
    
    # Initialize game.
    def __init__(self):
        self.game_mode = GAME_WAIT
        self.black_player = HUMAN
        self.white_player = COMPUTER
        self.board = Board()
        self.board.init_board()
  
    # Start game.
    def start(self, _black_player, _white_player):
        self.black_player = _black_player
        self.white_player = _white_player
        self.game_mode = GAME_ONGOING
        self.board.init_board()
    
    # Continue the game.
    def game_move(self, position):
        self.board.move(position)
        draw_board()
        
        # When the game is over.
        if self.board.is_game_end():
            self.game_mode = GAME_END
            show_status()
            messagebox.showinfo("Reversi", "The game is over.")
            return
        
        # When passed.
        move_list = self.board.get_move_list()
        if len(move_list) == 0:
            self.board.move_pass()    
            messagebox.showinfo("Pass", "Can not make a valid move.")
        
        show_status()
        
    # Is next move computer?
    def is_com_turn(self):
        if (self.board.turn == BLACK and self.black_player == COMPUTER) or \
            (self.board.turn == WHITE and self.white_player == COMPUTER):
            return True
        return False
    
    # Select next move by computer.
    def proc_com_turn(self):
        while True:
            if self.is_com_turn():
                position = Computer().select_move(self.board)
                self.game_move(position)
                if self.game_mode == GAME_END:
                    break
            else:
                break
# ------------------------
## Class : Computer thinking
class Computer:
    # Choose next move by computer.
    def select_move(self, board):
        # Wait 0.1 second.
        time.sleep(0.1)
        move_list = board.get_move_list()
        # Choose a next move at random
        r = random.randint(0, len(move_list) - 1)
        return move_list[r]

# ------------------------
## Re-Draw the board.
def draw_board():
    global game
    global canvas_board
    # Clear the canvas.
    canvas_board.delete('all')
    # Set background.
    canvas_board.create_rectangle(0, 0, \
        BOARD_PX_SIZE, BOARD_PX_SIZE, outline=COLOR_BOARD_LINE, \
        fill = COLOR_BOARD)
    
    for y in range(BOARD_SQUARE_Y):
        for x in range(BOARD_SQUARE_X):
            piece = game.board.board[y][x]
            if piece == SPACE:
                color = ""
            elif piece == BLACK:
                color = COLOR_PIECE_BLACK
            else: # piece == WHITE
                color = COLOR_PIECE_WHITE
            # Draw pieces.
            if color != "":
                canvas_board.create_oval( \
                    x*BOARD_SQUARE_PX_SIZE + GAP_PX_SIZE, y*BOARD_SQUARE_PX_SIZE + GAP_PX_SIZE, \
                    (x+1)*BOARD_SQUARE_PX_SIZE - GAP_PX_SIZE, (y+1)*BOARD_SQUARE_PX_SIZE - GAP_PX_SIZE, \
                    outline=COLOR_BOARD_LINE, fill=color) 
        
    # Draw border lines.
    for x in range(BOARD_SQUARE_X):
        canvas_board.create_line( x * BOARD_SQUARE_PX_SIZE, \
                                 0, x * BOARD_SQUARE_PX_SIZE, BOARD_PX_SIZE, \
                                 fill=COLOR_BOARD_LINE, width=1)
    for y in range(BOARD_SQUARE_Y):
        canvas_board.create_line(0, y * BOARD_SQUARE_PX_SIZE, \
                                 BOARD_PX_SIZE, y * BOARD_SQUARE_PX_SIZE, \
                                 fill=COLOR_BOARD_LINE, width=1)
        
    canvas_board.update()

# ------------------------
## Show status on the dialog.
def show_status():
    global game
    global msg_var
    
    msg = ""
    if game.game_mode == 0:
        msg = "Click [START] button."
        
    elif game.game_mode == 1:
        msg = "Count of turn : " + str(game.board.move_num) + " / "
        if game.board.turn == BLACK:
            msg += "Next turn : Black / "
        else:
            msg += "Next turn : White / "
        (black_discs, white_discs) = game.board.get_pieces()
        msg += " B=" + str(black_discs) + ", W=" + str(white_discs)
        
    elif game.game_mode == 2:
        (black_discs, white_discs) = game.board.get_pieces()    
        msg = "The game is over. / " + \
            "B=" + str(black_discs)+", W="+str(white_discs) + " / "
        if black_discs == white_discs:
            msg += "Draw"
        elif black_discs > white_discs:
            msg += "Black won!"
        else:
            msg += "White won!"
    msg_var.set(msg)

# ------------------------
## Game start.
def play_start():
    global game
    global black_var, white_var
    black_player = black_var.get()
    white_player = white_var.get()    

    game.start(black_player, white_player)    
    show_status()
    draw_board()
    
    game.proc_com_turn()

# ------------------------
## When the board clicked.
def click_board(event):
    global game
    if game.game_mode != 1:
        messagebox.showinfo("Reversi", "Click [Start] button.")
        return
    y = math.floor(event.y / BOARD_SQUARE_PX_SIZE)
    x = math.floor(event.x / BOARD_SQUARE_PX_SIZE)
    position = Position(y, x)
    if game.board.is_movable(position) == False:
        messagebox.showinfo("Reversi", "Cannot put a piece on there.")
        return
    
    game.game_move(position)
    if game.game_mode == 2:
        return

    game.proc_com_turn()

# ------------------------
## main
# Initialize the window.
root = tkinter.Tk()
root.title("Reversi")
window_width    = BOARD_PX_SIZE + 32
window_height = BOARD_PX_SIZE + 72
root.geometry(str(window_width) + "x" + str(window_height))     

# Create canvas.
canvas_board = tkinter.Canvas(root, width = BOARD_PX_SIZE, height = BOARD_PX_SIZE)
canvas_board.bind("<Button-1>", click_board)
canvas_board.place(x = 16, y = 58)                

# Game configration.
black_label = tkinter.Label(text="● Black")
black_label.place(x = 16, y = 4)
black_var = tkinter.IntVar()
black_rdo0 = tkinter.Radiobutton(root, value = HUMAN, variable = black_var, text = "Player")
black_rdo0.place(x = 90, y = 4)
black_rdo1 = tkinter.Radiobutton(root, value = COMPUTER, variable = black_var, text = "Computer")
black_rdo1.place(x = 160, y = 4)

white_label = tkinter.Label(text="〇 White")
white_label.place(x = 16, y = 24)
white_var = tkinter.IntVar()
white_rdo0 = tkinter.Radiobutton(root, value = HUMAN, variable = white_var, text = "Player")
white_rdo0.place(x = 90, y = 24)
white_rdo1 = tkinter.Radiobutton(root, value = COMPUTER, variable = white_var, text = "Computer")
white_rdo1.place(x = 160, y = 24)

# [Start] button.
button_start = tkinter.Button(root, text = "START", width=15, command=play_start)
button_start.place(x = 300, y = 24)

# Show status.
msg_var = tkinter.StringVar()
msg_label = tkinter.Label(root, textvariable = msg_var)
msg_label.place(x = 250, y = 4)

# Create Game instance.
game = Game()
# Draw a board.
draw_board()
# Show status.
show_status()

root.mainloop()
