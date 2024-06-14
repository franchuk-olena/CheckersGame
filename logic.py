import tkinter as tk
from tkinter import messagebox


class CheckersGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Шашки")
        self.canvas = tk.Canvas(root, width=800, height=800)
        self.canvas.pack(side=tk.LEFT)
        self.root.attributes('-fullscreen', True)
        self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


        # Панель інформації про гру
        self.info_frame = tk.Frame(root)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y, pady=150, padx=60)  # Змініть значення padx за необхідності

        self.turn_label = tk.Label(self.info_frame, text="Хід: Червоні", font=("Arial", 16))
        self.turn_label.pack(pady=20)

        self.red_captured_label = tk.Label(self.info_frame, text="Захоплено червоними: 0", font=("Arial", 16))
        self.red_captured_label.pack(pady=20)

        self.blue_captured_label = tk.Label(self.info_frame, text="Захоплено синіми: 0", font=("Arial", 16))
        self.blue_captured_label.pack(pady=20)

        self.turn_button = tk.Button(self.info_frame, text="Поточний хід: Червоні", font=("Arial", 16),
                                     command=self.show_turn)
        self.turn_button.pack(pady=20)

        # Додаємо кнопки "Завершити гру" та "Почати заново" з коричневим кольором
        self.end_game_button = tk.Button(self.info_frame, text="Завершити гру", font=("Arial", 16),
                                         command=self.end_game, bg="BurlyWood", fg="white")
        self.end_game_button.pack(pady=10)

        self.restart_game_button = tk.Button(self.info_frame, text="Почати заново", font=("Arial", 16),
                                             command=self.restart_game, bg="BurlyWood", fg="white")
        self.restart_game_button.pack(pady=10)

        self.red_captured = 0
        self.blue_captured = 0

        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.create_board()
        self.place_pieces()
        self.selected_piece = None
        self.turn = "red"
        self.canvas.bind("<Button-1>", self.select_piece)

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

    def select_piece(self, event):
        col = event.x // 100
        row = event.y // 100

        # Якщо вибраний шматок того ж кольору, що і поточний хід, то вибираємо його
        if self.board[row][col] and self.canvas.itemcget(self.board[row][col], "fill") == self.turn:
            self.selected_piece = (row, col)
        elif self.selected_piece and self.is_valid_move(self.selected_piece, (row, col)):
            # Перевірка наявності обов'язкових захоплень
            if self.has_mandatory_capture():
                if self.is_valid_capture_move(self.selected_piece, (row, col)):
                    self.move_piece(row, col, True)  # Передаємо параметр True для можливості багаторазового захоплення
            else:
                self.move_piece(row, col, False)

    def is_valid_move(self, old_pos, new_pos):
        old_row, old_col = old_pos
        new_row, new_col = new_pos
        piece = self.board[old_row][old_col]
        is_king = self.canvas.itemcget(piece, "outline") == "gold"

        if not is_king:
            direction = 1 if self.turn == 'red' else -1

            if abs(new_row - old_row) == 1 and abs(new_col - old_col) == 1:
                return self.board[new_row][new_col] is None and (new_row - old_row == direction)

            if abs(new_row - old_row) == 2 and abs(new_col - old_col) == 2:
                mid_row, mid_col = (old_row + new_row) // 2, (old_col + new_col) // 2
                return (self.board[mid_row][mid_col] is not None and
                        self.canvas.itemcget(self.board[mid_row][mid_col], "fill") != self.turn and
                        self.board[new_row][new_col] is None)

        else:
            if abs(new_row - old_row) == abs(new_col - old_col):
                delta_row = (new_row - old_row) // abs(new_row - old_row)
                delta_col = (new_col - old_col) // abs(new_col - old_col)
                row, col = old_row + delta_row, old_col + delta_col
                captured = False
                while row != new_row and col != new_col:
                    if self.board[row][col] is not None:
                        if self.canvas.itemcget(self.board[row][col], "fill") == self.turn:
                            return False
                        elif not captured:
                            captured = True
                        else:
                            return False
                    row += delta_row
                    col += delta_col
                return True

        return False

    def is_valid_capture_move(self, old_pos, new_pos):
        old_row, old_col = old_pos
        new_row, new_col = new_pos
        piece = self.board[old_row][old_col]
        is_king = self.canvas.itemcget(piece, "outline") == "gold"

        if not is_king:
            direction = 1 if self.turn == 'red' else -1

            if abs(new_row - old_row) == 2 and abs(new_col - old_col) == 2:
                mid_row, mid_col = (old_row + new_row) // 2, (old_col + new_col) // 2
                return (self.board[mid_row][mid_col] is not None and
                        self.canvas.itemcget(self.board[mid_row][mid_col], "fill") != self.turn and
                        self.board[new_row][new_col] is None)

        else:
            if abs(new_row - old_row) == abs(new_col - old_col):
                delta_row = (new_row - old_row) // abs(new_row - old_row)
                delta_col = (new_col - old_col) // abs(new_col - old_col)
                row, col = old_row + delta_row, old_col + delta_col
                captured = False
                while row != new_row and col != new_col:
                    if self.board[row][col] is not None:
                        if self.canvas.itemcget(self.board[row][col], "fill") == self.turn:
                            return False
                        elif not captured:
                            captured = True
                        else:
                            # Якщо зустрічається інша шашка противника, то хід неможливий
                            return False
                    row += delta_row
                    col += delta_col
                return captured and self.board[new_row][new_col] is None

        return False

    def move_piece(self, row, col, capture_again):
        old_row, old_col = self.selected_piece
        piece = self.board[old_row][old_col]
        is_king = self.canvas.itemcget(piece, "outline") == "gold"

        if is_king:
            delta_row = (row - old_row) // abs(row - old_row)
            delta_col = (col - old_col) // abs(col - old_col)
            current_row, current_col = old_row + delta_row, old_col + delta_col
            captured = False
            while current_row != row and current_col != col:
                if self.board[current_row][current_col] is not None:
                    self.capture_piece(current_row, current_col)
                    captured = True
                current_row += delta_row
                current_col += delta_col
        elif abs(row - old_row) == 2 and abs(col - old_col) == 2:
            mid_row, mid_col = (old_row + row) // 2, (old_col + col) // 2
            self.capture_piece(mid_row, mid_col)

        self.canvas.move(piece, (col - old_col) * 100, (row - old_row) * 100)
        self.board[row][col] = piece
        self.board[old_row][old_col] = None
        self.promote_to_king(row, col)
        self.selected_piece = None

        # Перевірка переможця після кожного ходу
        self.check_winner()

        # Перевірка на можливість ще одного захоплення для цього ж гравця
        if capture_again and self.has_mandatory_capture_for_piece(row, col):
            self.selected_piece = (row, col)
        else:
            self.turn = "blue" if self.turn == "red" else "red"
            self.update_turn_label()

    def capture_piece(self, mid_row, mid_col):
        captured_piece = self.canvas.itemcget(self.board[mid_row][mid_col], "fill")
        self.canvas.delete(self.board[mid_row][mid_col])
        self.board[mid_row][mid_col] = None
        if captured_piece == "red":
            self.red_captured += 1
            self.red_captured_label.config(text=f"Захоплено червоними: {self.red_captured}")
        else:
            self.blue_captured += 1
            self.blue_captured_label.config(text=f"Захоплено синіми: {self.blue_captured}")

    def promote_to_king(self, row, col):
        piece = self.board[row][col]
        if (self.turn == "red" and row == 7) or (self.turn == "blue" and row == 0):
            self.canvas.itemconfig(piece, outline="gold", width=4)

    def update_turn_label(self):
        turn_text = "Червоні" if self.turn == "red" else "Сині"
        self.turn_label.config(text=f"Хід: {turn_text}")
        self.turn_button.config(text=f"Поточний хід: {turn_text}")

    def show_turn(self):
        current_turn = "Червоні" if self.turn == "red" else "Сині"
        messagebox.showinfo("Поточний хід", f"Зараз хід {current_turn}")

    def has_mandatory_capture(self):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and self.canvas.itemcget(piece, "fill") == self.turn:
                    if self.has_capture_move(row, col):
                        return True
        return False

    def has_mandatory_capture_for_piece(self, row, col):
        piece = self.board[row][col]
        if piece and self.canvas.itemcget(piece, "fill") == self.turn:
            return self.has_capture_move(row, col)
        return False

    def has_capture_move(self, row, col):
        piece = self.board[row][col]
        is_king = self.canvas.itemcget(piece, "outline") == "gold"
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for direction in directions:
            if is_king:
                for i in range(1, 8):
                    new_row = row + direction[0] * i
                    new_col = col + direction[1] * i
                    if 0 <= new_row < 8 and 0 <= new_col < 8 and self.is_valid_capture_move((row, col), (new_row, new_col)):
                        return True
            else:
                new_row = row + direction[0] * 2
                new_col = col + direction[1] * 2
                if 0 <= new_row < 8 and 0 <= new_col < 8 and self.is_valid_capture_move((row, col), (new_row, new_col)):
                    return True
        return False

    def end_game(self):
        if messagebox.askyesno("Завершити гру", "Ви дійсно хочете завершити поточну гру?"):
            self.root.destroy()

    def restart_game(self):
        if messagebox.askyesno("Почати заново", "Ви дійсно хочете почати нову гру?"):
            self.root.destroy()
            root = tk.Tk()
            game = CheckersGame(root)
            root.mainloop()

    def check_winner(self):
        if self.red_captured == 12:
            messagebox.showinfo("Гра завершена", "Сині перемогли!")
            self.end_game()
        elif self.blue_captured == 12:
            messagebox.showinfo("Гра завершена", "Червоні перемогли!")
            self.end_game()


if __name__ == "__main__":
    root = tk.Tk()
    game = CheckersGame(root)
    root.mainloop()


#зі всіма гарними параметрами



    def move_king(self, old_row, old_col, new_row, new_col):
        delta_row = (new_row - old_row) // abs(new_row - old_row)
        delta_col = (new_col - old_col) // abs(new_col - old_col)
        current_row, current_col = old_row + delta_row, old_col + delta_col
        while current_row != new_row and current_col != new_col:
            if self.board[current_row][current_col] is not None:
                self.capture_piece(current_row, current_col)
            current_row += delta_row
            current_col += delta_col