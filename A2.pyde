from processing import *
import random

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
        row = 0
        while row < self.size:
            is_full = True
            col = 0
            while col < self.size:
                if self.grid[row][col] == -1:
                    is_full = False
                    break
                col += 1
            if is_full:
                rows_to_clear.append(row)
            row += 1

        # Check full columns
        col = 0
        while col < self.size:
            is_full = True
            row = 0
            while row < self.size:
                if self.grid[row][col] == -1:
                    is_full = False
                    break
                row += 1
            if is_full:
                cols_to_clear.append(col)
            col += 1

        # Clear detected rows
        i = 0
        while i < len(rows_to_clear):
            row = rows_to_clear[i]
            col = 0
            while col < self.size:
                self.grid[row][col] = -1
                col += 1
            i += 1

        # Clear detected columns
        i = 0
        while i < len(cols_to_clear):
            col = cols_to_clear[i]
            row = 0
            while row < self.size:
                self.grid[row][col] = -1
                row += 1
            i += 1

        return (len(rows_to_clear) + len(cols_to_clear)) * 100

class Piece:
    def __init__(self, blocks, color_idx, anchor_x, anchor_y,template_idx):
        self.blocks = blocks
        self.color_idx = color_idx
        self.template_idx = template_idx
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.x = anchor_x
        self.y = anchor_y
        self.is_dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.mini_cell = 24
    
    def draw(self):
        color = PALETTE[self.color_idx]
        border_color = (0,0,0)

        scale_size = self.mini_cell
        if self.is_dragging:
            scale_size = CELL_SIZE

        index = 0
        while index < len(self.blocks) :
            block = self.blocks[index]
            blockx = self.x + block[0] * scale_size
            blocky = self.y + block[1] * scale_size
            draw_square(blockx,blocky,scale_size - 2,color,border_color,1)
            index = index + 1

    def contains_point(self, px, py):
        i = 0
        while i < len(self.blocks):
            block = self.blocks[i]
            block_x = self.x + block[0] * self.mini_cell
            block_y = self.y + block[1] * self.mini_cell
            if block_x <= px and px <= block_x + self.mini_cell:
                if block_y <= py and py <= block_y + self.mini_cell:
                    return True
            i = i + 1
        return False
        
    def reset_pos(self):
        self.x = self.anchor_x
        self.y = self.anchor_y
        self.is_dragging = False

# --- GLOBAL GAME STATE ---
board = None
hand = [0, 0, 0]
score = 0
combo_streak = 0
combo_msg = ""
combo_timer = 0
combo_y = 0
status_notice = ""
status_timer = 0
game_over = False
selected_piece = None
selected_index = -1

def spawn_hand():
    slot_width = width / 3.0
    for idx in range(len(hand)):
        t_idx = random.randint(0, len(SHAPE_TEMPLATES) - 1)
        shape_data = SHAPE_TEMPLATES[t_idx]
        px = idx * slot_width + (slot_width / 2.0) - 30
        py = 490
        hand[idx] = Piece(shape_data[0], shape_data[1], px, py, t_idx)

def is_hand_empty():
    return all(p == 0 for p in hand)

def check_game_over():
    active_pieces = []
    i = 0
    while i < len(hand):
        p = hand[i]
        if p != 0:
            active_pieces.append(p)
        i += 1
    i = 0
    while i < len(active_pieces):
        piece = active_pieces[i]
        r = 0
        while r < board.size:
            c = 0
            while c < board.size:
                if board.can_place(piece, r, c):
                    return False
                c += 1
            r += 1
        i += 1
    return True

def save_game():
    global status_notice, status_timer
    try:
        with open(SAVE_FILE, "w") as f:
            flat_grid = [str(board.grid[r][c]) for r in range(board.size) for c in range(board.size)]
            f.write(",".join(flat_grid) + "\n")
            f.write(str(score) + "," + str(combo_streak) + "\n")
            
            hand_data = []
            for p in hand:
                if p == 0:
                    hand_data.append("EMPTY")
                else:
                    hand_data.append(str(p.template_idx) + ":" + str(p.color_idx))
            f.write(";".join(hand_data) + "\n")
            
        status_notice = "Game Saved!"
        status_timer = 60
    except Exception as e:
        status_notice = "Save Failed!"
        status_timer = 60

def load_game():
    global board, score, combo_streak, hand, selected_piece, selected_index, game_over, status_notice, status_timer
    try:
        with open(SAVE_FILE, "r") as f:
            lines = [l.strip() for l in f.readlines()]

        if len(lines) < 3:
            status_notice = "Corrupt Save!"
            status_timer = 60
            return

        cell_vals = lines[0].split(",")
        idx = 0
        for r in range(board.size):
            for c in range(board.size):
                board.grid[r][c] = int(cell_vals[idx])
                idx += 1

        score_parts = lines[1].split(",")
        score = int(score_parts[0])
        combo_streak = int(score_parts[1]) if len(score_parts) > 1 else 0

        hand_entries = lines[2].split(";")
        slot_width = width / 3.0
        for i, entry in enumerate(hand_entries):
            px = i * slot_width + (slot_width / 2.0) - 30
            py = 490
            if entry in ("EMPTY", ""):
                hand[i] = 0
            else:
                t_idx, c_idx = map(int, entry.split(":"))
                hand[i] = Piece(SHAPE_TEMPLATES[t_idx][0], c_idx, px, py, t_idx)

        selected_piece = None
        selected_index = -1
        game_over = check_game_over()
        status_notice = "Game Loaded!"
        status_timer = 60
    except Exception as e:
        status_notice = "No Save Found!"
        status_timer = 60

