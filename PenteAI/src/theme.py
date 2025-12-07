class Theme:
    def __init__(
        self,
        name,
        board_bg,
        line_color,
        coord_color,
        stone_black,
        stone_white,
        stone_outline_black,
        stone_outline_white,
        panel_bg,
        panel_text,
    ):
        self.name = name
        self.board_bg = board_bg
        self.line_color = line_color
        self.coord_color = coord_color
        self.stone_black = stone_black
        self.stone_white = stone_white
        self.stone_outline_black = stone_outline_black
        self.stone_outline_white = stone_outline_white
        self.panel_bg = panel_bg
        self.panel_text = panel_text


THEME_WOOD = Theme(
    name="Kaya Wood",
    board_bg=(220, 179, 92),
    line_color=(30, 30, 30),
    coord_color=(50, 40, 20),
    stone_black=(30, 30, 30),
    stone_white=(245, 245, 245),
    stone_outline_black=(0, 0, 0),
    stone_outline_white=(200, 200, 200),
    panel_bg=(240, 240, 240),
    panel_text=(10, 10, 10),
)

THEME_SUNSET = Theme(
    name="Desert Sunset",
    board_bg=(255, 218, 185),
    line_color=(139, 69, 19),
    coord_color=(160, 82, 45),
    stone_black=(70, 45, 30),
    stone_white=(255, 248, 220),
    stone_outline_black=(40, 25, 15),
    stone_outline_white=(210, 180, 140),
    panel_bg=(250, 235, 215),
    panel_text=(101, 67, 33),
)

THEME_OCEAN_MIST = Theme(
    name="Ocean Mist",
    board_bg=(173, 216, 230),
    line_color=(32, 64, 96),
    coord_color=(40, 80, 120),
    stone_black=(40, 100, 120),
    stone_white=(230, 240, 255),
    stone_outline_black=(20, 50, 60),
    stone_outline_white=(150, 180, 210),
    panel_bg=(210, 230, 245),
    panel_text=(30, 60, 90),
)

THEME_FOREST = Theme(
    name="Forest Green",
    board_bg=(143, 188, 143),
    line_color=(34, 139, 34),
    coord_color=(0, 100, 0),
    stone_black=(47, 79, 79),
    stone_white=(245, 255, 250),
    stone_outline_black=(0, 50, 0),
    stone_outline_white=(152, 251, 152),
    panel_bg=(240, 255, 240),
    panel_text=(0, 70, 0),
)

THEME_INDUSTRIAL_TECH = Theme(
    name="Industrial Tech Blue",
    board_bg=(28, 28, 40),
    line_color=(70, 130, 180),
    coord_color=(160, 180, 220),
    stone_black=(139, 0, 0),
    stone_white=(220, 230, 245),
    stone_outline_black=(100, 150, 200),
    stone_outline_white=(170, 200, 230),
    panel_bg=(40, 40, 55),
    panel_text=(200, 220, 255),
)
