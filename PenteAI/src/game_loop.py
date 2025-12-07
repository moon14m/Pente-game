import pygame
import sys
from config import Config
from pente_game import PenteGame
from pente_ai import PenteAI
from theme import *
from render_board import BoardRenderer
from render_pieces import PieceRenderer
from render_panel import PanelRenderer
from menu import Menu


class GameApp:
    def __init__(self):
        pygame.init()
        self.config = Config()
        self.config.load_sounds()
        self.screen = pygame.display.set_mode((self.config.WIDTH, self.config.HEIGHT))
        pygame.display.set_caption("Pente AI")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "MENU"
        self.themes = [
            THEME_WOOD,
            THEME_SUNSET,
            THEME_OCEAN_MIST,
            THEME_FOREST,
            THEME_INDUSTRIAL_TECH,
        ]
        self.current_theme_idx = 0
        self.game = PenteGame(self.config)
        self.menu = Menu(self.config)
        self.game_mode = "PVP"
        self.ai_player = None
        self.player_color = 1
        self.last_ai_move_time = 0
        self.ai_delay_ms = 500

        self._init_graphics(self.themes[self.current_theme_idx])
        self.menu.update_theme_name(self.themes[self.current_theme_idx].name)

    def _init_graphics(self, theme):
        self.board_gfx = BoardRenderer(self.config, theme)
        self.piece_gfx = PieceRenderer(self.config, theme, self.board_gfx)
        self.panel_gfx = PanelRenderer(self.config, theme)

    def run(self):
        while self.running:
            self._handle_input()
            self._update_ai()
            self._draw()
            self.clock.tick(60)
        self._shutdown()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if self.state == "MENU":
                action = self.menu.handle_event(event)
                if action == "PLAY_PVP":
                    self.game_mode = "PVP"
                    self._start_game()
                elif isinstance(action, tuple) and action[0] == "PLAY_AI":
                    self.game_mode = "AI"
                    self.player_color = action[1]
                    ai_color = 3 - self.player_color
                    self.ai_player = PenteAI(
                        self.config, ai_color, depth=self.menu.selected_difficulty
                    )
                    self._start_game()
                elif action == "NEXT_THEME":
                    self.current_theme_idx = (self.current_theme_idx + 1) % len(
                        self.themes
                    )
                    self.menu.update_theme_name(
                        self.themes[self.current_theme_idx].name
                    )
                elif action == "QUIT":
                    self.running = False

            elif self.state == "GAME":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "MENU"
                        self.menu.state = "MAIN"
                        return

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if (
                        self.panel_gfx.btn_resign.collidepoint(event.pos)
                        and not self.game.game_over
                    ):
                        resigning_player = self.game.turn
                        if self.game_mode == "AI":
                            resigning_player = self.player_color

                        self.game.resign(resigning_player)
                    else:
                        self._on_game_click()

        if self.state == "GAME" and not self.game.game_over:
            is_human_turn = (self.game_mode == "PVP") or (
                self.game.turn == self.player_color
            )
            if is_human_turn:
                self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                self.hover_pos = self.board_gfx.get_grid_pos(self.mouse_x, self.mouse_y)
            else:
                self.hover_pos = None
        else:
            self.hover_pos = None

    def _start_game(self):
        self._init_graphics(self.themes[self.current_theme_idx])
        self.state = "GAME"
        self.menu.state = "MAIN"
        self.game.reset()
        self.config.play_sound("start")
        self.last_ai_move_time = pygame.time.get_ticks()

    def _update_ai(self):
        if self.state == "GAME" and not self.game.game_over and self.game_mode == "AI":
            if self.game.turn != self.player_color:
                if pygame.time.get_ticks() - self.last_ai_move_time > self.ai_delay_ms:
                    self._draw()
                    move = self.ai_player.get_best_move(self.game)
                    if move:
                        self.game.make_move(move[0], move[1])
                    self.last_ai_move_time = pygame.time.get_ticks()

    def _on_game_click(self):
        if self.game.game_over:
            self.game.reset()
        elif self.hover_pos:
            if self.game_mode == "AI" and self.game.turn != self.player_color:
                return
            row, col = self.hover_pos
            if self.game.make_move(row, col):
                self.last_ai_move_time = pygame.time.get_ticks()

    def _draw(self):
        if self.state == "MENU":
            self.menu.draw(self.screen)
        else:
            self._draw_game()
        pygame.display.flip()

    def _draw_game(self):
        self.board_gfx.draw(self.screen)
        self.piece_gfx.draw_all(self.screen, self.game.board, self.game.last_move)
        if not self.game.game_over and self.hover_pos:
            r, c = self.hover_pos
            if self.game.board[r][c] == 0:
                self.piece_gfx.draw_ghost(self.screen, r, c, self.game.turn)
        self.panel_gfx.draw(self.screen, self.game)

    def _shutdown(self):
        pygame.quit()
        sys.exit()
