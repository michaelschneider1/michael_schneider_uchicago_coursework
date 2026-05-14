# CMSC 14200 Course Project

Team members:
- Art: Lucas Marquie (lucasmarquie)
- GUI: Michael Schneider (michaelschneider)
- TUI: Davis Schukar (dschukar)
- QA: Henry Rose (henryr)

## Revisions

### Game Logic

USE_HINT: (line and lines around 511) only allows hints if the hint_meter is at 
least as large as the hint_threshold and now subtracts from the hint_meter if 
a hint is used

OVERLAPPING STRAND: Added new variables (lines 323, 324) (found_words, and 
found_nontheme_words) to test for found words as well as found positions as 
well as following get functions for them.

INVALID GAME FILE HANDLING: On lines 312-319, the code now checks to make sure
that every letter in the board is visited and that the answer_word provided is
the same word that is evaluated by the given answer_strand

### GUI

OVERLAPPING STRAND: fixed in game logic now accepts an overlapping strand in 
the multiple types of spelling of a word

ART GUI: now implemented as a wallpaper of the screen

HINT_COUNTER: hint counter is now present and works properly

DOCSTRINGS: added docstrings to the functions explaining the purpose of each

### TUI
Completeness:
[Major] Found strands are not highlighted at all.
I completely reworked how the highlighting and connections are displayed, so it
now displays properly and correctly based on completion status and user inputs.
These changes changes a huge amount of my code, including the creation of a
several of the functions and the TUIGame class.

Code Quality:
[Major] Missing documentation of student created methods and/or functions.
Documentation has been added for all of the functions and methods.
(Lines 55, 118, 180, 264, 305, and 448)
[Major] Uses global variables.
All variables are now located within classes and functions, with the exception
of the professor keyboard input code and the text color constants.
(Lines 11 - 52)

### Art
- This component received two S scores in Milestone 2

### QA
- This component received two S scores in Milestone 2.


## TUI Enhancements

### Feature 1
TUI-TITLE-SCREEN - Will display text with the word "STRANDS" and a request to 
press enter to begin. When enter is pressed, either game will start or Feature 2
will be displayed. SHIFT+Q will exit the screen (as is true with other screens).

### Feature 2
TUI-GAME-MENU - If no game is specified, instead of randomly selecting a game,
the player will be taken to a game menu screen after the title screen. This menu
displays all of the available boards in the src/boards/ folder. The user can
then use the arrow keys to navigate the screen and ENTER to select a board.
The board will then be displayed and the game will begin.

### Feature 3
TUI-SCORING - The game keeps a simple scoring system, where the player gains 5
points for using a hint and 1 point for an invalid or incorrect guess. The final
score is displayed upon completion of the game, and the objective is to get the
lowest score possible (like golf).



## GUI Enhancements

### FEATURE-1

GUI TITLE-SCREEN - When running the GUI, you should see a blue screen with the 
title "Strands" with a white play button that when clicked or enter is clicked, 
starts the game with whatever settings you choose

### FEATURE-2

GUI - SPECIAL - When you run the following command:
python3 src/gui.py --special  
you will be prompted with a pokemon themed game with a frame with your favorite
pokemon!

### FEATURE-3
SCORING - scores the game in GUI based on how long it takes to complete the 
game and how many hints are used. Scoring rubric below:
    0-2 mins: 100 points
    2-4 mins: 80 points
    4-6 mins: 50 points
    6+ mins: 25 points
    Each hint used: -10 points
Score will display in GUI once board is complete! (Note that score can be 
negative if enough hints are used)
