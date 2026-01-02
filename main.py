import pygame
from engine import GameState

def main():
    pygame.init()
    window_size = 1400 
    window = pygame.display.set_mode((window_size + window_size//4,window_size))
    window.fill('grey')
    running = True
    sq_size = window_size // 8
    images, del_images = load_images(sq_size)
    game_state = GameState()
    redraw = True
    moves = []
    clock = pygame.time.Clock()
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                loc = get_loc(pos, sq_size)
                moves = game_state.handle_click(loc)
                redraw = True
            if event.type == pygame.MOUSEBUTTONUP:
                loc = get_loc(pygame.mouse.get_pos(), sq_size)
                game_state.click_move(loc, moves)
                moves = []
                redraw = True
            if event.type == pygame.QUIT:
                running = False
                break
        if not game_state.white_turn:
            game_state.bot_move()
            redraw = True
        if redraw or game_state.game_over:
            draw_game(window, sq_size, images, game_state, moves, del_images)
            if game_state.game_over:
                draw_game_over(window, game_state)
            pygame.display.flip()
            redraw = False   

def load_images(sq_size: int) -> tuple[dict[str, pygame.Surface], dict[str, pygame.Surface]]:
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    images = {}
    del_images = {}
    for piece in pieces:
        image = pygame.image.load("assets/" + piece + ".png")
        images[piece] = pygame.transform.scale(image, (sq_size, sq_size))
        del_images[piece] = pygame.transform.scale(image, (sq_size//2, sq_size//2))
    return images, del_images

def draw_game(window: pygame.Surface, sq_size: int, images, game_state: GameState, moves, del_images):
    draw_board(window, sq_size)
    draw_moves(window, sq_size, moves)
    draw_pieces(window, sq_size, images, game_state)
    draw_del_pieces(window, sq_size, del_images, game_state)

def draw_board(window: pygame.Surface, sq_size: int):
    colors = [(255,255,255), (125,215,100)] 
    for i in range(64):
        row, col = get_row_col(i)
        pygame.draw.rect(window, colors[(row+col)%2], (col*sq_size, row*sq_size, sq_size, sq_size)) 

def draw_pieces(window: pygame.Surface, sq_size: int, image, game_state: GameState):
    for i in range(64):
        row, col = get_row_col(i)
        current = game_state.board[i]
        if current != "  ":
            window.blit(image[current], (col*sq_size, row*sq_size))

def draw_del_pieces(window: pygame.Surface, sq_size: int, del_image, game_state: GameState):
    width = sq_size * 8
    pygame.draw.rect(window, (128, 128, 128), (width, 0, sq_size *2, sq_size*8))
    black_pawn = 0
    black_other = 0
    white_pawn = 0
    white_other = 0
    pieces = game_state.captured_pieces
    sorted_pieces = sort_pieces(pieces)
    for piece in sorted_pieces:
        if piece[0] == "w":
            if piece[1] == "p":
                horz_offset = width + sq_size//2
                vertical_offset = white_pawn * sq_size//2
                white_pawn += 1
            else:
                horz_offset = width
                vertical_offset = white_other * sq_size//2
                white_other += 1
            window.blit(del_image[piece], (horz_offset, vertical_offset))
        if piece[0] == "b":
            if piece[1] == "p":
                horz_offset = width + sq_size + sq_size//2
                vertical_offset = black_pawn * sq_size//2
                black_pawn += 1
            else:
                horz_offset = width + sq_size
                vertical_offset = black_other * sq_size//2
                black_other += 1
            window.blit(del_image[piece], (horz_offset, vertical_offset))

def draw_moves(window: pygame.Surface, sq_size: int, moves):
    alpha_surface = pygame.Surface(window.get_size(), pygame.SRCALPHA) 
    for move in moves:
        row, col = get_row_col(move.to_idx)
        pygame.draw.rect(alpha_surface, (0,0,0,128), (col*sq_size, row*sq_size, sq_size, sq_size))
    window.blit(alpha_surface, (0,0))

def draw_game_over(window: pygame.Surface, game_state: GameState):
    overlay = pygame.Surface((1400, 1400), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    window.blit(overlay, (0, 0))
    font = pygame.font.Font(None, 74)

    if game_state.checkmate:
        if game_state.winner == "w":
            text = "Checkmate! White wins"
        else:
            text = "Checkmate! Black wins"
    elif game_state.stalemate:
        text = "Stalemate! Draw"
    elif game_state.is_fifty_move_draw():
        text = "Draw by fifty-move rule"
    elif game_state.is_threefold_repetition():
        text = "Draw by threefold repetition"
    else:
        text = "Game Over"

    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(700, 700))
    window.blit(text_surface, text_rect)

def sort_pieces(pieces: list[str]):
    order = {"Q": 0, "R": 1, "B": 2, "N": 3, "p": 4}
    half_sorted = sorted(pieces, key=lambda p: order[p[1]])
    white_pieces = []
    black_pieces = []
    for piece in half_sorted:
        if piece[0] == "w":
            white_pieces.append(piece)
        else:
            black_pieces.append(piece)
    return white_pieces + black_pieces

def get_row_col(loc: int) -> tuple[int, int]:
    return loc//8, loc%8

def get_loc(pos: tuple[int, int], sq_size: int):
    row = pos[1]//sq_size
    col = pos[0]//sq_size
    return (row*8 + col)

if __name__ == "__main__":
    main()
