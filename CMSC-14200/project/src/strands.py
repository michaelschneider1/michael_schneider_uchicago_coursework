from base import Step, PosBase, StrandBase, BoardBase, StrandsGameBase

POSSIBLE_STEPS: dict["Step", tuple[int, int]] = {Step.N: (-1,0), 
    Step.S: (1, 0), 
    Step.W: (0, -1),
    Step.E: (0, 1),
    Step.NW: (-1, -1),
    Step.NE: (-1, 1),
    Step.SW: (1, -1),
    Step.SE: (1, 1)}

DICTIONARY = set()
with open("assets/web2.txt", "r") as file:
    for line in file:
        DICTIONARY.add(line.strip().lower())


class Pos(PosBase):
    """
    Positions on a board, represented as pairs of 0-indexed
    row and column integers. Position (0, 0) corresponds to
    the top-left corner of a board, and row and column
    indices increase down and to the right, respectively.
    """
    def take_step(self, step: Step) -> "PosBase":
        """
        Compute the position that results from starting at
        the current position and taking the specified step.
        """
        change_r, change_c = POSSIBLE_STEPS[step]
        return Pos(self.r + change_r, self.c + change_c)

    def step_to(self, other: "PosBase") -> Step:
        """
        Compute the difference in two positions, represented
        as a step from the current position to the other.

        Raises ValueError if the other position is more
        than two steps away from self.
        """
        change_r = other.r - self.r
        change_c = other.c - self.c

        if (change_r, change_c) == (0, 0):
            raise ValueError("No step taken")
        for step, (r, c) in POSSIBLE_STEPS.items():
            if (r, c) == (change_r, change_c):
                return step
        raise ValueError("Step not possible (other too far away)")

    def is_adjacent_to(self, other: "PosBase") -> bool:
        """
        Decide whether or not the two positions are
        neighbors (that is, connected by a single step).
        """
        change_r = abs(other.r - self.r)
        change_c = abs(other.c - self.c)

        if max(change_r, change_c) == 1:
            return True
        else:
            return False

class Strand(StrandBase):
    """
    Strands, represented as a start position
    followed by a sequence of steps.
    """
    def positions(self) -> list[PosBase]:
        """
        Compute the absolute positions represented by the
        strand. These positions are independent of any
        particular board size. That is, the resulting
        positions assume a board of infinite size in all
        directions.
        """
        pos_list = [self.start]
        current_pos = self.start

        for step in self.steps:
            current_pos = current_pos.take_step(step)
            pos_list.append(current_pos)
        
        return pos_list

    def is_cyclic(self) -> bool:
        """
        Decide whether or not the strand is cyclic. That is,
        check whether or not any position appears multiple
        times in the strand.
        """
        visited = set()

        for pos in self.positions():
            current = (pos.r, pos.c)
            if current in visited:
                return True
            visited.add(current)
        return False

    def is_folded(self) -> bool:
        """
        Decide whether or not the strand is folded. That is,
        check whether or not any connection in the strand
        crosses over another connection in the strand.
        """
        raise NotImplementedError("Not needed")
        

class Board(BoardBase):
    """
    Boards for the Strands game, consisting of a
    rectangular grid of letters.
    """
    def __init__(self, letters: list[list[str]]):
        """
        Constructor

        The two-dimensional matrix of strings (letters)
        is valid if (a) each row is non-empty and has
        the same length as other rows, and (b) each string
        is a single, lowercase, alphabetical character.

        Raises ValueError if the matrix is invalid.
        """
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
        """
        Return the number of rows on the board.
        """
        return len(self.letters)

    def num_cols(self) -> int:
        """
        Return the number of columns on the board.
        """
        return len(self.letters[0])

    def get_letter(self, pos: PosBase) -> str:
        """
        Return the letter at a given position on the board.

        Raises ValueError if the position is not within the
        bounds of the board.
        """
        if pos.r >= self.num_rows() or pos.c >= self.num_cols() or pos.r < 0 or \
        pos.c < 0:
            raise ValueError("Invalid board position")
        
        return self.letters[pos.r][pos.c]

    def evaluate_strand(self, strand: StrandBase) -> str:
        """
        Evaluate a strand, returning the string of
        corresponding letters from the board.

        Raises ValueError if any of the strand's positions
        are not within the bounds of the board.
        """
        word = ""
        for pos in strand.positions():
            word += self.get_letter(pos)
        return word

