class BoardClone:
    def __init__(self, board_matrix, captures, turn, config):
        self.board = [row[:] for row in board_matrix]
        self.captures = captures.copy()
        self.turn = turn
        self.rows = config.ROWS
        self.cols = config.COLS
        self.win_capture_count = config.WIN_CAPTURE_COUNT
        self.game_over = False
        self.winner = None

    def make_move(self, row, col):
        if self.board[row][col] != 0:
            return False
        self.board[row][col] = self.turn
        self._check_captures(row, col)
        if self._check_win(row, col):
            self.game_over = True
            self.winner = self.turn
        self.turn = 3 - self.turn
        return True

    def _check_captures(self, r, c):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        me = self.turn
        opp = 3 - me
        for dr, dc in directions:
            for sign in [1, -1]:
                r1, c1 = r + dr * sign, c + dc * sign
                r2, c2 = r + 2 * dr * sign, c + 2 * dc * sign
                r3, c3 = r + 3 * dr * sign, c + 3 * dc * sign
                if 0 <= r3 < self.rows and 0 <= c3 < self.cols:
                    if (
                        self.board[r1][c1] == opp
                        and self.board[r2][c2] == opp
                        and self.board[r3][c3] == me
                    ):
                        self.board[r1][c1] = 0
                        self.board[r2][c2] = 0
                        self.captures[me] += 2

    def _check_win(self, r, c):
        if self.captures[self.turn] >= self.win_capture_count:
            return True
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            for i in range(1, 6):
                tr, tc = r + dr * i, c + dc * i
                if (
                    0 <= tr < self.rows
                    and 0 <= tc < self.cols
                    and self.board[tr][tc] == self.turn
                ):
                    count += 1
                else:
                    break
            for i in range(1, 6):
                tr, tc = r - dr * i, c - dc * i
                if (
                    0 <= tr < self.rows
                    and 0 <= tc < self.cols
                    and self.board[tr][tc] == self.turn
                ):
                    count += 1
                else:
                    break
            if count >= 5:
                return True
        return False
