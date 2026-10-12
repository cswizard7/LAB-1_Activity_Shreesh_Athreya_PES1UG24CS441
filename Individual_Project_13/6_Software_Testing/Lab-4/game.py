from board import Board


class Minesweeper:
    DIFFICULTIES = {
        "easy": (6, 6, 6),
        "medium": (8, 8, 12),
        "hard": (10, 10, 20),
    }

    def __init__(self):
        while True:
            choice = input("Choose difficulty (Easy/Medium/Hard): ").strip().lower()

            if choice in self.DIFFICULTIES:
                rows, cols, mines = self.DIFFICULTIES[choice]
                self.board = Board(rows=rows, cols=cols, mines=mines)
                print(
                    f"{choice.title()} mode: "
                    f"{rows}x{cols} board with {mines} mines."
                )
                break

            print("Invalid difficulty. Choose Easy, Medium, or Hard.")

    def display(self, reveal_mines=False):
        b = self.board
        print("\n   " + " ".join(str(c + 1) for c in range(b.cols)))
        for r in range(b.rows):
            cells = []
            for c in range(b.cols):
                pos = (r, c)
                if reveal_mines and pos in b.mines:
                    ch = "*"
                elif pos in b.flags:
                    ch = "F"
                elif pos not in b.revealed:
                    ch = "#"
                elif pos in b.mines:
                    ch = "*"
                else:
                    ch = str(b.adjacent_mines(r, c))
                cells.append(ch)
            print(f"{r + 1:2} " + " ".join(cells))

    def run(self):
        print("Minesweeper")
        print("Commands: r row col | f row col | q")
        while True:
            self.display()
            raw = input("> ").strip().lower()
            if raw == "q":
                return
            parts = raw.split()
            if len(parts) != 3 or parts[0] not in {"r", "f"}:
                print("Use r row col or f row col.")
                continue
            try:
                r, c = int(parts[1]) - 1, int(parts[2]) - 1
            except ValueError:
                print("Coordinates must be numbers.")
                continue
            if not self.board.in_bounds(r, c):
                print("Outside the board.")
                continue

            if parts[0] == "f":
                self.board.toggle_flag((r, c))
                continue

            pos = (r, c)

            if pos in self.board.revealed:
                print("Cell already revealed.")
                continue

            if self.board.reveal(pos):
                self.display(reveal_mines=True)
                print("BOOM! You hit a mine.")
                return

            if pos in self.board.revealed:
                print("Cell revealed.")

            if self.board.won():
                self.display()
                print("You cleared the board!")
                return
