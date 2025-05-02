from tkinter import *
import copy
import random

class TicTacToe:
    winning_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                            [0, 3, 6], [1, 4, 7], [2, 5, 8],
                            [0, 4, 8], [2, 4, 6]]
    buttons = []

    def __init__(self, root):
        self.root = root
        self.board = [" "] * 9
        self.moves = [StringVar() for _ in range(9)]
        self.curr_player = "X"
        self.move_number = 0
        self.winning_squares = []
        self.game_over = False
        self.auto_ai_vs_ai = False
        self.apply_to_each(lambda x: x.set(" "), self.moves)
        self.create_ui()

    def create_ui(self):
        self.status_label = Label(self.root, text="player x", font=("Cairo", 22), bg="#1e1e2f", fg="white", pady=10)
        self.status_label.grid(row=0, column=0, columnspan=3)

        for i in range(9):
            btn = Button(self.root, textvariable=self.moves[i], font=("Arial", 36, "bold"), width=6, height=3,
                         bg="#2e2e3e", fg="white", activebackground="#444", bd=0,
                         command=lambda i=i: self.make_move(i))
            btn.grid(row=(i // 3) + 1, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        restart = Button(self.root, text="🔁 إعادة", font=("cairo", 18), command=self.reset,
                         bg="#444", fg="white", bd=0)
        restart.grid(row=4, column=0, sticky="nsew", pady=(10, 0), padx=5)

        self.ai_on_var = IntVar()
        self.ai_on = Checkbutton(self.root, text="AIلاعب ال ", font=("cairo", 18), variable=self.ai_on_var,
                                 bg="#444", fg="white", selectcolor="#1e1e2f",
                                 activebackground="#1e1e2f")
        self.ai_on.grid(row=4, column=1, sticky="nsew", pady=(10, 0), padx=5)

        ai_vs_ai_btn = Button(self.root, text="Ai ضد Ai", font=("cairo", 18), command=self.toggle_ai_vs_ai,
                              bg="#444", fg="white", bd=0)
        ai_vs_ai_btn.grid(row=4, column=2, sticky="nsew", pady=(10, 0), padx=5)

    def toggle_ai_vs_ai(self):
        self.reset()
        self.auto_ai_vs_ai = True
        self.root.after(500, self.ai_mm_init)

    def make_move(self, move):
        if self.game_over or self.board[move] != " ":
            return

        self.move_number += 1
        self.board[move] = self.curr_player
        self.moves[move].set(self.curr_player)

        # تغيير خلفية الزر بناءً على اللاعب
        if self.curr_player == "X":
            self.buttons[move].config(fg="#00BFFF", bg="#ADD8E6")  # لون خلفية X (أزرق فاتح)
        else:
            self.buttons[move].config(fg="#FF6347", bg="#FFCCCB")  # لون خلفية O (أحمر فاتح)

        # تغيير اللون عند الفوز
        if self.check_winner():
            self.status_label.config(text=f"{self.curr_player} فاز!", fg="#00FF7F")
            for s in self.winning_squares:
                self.buttons[s].config(bg="#4CAF50")
            self.game_over = True
            self.auto_ai_vs_ai = False
            return

        if self.move_number == 9 and self.board_full():
            self.status_label.config(text="تعادل 🤝", fg="orange")
            self.game_over = True
            self.auto_ai_vs_ai = False
            return

        self.curr_player = "O" if self.curr_player == "X" else "X"
        self.status_label.config(text=f"player {self.curr_player}", fg="white")

        if self.curr_player == "O" and self.ai_on_var.get():
            self.root.after(500, self.ai_mm_init)

        if self.auto_ai_vs_ai and not self.game_over:
            self.root.after(500, self.ai_mm_init)

    def check_winner(self):
        for combo in TicTacToe.winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != " ":
                self.winning_squares = combo
                return True
        return False

    def board_full(self):
        return all(cell != " " for cell in self.board)

    def reset(self):
        self.curr_player = "X"
        self.board = [" "] * 9
        self.move_number = 0
        self.game_over = False
        self.winning_squares = []
        self.status_label.config(text="player x", fg="white")
        for i in range(9):
            self.moves[i].set(" ")
            self.buttons[i].config(bg="#2e2e3e", fg="white")
        self.auto_ai_vs_ai = False

    def apply_to_each(self, func, lst):
        for item in lst:
            func(item)

    def get_enemy(self, player):
        return "O" if player == "X" else "X"

    def ai_mm_init(self):
        if self.game_over:
            return

        player = self.curr_player
        best_score = -100
        best_moves = []

        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = player
                score = self.minimax(self.get_enemy(player), self.board[:], -1000, 1000)
                self.board[i] = " "
                if score > best_score:
                    best_score = score
                    best_moves = [i]
                elif score == best_score:
                    best_moves.append(i)

        if best_moves:
            best_move = random.choice(best_moves)
            self.make_move(best_move)

    def minimax(self, player, board, alpha, beta):
        for combo in TicTacToe.winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != " ":
                return 1 if board[combo[0]] == "O" else -1

        if all(cell != " " for cell in board):
            return 0

        if player == "O":
            max_eval = -1000
            for i in range(9):
                if board[i] == " ":
                    board[i] = player
                    eval = self.minimax("X", board, alpha, beta)
                    board[i] = " "
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = 1000
            for i in range(9):
                if board[i] == " ":
                    board[i] = player
                    eval = self.minimax("O", board, alpha, beta)
                    board[i] = " "
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

if __name__ == "__main__":
    root = Tk()
    root.title("Tic Tac Toe")
    root.configure(bg="#1e1e2f")
    TicTacToe(root)
    root.mainloop()
