from board_clone import BoardClone
from heuristics import PenteHeuristics
from performance_tracker import PerformanceTracker


class PenteAI:
    def __init__(self, config, ai_color, depth=2):
        self.config = config
        self.color = ai_color
        self.depth = depth
        self.opponent_color = 3 - ai_color 

    
    def get_best_move(self, game, tracker: PerformanceTracker):
        initial_state = BoardClone(game.board, game.captures, game.turn, self.config)
        possible_moves = self._get_relevant_moves(initial_state)

        if not possible_moves:
          
            if not initial_state.board_occupied():
                return (self.config.ROWS // 2, self.config.COLS // 2)
            return None

        
        center_r, center_c = self.config.ROWS // 2, self.config.COLS // 2
        possible_moves.sort(key=lambda m: abs(m[0] - center_r) + abs(m[1] - center_c))

        best_score = float("-inf")
        best_move = possible_moves[0]
        alpha = float("-inf")
        beta = float("inf")

        for r, c in possible_moves:
            next_state = BoardClone(
                initial_state.board,
                initial_state.captures,
                initial_state.turn,
                self.config,
            )
            
          
            if next_state.make_move(r, c): 
               
                score = self._minimax(next_state, self.depth - 1, alpha, beta, False, tracker) 
                
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break 
        return best_move

   
    def _minimax(self, state, depth, alpha, beta, maximizing, tracker: PerformanceTracker):
        
       
        tracker.increment_node() 
        
        if depth == 0 or state.game_over:
            return PenteHeuristics.evaluate(state, self.color)

       
        possible_moves = self._get_relevant_moves(state)
        if not possible_moves:
            
            return PenteHeuristics.evaluate(state, self.color) 

        if maximizing:
            max_eval = float("-inf")
            
            for r, c in possible_moves:
                child = BoardClone(state.board, state.captures, state.turn, self.config)
                if child.make_move(r, c):
                  
                    eval = self._minimax(child, depth - 1, alpha, beta, False, tracker)
                    
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float("inf")
            
            for r, c in possible_moves:
                child = BoardClone(state.board, state.captures, state.turn, self.config)
                if child.make_move(r, c):
                    
                    eval = self._minimax(child, depth - 1, alpha, beta, True, tracker)
                    
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

    def _get_relevant_moves(self, state):
        rows, cols = state.rows, state.cols
        board = state.board
        relevant = set()
        occupied = []

        for r in range(rows):
            for c in range(cols):
                if board[r][c] != 0:
                    occupied.append((r, c))

        if not occupied:
            
            return [(rows // 2, cols // 2)]

        
        radius = 2 if self.depth > 3 else 1 
        if not occupied or len(occupied) < 5: 
             radius = 2

        
        for r, c in occupied:
            for dr in range(-radius, radius + 1):
                for dc in range(-radius, radius + 1):
                   
                    if dr == 0 and dc == 0:
                        continue 
                        
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == 0:
                        relevant.add((nr, nc))
        return list(relevant)

    def _get_opponent_color(self):
        return 3 - self.color