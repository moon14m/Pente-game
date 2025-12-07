import pygame


class PanelRenderer:
    def __init__(self, config, theme):
        self.config = config
        self.theme = theme
        self.rect = pygame.Rect(
            config.BOARD_WIDTH, 0, config.PANEL_WIDTH, config.HEIGHT
        )

        self.font_large = pygame.font.SysFont(self.config.FONT_NAME, 22)
        self.font_std = pygame.font.SysFont(self.config.FONT_NAME, 18)
        self.font_bold = pygame.font.SysFont(self.config.FONT_NAME, 18, bold=True)
        self.font_btn = pygame.font.SysFont(self.config.FONT_NAME, 16, bold=True)

        self.lbl_captures = self.font_bold.render(
            "Captures:", True, self.theme.panel_text
        )
        self.btn_resign = pygame.Rect(
            self.config.BOARD_WIDTH + 40, self.config.HEIGHT - 80, 120, 40
        )

    def draw(self, surface, game):
        pygame.draw.rect(surface, self.theme.panel_bg, self.rect)
        start_x = self.config.BOARD_WIDTH + 20
        text_color = self.theme.panel_text

        if game.game_over:
            if game.resigned:
                loser = "White" if game.winner == 2 else "Black"
                txt = f"{loser} Resigned"
            else:
                winner = "White" if game.winner == 1 else "Black"
                txt = f"{winner} Wins!"
        else:
            txt = "White's Turn" if game.turn == 1 else "Black's Turn"

        surf_turn = self.font_large.render(txt, True, text_color)
        surface.blit(surf_turn, (start_x, 30))
        surface.blit(self.lbl_captures, (start_x, 80))

        surf_cap_w = self.font_std.render(
            f"White: {game.captures[1]}", True, text_color
        )
        surf_cap_b = self.font_std.render(
            f"Black: {game.captures[2]}", True, text_color
        )

        surface.blit(surf_cap_w, (start_x, 110))
        surface.blit(surf_cap_b, (start_x, 140))

        if game.game_over:
            surf_restart = self.font_std.render(
                "Click Board to Restart", True, (50, 50, 200)
            )
            surface.blit(surf_restart, (start_x, 200))
        else:
            self._draw_button(surface, self.btn_resign, "Resign", (200, 100, 100))

    def _draw_button(self, screen, rect, text, color):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = rect.collidepoint(mouse_pos)
        draw_color = [min(c + 30, 255) for c in color] if is_hover else color
        draw_rect = rect.inflate(4, 4) if is_hover else rect

        pygame.draw.rect(screen, draw_color, draw_rect, border_radius=8)
        pygame.draw.rect(screen, (50, 50, 50), draw_rect, 2, border_radius=8)

        text_surf = self.font_btn.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)
