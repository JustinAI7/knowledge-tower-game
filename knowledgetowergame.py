import tkinter as tk
from tkinter import messagebox
import random


class KnowledgeTowerFinal:
    STACK_LIMIT = 10
    MAX_LIVES = 3
    SCORE_INCREMENT = 50

    LEVELS = [
        {"name": "EASY", "ops": ["+", "×"], "color": "#2ecc71"},
        {"name": "MEDIUM", "ops": ["+", "-", "×"], "color": "#f1c40f"},
        {"name": "HARD", "ops": ["+", "-", "×", "÷"], "color": "#e74c3c"}
    ]

    FUN_FACTS = [
        "Stacks follow LIFO — Last In, First Out.",
        "Multiplication is repeated addition.",
        "Stacks are used in undo operations.",
        "Algorithms help computers solve problems."
    ]

    AFFIRMATIONS = [
        "🌟 You are capable of mastering challenges!",
        "🚀 Learning grows your confidence.",
        "🏆 Practice leads to success."
    ]

    def __init__(self, root):
        self.root = root
        self.root.title("Knowledge Tower")
        self.root.geometry("900x700")
        self.root.configure(bg="#0b132b")

        self.level_index = 0
        self.stack = []
        self.score = 0
        self.lives = self.MAX_LIVES
        self.correct_ans = 0

        self.show_main_menu()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def styled_button(self, parent, text, cmd, bg):
        btn = tk.Button(
            parent, text=text,
            font=("Arial", 14, "bold"),
            bg=bg, fg="white",
            bd=0, padx=20, pady=10,
            command=cmd, cursor="hand2"
        )
        btn.bind("<Enter>", lambda e: btn.config(bg="#34495e"))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    def show_main_menu(self):
        self.clear()

        tk.Label(self.root, text="KNOWLEDGE TOWER",
                 font=("Courier", 44, "bold"),
                 fg="gold", bg="#0b132b").pack(pady=20)

        tk.Label(
            self.root,
            text=(
                "In Partial Fulfillment of the Requirements\n"
                "for the Course CIT10333P\n\n"
                "Submitted to:\n"
                "Mr. Maxil S. Urocay, MSCS\n\n"
                "A Research Project\n"
                "Data Structures and Algorithms"
            ),
            font=("Arial", 14),
            fg="white",
            bg="#0b132b",
            justify="center"
        ).pack(pady=20)

        self.styled_button(
            self.root, "PLAY GAME",
            self.show_level_select, "#1f4068"
        ).pack(pady=10)

        self.styled_button(
            self.root, "HELP / FAQ",
            self.show_help, "#4b7bec"
        ).pack(pady=10)

        self.styled_button(
            self.root, "EXIT",
            self.root.quit, "#3a3a3a"
        ).pack(pady=10)

    def show_help(self):
        self.clear()

        tk.Label(
            self.root,
            text="HOW TO PLAY",
            font=("Courier", 36, "bold"),
            fg="gold", bg="#0b132b"
        ).pack(pady=30)

        help_text = (
            "🎯 OBJECTIVE\n"
            "• Answer math questions correctly to build the tower\n"
            "• Reach 10 blocks to complete the tower\n\n"

            "📦 STACK MECHANIC (LIFO)\n"
            "• Correct answer → PUSH a block\n"
            "• Wrong answer → POP the last block\n\n"

            "❤️ LIVES\n"
            "• You start with 3 lives\n"
            "• Wrong answers remove a life\n"
            "• Game ends when lives reach zero\n\n"

            "⚙️ DIFFICULTY LEVELS\n"
            "• EASY: Addition & Multiplication\n"
            "• MEDIUM: +, -, ×\n"
            "• HARD: +, -, ×, ÷\n\n"

            "🏆 REWARD\n"
            "• Completing the tower gives a positive affirmation\n"
            "• Learn while playing!"
        )

        tk.Label(
            self.root,
            text=help_text,
            font=("Arial", 14),
            fg="white",
            bg="#0b132b",
            justify="left",
            wraplength=700
        ).pack(pady=20)

        self.styled_button(
            self.root, "BACK",
            self.show_main_menu, "#555"
        ).pack(pady=20)

    def show_level_select(self):
        self.clear()

        tk.Label(self.root, text="SELECT DIFFICULTY",
                 font=("Courier", 32, "bold"),
                 fg="white", bg="#0b132b").pack(pady=30)

        for i, lvl in enumerate(self.LEVELS):
            self.styled_button(
                self.root,
                lvl["name"],
                lambda x=i: self.start_game(x),
                lvl["color"]
            ).pack(pady=10)

        self.styled_button(
            self.root, "BACK",
            self.show_main_menu, "#555"
        ).pack(pady=20)

    def start_game(self, idx):
        self.clear()
        self.level_index = idx
        self.stack.clear()
        self.score = 0
        self.lives = self.MAX_LIVES

        theme = self.LEVELS[self.level_index]["color"]

        header = tk.Frame(self.root, bg=theme, height=60)
        header.pack(fill="x")

        self.lbl_status = tk.Label(
            header,
            text=f"{self.LEVELS[self.level_index]['name']} | SCORE: 0",
            bg=theme, fg="black",
            font=("Arial", 14, "bold")
        )
        self.lbl_status.pack(side="left", padx=20)

        self.lbl_lives = tk.Label(
            header,
            text=f"LIVES: {'❤️'*self.lives}",
            bg=theme, fg="black",
            font=("Arial", 14)
        )
        self.lbl_lives.pack(side="right", padx=20)

        self.progress = tk.Canvas(self.root, height=15, bg="#222")
        self.progress.pack(fill="x")


        card = tk.Frame(self.root, bg="#1c2541", bd=0)
        card.pack(expand=True, pady=30, padx=30)

        self.question = tk.Label(
            card, font=("Courier", 48, "bold"),
            fg="white", bg="#1c2541"
        )
        self.question.pack(pady=20)

        self.entry = tk.Entry(
            card, font=("Arial", 28),
            justify="center", width=6
        )
        self.entry.pack()
        self.entry.bind("<Return>", lambda e: self.check())

        self.fact = tk.Label(
            card, font=("Arial", 12, "italic"),
            fg="#dcdcdc", bg="#1c2541",
            wraplength=400
        )
        self.fact.pack(pady=15)

        self.canvas = tk.Canvas(
            card, width=220, height=350,
            bg="#1c2541", highlightthickness=0
        )
        self.canvas.pack(pady=10)

        self.new_question()

    def new_question(self):
        op = random.choice(self.LEVELS[self.level_index]["ops"])

        if op == "+":
            a, b = random.randint(1, 20), random.randint(1, 20)
            self.correct_ans = a + b
        elif op == "-":
            a, b = sorted([random.randint(1, 20), random.randint(1, 20)], reverse=True)
            self.correct_ans = a - b
        elif op == "×":
            a, b = random.randint(1, 12), random.randint(1, 12)
            self.correct_ans = a * b
        else:
            b = random.randint(1, 10)
            self.correct_ans = random.randint(1, 10)
            a = b * self.correct_ans

        self.question.config(text=f"{a} {op} {b}")
        self.entry.delete(0, tk.END)
        self.entry.focus()

    def check(self):
        try:
            if int(self.entry.get()) == self.correct_ans:
                self.stack.append(1)
                self.score += self.SCORE_INCREMENT
                self.fact.config(text="💡 " + random.choice(self.FUN_FACTS))

                if len(self.stack) == self.STACK_LIMIT:
                    messagebox.showinfo(
                        "🏆 Tower Completed",
                        random.choice(self.AFFIRMATIONS)
                    )
                    self.stack.clear()

            else:
                self.lives -= 1
                self.fact.config(text="❌ LIFO removes the last block.")
                if self.stack:
                    self.stack.pop()

            if self.lives <= 0:
                messagebox.showinfo("Game Over", f"Final Score: {self.score}")
                self.show_main_menu()
                return

            self.update_ui()
            self.new_question()

        except:
            pass

    def update_ui(self):
        self.lbl_status.config(
            text=f"{self.LEVELS[self.level_index]['name']} | SCORE: {self.score}"
        )
        self.lbl_lives.config(text=f"LIVES: {'❤️'*self.lives}")
        self.draw_stack()
        self.draw_progress()

    def draw_stack(self):
        self.canvas.delete("all")
        for i in range(len(self.stack)):
            y = 320 - i * 28
            self.canvas.create_rectangle(
                60, y, 160, y - 24,
                fill="gold", outline="#f1c40f"
            )

    def draw_progress(self):
        self.progress.delete("all")
        w = int((len(self.stack) / self.STACK_LIMIT) * self.root.winfo_width())
        self.progress.create_rectangle(0, 0, w, 15, fill="gold")


if __name__ == "__main__":
    root = tk.Tk()
    KnowledgeTowerFinal(root)
    root.mainloop()
