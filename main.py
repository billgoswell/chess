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
    difficulty = None
    clock = pygame.time.Clock()
    new_game_btn = pygame.Rect(window_size+10, window_size - 80, sq_size * 2 - 20, 60)
    undo_btn = pygame.Rect(window_size+10, window_size - 160, sq_size * 2 - 20, 60)
    easy_btn = pygame.Rect(window_size//2 + 25, window_size//2 - 90, 300, 80)
    medium_btn = pygame.Rect(window_size//2 + 25, window_size//2 + 10, 300, 80)
    hard_btn = pygame.Rect(window_size//2 + 25, window_size//2 + 110, 300, 80)
    white_btn = pygame.Rect(window_size//2 + 25, window_size//2 - 40, 300, 80)
    black_btn = pygame.Rect(window_size//2 + 25, window_size//2 + 60, 300, 80)
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if difficulty is None:
                    if easy_btn.collidepoint(pos):
                        difficulty = "easy"
                        redraw = True
                    elif medium_btn.collidepoint(pos):
                        difficulty = "medium"
                        redraw = True
                    elif hard_btn.collidepoint(pos):
                        difficulty = "hard"
                        redraw = True
                elif player_color is None:
                    if white_btn.collidepoint(pos):
                        player_color = "w"
                        redraw = True
                    elif black_btn.collidepoint(pos):
                        player_color = "b"
                        game_state.bot_move(difficulty)
                        redraw = True
                elif pending_promotion:
                    chosen = get_promotion_choice(pos, sq_size, pending_promotion, player_color)
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
                    difficulty = None
                    redraw = True
                elif undo_btn.collidepoint(pos):
                    if len(game_state.move_history) >= 2:
                        game_state.undo_last_move()
                        game_state.undo_last_move()
                        moves = []
                        redraw = True
                else:
                    loc = get_loc(pos, sq_size, player_color == "b")
                    moves = game_state.handle_click(loc)
                    if moves:
                        dragging = loc
                    redraw = True
            if event.type == pygame.MOUSEBUTTONUP and not pending_promotion and player_color:
                loc = get_loc(pygame.mouse.get_pos(), sq_size, player_color == "b")
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
            game_state.bot_move(difficulty)
            redraw = True
        if redraw or game_state.game_over or dragging:
            if difficulty is None:
                draw_difficulty_screen(window, window_size, easy_btn, medium_btn, hard_btn)
            elif player_color is None:
                draw_color_screen(window, window_size, white_btn, black_btn)
            else:
                draw_game(window, sq_size, images, game_state, moves, del_images, new_game_btn, undo_btn, dragging, player_color)
                if dragging:
                    mouse_pos = pygame.mouse.get_pos()
                    piece = game_state.board[dragging]
                    window.blit(images[piece], (mouse_pos[0] - sq_size//2, mouse_pos[1] - sq_size//2))
                if pending_promotion:
                    draw_promotion_ui(window, sq_size, images, pending_promotion, player_color)
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

def draw_game(window: pygame.Surface, sq_size: int, images, game_state: GameState, moves, del_images, new_game_btn, undo_btn, dragging=None, player_color="w"):
    flipped = player_color == "b"
    draw_board(window, sq_size, flipped)
    draw_moves(window, sq_size, moves, flipped)
    draw_pieces(window, sq_size, images, game_state, dragging, flipped)
    draw_del_pieces(window, sq_size, del_images, game_state)
    draw_sidebar_buttons(window, new_game_btn, undo_btn)

def draw_button(window, rect, label, bg_color, border_color, text_color=(255, 255, 255), font_size=40):
    pygame.draw.rect(window, bg_color, rect, border_radius=10)
    pygame.draw.rect(window, border_color, rect, 3, border_radius=10)
    font = pygame.font.Font(None, font_size)
    text = font.render(label, True, text_color)
    window.blit(text, text.get_rect(center=rect.center))

def draw_sidebar_buttons(window: pygame.Surface, new_game_btn, undo_btn):
    draw_button(window, new_game_btn, "New Game", (70, 130, 70), (50, 100, 50))
    draw_button(window, undo_btn, "Undo", (130, 100, 70), (100, 70, 50))

def draw_difficulty_screen(window: pygame.Surface, window_size: int, easy_btn, medium_btn, hard_btn):
    window.fill((50, 50, 50))
    font_title = pygame.font.Font(None, 100)
    title = font_title.render("Chess", True, (255, 255, 255))
    title_rect = title.get_rect(center=(window_size//2 + window_size//8, window_size//3))
    window.blit(title, title_rect)
    draw_button(window, easy_btn, "Easy", (100, 180, 100), (70, 140, 70), (255, 255, 255), 50)
    draw_button(window, medium_btn, "Medium", (180, 140, 100), (140, 100, 70), (255, 255, 255), 50)
    draw_button(window, hard_btn, "Hard", (180, 100, 100), (140, 70, 70), (255, 255, 255), 50)

def draw_color_screen(window: pygame.Surface, window_size: int, white_btn, black_btn):
    window.fill((50, 50, 50))
    font_title = pygame.font.Font(None, 100)
    title = font_title.render("Chess", True, (255, 255, 255))
    title_rect = title.get_rect(center=(window_size//2 + window_size//8, window_size//3))
    window.blit(title, title_rect)
    draw_button(window, white_btn, "Play as White", (255, 255, 255), (200, 200, 200), (0, 0, 0), 50)
    draw_button(window, black_btn, "Play as Black", (30, 30, 30), (60, 60, 60), (255, 255, 255), 50)

def get_promotion_ui_pos(sq_size, promo_moves, player_color):
    to_idx = promo_moves[0].to_idx
    row, col = get_row_col(to_idx)
    flipped = player_color == "b"
    draw_row, draw_col = flip_coords(row, col, flipped)
    is_white = promo_moves[0].piece[0] == "w"
    x = draw_col * sq_size
    if (is_white and not flipped) or (not is_white and flipped):
        y = draw_row * sq_size
    else:
        y = draw_row * sq_size + sq_size - sq_size * 4
    return x, y

def draw_promotion_ui(window: pygame.Surface, sq_size: int, images, promo_moves, player_color="w"):
    x, y = get_promotion_ui_pos(sq_size, promo_moves, player_color)
    pygame.draw.rect(window, (200, 200, 200), (x, y, sq_size, sq_size * 4))
    pygame.draw.rect(window, (100, 100, 100), (x, y, sq_size, sq_size * 4), 2)
    for i, move in enumerate(promo_moves):
        window.blit(images[move.promotion_piece], (x, y + i * sq_size))

def get_promotion_choice(pos, sq_size, promo_moves, player_color="w"):
    x, y = get_promotion_ui_pos(sq_size, promo_moves, player_color)
    for i, move in enumerate(promo_moves):
        rect = pygame.Rect(x, y + i * sq_size, sq_size, sq_size)
        if rect.collidepoint(pos):
            return move
    return None

def draw_board(window: pygame.Surface, sq_size: int, flipped=False):
    colors = [(255,255,255), (125,215,100)]
    for i in range(64):
        row, col = get_row_col(i)
        draw_row, draw_col = flip_coords(row, col, flipped)
        pygame.draw.rect(window, colors[(row+col)%2], (draw_col*sq_size, draw_row*sq_size, sq_size, sq_size)) 

def draw_pieces(window: pygame.Surface, sq_size: int, image, game_state: GameState, dragging=None, flipped=False):
    for i in range(64):
        if i == dragging:
            continue
        row, col = get_row_col(i)
        draw_row, draw_col = flip_coords(row, col, flipped)
        current = game_state.board[i]
        if current != "  ":
            window.blit(image[current], (draw_col*sq_size, draw_row*sq_size))

def draw_del_pieces(window: pygame.Surface, sq_size: int, del_image, game_state: GameState):
    width = sq_size * 8
    pygame.draw.rect(window, (128, 128, 128), (width, 0, sq_size * 2, sq_size * 8))
    counters = {"wp": 0, "wo": 0, "bp": 0, "bo": 0}
    sorted_pieces = sort_pieces(game_state.captured_pieces)
    for piece in sorted_pieces:
        color, is_pawn = piece[0], piece[1] == "p"
        if color == "w":
            horz_offset = width + (sq_size//2 if is_pawn else 0)
            key = "wp" if is_pawn else "wo"
        else:
            horz_offset = width + sq_size + (sq_size//2 if is_pawn else 0)
            key = "bp" if is_pawn else "bo"
        vertical_offset = counters[key] * sq_size//2
        counters[key] += 1
        window.blit(del_image[piece], (horz_offset, vertical_offset))

def draw_moves(window: pygame.Surface, sq_size: int, moves, flipped=False):
    alpha_surface = pygame.Surface(window.get_size(), pygame.SRCALPHA)
    for move in moves:
        row, col = get_row_col(move.to_idx)
        draw_row, draw_col = flip_coords(row, col, flipped)
        pygame.draw.rect(alpha_surface, (0,0,0,128), (draw_col*sq_size, draw_row*sq_size, sq_size, sq_size))
    window.blit(alpha_surface, (0,0))

def draw_game_over(window: pygame.Surface, game_state: GameState):
    width, height = window.get_size()
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    window.blit(overlay, (0, 0))
    font = pygame.font.Font(None, 74)

    if game_state.checkmate:
        winner = "White" if game_state.winner == "w" else "Black"
        text = f"Checkmate! {winner} wins"
    elif game_state.stalemate:
        text = "Stalemate! Draw"
    elif game_state.is_fifty_move_draw():
        text = "Draw by fifty-move rule"
    elif game_state.is_threefold_repetition():
        text = "Draw by threefold repetition"
    else:
        text = "Game Over"

    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(width//2, height//2))
    window.blit(text_surface, text_rect)

def sort_pieces(pieces: list[str]):
    order = {"Q": 0, "R": 1, "B": 2, "N": 3, "p": 4}
    sorted_list = sorted(pieces, key=lambda p: order[p[1]])
    return [p for p in sorted_list if p[0] == "w"] + [p for p in sorted_list if p[0] == "b"]

def get_row_col(loc: int) -> tuple[int, int]:
    return loc//8, loc%8

def flip_coords(row: int, col: int, flipped: bool) -> tuple[int, int]:
    return (7 - row, 7 - col) if flipped else (row, col)

def get_loc(pos: tuple[int, int], sq_size: int, flipped=False):
    row = pos[1]//sq_size
    col = pos[0]//sq_size
    row, col = flip_coords(row, col, flipped)
    return (row*8 + col)

if __name__ == "__main__":
    main()
