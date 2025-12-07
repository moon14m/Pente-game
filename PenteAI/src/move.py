class Move:
    def __init__(self, row, col, piece=0):
        self.row = row
        self.col = col
        self.piece = piece

    def __eq__(self, other):
        if isinstance(other, Move):
            return (
                self.row == other.row
                and self.col == other.col
                and self.piece == other.piece
            )
        return False

    def __repr__(self):
        color = "Black" if self.piece == 1 else "White"
        return f"Move({self.row}, {self.col}, {color})"
