import pygame
import sys
import click
import random
from art_gui import ArtGUI9Slice, PolkaDotsGUI, HoneycombGUI, PokemonGUI
from strands import StrandsGame, Pos, Strand

"""
External Links used:

Pygame resources:
https://www.pygame.org/docs/ref/draw.html
^^^other pygame.org links 
Click resources:
https://click.palletsprojects.com/en/stable/
https://github.com/pallets/click
Lecture notes
"""

LETTER_SPACING = 30
MARGIN = 20
LIGHT_GRAY = (83, 83, 83)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
LETTER_Y_OFFSET = 40
LETTER_X_OFFSET = 15

TIMER_EVENT = pygame.USEREVENT + 1

class GameTypeError(Exception):
    pass

COLOR_LIBRARY = {0: (0, 0, 255), #blue
1: (0, 255, 0), #green
2: (255, 0, 0), #red
3: (255, 20, 147), #pink
4: (148, 0, 211), #purple
5: (255, 140, 0), #orange
6: (0, 255, 255), #cyan
7: (255, 255, 0), #yellow
8: (160, 82, 45), #brown
9: (230, 230, 250), #lilac
10: (128, 0, 0)} #maroon

class StrandsGUI:
    def __init__(self, game, show_all = False, art = "stub") -> None:
        """
        Initializes the game
        """
        pygame.init()
        pygame.display.set_caption("Strands Game")

        self.game = game
        self.show_all = show_all
        self.art = art
        self.frame = self.load_art_frame_(art)
        self.selected_positions: list[Pos] = []
        self.active_hint_strand = None
        self.hint_status_message = ""
        self.submit_status_message = ""
        self.elapsed_time = 0
        pygame.time.set_timer(TIMER_EVENT, 1000)
        self.board_x = 0
        self.board_y = 0

        width = (MARGIN * 2) + (self.game.board().num_cols() * LETTER_SPACING) + 300
        height = (MARGIN * 2) + (self.game.board().num_rows() * LETTER_SPACING) + 300
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.SysFont(None, 25)
        self.clock = pygame.time.Clock()
        self.running: bool = True
        self.title_screen()
        self.run_event_loop()
    
    def load_art_frame_(self, art: str):
        """
        based on input given, loads that given art
        """
        if art == "stub":
            return None
        elif art == "cat0":
            return ArtGUI9Slice(85)
        elif art == "polka":
            return PolkaDotsGUI(30)
        elif art == "cat1":
            return PolkaDotsGUI(30)
        elif art == "cat2":
            raise NotImplementedError
        elif art == "cat3":
            return HoneycombGUI(30)
        elif art == "cat4":
            raise NotImplementedError
        elif art == "special":
            return PokemonGUI(30)
        else:
            return None

    def title_screen(self):
        """
        Displays a title screen. Can use the following inputs:
        q: quit
        return: start game
        click: if click the start button, starts game
        """
        while True:
            self.screen.fill((173, 216, 230))

            title_font = pygame.font.SysFont(None, 72)
            play_font = pygame.font.SysFont(None, 36)

            title = title_font.render("Strands", True, BLACK)
            play = play_font.render("Play", True, BLACK)

            title_pos = title.get_rect(center = (self.screen.get_width() // 2, self.screen.get_height() // 2 - 60))

            play_button = pygame.Rect(0, 0, 120, 50)
            play_button.center = (self.screen.get_width() // 2, self.screen.get_height() // 2 + 10)
            

            self.screen.blit(title, title_pos)
            pygame.draw.rect(self.screen, (255, 255, 255), play_button)
            self.screen.blit(play, play.get_rect(center = play_button.center))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit(0)
                    if event.key == pygame.K_RETURN:
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.collidepoint(event.pos):
                        return

    def assign_color(self, strand, color, positions_to_color) -> None:
        """
        assigns a color to a strand
        """
        for position in strand.positions():
            positions_to_color[(position.r, position.c)] = color
    
    def draw_connecting_line(self, strand, color) -> None:
        """
        draws the line between a strand 
        """
        points_to_connect = []

        for position in strand.positions():
            x = self.board_x + LETTER_X_OFFSET + position.c * LETTER_SPACING + 2
            y = self.board_y + LETTER_Y_OFFSET + position.r * LETTER_SPACING + 5
            points_to_connect.append((x, y))
        
        pygame.draw.lines(self.screen, color, False, points_to_connect, 2)

    def is_close_enough(self, position: Pos) -> bool:
        """
        Returns True if the click is within an appropriate boundry of the letter
        you are trying to click. False otherwise.
        """
        return (0 <= position.r < self.game.board().num_rows() and 
        0 <= position.c < self.game.board().num_cols())
    
    def submit_current_strand(self, positions: list[Pos]) -> None:
        """
        Submits the strand of the selected positions as well as updates the 
        display messages
        """
        self.submit_status_message = ""
        self.hint_status_message = ""
        if len(positions) < 4:
            self.submit_status_message = "Too short"
            self.selected_positions.clear()
            return
        
        steps = []
        for index, _ in enumerate(positions[:-1]):
            steps.append(positions[index].step_to(positions[index + 1]))
        
        built_strand = Strand(positions[0], steps)
        result = self.game.submit_strand(built_strand)

        if not isinstance(result, tuple):
            self.submit_status_message = result

        if self.active_hint_strand and built_strand.positions() == self.active_hint_strand.positions():
            self.active_hint_strand = None
        
        self.selected_positions.clear()
    
    def get_score(self) -> int:
        """
        calcuates a final score based on time and hints used.
        0-2 mins: 100 points
        2-4 mins: 80 points
        4-6 mins: 50 points
        6+ mins: 25 points

        each hint used: -10 points
        """
        score = 0
        minutes_elapsed = self.elapsed_time / 60

        if minutes_elapsed <= 2:
            score += 100
        elif minutes_elapsed <= 4:
            score += 80
        elif minutes_elapsed <= 6:
            score += 60
        else:
            score += 25
        
        penalty = -10 * self.game._hints_used

        return score + penalty

    def draw(self) -> None:
        """
        Draws all the seen features on the screen
        """
        board_width = (MARGIN * 2) + (self.game.board().num_cols() * LETTER_SPACING) + 130
        board_height = (MARGIN * 2) + (self.game.board().num_rows() * LETTER_SPACING) + 130
        if self.frame:
            self.frame.draw_background(self.screen)

            self.board_x = (self.screen.get_width() - board_width) // 2
            self.board_y = (self.screen.get_height() - board_height) // 2

            pygame.draw.rect(self.screen, (255, 255, 255), (self.board_x, self.board_y, board_width, board_height))
        else:
            self.screen.fill((255, 255, 255))

        board = self.game.board()
        found_words = set()
        positions_to_color = {}
        color_index = 0
        strands_to_display = self.game.found_strands()
        
        for index, strand in enumerate(strands_to_display):
            color = COLOR_LIBRARY[index % len(COLOR_LIBRARY)]
            self.assign_color(strand, color, positions_to_color)
            self.draw_connecting_line(strand, color)
        
        for row in range(board.num_rows()):
            for col in range(board.num_cols()):
                letter_coord_x = self.board_x + (col * LETTER_SPACING) + LETTER_X_OFFSET
                letter_coord_y = self.board_y + (row * LETTER_SPACING) + LETTER_Y_OFFSET

                letter = board.get_letter(Pos(row, col))

                color = positions_to_color.get((row, col), BLACK)
                
                letter_display = self.font.render(letter, True, color)
                self.screen.blit(letter_display, \
                (letter_coord_x, letter_coord_y))

        found_words = len(self.game.found_strands())
        total_words = len(self.game.answers())

        found_counter = self.font.render(f"Found: {found_words}/{total_words}", True, BLACK)
        use_hint_message = self.font.render(f"Use a hint: {self.game._hint_meter}/{self.game._hint_threshold}", True, BLACK)
        theme_text = self.font.render(f"{self.game.theme()}", True, BLACK)
        submit_message = self.font.render(f"{self.submit_status_message}", True, BLACK)
        hint_message = self.font.render(f"{self.hint_status_message}", True, BLACK)

        self.screen.blit(theme_text, (self.board_x , self.board_y + 10))
        self.screen.blit(use_hint_message, (self.board_x, self.board_y + board_height - 110))
        self.screen.blit(found_counter, (self.board_x, self.board_y + board_height - 90))
        self.screen.blit(submit_message, (self.board_x, self.board_y + board_height - 70))
        self.screen.blit(hint_message, (self.board_x, self.board_y + board_height - 50))

        if not self.show_all and self.selected_positions:
            points_to_connect = []
            for position in self.selected_positions:
                x = self.board_x + LETTER_X_OFFSET + position.c * LETTER_SPACING + 2
                y =  self.board_y + LETTER_Y_OFFSET + position.r * LETTER_SPACING + 5
                points_to_connect.append((x, y))
            
            if len(points_to_connect) > 1:
                pygame.draw.lines(self.screen, LIGHT_GRAY, False, points_to_connect, 2)
            
        active_hint = self.game.active_hint()
        if not self.show_all and active_hint is not None:
            i, status = active_hint
            _, strand = self.game.answers()[i]
            hint_positions = strand.positions()

            for index, position in enumerate(hint_positions):
                x = self.board_x + LETTER_X_OFFSET + position.c * LETTER_SPACING + 6
                y = self.board_y + LETTER_Y_OFFSET + position.r * LETTER_SPACING + 9
                radius = 10
                if status:
                    if index == 0 or index == len(hint_positions) - 1:
                        pygame.draw.circle(self.screen, GREEN, (x, y), radius, 2)
                    else:
                        pygame.draw.circle(self.screen, BLACK, (x, y), radius, 2)
                else:
                    pygame.draw.circle(self.screen, BLACK, (x, y), radius, 2)
        
        #timer
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        timer_display = self.font.render(f"Time: {minutes}: {seconds}", True, BLACK)
        timer_x = self.board_x + board_width - 110
        timer_y = self.board_y + board_height - 110
        self.screen.blit(timer_display, (timer_x, timer_y))

        #hints used
        hints_used = self.game._hints_used
        hints_used_display = self.font.render(f"Hints used: {hints_used}", True, BLACK)
        self.screen.blit(hints_used_display, (timer_x - 40, timer_y + 20))

        if self.game.game_over():
                pygame.time.set_timer(TIMER_EVENT, 0)
                game_over =self.font.render(f"Game Complete! Final Score: {self.get_score()}", True, BLACK)
                game_over_x = self.board_x
                game_over_y = self.board_y + board_height - 20
                self.screen.blit(game_over, (game_over_x, game_over_y))
                
        pygame.display.flip()
    
    def click_possibility(self, position: Pos):
        """
        Handles what happens when you click with your mouse. Here are the 
        possible actions:

        - Adds letter if clicked on to selected_positions if empty
        - Add letter if clicked to selected_positions if it is adjacent to the
        most recent selected letter
        - If there is an existing strand being built, it will truncate to a 
        specific letter if a previous letter in the strand is clicked
        - If the final letter of selected_positions is clicked, it will 
        submit the strand


        """
        if self.selected_positions == []:
            self.selected_positions.append(position)
            return
        
        most_recent = self.selected_positions[-1]
        if position in self.selected_positions:
            index = self.selected_positions.index(position)
            self.selected_positions = self.selected_positions[:index + 1]
        elif position.is_adjacent_to(most_recent):
            self.selected_positions.append(position)
        else:
            self.selected_positions = [position]
        
        if most_recent == position and len(self.selected_positions) >= 4:
            self.submit_current_strand(self.selected_positions)

    def run_event_loop(self) -> None:
        """
        Handles all the different game input operations such as:

        q: quits game
        return: submits a strand
        esc: deselects a selected strand
        click: selects letters for strands (more info in click_possibility)
        h: uses hint if able to
        """
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit(0)
                if not self.game.game_over():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if len(self.selected_positions) >= 4:
                                self.submit_current_strand(self.selected_positions)
                        elif event.key == pygame.K_ESCAPE:
                            self.selected_positions.clear()
                        elif event.key == pygame.K_h:
                            self.hint_status_message = ""
                            use_hint_result = self.game.use_hint()
                            if not isinstance(use_hint_result, tuple):
                                self.hint_status_message = use_hint_result
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        click_x, click_y = event.pos
                        row_position = (click_y - self.board_y - LETTER_Y_OFFSET) // LETTER_SPACING
                        col_position = (click_x - self.board_x - LETTER_X_OFFSET) // LETTER_SPACING
                        click_position = Pos(row_position, col_position)

                        if self.is_close_enough(click_position):
                            self.click_possibility(click_position)
                    elif event.type == TIMER_EVENT:
                        self.elapsed_time += 1

            self.draw()
            self.clock.tick(30)


RANDOM_BOARDS = {1: "___ a ___",
2: "a-good-roast",
3: "best-in-class",
4: "buzzing-in",
5: "coarse-material",
6: "cs-142",
7: "directions",
8: "face-time",
9: "fore",
10: "free-for-all",
11: "grrr",
12: "i-get-around",
13: "in-stitches",
14: "its-in-the-stars",
15: "ive-got-you-covered",
16: "join-the-chorus",
17: "kitty-corner",
18: "my-bad",
19: "on-the-hunt",
20: "shine-on",
21: "sleep-tight",
22: "step-on-it",
23: "thats-quite-a-tasty-mouthful",
24: "the-feeling-is-mutual",
25: "the-movies",
26: "two-thumbs-up",
27: "wetland-patrol",
28: "what-a-softie",
29: "what-a-trill",
30: "what-talent",
31: "a-little-respect",
32: "boogie-woogie-woogie",
33: "find-the-missing-links",
34: "happy",
35: "im-in-lobe",
36: "keep-on-keeping-on",
37: "on-the-side",
38: "outsiders",
39: "say-ah",
40: "star-wars-a-new-hope",
41: "to-a-degree",
42: "training-day",
43: "well-fancy-that"}

def pick_random_board() -> str:
    """
    Picks a random board of the 30 boards given above. Note that some boards 
    are invalid boards and will not run
    """
    random_board_num = random.randint(1, 43)
    return RANDOM_BOARDS[random_board_num]

@click.command()
@click.option("--show", is_flag = True)
@click.option("-g", "--game", type = str)
@click.option("-h", "--hint", "hint_threshold", type = int, default = 3)
@click.option("-a", "--art", type = str, default = "stub")
@click.option("--special", is_flag = True)
def main(show: bool, game: str | None, hint_threshold: int, art: str, special: bool):
    """
    General set up for a game. Will load game with different modes and features
    based on command line input.

    --show: will instantly display all answers (answer key mode)
    -g, --game: will dispaly specific game. If none is given, will load a 
    random game from the RANDOM_BOARDS dictionary if no game is sepcified.
    -h, --hint: allows user to set the hint_threshold in command line. Default
    hint threshold will be 3 (as per the NYT game)
    -a, --art: allows to play the game with an art background. Default is stub
    """
    if game is None:
        game = pick_random_board()

    board_filename = f"boards/{game}.txt"

    if special:
        board_filename = f"assets/GUI-SPECIAL.txt"
        art = "special"

    load_game = StrandsGame(board_filename, hint_threshold)

    if show:
        for _, strand in load_game.answers():
            load_game.submit_strand(strand)
        StrandsGUI(load_game, show_all = True, art = art)
    else:
        StrandsGUI(load_game, show_all = False, art = art)
if __name__ == "__main__":
    main()

