import pygame


class Menu:
    def __init__(self, config):
        self.config = config
        self.current_theme_name = "Kaya Wood"
        self.state = "MAIN"
        self.selected_difficulty = 2

        self._init_resources()
        self._init_ui()

    def update_theme_name(self, name):
        self.current_theme_name = name

    def _init_resources(self):
        self.bg_image = None
        try:
            img = pygame.image.load(self.config.MENU_BACKGROUND_PATH).convert()
            self.bg_image = pygame.transform.scale(
                img, (self.config.WIDTH, self.config.HEIGHT)
            )
        except Exception as e:
            print(f"Error loading menu background: {e}")

       
        self.font_title = pygame.font.SysFont(self.config.FONT_NAME, 60, bold=True)
        self.font_btn = pygame.font.SysFont(self.config.FONT_NAME, 20, bold=True)
        self.font_small = pygame.font.SysFont(self.config.FONT_NAME, 18)

    def _init_ui(self):
        cx = self.config.WIDTH // 2
        cy = self.config.HEIGHT // 2

        BTN_W = 260
        BTN_H = 50

        self.btn_pvp = pygame.Rect(0, 0, BTN_W, BTN_H)
        self.btn_pvp.center = (cx, cy)

        self.btn_ai = pygame.Rect(0, 0, BTN_W, BTN_H)
        self.btn_ai.center = (cx, cy + 60)

        self.btn_theme = pygame.Rect(0, 0, BTN_W, BTN_H)
        self.btn_theme.center = (cx, cy + 120)

        self.btn_quit = pygame.Rect(0, 0, BTN_W, BTN_H)
        self.btn_quit.center = (cx, cy + 180)

        base_y = cy - 30

        self.btn_ai_white = pygame.Rect(0, 0, BTN_W, BTN_H)
        self.btn_ai_white.center = (cx, base_y)

        self.btn_ai_black = pygame.Rect(0, 0, BTN_W, BTN_H)
        self.btn_ai_black.center = (cx, base_y + 60)

        self.btn_diff_down = pygame.Rect(0, 0, 40, 40)
        self.btn_diff_down.center = (cx - 100, base_y + 130)

        self.btn_diff_up = pygame.Rect(0, 0, 40, 40)
        self.btn_diff_up.center = (cx + 100, base_y + 130)

        self.btn_back = pygame.Rect(0, 0, BTN_W, BTN_H)
        self.btn_back.center = (cx, base_y + 190)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.state == "MAIN":
                if self.btn_pvp.collidepoint(event.pos):
                    return "PLAY_PVP"
                elif self.btn_ai.collidepoint(event.pos):
                    self.state = "AI_SETUP"
                    return None
                elif self.btn_theme.collidepoint(event.pos):
                    return "NEXT_THEME"
                elif self.btn_quit.collidepoint(event.pos):
                    return "QUIT"

            elif self.state == "AI_SETUP":
                if self.btn_ai_white.collidepoint(event.pos):
                    return ("PLAY_AI", 1)
                elif self.btn_ai_black.collidepoint(event.pos):
                    return ("PLAY_AI", 2)

                elif self.btn_diff_down.collidepoint(event.pos):
                    if self.selected_difficulty > 1:
                        self.selected_difficulty -= 1
                elif self.btn_diff_up.collidepoint(event.pos):
                    if self.selected_difficulty < 4:
                        self.selected_difficulty += 1

                elif self.btn_back.collidepoint(event.pos):
                    self.state = "MAIN"
                    return None
        return None

    def draw(self, screen):
        WOOD_LIGHT = (210, 180, 140)
        WOOD_DARK = (139, 69, 19)
        WOOD_TEXT = (50, 30, 10)

        if self.bg_image:
            screen.blit(self.bg_image, (0, 0))
        else:
            screen.fill((40, 40, 50))

        overlay = pygame.Surface(
            (self.config.WIDTH, self.config.HEIGHT), pygame.SRCALPHA
        )
        pygame.draw.rect(
            overlay,
            (0, 0, 0, 100),
            (
                0,
                self.config.HEIGHT // 2 - 80,
                self.config.WIDTH,
                self.config.HEIGHT // 2 + 100,
            ),
        )
        screen.blit(overlay, (0, 0))

        self._draw_text_centered(
            screen, "PENTE AI", self.font_title, (self.config.WIDTH // 2, 80)
        )

        if self.state == "MAIN":
            self._draw_button(
                screen, self.btn_pvp, "Player vs Player", WOOD_LIGHT, WOOD_TEXT
            )
            self._draw_button(
                screen, self.btn_ai, "Player vs AI", WOOD_LIGHT, WOOD_TEXT
            )
            self._draw_button(
                screen,
                self.btn_theme,
                f"Theme: {self.current_theme_name}",
                (222, 184, 135),
                WOOD_TEXT,
                font_size=20,
            )
            self._draw_button(
                screen, self.btn_quit, "Quit", (160, 82, 45), (255, 230, 200)
            )

        elif self.state == "AI_SETUP":
            self._draw_text_centered(
                screen,
                "Select Your Color",
                self.font_btn,
                (self.config.WIDTH // 2, self.config.HEIGHT // 2 - 80),
            )

            self._draw_button(
                screen,
                self.btn_ai_white,
                "Play as White (First)",
                (230, 220, 200),
                (20, 20, 20),
            )
            self._draw_button(
                screen,
                self.btn_ai_black,
                "Play as Black (Second)",
                (101, 67, 33),
                (240, 240, 240),
            )

            diff_panel_rect = pygame.Rect(0, 0, 180, 40)
            diff_panel_rect.center = (
                self.config.WIDTH // 2,
                self.btn_diff_down.centery,
            )
            pygame.draw.rect(screen, (0, 0, 0, 80), diff_panel_rect, border_radius=5)

            self._draw_button(screen, self.btn_diff_down, "-", WOOD_LIGHT, WOOD_TEXT)
            self._draw_button(screen, self.btn_diff_up, "+", WOOD_LIGHT, WOOD_TEXT)

            self._draw_text_centered(
                screen,
                f"Depth: {self.selected_difficulty}",
                self.font_btn,
                (self.config.WIDTH // 2, self.btn_diff_down.centery),
            )
            self._draw_button(
                screen, self.btn_back, "Back", (160, 82, 45), (255, 230, 200)
            )

    def _draw_button(
        self, screen, rect, text, color, text_color=(30, 30, 30), font_size=20
    ):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = rect.collidepoint(mouse_pos)

        if is_hover:
            draw_color = [min(c + 30, 255) for c in color]
            draw_rect = rect.inflate(4, 4)
        else:
            draw_color = color
            draw_rect = rect

        pygame.draw.rect(screen, draw_color, draw_rect, border_radius=8)
        pygame.draw.rect(screen, (60, 40, 10), draw_rect, 3, border_radius=8)

        font = (
            self.font_btn
            if font_size == 20
            else pygame.font.SysFont(self.config.FONT_NAME, font_size, bold=True)
        )
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    def _draw_text_centered(self, screen, text, font, center):
        shadow_surf = font.render(text, True, (0, 0, 0))
        shadow_rect = shadow_surf.get_rect(center=(center[0] + 2, center[1] + 2))
        screen.blit(shadow_surf, shadow_rect)

        main_surf = font.render(text, True, (255, 255, 255))
        main_rect = main_surf.get_rect(center=center)
        screen.blit(main_surf, main_rect)
