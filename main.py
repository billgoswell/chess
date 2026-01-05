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
    pending_promotion = None
    dragging = None
    player_color = None
    clock = pygame.time.Clock()
    new_game_btn = pygame.Rect(window_size+10, window_size - 80, sq_size * 2 - 20, 60)
    undo_btn = pygame.Rect(window_size+10, window_size - 160, sq_size * 2 - 20, 60)
    white_btn = pygame.Rect(window_size//2 - 150, window_size//2 - 40, 300, 80)
    black_btn = pygame.Rect(window_size//2 - 150, window_size//2 + 60, 300, 80)
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if player_color is None:
                    if white_btn.collidepoint(pos):
                        player_color = "w"
                        redraw = True
                    elif black_btn.collidepoint(pos):
                        player_color = "b"
                        game_state.bot_move()
                        redraw = True
                elif pending_promotion:
                    chosen = get_promotion_choice(pos, sq_size, pending_promotion)
                    if chosen:
                        game_state.make_move(chosen)
                        game_state.move_history.append(chosen)
                        game_state.switch_turn()
                    pending_promotion = None
                    moves = []
                    redraw = True
                elif new_game_btn.collidepoint(pos):
                    game_state = GameState()
                    moves = []
                    pending_promotion = None
                    dragging = None
                    player_color = None
                    redraw = True
                elif undo_btn.collidepoint(pos):
                    if len(game_state.move_history) >= 2:
                        game_state.undo_last_move()
                        game_state.undo_last_move()
                        moves = []
                        redraw = True
                else:
                    loc = get_loc(pos, sq_size)
                    moves = game_state.handle_click(loc)
                    if moves:
                        dragging = loc
                    redraw = True
            if event.type == pygame.MOUSEBUTTONUP and not pending_promotion and player_color:
                loc = get_loc(pygame.mouse.get_pos(), sq_size)
                promo_moves = [m for m in moves if m.to_idx == loc and m.move_type.value == "promotion"]
                if promo_moves:
                    pending_promotion = promo_moves
                    redraw = True
                else:
                    game_state.click_move(loc, moves)
                    moves = []
                    redraw = True
                dragging = None
            if event.type == pygame.QUIT:
                running = False
                break
        is_player_turn = (player_color == "w" and game_state.white_turn) or (player_color == "b" and not game_state.white_turn)
        if player_color and not is_player_turn and not game_state.game_over:
            game_state.bot_move()
            redraw = True
        if redraw or game_state.game_over or dragging:
            if player_color is None:
                draw_start_screen(window, window_size, white_btn, black_btn)
            else:
                draw_game(window, sq_size, images, game_state, moves, del_images, dragging)
                if dragging:
                    mouse_pos = pygame.mouse.get_pos()
                    piece = game_state.board[dragging]
                    window.blit(images[piece], (mouse_pos[0] - sq_size//2, mouse_pos[1] - sq_size//2))
                if pending_promotion:
                    draw_promotion_ui(window, sq_size, images, pending_promotion)
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

def draw_game(window: pygame.Surface, sq_size: int, images, game_state: GameState, moves, del_images, dragging=None):
    draw_board(window, sq_size)
    draw_moves(window, sq_size, moves)
    draw_pieces(window, sq_size, images, game_state, dragging)
    draw_del_pieces(window, sq_size, del_images, game_state)
    draw_new_game_btn(window, sq_size)
    draw_undo_btn(window, sq_size)

def draw_new_game_btn(window: pygame.Surface, sq_size: int):
    width = sq_size * 8
    btn_rect = pygame.Rect(width + 10, width - 80, sq_size * 2 - 20, 60)
    pygame.draw.rect(window, (70, 130, 70), btn_rect, border_radius=10)
    pygame.draw.rect(window, (50, 100, 50), btn_rect, 3, border_radius=10)
    font = pygame.font.Font(None, 40)
    text = font.render("New Game", True, (255, 255, 255))
    text_rect = text.get_rect(center=btn_rect.center)
    window.blit(text, text_rect)

def draw_start_screen(window: pygame.Surface, window_size: int, white_btn, black_btn):
    window.fill((50, 50, 50))
    font_title = pygame.font.Font(None, 100)
    font_btn = pygame.font.Font(None, 50)
    title = font_title.render("Chess", True, (255, 255, 255))
    title_rect = title.get_rect(center=(window_size//2 + window_size//8, window_size//3))
    window.blit(title, title_rect)
    pygame.draw.rect(window, (255, 255, 255), white_btn, border_radius=10)
    pygame.draw.rect(window, (200, 200, 200), white_btn, 3, border_radius=10)
    white_text = font_btn.render("Play as White", True, (0, 0, 0))
    window.blit(white_text, white_text.get_rect(center=white_btn.center))
    pygame.draw.rect(window, (30, 30, 30), black_btn, border_radius=10)
    pygame.draw.rect(window, (60, 60, 60), black_btn, 3, border_radius=10)
    black_text = font_btn.render("Play as Black", True, (255, 255, 255))
    window.blit(black_text, black_text.get_rect(center=black_btn.center))

def draw_undo_btn(window: pygame.Surface, sq_size: int):
    width = sq_size * 8
    btn_rect = pygame.Rect(width + 10, width - 160, sq_size * 2 - 20, 60)
    pygame.draw.rect(window, (130, 100, 70), btn_rect, border_radius=10)
    pygame.draw.rect(window, (100, 70, 50), btn_rect, 3, border_radius=10)
    font = pygame.font.Font(None, 40)
    text = font.render("Undo", True, (255, 255, 255))
    text_rect = text.get_rect(center=btn_rect.center)
    window.blit(text, text_rect)

def draw_promotion_ui(window: pygame.Surface, sq_size: int, images, promo_moves):
    to_idx = promo_moves[0].to_idx
    row, col = get_row_col(to_idx)
    is_white = promo_moves[0].piece[0] == "w"
    x = col * sq_size
    if is_white:
        y = row * sq_size
    else:
        y = row * sq_size + sq_size - sq_size * 4
    pygame.draw.rect(window, (200, 200, 200), (x, y, sq_size, sq_size * 4))
    pygame.draw.rect(window, (100, 100, 100), (x, y, sq_size, sq_size * 4), 2)
    for i, move in enumerate(promo_moves):
        window.blit(images[move.promotion_piece], (x, y + i * sq_size))

def get_promotion_choice(pos, sq_size, promo_moves):
    to_idx = promo_moves[0].to_idx
    row, col = get_row_col(to_idx)
    is_white = promo_moves[0].piece[0] == "w"
    x = col * sq_size
    if is_white:
        y = row * sq_size
    else:
        y = row * sq_size + sq_size - sq_size * 4
    for i, move in enumerate(promo_moves):
        rect = pygame.Rect(x, y + i * sq_size, sq_size, sq_size)
        if rect.collidepoint(pos):
            return move
    return None

def draw_board(window: pygame.Surface, sq_size: int):
    colors = [(255,255,255), (125,215,100)] 
    for i in range(64):
        row, col = get_row_col(i)
        pygame.draw.rect(window, colors[(row+col)%2], (col*sq_size, row*sq_size, sq_size, sq_size)) 

def draw_pieces(window: pygame.Surface, sq_size: int, image, game_state: GameState, dragging=None):
    for i in range(64):
        if i == dragging:
            continue
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
