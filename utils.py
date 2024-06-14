def create_board(canvas):
    for row in range(8):
        for col in range(8):
            color = "BurlyWood" if (row + col) % 2 == 0 else "black"
            canvas.create_rectangle(col * 100, row * 100, (col + 1) * 100, (row + 1) * 100, fill=color)

def place_pieces(canvas, board):
    for row in range(8):
        for col in range(8):
            if row < 3 and (row + col) % 2 != 0:
                board[row][col] = canvas.create_oval(col * 100 + 10, row * 100 + 10, (col + 1) * 100 - 10,
                                                     (row + 1) * 100 - 10, fill="red", tags="piece")
            elif row > 4 and (row + col) % 2 != 0:
                board[row][col] = canvas.create_oval(col * 100 + 10, row * 100 + 10, (col + 1) * 100 - 10,
                                                     (row + 1) * 100 - 10, fill="blue", tags="piece")