def setup():
    global board, score, combo_streak, combo_msg, combo_timer, game_over, status_notice, status_timer
    size(500, 600)

    board = Board(GRID_SIZE, CELL_SIZE, BOARD_X, BOARD_Y)
    score = 0
    combo_streak = 0
    combo_msg = ""
    combo_timer = 0
    status_notice = ""
    status_timer = 0
    game_over = False
    
    spawn_hand()

def draw():
    global combo_timer, combo_y, status_timer

    background(176, 217, 255)
    # Header HUD
    fill(40, 40, 40)
    textSize(22)
    text("Score: " + str(score), BOARD_X, 36)
    
    textSize(12)
    fill(90, 90, 90)
    text("[S] Save  |  [L] Load", BOARD_X, 52)

    if combo_streak > 1:
        fill(245, 93, 62)
        textSize(18)
        text("Streak x" + str(combo_streak), width - 140, 36)

    board.draw()
    
    # Fast Ghost Placement Preview
    if selected_piece is not None:
        cs = board.cell_size
        target_c = int(round((selected_piece.x - board.ox) / float(cs)))
        target_r = int(round((selected_piece.y - board.oy) / float(cs)))

        if board.can_place(selected_piece, target_r, target_c):
            p_color = PALETTE[selected_piece.color_idx]
            noFill()
            stroke(p_color[0], p_color[1], p_color[2])
            strokeWeight(2)
            
            for b in selected_piece.blocks:
                gx = board.ox + (target_c + b[0]) * cs
                gy = board.oy + (target_r + b[1]) * cs
                rect(gx, gy, cs - 4, cs - 4)

    # Inactive hand items
    for p in hand:
        if p != 0 and not p.is_dragging:
            p.draw()

    # Dragged item on top
    if selected_piece is not None:
        selected_piece.draw()

    # Floating combo feedback
    if combo_timer > 0:
        fill(245, 93, 62)
        textSize(20)
        text(combo_msg, width / 2 - 80, combo_y)
        combo_y -= 0.6
        combo_timer -= 1

    # Save/Load status toast
    if status_timer > 0:
        fill(30, 130, 60)
        textSize(16)
        text(status_notice, width / 2 - 45, 52)
        status_timer -= 1
        
    # Game over overlay
    if game_over:
        fill(255, 255, 255, 230)
        stroke(0)
        strokeWeight(2)
        rect(width / 2 - 120, height / 2 - 60, 240, 120)
            
        fill(40, 40, 40)
        textSize(36)
        text("YOU LOSE", width / 2 - 90, height / 2 - 5)
        textSize(16)
        text("Click to restart", width / 2 - 55, height / 2 + 30)

def keyPressed():
    if key in ('s', 'S'):
        save_game()
    elif key in ('l', 'L'):
        load_game()

def mousePressed():
    global selected_piece, selected_index

    if game_over:
        setup()
        return

    for idx, piece in enumerate(hand):
        if piece != 0 and piece.contains_point(mouseX, mouseY):
            selected_piece = piece
            selected_index = idx
            piece.is_dragging = True
            piece.drag_offset_x = mouseX - piece.x
            piece.drag_offset_y = mouseY - piece.y
            break

def mouseDragged():
    if selected_piece is not None:
        selected_piece.x = mouseX - selected_piece.drag_offset_x
        selected_piece.y = mouseY - selected_piece.drag_offset_y

def mouseReleased():
    global selected_piece, selected_index, score, combo_streak, combo_msg, combo_timer, combo_y, game_over

    if selected_piece is None:
        return

    cs = board.cell_size
    target_c = int(round((selected_piece.x - board.ox) / float(cs)))
    target_r = int(round((selected_piece.y - board.oy) / float(cs)))

    if board.can_place(selected_piece, target_r, target_c):
        board.place(selected_piece, target_r, target_c)
        
        base_points = len(selected_piece.blocks) * 10
        lines_points = board.clear_lines()
        
        if lines_points > 0:
            combo_streak += 1
            combo_bonus = (combo_streak - 1) * 50
            score += base_points + lines_points + combo_bonus

            if combo_streak > 1:
                combo_msg = "STREAK x" + str(combo_streak) + "! +" + str(lines_points + combo_bonus)
            else:
                combo_msg = "LINE CLEAR! +" + str(lines_points)
            combo_timer = 50
            combo_y = 50
        else:
            combo_streak = 0
            score += base_points

        hand[selected_index] = 0

        if is_hand_empty():
            spawn_hand()
        
        if check_game_over():
            game_over = True
    else:
        selected_piece.reset_pos()

    selected_piece = None
    selected_index = -1
    
run()