import pygame


class BoardRenderer:
    def __init__(self, config, theme):
        self.config = config
        self.theme = theme
        self.margin = 35
        self.width = config.BOARD_WIDTH
        self.height = config.BOARD_HEIGHT
        self.grid_w = self.width - (2 * self.margin)
        self.cell_size = self.grid_w / (config.COLS - 1)
        self.snap_dist_sq = (self.cell_size * 0.4) ** 2
        self.cached_background = pygame.Surface((self.width, self.height))
        self._pre_render_board()

    def _pre_render_board(self):
        self.cached_background.fill(self.theme.board_bg)
        line_color = self.theme.line_color

        for i in range(self.config.COLS):
            pos = int(self.margin + (i * self.cell_size))
            pygame.draw.line(
                self.cached_background,
                line_color,
                (pos, self.margin),
                (pos, self.height - self.margin),
                1,
            )
            pygame.draw.line(
                self.cached_background,
                line_color,
                (self.margin, pos),
                (self.width - self.margin, pos),
                1,
            )

        star_points = [3, 9, 15]
        for r in star_points:
            for col in star_points:
                x = int(self.margin + (col * self.cell_size))
                y = int(self.margin + (r * self.cell_size))
                pygame.draw.circle(self.cached_background, line_color, (x, y), 3)

        font = pygame.font.SysFont(self.config.FONT_NAME, 12, bold=True)
        letters = "ABCDEFGHJKLMNOPQRST"

        for i in range(self.config.COLS):
            lbl = font.render(letters[i], True, self.theme.coord_color)
            rect = lbl.get_rect(
                center=(self.margin + i * self.cell_size, self.margin / 2)
            )
            self.cached_background.blit(lbl, rect)

            num_str = str(self.config.ROWS - i)
            num = font.render(num_str, True, self.theme.coord_color)
            self.cached_background.blit(
                num,
                num.get_rect(
                    center=(self.margin / 2, self.margin + i * self.cell_size)
                ),
            )
            self.cached_background.blit(
                num,
                num.get_rect(
                    center=(
                        self.width - self.margin / 2,
                        self.margin + i * self.cell_size,
                    )
                ),
            )

    def draw(self, surface):
        surface.blit(self.cached_background, (0, 0))

    def get_grid_pos(self, mouse_x, mouse_y):
        if mouse_x > self.width:
            return None
        col = int(round((mouse_x - self.margin) / self.cell_size))
        row = int(round((mouse_y - self.margin) / self.cell_size))
        if not (0 <= col < self.config.COLS and 0 <= row < self.config.ROWS):
            return None
        target_x = self.margin + (col * self.cell_size)
        target_y = self.margin + (row * self.cell_size)
        dist_sq = (mouse_x - target_x) ** 2 + (mouse_y - target_y) ** 2
        if dist_sq <= self.snap_dist_sq:
            return row, col
        return None
