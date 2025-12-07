class PenteHeuristics:
    SCORE_WIN = 1_000_000
    SCORE_BLOCK_WIN = 500_000
    SCORE_OPEN_FOUR = 100_000
    SCORE_CLOSED_FOUR = 5_000
    SCORE_OPEN_THREE = 10_000
    SCORE_SPLIT_THREE = 8_000
    SCORE_CLOSED_THREE = 1_000
    SCORE_OPEN_TWO = 500
    SCORE_CAPTURE_EXISTING = 50_000
    SCORE_CAPTURE_THREAT = 15_000
    SCORE_CENTER_CONTROL = 50

    @staticmethod
    def evaluate(board_clone, player_color):
        if board_clone.game_over:
            if board_clone.winner == player_color:
                return PenteHeuristics.SCORE_WIN * 10
            elif board_clone.winner is not None:
                return -PenteHeuristics.SCORE_WIN * 10
            return 0

        score = 0
        opponent = 3 - player_color

        score += (
            board_clone.captures[player_color] * PenteHeuristics.SCORE_CAPTURE_EXISTING
        )
        score -= board_clone.captures[opponent] * (
            PenteHeuristics.SCORE_CAPTURE_EXISTING * 1.2
        )

        my_shapes = PenteHeuristics._scan_board(board_clone, player_color)
        opp_shapes = PenteHeuristics._scan_board(board_clone, opponent)

        score += my_shapes
        score -= opp_shapes * 1.1
        return score

    @staticmethod
    def _scan_board(clone, color):
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        rows, cols = clone.rows, clone.cols
        board = clone.board

        for r in range(rows):
            for c in range(cols):
                if board[r][c] == color:
                    dist = abs(r - rows // 2) + abs(c - cols // 2)
                    score += max(0, (20 - dist) * PenteHeuristics.SCORE_CENTER_CONTROL)

                    for dr, dc in directions:
                        prev_r, prev_c = r - dr, c - dc
                        is_start = True
                        if 0 <= prev_r < rows and 0 <= prev_c < cols:
                            if board[prev_r][prev_c] == color:
                                is_start = False

                        if is_start:
                            score += PenteHeuristics._evaluate_line(
                                clone, r, c, dr, dc, color
                            )
        return score

    @staticmethod
    def _evaluate_line(clone, start_r, start_c, dr, dc, color):
        rows, cols = clone.rows, clone.cols
        board = clone.board
        sequence = []
        for i in range(6):
            tr, tc = start_r + dr * i, start_c + dc * i
            if 0 <= tr < rows and 0 <= tc < cols:
                sequence.append(board[tr][tc])
            else:
                sequence.append(-1)

        stone_count = 0
        gap_index = -1

        for i, val in enumerate(sequence):
            if val == color:
                stone_count += 1
            elif val == 0:
                if gap_index == -1:
                    gap_index = i
                else:
                    break
            else:
                break

        if stone_count >= 5:
            return PenteHeuristics.SCORE_WIN

        if stone_count == 4:
            open_start = PenteHeuristics._is_open(clone, start_r - dr, start_c - dc)

            stones_seen = 0
            last_stone_idx = -1
            for i, val in enumerate(sequence):
                if val == color:
                    stones_seen += 1
                    last_stone_idx = i
                if stones_seen == 4:
                    break

            check_r = start_r + dr * (last_stone_idx + 1)
            check_c = start_c + dc * (last_stone_idx + 1)
            open_end = PenteHeuristics._is_open(clone, check_r, check_c)

            open_count = (1 if open_start else 0) + (1 if open_end else 0)
            if open_count >= 1:
                return PenteHeuristics.SCORE_OPEN_FOUR
            return PenteHeuristics.SCORE_CLOSED_FOUR

        if stone_count == 3:
            is_split = False
            if len(sequence) >= 4:
                p = sequence[0:4]
                if (
                    p[0] == color and p[1] == 0 and p[2] == color and p[3] == color
                ) or (p[0] == color and p[1] == color and p[2] == 0 and p[3] == color):
                    is_split = True

            open_start = PenteHeuristics._is_open(clone, start_r - dr, start_c - dc)
            len_offset = 4 if is_split else 3
            check_r = start_r + dr * len_offset
            check_c = start_c + dc * len_offset
            open_end = PenteHeuristics._is_open(clone, check_r, check_c)

            open_count = (1 if open_start else 0) + (1 if open_end else 0)

            if is_split and open_count > 0:
                return PenteHeuristics.SCORE_SPLIT_THREE
            if open_count == 2:
                return PenteHeuristics.SCORE_OPEN_THREE
            if open_count == 1:
                return PenteHeuristics.SCORE_CLOSED_THREE

        if stone_count == 2:
            open_start = PenteHeuristics._is_open(clone, start_r - dr, start_c - dc)
            check_r = start_r + dr * 2
            check_c = start_c + dc * 2
            open_end = PenteHeuristics._is_open(clone, check_r, check_c)
            if open_start and open_end:
                return PenteHeuristics.SCORE_OPEN_TWO

        return 0

    @staticmethod
    def _is_open(clone, r, c):
        if 0 <= r < clone.rows and 0 <= c < clone.cols:
            return clone.board[r][c] == 0
        return False
