class GameBoard:
    def __init__(self, canvas):
        self.canvas = canvas
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.create_board()
        self.place_pieces()

    def create_board(self):
        for row in range(8):
            for col in range(8):
                color = "BurlyWood" if (row + col) % 2 == 0 else "black"
                self.canvas.create_rectangle(col * 100, row * 100, (col + 1) * 100, (row + 1) * 100, fill=color)

    def place_pieces(self):
        for row in range(8):
            for col in range(8):
                if row < 3 and (row + col) % 2 != 0:
                    self.board[row][col] = self.canvas.create_oval(col * 100 + 10, row * 100 + 10, (col + 1) * 100 - 10,
                                                                   (row + 1) * 100 - 10, fill="red", tags="piece")
                elif row > 4 and (row + col) % 2 != 0:
                    self.board[row][col] = self.canvas.create_oval(col * 100 + 10, row * 100 + 10, (col + 1) * 100 - 10,
                                                                   (row + 1) * 100 - 10, fill="blue", tags="piece")

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_piece_color(self, row, col):
        piece = self.board[row][col]
        if piece:
            return self.canvas.itemcget(piece, "fill")
        return None

    def is_king(self, piece):
        return self.canvas.itemcget(piece, "outline") == "gold"

    def move_piece(self, old_row, old_col, new_row, new_col):
        piece = self.board[old_row][old_col]
        self.canvas.move(piece, (new_col - old_col) * 100, (new_row - old_row) * 100)
        self.board[new_row][new_col] = piece
        self.board[old_row][old_col] = None

    def capture_piece(self, row, col):
        piece_color = self.canvas.itemcget(self.board[row][col], "fill")
        self.canvas.delete(self.board[row][col])
        self.board[row][col] = None
        return piece_color

    def promote_to_king(self, row, col):
        piece = self.board[row][col]
        self.canvas.itemconfig(piece, outline="gold", width=4)

    def move_king(self, old_row, old_col, new_row, new_col):
        delta_row = (new_row - old_row) // abs(new_row - old_row)
        delta_col = (new_col - old_col) // abs(new_col - old_col)
        current_row, current_col = old_row + delta_row, old_col + delta_col
        while current_row != new_row and current_col != new_col:
            if self.board[current_row][current_col] is not None:
                self.capture_piece(current_row, current_col)
            current_row += delta_row
            current_col += delta_col
