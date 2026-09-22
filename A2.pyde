import random
from processing import *

GRID_SIZE = 8
CELL_SIZE = 48
BOARD_X = 58
BOARD_Y = 60

PALETTE = [
    (245, 93, 62),   # Orange-Red
    (66, 133, 244),  # Blue
    (52, 168, 83),   # Green
    (251, 188, 5),   # Yellow
    (171, 71, 188),  # Purple
]

SHAPE_TEMPLATES = [
    ([(0, 0)], 0),
    ([(0, 0), (1, 0), (0, 1), (1, 1)], 1),
    ([(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)], 2),
    ([(0, 0), (1, 0)], 3),
    ([(0, 0), (1, 0), (2, 0)], 4),
    ([(0, 0), (1, 0), (2, 0), (3, 0)], 0),
    ([(0, 0), (0, 1)], 1),
    ([(0, 0), (0, 1), (0, 2)], 2),
    ([(0, 0), (0, 1), (0, 2), (0, 3)], 3),
    ([(0, 0), (0, 1), (1, 1)], 4),
    ([(0, 0), (1, 0), (0, 1)], 0),
    ([(0, 0), (1, 0), (1, 1)], 1),
    ([(0, 1), (1, 1), (1, 0)], 2),
]

def draw_square(x, y, size, fill_color, stroke_color,corner_weight):
    stroke(fill_color[0],fill_color[1],fill_color[2])
    strokeWeight(1)
    offset_y = 0
    while offset_y < size:
        line(x, y + offset_y, x + size, y + offset_y)
        offset_y += 1

    stroke(stroke_color[0], stroke_color[1], stroke_color[2])
    strokeWeight(corner_weight)
    line(x,y,x+size,y)              #top
    line(x+size,y,x+size,y+size)    #bottom
    line(x+size,y+size,x,y+size)    #right
    line(x,y+size,x,y)              #left

class Board:
    def __init__(self, size, cell_size, origin_x, origin_y):
        self.size = size
        self.cell_size = cell_size
        self.ox = origin_x
        self.oy = origin_y
        
        self.grid = []
        index_row = 0
        while index_row < size:
            row = []
            index_col = 0
            while index_col < size:
                row.append(-1)
                index_col += 1
            self.grid.append(row)
            index_row += 1
    
    def draw(self):
        index_row = 0
        while index_row < self.size:
            index_col = 0
            while index_col < self.size:
                cell_value = self.grid[index_row][index_col]
                if cell_value == -1:
                    fill_color = (255, 255, 255)
                else:
                    fill_color = PALETTE[cell_value]
                draw_square(self.ox + index_col * self.cell_size,
                            self.oy + index_row * self.cell_size,
                            self.cell_size, fill_color, (0, 0, 0), 2)
                index_col += 1
            index_row += 1

    def can_place(self, piece, target_r, target_c):
        index = 0
        while index < len(piece.blocks):
            block = piece.blocks[index]
            r = target_r + block[1]
            c = target_c + block[0]
            if r < 0 or r >= self.size or c < 0 or c >= self.size:
                return False
            if self.grid[r][c] != -1:
                return False
            index += 1
        return True

    def place(self, piece, target_r, target_c):
        if not self.can_place(piece, target_r, target_c):
            return False

        for block in piece.blocks:
            r = target_r + block[1]
            c = target_c + block[0]
            self.grid[r][c] = piece.color_idx
        return True

    def clear_lines(self):
        rows_to_clear = []
        cols_to_clear = []

        # Check full rows
        # Check full columns
        # Clear detected rows
        # Clear detected columns

class Piece:
    def __init__(self, blocks, color_idx, anchor_x, anchor_y):
        self.blocks = blocks
        self.color_idx = color_idx
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.x = anchor_x
        self.y = anchor_y
        self.is_dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.mini_cell = 24
    
    def draw(self):
    def contains_point(self, px, py):
    def reset_pos(self):

# --- GLOBAL GAME STATE ---
board = None
hand = [0, 0, 0]
score = 0
game_over = False
selected_piece = None
selected_index = -1

def spawn_hand():
    global hand

def is_hand_empty():
def check_game_over():
    global game_over

def setup():
    global board, score, game_over

def draw():
    # Draw selected piece on top
    if selected_piece != None:
    # When Game over
    if game_over:

def mousePressed():
    global selected_piece, selected_index, game_over

def mouseDragged():

def mouseReleased():
    global selected_piece, selected_index, score, game_over
    if selected_piece == None:
    if board.can_place(selected_piece, target_r, target_c):
    
    