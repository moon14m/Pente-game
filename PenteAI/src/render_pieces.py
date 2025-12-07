import pygame


class PieceRenderer:
    def __init__(self, config, theme, board_renderer):
        self.config = config
        self.theme = theme
        self.board = board_renderer
        self.radius = int(self.board.cell_size * 0.45)
        self.sprites = {}
        self._pre_render_sprites()

    def _pre_render_sprites(self):
        size = self.radius * 2 + 4
        center = size // 2

        def make_stone(color, outline_color, alpha=255, is_shadow=False):
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            if is_shadow:
                pygame.draw.circle(
                    surf, (0, 0, 0, 50), (center + 2, center + 2), self.radius
                )
            fill_color = (*color, alpha) if alpha < 255 else color
            pygame.draw.circle(surf, fill_color, (center, center), self.radius)
            if outline_color:
                pygame.draw.circle(
                    surf, outline_color, (center, center), self.radius, 1
                )
            return surf

        self.sprites[1] = make_stone(
            self.theme.stone_white, self.theme.stone_outline_white, is_shadow=True
        )
        self.sprites[2] = make_stone(
            self.theme.stone_black, self.theme.stone_outline_black, is_shadow=True
        )
        self.sprites["ghost_1"] = make_stone(self.theme.stone_white, None, alpha=150)
        self.sprites["ghost_2"] = make_stone(self.theme.stone_black, None, alpha=180)

    def draw_all(self, surface, board_state, last_move):
        offset = self.radius + 2
        for r in range(self.config.ROWS):
            for col in range(self.config.COLS):
                piece = board_state[r][col]
                if piece != 0:
                    x = self.board.margin + (col * self.board.cell_size)
                    y = self.board.margin + (r * self.board.cell_size)
                    surface.blit(self.sprites[piece], (x - offset, y - offset))
        if last_move:
            self._draw_last_move(surface, last_move)

    def draw_ghost(self, surface, row, col, turn):
        offset = self.radius + 2
        x = self.board.margin + (col * self.board.cell_size)
        y = self.board.margin + (row * self.board.cell_size)
        key = "ghost_1" if turn == 1 else "ghost_2"
        surface.blit(self.sprites[key], (x - offset, y - offset))

    def _draw_last_move(self, surface, move):
        x = self.board.margin + (move.col * self.board.cell_size)
        y = self.board.margin + (move.row * self.board.cell_size)
        color = (0, 0, 0) if move.piece == 1 else (255, 255, 255)
        pygame.draw.circle(surface, color, (x, y), self.radius * 0.5, 2)
