import os
import sys
import termios
import tty
import click
import random
from strands import *
from ui import *
from art_tui import *

########################## Keyboard Input Stuff ################################
# https://stackoverflow.com/a/52461891

key_Enter = 13
key_Esc = 27
key_Up = "\033[A"
key_Dn = "\033[B"
key_Rt = "\033[C"
key_Lt = "\033[D"
fdInput = sys.stdin.fileno()
termAttr = termios.tcgetattr(0)
def getch():
    tty.setraw(fdInput)
    ch = sys.stdin.buffer.raw.read(4).decode(sys.stdin.encoding)
    if len(ch) == 1:
        if ord(ch) < 32 or ord(ch) > 126:
            ch = ord(ch)
    elif ord(ch[0]) == 27:
        ch = "\033" + ch[1:]
    termios.tcsetattr(fdInput, termios.TCSADRAIN, termAttr)
    return ch

# https://www.reddit.com/r/learnpython/comments/1b4sk5n/how_to_clear_a_console_in_python/

def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")
######################################################################



############################## COLOR CONSTANTS #################################
WHITE: str = '\033[37m'
RED: str = '\033[31m'
REDBG: str = '\033[41m'
CYAN: str = '\033[96m'
BLUE: str = '\033[34m'
GREEN: str = '\033[92m'
GREENBG: str = '\033[42m'
YELLOW: str = '\033[33m'
YELLOWBG: str = '\033[43m'
RESET: str = '\033[0m'
################################################################################

