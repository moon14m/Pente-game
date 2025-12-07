from move import Move


class PenteGame:
    def __init__(self, config):
        self.config = config
        self.board = [[0] * config.COLS for _ in range(config.ROWS)]
        self.turn = 1
        self.captures = {1: 0, 2: 0}
        self.game_over = False
        self.winner = None
        self.resigned = False
        self.move_history = []
        self.last_move = None

    def make_move(self, row, col):
        if self.game_over or self.board[row][col] != 0:
            return False

        move = Move(row, col, self.turn)
        self.board[row][col] = self.turn
        self.last_move = move
        self.move_history.append(move)

        if self.check_captures(move):
            self.config.play_sound("capture")
        else:
            self.config.play_sound("move")

        if self.check_win(move):
            self.game_over = True
            self.winner = self.turn
            if self.winner == 2:
                self.config.play_sound("win_black")
            else:
                self.config.play_sound("win_white")
        else:
            self.turn = 3 - self.turn

        return True

    def resign(self, resigning_player=None):
        # If no specific player is passed, assume the current turn player is resigning
        if resigning_player is None:
            resigning_player = self.turn

        self.resigned = True
        self.game_over = True
        self.winner = 3 - resigning_player

    def check_captures(self, move):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        me = move.piece
        opp = 3 - me
        r, c_idx = move.row, move.col
        captured_any = False

        for dr, dc in directions:
            for sign in [1, -1]:
                r1, c1 = r + dr * sign, c_idx + dc * sign
                r2, c2 = r + 2 * dr * sign, c_idx + 2 * dc * sign
                r3, c3 = r + 3 * dr * sign, c_idx + 3 * dc * sign

                if 0 <= r3 < self.config.ROWS and 0 <= c3 < self.config.COLS:
                    if (
                        self.board[r1][c1] == opp
                        and self.board[r2][c2] == opp
                        and self.board[r3][c3] == me
                    ):
                        self.board[r1][c1] = 0
                        self.board[r2][c2] = 0
                        self.captures[me] += 2
                        captured_any = True

        return captured_any

    def check_win(self, move):
        if self.captures[self.turn] >= self.config.WIN_CAPTURE_COUNT:
            return True

        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        r, c_idx = move.row, move.col

        for dr, dc in directions:
            count = 1
            for i in range(1, 5):
                tr, tc = r + dr * i, c_idx + dc * i
                if (
                    0 <= tr < self.config.ROWS
                    and 0 <= tc < self.config.COLS
                    and self.board[tr][tc] == self.turn
                ):
                    count += 1
                else:
                    break
            for i in range(1, 5):
                tr, tc = r - dr * i, c_idx - dc * i
                if (
                    0 <= tr < self.config.ROWS
                    and 0 <= tc < self.config.COLS
                    and self.board[tr][tc] == self.turn
                ):
                    count += 1
                else:
                    break
            if count >= 5:
                return True
        return False

    def reset(self):
        self.__init__(self.config)