class StrandsGame(StrandsGameBase):
    """
    Abstract base class for Strands game logic.
    """
    def __init__(self, game_file: str | list[str], hint_threshold: int = 3):
        """
        Constructor

        Load the game specified in a given file, and set
        a particular threshold for giving hints. The game
        file can be specified either as a string filename,
        or as the list of lines that result from calling
        readlines() on the file.

        Raises ValueError if the game file is invalid.

        Valid game files include:

          1. a theme followed by a single blank line, then

          2. multiple lines defining the board followed
             by a single blank line, then

          3. multiple lines defining the answers,
             optionally followed by

          4. a blank line and then any number of remaining
             lines which have no semantic meaning.

        Valid game files require:

          - boards to be rectangular

          - boards where each string is a single,
            alphabetical character (either upper- or
            lower case; for example, both "a" and "A"
            denote the same letter, which is stored
            as "a" in the board object)

          - each line for an answer of the form
            "WORD R C STEP1 STEP2 ..." where
              * WORD has at least three letters,
              * the position (R, C) is within bounds
                of the board,
              * the positions implied by the steps are
                all within bounds of the board, and
              * the letters implied by the strand
                spell the WORD (modulo capitalization)
              * the WORDs and STEPs may be spelled with
                either lower- or uppercase letters, but
                regardless the WORDs are stored in the
                game object with only lowercase letters.

           - that each answer strand has no folds
             (edges do not cross)

           - that answers fill the board

        Game files are allowed to use multiple space
        characters to separate tokens on a line. Also,
        leading and trailing whitespace will be ignored.
        """
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

        self._board = Board(letters)
        
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
            strand = Strand(Pos(start_r - 1, start_c - 1), steps)
            self._answers.append((word, strand))
        
        #check to make sure that every letter is accounted for
        all_positions = set()
        for r in range(self._board.num_rows()):
            for c in range(self._board.num_cols()):
                all_positions.add((r, c))
        
        visited_positions = set()
        for _, strand in self._answers:
            for position in strand.positions():
                coord = (position.r, position.c)
                if coord in visited_positions:
                    raise ValueError(f"{coord} is visited more than once")
                visited_positions.add(coord)

        if visited_positions != all_positions:
            raise ValueError("Not all positions are visited!")
        #validate that the answers correspond to the board correctly
        for answer_word, strand in self._answers:     
            try:
                board_word = self._board.evaluate_strand(strand).lower()
            except ValueError:
                raise ValueError(f"Strand for '{answer_word}' is out of bounds")
            if board_word != answer_word:
                raise ValueError(f"Strand spells {board_word} but expected is {answer_word}")

        #stuff that tracks found strands and words
        self._found_strands: list[StrandBase] = []
        self._found_nontheme_strands: list[StrandBase] = []
        self._found_words: set[str] = set()
        self._found_nontheme_words: set[str] = set()
        
        #stuff related to hint
        self._hint_meter = 0
        self._hint_threshold = hint_threshold
        self._active_hint = None
        self._hints_used = 0

    def theme(self) -> str:
        """
        Return the theme for the game.
        """
        return self._theme

    def board(self) -> BoardBase:
        """
        Return the board for the game.
        """
        return self._board

    def answers(self) -> list[tuple[str, StrandBase]]:
        """
        Return the answers for the game. Each answer
        is a pair comprising a theme word and the
        corresponding strand on the board. Words are
        stored using lowercase letters, even if the
        game file used uppercase letters.
        """
        return self._answers

    def found_strands(self) -> list[StrandBase]:
        """
        Return the theme words that have been found so far,
        represented as strands. The order of strands in the
        output matches the order in which they were found.

        Note two strands may conflict, meaning they involve
        different sequences of steps yet identify the same
        absolute positions on the board. This method returns
        the strands that have been submitted through the
        user interface (i.e. submit_strand) and thus may
        deviate from the strands stored in answers.
        """
        return self._found_strands
    
    def found_nontheme_strands(self) -> list[StrandBase]:
        """
        Returns the STRANDs of the words that have been found but 
        are NOT theme words in the order in which they were found
        """
        return self._found_nontheme_strands
    
    def found_words(self) -> set[str]:
        """
        Returns a list of the found theme WORDS (not the strand itself) 
        in the order in which they were found
        """
        return self._found_words
    
    def found_nontheme_words(self) -> set[str]:
        """
        Returns a list of the found NONTHEME WORDS (not the strand itself) 
        in the order in which they were found
        """
        return self._found_nontheme_words

    def game_over(self) -> bool:
        """
        Decide whether or not the game is over, which means
        checking whether or not all theme words have been
        found.
        """
        return len(self._found_strands) == len(self._answers)

    def hint_threshold(self) -> int:
        """
        Return the hint threshold for the game.
        """
        return self._hint_threshold

    def hint_meter(self) -> int:
        """
        Return the current hint meter for the game.
        If it is greater than or equal to the hint
        threshold, then the user can request a hint.
        """
        return self._hint_meter

    def active_hint(self) -> None | tuple[int, bool]:
        """
        Return the active hint, if any.

        Returns None:
            if there is no active hint.

        Returns (i, False):
            if the active hint corresponds to the ith answer
            in the list of answers, but the start and end
            positions _should not_ be shown to the user.

        Returns (i, True):
            if the active hint corresponds to the ith answer
            in the list of answers, and the start and end
            positions _should_ be shown to the user.
        """
        return self._active_hint

    def submit_strand(self, strand: StrandBase) -> tuple[str, bool] | str:
        """
        Play a selected strand.

        Returns (word, True):
            if the strand corresponds to a theme word which
            has not already been found.

        Returns (word, False):
            if the strand does not correspond to a theme
            word but does correspond to a valid dictionary
            word that has not already been found.

        Returns "Already found":
            if the strand corresponds to a theme word or
            dictionary word that has already been found.

        Returns "Too short":
            if the strand corresponds to fewer than four
            letters.

        Returns "Not in word list":
            if the strand corresponds to a string that
            is not a valid dictionary word.
        """
        word = self._board.evaluate_strand(strand).lower()
        
        for index, (answer_word, answer_strand) in enumerate(self._answers):
            if answer_strand.positions() == strand.positions() or answer_word == word:
                if strand in self._found_strands or word in self._found_words:
                    return "Already found"
                self._found_strands.append(strand)
                self._found_words.add(word)

                if self._active_hint is not None and self._active_hint[0] == index:
                    self._active_hint = None
                
                return (answer_word, True)
            
        if len(word) < 4:
            return "Too short"
        
        if word not in DICTIONARY:
            return "Not in word list"
        
        if strand in self._found_nontheme_strands or word in self._found_nontheme_words:
            return "Already found"
        
        self._found_nontheme_strands.append(strand)
        self._found_nontheme_words.add(word)
        self._hint_meter += 1
        return (word, False)
 
    def use_hint(self) -> tuple[int, bool] | str:
        """
        Play a hint.

        Returns (i, b):
            if successfully updated the active hint. The new
            hint corresponds to the ith answer in the list of
            all answers, which is the first answer that has
            not already been found. The boolean b describes
            whether there was already an active hint before
            this call to use_hint (and thus whether or not the
            first and last letters of the hint word should be
            highlighted).

        Returns "No hint yet":
            if the current hint meter does not yet warrant
            a hint.

        Returns "Use your current hint":
            if there is already an active hint where the
            first and last letters are being displayed.
        """
        if self._active_hint is not None:
            index, status = self._active_hint
            if status == True:
                return "Use your current hint"
            elif self._hint_meter < self._hint_threshold:
                return "No hint yet"
            else:
                self._active_hint = (index, True)
                self._hint_meter -= self._hint_threshold
                self._hints_used += 1
                return self._active_hint

        if self._hint_meter < self._hint_threshold:
            return "No hint yet"
        
        for i, (answer_word, answer_strand) in enumerate(self._answers):
            if answer_word not in self._found_words:
                self._active_hint = (i, False)
                self._hint_meter -= self._hint_threshold
                self._hints_used += 1
                return self._active_hint
        
        return "No hint yet"