class TUIGame:
    def __init__(self, show, game, hint, art) -> None:
        """
        Initialization of all game variables needed
        """
        # Game variables
        try:
            self._game: StrandsGameBase = StrandsGame(game, hint)
        except:
            print(f"{game} is not a valid game board")
            sys.exit(1)
        if show:
            self._game_type: str = "show"
        else:
            self._game_type: str = "play"
        # Cursor Variables
        self._curr_pos: Pos = Pos(0, 0)
        # Board Printing Variables
        self._game_board: BoardBase = self._game.board()
        self._rows: int = self._game_board.num_rows()
        self._cols: int = self._game_board.num_cols()
        self._answers: list[tuple[str, StrandBase]] = self._game.answers()
        self._found_pos: set[tuple[int, int]] = set()
        self._empty_line_len: int = (self._cols * 3 - 2)
        self._board_height: int = 2 * self._rows + 5
        # Game Type
        if self._game_type == "show":
            self._found_ans: list[StrandBase] = [answ[1] for answ in self._answers]
        else:
            self._found_ans: list[StrandBase] = self._game.found_strands()
        # Letter Connecting Variables
        self._blank: str = "  "
        self._horizontal: str = "══"
        self._vertical: str = "‖"
        self._diag_right: str = "⟋"
        self._diag_left: str = "⟍"
        self._diag_both: str = "⤬"
        # Board Word Selecting Variables
        self._pending_word: bool = False
        self._pending_pos: set[tuple[int, int]] = set()
        self._word_start: Pos = None
        self._step_order: list[Step] = []
        # Hint Variables
        self._hint: tuple[int, bool] | str = self._game.active_hint()
        self._hint_word_letters: set[tuple[int, int]] = set()
        self._hint_bookend_letters: set[tuple[int, int]] = set()
        self._score: int = 0 # Game score, lower scores are better
        # Art Variables
        if art == 'cat0':
            self._border = ArtTUIWrappers(8, self._empty_line_len, self._board_height)
        elif art == 'cat2':
            self._border = ArgyleTUI(2, self._empty_line_len, self._board_height)
        elif art == 'cat4':
            self._border = GraphStrandsTUI(2, self._empty_line_len, self._board_height)
        elif art == 'stub':
            self._border: ArtTUIBase = ArtTUIStub(2, self._empty_line_len)
        else:
            print("Art style not currently implemented.")
            sys.exit(1)
        # Game Finishing Logic
        self.one_more_time: bool = False
        self.game_running: bool = True

    # Board Printing Methods
    def print_board_row(self, row: int) -> None:
        """
        Prints the specified row of the game board in the terminal

        Input (Int): The index of the row to print

        Output(None): Returns nothing, only prints to terminal
        """
        self._border.print_left_bar()
        for col in range(self._cols):
            curr_pos: PosBase = Pos(row, col)
            curr_letter: str = self._game_board.get_letter(curr_pos)
            color: str = WHITE
            horiz: bool = False
            # Found Word Letters
            if (row, col) in self._found_pos:
                if (row, col) == (self._curr_pos.r, self._curr_pos.c):
                    color = RED
                else:
                    color = BLUE
                if col != self._cols - 1:
                    for answer in self._found_ans:
                        if curr_pos in answer.positions():
                            key_answ: StrandBase = answer
                            key_answ_pos: list[PosBase] = key_answ.positions()
                            curr_pos_i = key_answ_pos.index(curr_pos)
                            right_pos = curr_pos.take_step(Step.E)
                            right_pos_i = -2
                            if right_pos in key_answ_pos:
                                right_pos_i = key_answ_pos.index(right_pos)
                            if curr_pos_i + 1 == right_pos_i or \
                            curr_pos_i - 1 == right_pos_i:
                                horiz = True
            # Current Position Letter
            elif (row, col) == (self._curr_pos.r, self._curr_pos.c):
                if (row, col) in self._hint_bookend_letters:
                    color = REDBG
                else:
                    color = RED
            # Pending Word Letters
            elif (row, col) in self._pending_pos:
                color = CYAN
            # Hint Word Letters
            elif (row, col) in self._hint_word_letters:
                color = GREEN
                if (row, col) in self._hint_bookend_letters:
                    color = GREENBG
            # Regular Letters
            else:
                color = WHITE
            # All letters are blue for Game Type: Show
            if self._game_type == "show":
                    color = BLUE
            if col == self._cols - 1:
                print(f"{color}{curr_letter}{RESET}", end="")
            else:
                if horiz:
                    print(f"{color}{curr_letter}{RESET}", end=self._horizontal)
                else:
                    print(f"{color}{curr_letter}{RESET}", end=self._blank)
        self._border.print_right_bar()

    def print_spacing_row(self, row: int) -> None:
        """
        Prints the spacing row which may or may not contain connections, depending
        on the game and how much is solved

        Input(Int): The index of the game board row above it

        Output(None): Returns nothing, only prints to terminal
        """
        self._border.print_left_bar()
        for i in range(self._empty_line_len):
            # Vertical Connection Check
            if i % 3 == 0: # All board characters are printed with 2 spaces b/w.
                if (row, i / 3) in self._found_pos:
                    curr_pos = Pos(row, i / 3)
                    for answer in self._found_ans:
                        if curr_pos in answer.positions():
                            key_answ: StrandBase = answer
                            key_answ_pos: list[PosBase] = key_answ.positions()
                            curr_pos_i = key_answ_pos.index(curr_pos)
                            down_pos = curr_pos.take_step(Step.S)
                            down_pos_i = -2
                            if down_pos in key_answ_pos:
                                down_pos_i = key_answ_pos.index(down_pos)
                            if curr_pos_i + 1 == down_pos_i or \
                            curr_pos_i - 1 == down_pos_i:
                                print(self._vertical, end="")
                                break
                            else:
                                print(" ", end="")
                else:
                    print(" ", end="")
            # SW/NE and SE/NW Connection
            else:
                se_nw: bool = False
                sw_ne: bool = False
                key_left_answ = None
                key_right_answ = None
                curr_left_pos = Pos(row, i // 3)
                curr_right_pos = Pos(row, i // 3 + 1)
                for answer in self._found_ans:
                    if curr_left_pos in answer.positions():
                        key_left_answ = answer
                    if curr_right_pos in answer.positions():
                        key_right_answ = answer
                # Finds the board pos NE and SW of the current whitespace
                # Current whitespace is in the middle of 4 letters
                if key_left_answ:
                    key_left_answ_pos: list[PosBase] = key_left_answ.positions()
                    curr_left_pos_i = key_left_answ_pos.index(curr_left_pos)
                    se_pos = curr_left_pos.take_step(Step.SE)
                    se_pos_i = -2
                    if se_pos in key_left_answ_pos:
                        se_pos_i = key_left_answ_pos.index(se_pos)
                # Finds the board pos NW and SE of the current whitespace
                # Current whitespace is in the middle of 4 letters
                if key_right_answ:
                    key_right_answ_pos: list[PosBase] = key_right_answ.positions()
                    curr_right_pos_i = key_right_answ_pos.index(curr_right_pos)
                    sw_pos = curr_right_pos.take_step(Step.SW)
                    sw_pos_i = -2
                    if sw_pos in key_right_answ_pos:
                        sw_pos_i = key_right_answ_pos.index(sw_pos)
                # Computes if NE/SW and/or NW/SE are directly next to each other
                # on the strand
                # SE/NW
                if key_left_answ and (curr_left_pos_i + 1 == se_pos_i or \
                curr_left_pos_i - 1 == se_pos_i):
                    se_nw = True
                # SW/NE
                if key_right_answ and (curr_right_pos_i + 1 == sw_pos_i or \
                curr_right_pos_i - 1 == sw_pos_i):
                    sw_ne = True
                # Prints the correct connection based on which are neighbors
                if se_nw and sw_ne:
                    print(self._diag_both, end="")
                elif se_nw:
                    print(self._diag_left, end="")
                elif sw_ne:
                    print(self._diag_right, end="")
                else:
                    print(" ", end="")
        self._border.print_right_bar()

    def print_info_box(self) -> None:
        """
        Prints the box of information (hints, etc) in the terminal

        Input(None): None

        Output(None): Returns nothing, prints to terminal
        """
        # Empty row for spacing purposes
        self._border.print_left_bar()
        print(" " * self._empty_line_len, end="")
        self._border.print_right_bar()
        # Actual Info Box display
            # Selection Status
        self._border.print_left_bar()
        selection_status: str = f"{YELLOW}SELECTING{RESET}"
        selection_spacer: str = " " * (self._empty_line_len - len("SELECTING"))
        if self._pending_word:
            print(f"{selection_status}{selection_spacer}", end="")
        else:
            print(" " * self._empty_line_len, end="")
        self._border.print_right_bar()
            # Num Found
        self._border.print_left_bar()
        num_found: str = f"{len(self._found_ans)}/{len(self._answers)} Are Found"
        num_found_len: int = len(num_found)
        num_found_spacer: str = " " * (self._empty_line_len - num_found_len)
        print(f"{num_found}{num_found_spacer}", end="")
        self._border.print_right_bar()
            # Hint Meter
        self._border.print_left_bar()
        hint_meter: str = f"Hint Meter: {self._game.hint_meter()}"
        hint_meter_len: int = len(hint_meter)
        hint_meter_spacer: str = " " * (self._empty_line_len - hint_meter_len)
        print(f"{hint_meter}{hint_meter_spacer}", end="")
        self._border.print_right_bar()
        # Empty Row for spacing purposes
        self._border.print_left_bar()
        print(" " * self._empty_line_len, end="")
        self._border.print_right_bar()

    def play_game(self) -> None:
        """
        The game loop in charge of all the printing and display logic.
        
        Inputs(None)
        
        Outputs(None): Returns nothing, only prints to terminal
        """
        pr_hint: bool = False
        pr_corr_answ: bool = False
        while self.game_running:
            clear_screen()
            # Prints game theme
            print(self._game.theme())
            print()

            # Keeps track of all positions of found words
            for strand in self._found_ans:
                for pos in strand.positions():
                    self._found_pos.add((pos.r, pos.c))
            
            # Keeps track of all positions in the pending word
            if self._pending_word:
                self._pending_pos.add((self._curr_pos.r, self._curr_pos.c))

            # Keeps track of letters to display for a hint request
            if isinstance(self._hint, tuple):
                hint_index, hint_display = self._hint
                h_word = self._answers[hint_index]
                # Emphasizes first and last letters
                if hint_display:
                    first_letter = h_word[1].positions()[0]
                    self._hint_bookend_letters.add((first_letter.r, first_letter.c))
                    last_letter = h_word[1].positions()[-1]
                    self._hint_bookend_letters.add((last_letter.r, last_letter.c))
                # Shows all letters
                else:
                    for letter in h_word[1].positions():
                        self._hint_word_letters.add((letter.r, letter.c))
            
            # If game ends, runs the loop one more time (to display finished board)
            if self.one_more_time or self._game_type == "show":
                self.game_running = False
            if self._game.game_over():
                self.one_more_time = True

        ########################## GAME DISPLAY ####################################                
            # Prints top of frame
            self._border.print_top_edge()
            self._border.print_left_bar()
            # Spacer for empty rows ############
            print((" " * self._empty_line_len), end="")
            ####################################
            self._border.print_right_bar()
            # Prints the board
            for row in range(self._rows):
                self.print_board_row(row)
                if row < self._rows - 1:
                    self.print_spacing_row(row)
            self.print_info_box()
            # Prints bottom of frame
            self._border.print_bottom_edge()
            # Prints rule broken texts
            if pr_hint:
                print(self._hint)
                pr_hint = False
            if pr_corr_answ:
                print(correct_answer)
                pr_corr_answ = False

            # Exit msg for Game Type: Show
            if self._game_type == "show":
                print("Displaying solved game board")
                print("Press any key to exit:")

            # Various print variable testings
            if False:
                print(f"Game type is: {self._game_type}")
                print(f"Word start: {self._word_start}, Step Order: {self._step_order}")
                print(f"Found Positions: {self._found_pos}")


        ############################ KEYBOARD INPUTS ###############################
            # Key Directions
            key_directions = {"q": Step.NW, "w": Step.N, "e": Step.NE,
                            "a": Step.W,               "d": Step.E,
                            "z": Step.SW, "x": Step.S, "c": Step.SE}

            # Input reading
            sys.stdout.flush()
            ch = getch()
            if ch == "Q":
                break
            elif ch == "h":
                self._hint = self._game.use_hint()
                if isinstance(self._hint, str):
                    pr_hint = True
                else:
                    self._score += 5
            elif ch == 13: # Enter
                if self._pending_word:
                    potential_answ: StrandBase = Strand(self._word_start, self._step_order)
                    correct_answer = self._game.submit_strand(potential_answ)
                    if isinstance(correct_answer, str):
                        pr_corr_answ = True
                        self._score += 1
                    self._pending_pos = set()
                    self._pending_word = False
                    self._step_order = []
                    self._hint_word_letters = set()
                else:
                    # Starts keeping track of new strand
                    self._pending_word = True
                    self._word_start = self._curr_pos
            elif ch == 27: # Escape
                self._pending_word = False
                self._pending_pos = set()
            # Cursor Movement
            elif ch in key_directions:
                new_pos = self._curr_pos.take_step(key_directions[ch])
                if (new_pos.c < self._cols and new_pos.c >= 0) and \
                (new_pos.r < self._rows and new_pos.r >= 0):
                    self._curr_pos = new_pos
                    # Keeps track of pending word step order
                    if self._pending_word:
                        self._step_order.append(key_directions[ch])

            # Additional key implementations
            # else:
            #     print(f"Other key [{ch}]")
        if self._game.game_over():
            print("CONGRATULATIONS! YOU WIN!!!")
            print(f"Your score is: {self._score} (lower is better)")


############################## Game Loading ####################################
BOARDS = [f for f in os.listdir("boards/")]

@click.command()
@click.option('--show', is_flag= True, help= 'Flag which shows solved board when called')
@click.option('-g', '--game', type= str, default= None, help= 'The board to be played')
@click.option('-h', '--hint', default= 3, help= 'The hint threshold need to use a hint')
@click.option('-a', '--art', default= 'cat2', help= 'The art frame to display around the game board')
def main(show: bool, game: str | None, hint: int, art: str) -> None:
    """
    Main function to be called by __name__ == "__main__". Displays title screen,
    if no game provided, will display the select game menu, then takes the click
    flags, initializes the game and runs it

    Run --help for information regarding flags and other in-line commands
    """
    # Title Screen
    clear_screen()
    for _ in range(21):
        print()
    print(f"{YELLOW}                                    T══S  D")
    print(f"{YELLOW}                                    ‖   ⟋⟋‖")
    print(f"{YELLOW}                                    R  S  N")
    print(f"{YELLOW}                                     ⟍⟍ ⟋⟋")
    print(f"{YELLOW}                                       A{RESET}")
    print()
    print("                              PRESS ENTER TO START")
    for _ in range(22):
        print()
    game_start: bool = False
    while not game_start:
        sys.stdout.flush()
        ch = getch()
        if ch == 13:
            game_start = True
        elif ch == "Q":
            sys.exit(1)
    # Game initialization
    if not game:
        # Board Select Screen
        curs_pos: int = 0
        menu_select: bool = False
        while not menu_select:
            clear_screen()
            print(f"{YELLOW}                                    MAIN MENU")
            print(f"{RESET}                                  CHOOSE A GAME")
            for board in BOARDS:
                if BOARDS.index(board) == curs_pos:
                    color = RED
                else:
                    color = BLUE
                print(f"{color}{board}{RESET}")
            sys.stdout.flush()
            ch = getch()
            if ch == key_Up and curs_pos > 0:
                curs_pos -= 1
            elif ch == key_Dn and curs_pos < len(BOARDS) - 1:
                curs_pos += 1
            elif ch == 13:
                board = f"boards/{BOARDS[curs_pos]}"
                menu_select = True
            elif ch == "Q":
                sys.exit(1)
            else:
                continue
    else:
        board = f"boards/{game}.txt"
    load_game: TUIGame = TUIGame(show, board, hint, art)
    load_game.play_game()

if __name__ == "__main__":
    main()
    