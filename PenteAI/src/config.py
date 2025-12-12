import pygame
import os


class Config:
    def __init__(self):
        self.BOARD_WIDTH = 512
        self.BOARD_HEIGHT = 512
        self.PANEL_WIDTH = 200
        self.WIDTH = self.BOARD_WIDTH + self.PANEL_WIDTH
        self.HEIGHT = 512
        self.ROWS = 19
        self.COLS = 19
        self.WIN_CAPTURE_COUNT = 10
        self.sound_enabled = True
        self.sounds = {}

        
        self.FONT_NAME = "georgia"

        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.MENU_BACKGROUND_PATH = os.path.join(
            base_path, "assets", "images", "backgrounds", "menu-background.png"
        )

    def load_sounds(self):
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()
            except pygame.error:
                print("Warning: Audio device not available.")
                self.sound_enabled = False
                return

        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sound_dir = os.path.join(base_path, "assets", "sounds")

        self._load_sound("move", os.path.join(sound_dir, "move.wav"))
        self._load_sound("capture", os.path.join(sound_dir, "capture.wav"))
        self._load_sound("start", os.path.join(sound_dir, "game-started.wav"))
        self._load_sound("win_black", os.path.join(sound_dir, "black-wins.wav"))
        self._load_sound("win_white", os.path.join(sound_dir, "white-wins.wav"))

    def _load_sound(self, name, path):
        if self.sound_enabled:
            try:
                if os.path.exists(path):
                    self.sounds[name] = pygame.mixer.Sound(path)
                else:
                    print(f"Warning: Sound file not found: {path}")
            except Exception as e:
                print(f"Warning: Could not load sound {name}: {e}")

    def play_sound(self, name):
        if self.sound_enabled and name in self.sounds:
            self.sounds[name].play()
