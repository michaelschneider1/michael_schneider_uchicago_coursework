import sys
from ui import ArtTUIBase

class ArtTUIWrappers(ArtTUIBase):
    def __init__(self, num_wrappers: int, width: int, height: int):
        self.num_wrappers = num_wrappers
        self.width = width
        self.height = height
        self.colors = [
            "\033[41m",  #red
            "\033[42m",  #green
            "\033[43m",  #yellow
            "\033[44m",  #blue
            "\033[45m",  #magenta
            "\033[46m",  #light blue
            "\033[47m",  #white
        ]
        self.reset = "\033[0m"
        self.red = "\033[41m"
        self.green = "\033[42m"

    def draw(self):
        total_width = self.width + 2 * self.num_wrappers
        total_height = self.height + 2 * self.num_wrappers

        for y in range(total_height):
            line = ''
            for x in range(total_width):
                layer = min(x, y, total_width - 1 - x, total_height - 1 - y)
                if layer < self.num_wrappers:
                    color = self.colors[layer % len(self.colors)]
                    line += f"{color} {self.reset}"
                else:
                    line += ' '
            print(line)

    def print_top_edge(self) -> None:
        for _ in range(self.width + 4):
            print(self.red, end=" ")
        print(self.reset)
        for wide in range(self.width + 4):
            if wide == 0 or wide == self.width + 3:
                print(self.red, end=" ")
            else:
                print(self.green, end=" ")
        print(self.reset)
    def print_bottom_edge(self) -> None:
        for wide in range(self.width + 4):
            if wide == 0 or wide == self.width + 3:
                print(self.red, end=" ")
            else:
                print(self.green, end=" ")
        print(self.reset)
        for _ in range(self.width + 4):
            print(self.red, end=" ")
        print(self.reset)
    def print_left_bar(self) -> None:
        print(self.red, self.green, self.reset, end= "")
    def print_right_bar(self) -> None:
        print(self.green, self.red, self.reset)

class ArgyleTUI(ArtTUIBase):  # trying out pattern
    def __init__(self, wraps, w, h):
        self.wraps = wraps
        self.w = w
        self.h = h
        self.pats = ['/', '\\', 'X', 'o']

    def draw(self):
        tw = self.w + 2 * self.wraps
        th = self.h + 2 * self.wraps

        for y in range(th):
            line = ''
            for x in range(tw):
                depth = min(x, y, tw - 1 - x, th - 1 - y)
                if depth < self.wraps:
                    line += self.pats[depth % len(self.pats)]
                else:
                    line += ' '
            print(line)

    def print_top_edge(self) -> None:
        for _ in range(self.w + 6):
            print("/", end="")
        print()
        print("/", end="")
        for _ in range(1, self.w + 5):
            print("\\", end= "")
        print("/")
    def print_bottom_edge(self) -> None:
        print("/", end="")
        for _ in range(1, self.w + 5):
            print("\\", end= "")
        print("/")
        for _ in range(self.w + 6):
            print("/", end="")
        print()
    def print_left_bar(self) -> None:
        print("/\\", end=" ")
    def print_right_bar(self) -> None:
        print(" \\/")

class GraphStrandsTUI(ArtTUIBase):  
    def __init__(self, frame_width=2, board_width=6, board_height=8):
        self.pattern = ["/---\\", "|   |", "\\---/"]
        self.frame_width = frame_width
        self.board_width = board_width
        self.board_height = board_height

    def draw(self):
        # Surround the board area with fixed width and height
        total_height = self.board_height + 2 * self.frame_width
        total_width = self.board_width * len(self.pattern[0]) + 2 * self.frame_width

        border_char = "#"
        for row in range(total_height):
            if row < self.frame_width or row >= total_height - self.frame_width:
                print(border_char * total_width)
            else:
                line = border_char * self.frame_width
                pattern_row = self.pattern[(row - self.frame_width) % len(self.pattern)]
                line += pattern_row * self.board_width
                line += border_char * self.frame_width
                print(line)

    def print_top_edge(self) -> None:
        print("#" * (self.board_width + 6))
        print("#" * (self.board_width + 6))
    def print_bottom_edge(self) -> None:
        print("#" * (self.board_width + 6))
        print("#" * (self.board_width + 6))
    def print_left_bar(self) -> None:
        print("## ", end= "")
    def print_right_bar(self) -> None:
        print(" ##")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Need to specify a TUI category.")
        sys.exit(1)

    cat = sys.argv[1]

    try:
        if cat == 'cat0':
            n, w, h = map(int, sys.argv[2:])
            ArtTUIWrappers(n, w, h).draw()
        elif cat == 'cat2':
            n, w, h = map(int, sys.argv[2:])
            ArgyleTUI(n, w, h).draw()
        elif cat == 'cat4':
            GraphStrandsTUI().draw()  
        elif cat in {'cat1', 'cat3'}:
            print("pattern not supported for now")
            sys.exit(0)
        else:
            print(f"Unknown category: {cat}")
            sys.exit(1)
    except Exception as e:
        print("error running TUI:", e)
        sys.exit(1)
