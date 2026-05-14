"""
Game logic for Milestone 1:
Pos, StrandFake, BoardFake, StrandsGameFake
"""
import math
from base import Step, PosBase, StrandBase, BoardBase, StrandsGameBase

possible_steps: dict["Step", tuple[int, int]] = {Step.N: (-1,0), 
    Step.S: (1, 0), 
    Step.W: (0, -1),
    Step.E: (0, 1),
    Step.NW: (-1, -1),
    Step.NE: (-1, 1),
    Step.SW: (1, -1),
    Step.SE: (1, 1)}

class Pos(PosBase):
    def take_step(self, step: Step) -> "PosBase":
        #if step == Step.N:
        #    return PosBase(self.r, self.c + 1)
        #if step == Step.S:
        #    return PosBase(self.r, self.c - 1)
        #if step == Step.E:
        #    return PosBase(self.r + 1, self.c)
        #if step == Step.W:
        #    return PosBase(self.r - 1, self.c)
        #if step == Step.NE:
        #    return PosBase(self.r + 1, self.c + 1)
        #if step == Step.NW:
        #    return PosBase(self.r - 1, self.c + 1)
        #if step == Step.SE:
        #    return PosBase(self.r + 1, self.c - 1)
        #if step == Step.SW:
        #    return PosBase(self.r - 1, self.c - 1)

        change_r, change_c = possible_steps[step]
        return Pos(self.r + change_r, self.c + change_c)
    
    def step_to(self, other: "PosBase") -> "Step":
        change_r = other.r - self.r
        change_c = other.c - self.c

        if (change_r, change_c) == (0, 0):
            raise ValueError("No step taken")
        for step, (r, c) in possible_steps.items():
            if (r, c) == (change_r, change_c):
                return step
        raise ValueError("Step not possible (other too far away)")
    
    def is_adjacent_to(self, other: "PosBase") -> bool:
        change_r = abs(other.r - self.r)
        change_c = abs(other.c - self.c)

        if max(change_r, change_c) == 1:
            return True
        else:
            return False

class StrandFake(StrandBase):
    def positions(self) -> list["PosBase"]:
        pos_list = [self.start]
        current_pos = self.start

        for step in self.steps:
            current_pos = current_pos.take_step(step)
            pos_list.append(current_pos)
        
        return pos_list
    
    def is_cyclic(self) -> bool:
        visited = set()

        for pos in self.positions():
            current = (pos.r, pos.c)
            if current in visited:
                return True
            visited.add(current)
        return False
    
    def is_folded(self) -> bool:
        raise NotImplementedError

class BoardFake(BoardBase):
    def __init__(self, letters: list[list[str]]):
        if not letters:
            raise ValueError("Board is empty")
    
        required_row_length = len(letters[0])
        if required_row_length == 0:
            raise ValueError("1st row is empty")

        for row in letters:
            if len(row) != required_row_length:
                raise ValueError("Length of rows are inconsistent")

            for char in row:
                if len(char) != 1:
                    raise ValueError("Letter longer than one character")
                if not char.islower():
                    raise ValueError("Letter is not lower case")
                if not char.isalpha():
                    raise ValueError("Character is not a letter")
        self.letters = letters
    
    def num_rows(self) -> int:
        return len(self.letters)
    
    def num_cols(self) -> int:
        return len(self.letters[0])
    
    def get_letter(self, pos: "PosBase") -> str:
        if pos.r >= self.num_rows() or pos.c >= self.num_cols() or pos.r < 0 or \
        pos.c < 0:
            raise ValueError("Invalid board position")
        
        return self.letters[pos.r][pos.c]
    
    def evaluate_strand(self, strand: "StrandBase") -> str:
        word = ""
        for pos in strand.positions():
            word += self.get_letter(pos)
        return word
    
class StrandsGameFake(StrandsGameBase):
    def __init__(self, game_file: str | list[str], hint_threshold: int = 3):
        if isinstance(game_file, str):
            with open(game_file, 'r') as file:
                lines = file.readlines()
        else:
            lines = game_file
        
        sections = []
        current: list[str] = []
        for line in lines:
            if line.strip() == "":
                if current:
                    sections.append(current)
                    current = []
            else:
                current.append(line.strip())
        if current:
            sections.append(current)

        #theme (prints the theme with qutoations around the themed word)
        self._theme = sections[0][0].strip()

        #board letters
        board_lines = sections[1]
        letters = []
        for line in board_lines:
            line = line.strip().lower()
            row = []
            for letter in line:
                if letter.isalpha():
                    row.append(letter)
            letters.append(row)

        self._board = BoardFake(letters)
        
        #answers
        self._answers: list[tuple[str, StrandBase]] = []
        for answer in sections[2]:
            line = answer.strip().lower().split()
            if line == []:
                continue
            word: str = line[0]
            start_r = int(line[1])
            start_c = int(line[2])

            steps = []
            for step in line[3:]:
                steps.append(Step(step))
            strand = StrandFake(Pos(start_r - 1, start_c - 1), steps)
            self._answers.append((word, strand))

        #other add
        self._found_strands: list[StrandBase] = []
        self._hint_meter = 0
        self._hint_threshold = hint_threshold
        self._active_hint = None

    def theme(self) -> str:
        return self._theme
    
    def board(self) -> BoardBase:
        return self._board
    
    def answers(self) -> list[tuple[str, StrandBase]]:
        return self._answers
    
    def found_strands(self) -> list[StrandBase]:
        return self._found_strands
    
    def game_over(self) -> bool:
        return len(self._found_strands) == len(self._answers)
    
    def hint_threshold(self) -> int:
        return self._hint_threshold
    
    def hint_meter(self) -> int:
        return self._hint_meter
    
    def active_hint(self) -> None | tuple[int, bool]:
        return self._active_hint
    
    def submit_strand(self, strand: StrandBase) -> tuple[str, bool] | str:
        start_coord = strand.positions()[0]

        for index, (word, answer) in enumerate(self._answers):
            if answer in self._found_strands:
                if answer.positions()[0] == start_coord:
                    return "Already found"
            
            if answer.positions()[0] == start_coord:
                self._found_strands.append(answer)

                if self._active_hint is not None:
                    active_index, _ = self._active_hint
                    if active_index == index:
                        self._active_hint = None

                return (word, True)
    
        return "Not a theme word"

    def use_hint(self) -> tuple[int, bool] | str:
        if self._active_hint is None:
            for index, (word, strand) in enumerate(self._answers):
                if strand not in self._found_strands:
                    self._active_hint = (index, False)
                    return self._active_hint
        
        index, revealed = self._active_hint
        if revealed == False:
            self._active_hint = (index, True)
            return self._active_hint
        
        return "Use your current hint"
