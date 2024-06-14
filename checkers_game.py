import tkinter as tk
from tkinter import messagebox
from game_board import GameBoard
from game_logic import is_valid_move, is_valid_capture_move, has_mandatory_capture, has_mandatory_capture_for_piece

class CheckersGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Шашки")
        self.canvas = tk.Canvas(root, width=800, height=800)
        self.canvas.pack(side=tk.LEFT)
        self.root.attributes('-fullscreen', True)
        self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.info_frame = tk.Frame(root)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y, pady=150, padx=60)

        self.turn_label = tk.Label(self.info_frame, text="Хід: Червоні", font=("Arial", 16))
        self.turn_label.pack(pady=20)

        self.red_captured_label = tk.Label(self.info_frame, text="Захоплено червоними: 0", font=("Arial", 16))
        self.red_captured_label.pack(pady=20)

        self.blue_captured_label = tk.Label(self.info_frame, text="Захоплено синіми: 0", font=("Arial", 16))
        self.blue_captured_label.pack(pady=20)

        self.turn_button = tk.Button(self.info_frame, text="Поточний хід: Червоні", font=("Arial", 16),
                                     command=self.show_turn)
        self.turn_button.pack(pady=20)

        self.end_game_button = tk.Button(self.info_frame, text="Завершити гру", font=("Arial", 16),
                                         command=self.end_game, bg="BurlyWood", fg="white")
        self.end_game_button.pack(pady=10)

        self.restart_game_button = tk.Button(self.info_frame, text="Почати заново", font=("Arial", 16),
                                             command=self.restart_game, bg="BurlyWood", fg="white")
        self.restart_game_button.pack(pady=10)

        self.red_captured = 0
        self.blue_captured = 0

        self.board = GameBoard(self.canvas)
        self.selected_piece = None
        self.turn = "red"
        self.canvas.bind("<Button-1>", self.select_piece)

    def select_piece(self, event):
        col = event.x // 100
        row = event.y // 100

        if self.board.get_piece(row, col) and self.board.get_piece_color(row, col) == self.turn:
            self.selected_piece = (row, col)
        elif self.selected_piece and is_valid_move(self.board, self.selected_piece, (row, col), self.turn):
            if has_mandatory_capture(self.board, self.turn):
                if is_valid_capture_move(self.board, self.selected_piece, (row, col), self.turn):
                    self.move_piece(row, col, True)
            else:
                self.move_piece(row, col, False)

    def move_piece(self, row, col, capture_again):
        old_row, old_col = self.selected_piece
        piece = self.board.get_piece(old_row, old_col)
        is_king = self.board.is_king(piece)

        if is_king:
            self.board.move_king(old_row, old_col, row, col)
        elif abs(row - old_row) == 2 and abs(col - old_col) == 2:
            mid_row, mid_col = (old_row + row) // 2, (old_col + col) // 2
            self.capture_piece(mid_row, mid_col)

        self.board.move_piece(old_row, old_col, row, col)
        self.promote_to_king(row, col)
        self.selected_piece = None

        self.check_winner()

        if capture_again and has_mandatory_capture_for_piece(self.board, row, col):
            self.selected_piece = (row, col)
        else:
            self.turn = "blue" if self.turn == "red" else "red"
            self.update_turn_label()

    def capture_piece(self, mid_row, mid_col):
        captured_piece_color = self.board.capture_piece(mid_row, mid_col)
        if captured_piece_color == "red":
            self.red_captured += 1
            self.red_captured_label.config(text=f"Захоплено червоними: {self.red_captured}")
        else:
            self.blue_captured += 1
            self.blue_captured_label.config(text=f"Захоплено синіми: {self.blue_captured}")

    def promote_to_king(self, row, col):
        if (self.turn == "red" and row == 7) or (self.turn == "blue" and row == 0):
            self.board.promote_to_king(row, col)

    def update_turn_label(self):
        turn_text = "Червоні" if self.turn == "red" else "Сині"
        self.turn_label.config(text=f"Хід: {turn_text}")
        self.turn_button.config(text=f"Поточний хід: {turn_text}")

    def show_turn(self):
        current_turn = "Червоні" if self.turn == "red" else "Сині"
        messagebox.showinfo("Поточний хід", f"Зараз хід {current_turn}")

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
