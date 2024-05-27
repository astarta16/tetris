import pygame
import random

WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
ROWS = 20
COLS = 10
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (0, 255, 255), (128, 0, 128)]

tetrominos = [
    [[1, 1, 1, 1]],  
    [[1, 1, 1], [0, 1, 0]],  
    [[1, 1, 1], [1, 0, 0]], 
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1], [1, 1]],       # O
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1, 0], [0, 1, 1]]   # S
]

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    board = [[0] * COLS for _ in range(ROWS)]
    falling_piece = new_piece()
    next_piece = new_piece()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_piece(board, falling_piece, -1)
                if event.key == pygame.K_RIGHT:
                    move_piece(board, falling_piece, 1)
                if event.key == pygame.K_DOWN:
                    move_piece_down(board, falling_piece)
                if event.key == pygame.K_UP:
                    rotate_piece(board, falling_piece)

        if not move_piece_down(board, falling_piece):
            place_piece(board, falling_piece)
            remove_completed_lines(board)
            falling_piece = next_piece
            next_piece = new_piece()
            if not is_valid_position(board, falling_piece):
                print("Game Over")
                pygame.quit()
                return

        screen.fill(BLACK)
        draw_board(screen, board)
        draw_piece(screen, falling_piece)
        draw_next_piece(screen, next_piece)
        pygame.display.flip()
        clock.tick(5)

def new_piece():
    return {
        "shape": random.choice(tetrominos),
        "x": COLS // 2 - 2,
        "y": 0,
        "color": random.choice(COLORS)
    }

def draw_board(screen, board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, cell, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_piece(screen, piece):
    shape = piece["shape"]
    color = piece["color"]
    x = piece["x"]
    y = piece["y"]
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col]:
                pygame.draw.rect(screen, color,
                                 ((x + col) * BLOCK_SIZE, (y + row) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, GRAY, ((x + col) * BLOCK_SIZE, (y + row) * BLOCK_SIZE,
                                                BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_next_piece(screen, piece):
    shape = piece["shape"]
    color = piece["color"]
    x_offset, y_offset = COLS * BLOCK_SIZE + 20, 50
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col]:
                pygame.draw.rect(screen, color,
                                 ((x_offset + col) * BLOCK_SIZE, (y_offset + row) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, GRAY, ((x_offset + col) * BLOCK_SIZE, (y_offset + row) * BLOCK_SIZE,
                                                BLOCK_SIZE, BLOCK_SIZE), 1)

def move_piece_down(board, piece):
    piece["y"] += 1
    if not is_valid_position(board, piece):
        piece["y"] -= 1
        return False
    return True

def move_piece(board, piece, direction):
    piece["x"] += direction
    if not is_valid_position(board, piece):
        piece["x"] -= direction

def rotate_piece(board, piece):
    if piece["shape"] == [[1, 1], [1, 1]]: 
        return 

    original_shape = piece["shape"]
    piece["shape"] = [list(reversed(row)) for row in zip(*piece["shape"])]
    if not is_valid_position(board, piece):
        piece["shape"] = original_shape

def is_valid_position(board, piece):
    shape = piece["shape"]
    x, y = piece["x"], piece["y"]
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col]:
                if x + col < 0 or x + col >= COLS or y + row >= ROWS or board[y + row][x + col]:
                    return False
    return True

def place_piece(board, piece):
    shape = piece["shape"]
    color = piece["color"]
    x, y = piece["x"], piece["y"]
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col]:
                board[y + row][x + col] = color

def remove_completed_lines(board):
    lines_to_remove = [row for row in range(ROWS) if all(board[row])]
    for row in lines_to_remove:
        del board[row]
        board.insert(0, [0] * COLS)

if __name__ == "__main__":
    main()

