import pytest

from base import Step, PosBase, StrandBase, BoardBase, StrandsGameBase
from strands import Pos, Strand, Board, StrandsGame

def test_inheritance() -> None:
    assert issubclass(Pos, PosBase)
    assert issubclass(Strand, StrandBase)
    assert issubclass(Board, BoardBase)
    assert issubclass(StrandsGame, StrandsGameBase)

def test_pos_take_step() -> None:
    pos = Pos(0, 0)
    assert pos.take_step(Step.N) == Pos(-1, 0)
    assert pos.take_step(Step.E) == Pos(0, 1)
    assert pos.take_step(Step.S) == Pos(1, 0)
    assert pos.take_step(Step.W) == Pos(0, -1)

    assert pos.take_step(Step.NE) == Pos(-1, 1)
    assert pos.take_step(Step.SE) == Pos(1, 1)
    assert pos.take_step(Step.SW) == Pos(1, -1)
    assert pos.take_step(Step.NW) == Pos(-1, -1)

def test_pos_step_to_success() -> None:
    pos = Pos(0, 0)
    assert pos.step_to(Pos(-1, 0)) == Step.N
    assert pos.step_to(Pos(0, 1)) == Step.E
    assert pos.step_to(Pos(1, 0)) == Step.S
    assert pos.step_to(Pos(0, -1)) == Step.W

    assert pos.step_to(Pos(-1, 1)) == Step.NE
    assert pos.step_to(Pos(1, 1)) == Step.SE
    assert pos.step_to(Pos(1, -1)) == Step.SW
    assert pos.step_to(Pos(-1, -1)) == Step.NW

def test_pos_step_to_failure() -> None:
    pos = Pos(0, 0)
    with pytest.raises(ValueError):
        pos.step_to(Pos(-2, 0))
    with pytest.raises(ValueError):
        pos.step_to(Pos(0, 2))
    with pytest.raises(ValueError):
        pos.step_to(Pos(2, 0))
    with pytest.raises(ValueError):
        pos.step_to(Pos(0, -2))

    with pytest.raises(ValueError):
        pos.step_to(Pos(-3, 0))
    with pytest.raises(ValueError):
        pos.step_to(Pos(0, 3))
    with pytest.raises(ValueError):
        pos.step_to(Pos(3, 0))
    with pytest.raises(ValueError):
        pos.step_to(Pos(0, -3))

def test_strand_positions_straight_cardinal() -> None:
    pos = Pos(0, 0)
    assert Strand(pos, [Step.N, Step.N, Step.N, Step.N]).positions() \
        == [Pos(0, 0), Pos(-1, 0), Pos(-2, 0), Pos(-3, 0), Pos(-4, 0)]

    assert Strand(pos, [Step.E, Step.E, Step.E, Step.E]).positions() \
        == [Pos(0, 0), Pos(0, 1), Pos(0, 2), Pos(0, 3), Pos(0, 4)]

    assert Strand(pos, [Step.S, Step.S, Step.S, Step.S]).positions() \
        == [Pos(0, 0), Pos(1, 0), Pos(2, 0), Pos(3, 0), Pos(4, 0)]

    assert Strand(pos, [Step.W, Step.W, Step.W, Step.W]).positions() \
        == [Pos(0, 0), Pos(0, -1), Pos(0, -2), Pos(0, -3), Pos(0, -4)]

def test_strand_positions_straight_intercardinal() -> None:
    pos = Pos(0, 0)
    assert Strand(pos, [Step.NE, Step.NE, Step.NE, Step.NE]).positions() \
        == [Pos(0, 0), Pos(-1, 1), Pos(-2, 2), Pos(-3, 3), Pos(-4, 4)]

    assert Strand(pos, [Step.SE, Step.SE, Step.SE, Step.SE]).positions() \
        == [Pos(0, 0), Pos(1, 1), Pos(2, 2), Pos(3, 3), Pos(4, 4)]

    assert Strand(pos, [Step.SW, Step.SW, Step.SW, Step.SW]).positions() \
        == [Pos(0, 0), Pos(1, -1), Pos(2, -2), Pos(3, -3), Pos(4, -4)]

    assert Strand(pos, [Step.NW, Step.NW, Step.NW, Step.NW]).positions() \
        == [Pos(0, 0), Pos(-1, -1), Pos(-2, -2), Pos(-3, -3), Pos(-4, -4)]

#is folded and this test not tested
"""def test_strand_positions_long() -> None:
    crossless_strand = Strand(Pos(0, 0), [Step.N, Step.NE, Step.E, Step.SE, \
                                          Step.S, Step.SW, Step.W, Step.NW])
    
    assert crossless_strand.positions() == [Pos(0, 0), Pos(-1, 0), Pos(-2, 1), \
                                            Pos(-2, 2), Pos(-1, 3), Pos(0, 3), \
                                            Pos(1, 2), Pos(1, 1), Pos(0, 0)]
    assert not crossless_strand.is_folded()

    cross_strand = Strand(Pos(0, 0), [Step.N, Step.NE, Step.E, Step.SE, \
                                      Step.S, Step.SW, Step.W, Step.NW, \
                                        Step.E, Step.SW])
    
    assert cross_strand.positions() == [Pos(0, 0), Pos(-1, 0), Pos(-2, 1), \
                                        Pos(-2, 2), Pos(-1, 3), Pos(0, 3), \
                                        Pos(1, 2), Pos(1, 1), Pos(0, 0), \
                                            Pos(0, 1), Pos(1, 0)]
    
    assert cross_strand.is_folded()"""

def test_load_game_fore_file() -> None:
    game = StrandsGame("boards/fore.txt")

    assert game.theme() == '"Fore!"'

    assert game.board().num_rows() == 8
    assert game.board().num_cols() == 6

    answers = [
        ("wood", Strand(Pos(2, 0), [Step.S, Step.SE, Step.W])),
        ("iron", Strand(Pos(1, 4), [Step.W, Step.NE, Step.W])),
        ("wedge", Strand(Pos(2, 3), [Step.E, Step.E, Step.N, Step.N])),
        ("driver", Strand(Pos(1, 0), [Step.N, Step.E, Step.S, Step.S, Step.S])),
        ("putter", Strand(Pos(7, 0), [Step.E, Step.N, Step.W, Step.N, Step.E])),
        ("chipper", Strand(Pos(3, 4), [Step.E, Step.S, Step.S, Step.NW, Step.W,\
                                       Step.N])),
        ("utility", Strand(Pos(6, 3), [Step.SE, Step.N, Step.SE, Step.N, \
                                       Step.NW, Step.W])),
        ("golfclubs", Strand(Pos(7, 3), [Step.W, Step.N, Step.N, Step.N, \
                                         Step.N, Step.N, Step.N, Step.N])),
    ]

    assert game.answers() == answers

def test_load_game_fore_variations() -> None:
    txt_variations = [
        """
        "Fore!"

        R I S N O E
        D V B R I G
        W E U W E D
        O R L R C H
        D O C E P I
        E R F Y T P
        T T L U I I
        P U O G T L

        wood       3 1  s se w
        iron       2 5  w ne w
        wedge      3 4  e e n n
        driver     2 1  n e s s s
        putter     8 1  e n w n e
        chipper    4 5  e s s nw w n
        utility    7 4  se n se n nw w
        golfclubs  8 4  w n n n n n n n
        """,
        """
        "Fore!"

        R   I   S   N   O   E
        D   V   B   R   I   G
        W   E   U   W   E   D
        O   R   L   R   C   H
        D   O   C   E   P   I
        E   R   F   Y   T   P
        T   T   L   U   I   I
        P   U   O   G   T   L

        wood       3 1  s se w
        iron       2 5  w ne w
        wedge      3 4  e e n n
        driver     2 1  n e s s s
        putter     8 1  e n w n e
        chipper    4 5  e s s nw w n
        utility    7 4  se n se n nw w
        golfclubs  8 4  w n n n n n n n
        """,
        """
        "Fore!"

        R I S N O E
        D V B R I G
        W E U W E D
        O R L R C H
        D O C E P I
        E R F Y T P
        T T L U I I
        P U O G T L

        wood 3 1 s se w
        iron 2 5 w ne w
        wedge 3 4 e e n n
        driver 2 1 n e s s s
        putter 8 1 e n w n e
        chipper 4 5 e s s nw w n
        utility 7 4 se n se n nw w
        golfclubs 8 4 w n n n n n n n
        """,
        """
        "Fore!"

        R I S N O E
        D V B R I G
        W E U W E D
        O R L R C H
        D O C E P I
        E R F Y T P
        T T L U I I
        P U O G T L

        wood   3 1  s se w
        iron       2     5  w ne w
            wedge      3 4  e e  n n
        driver         2 1  n e s s s
        putter       8 1    e n w   n e
        chipper    4 5         e s s nw w n
            utility    7 4  se n se     n nw w
        golfclubs  8 4      w n n n n n n n
        """,
        """
        "Fore!"

        R I S N O E
        D V B R I G
        W E U W E D
        O R L R C H
        D O C E P I
        E R F Y T P
        T T L U I I
        P U O G T L

        WoOd       3 1  s se w
        iRon       2 5  w ne w
        wedGe      3 4  e e n n
        drIveR     2 1  n e s s s
        PUTTER     8 1  e n w n e
        chIPper    4 5  e s s nw w n
        UtilitY    7 4  se n se n nw w
        golfCLUBS  8 4  w n n n n n n n
        """
    ]

    answers = [
        ("wood", Strand(Pos(2, 0), [Step.S, Step.SE, Step.W])),
        ("iron", Strand(Pos(1, 4), [Step.W, Step.NE, Step.W])),
        ("wedge", Strand(Pos(2, 3), [Step.E, Step.E, Step.N, Step.N])),
        ("driver", Strand(Pos(1, 0), [Step.N, Step.E, Step.S, Step.S, Step.S])),
        ("putter", Strand(Pos(7, 0), [Step.E, Step.N, Step.W, Step.N, Step.E])),
        ("chipper", Strand(Pos(3, 4), [Step.E, Step.S, Step.S, Step.NW, Step.W,\
                                       Step.N])),
        ("utility", Strand(Pos(6, 3), [Step.SE, Step.N, Step.SE, Step.N, \
                                       Step.NW, Step.W])),
        ("golfclubs", Strand(Pos(7, 3), [Step.W, Step.N, Step.N, Step.N, \
                                         Step.N, Step.N, Step.N, Step.N])),
    ]

    for txt in txt_variations:
        lines = txt.split("\n")
        lines = lines[1:]
        game = StrandsGame(lines)

        assert game.theme() == '"Fore!"'
        assert game.board().num_rows() == 8
        assert game.board().num_cols() == 6
        assert game.board().get_letter(Pos(0, 4)) == "o"
        assert game.answers() == answers
        assert len(game.found_strands()) == 0
        assert not game.game_over()

def test_load_game_fore_invalid() -> None:
    txt_variations = [
        """
        "Fore!"

        R I S  O E
        D V B R I G
        W E U W E D
        O R L R C H
        D O C E P I
        E R F Y T P
        T T L U I I
        P U O G T L

        wood       3 1  s se w
        iron       2 5  w ne w
        wedge      3 4  e e n n
        driver     2 1  n e s s s
        putter     8 1  e n w n e
        chipper    4 5  e s s nw w n
        utility    7 4  se n se n nw w
        golfclubs  8 4  w n n n n n n n
        """,
        """
        "Fore!"

        R   I   S   N   O   E
        D   V   B   R   I   G
        W   E   U   W   E   D
        O   R   L   R   C   H
        D   O   C   E   P   I
        E   R   F   Y   T   P
        T   T   L   U   I   I
        P   U   O   G   T   L

        wood       3 4  e e n n
        iron       3 1  s se w
        driver     2 1  n e s s s
        putter     8 1  e n w n e
        chipper    4 5  e s s nw w n
        utility    7 4  se n se n nw w
        golfclubs  8 4  w n n n n n n n
        """,
        """
        "Fore!"

        R I S N O E
        D V B R I G
        W E U W E D
        O R L R C H
        D O C E P I
        E R F Y T P
        T T L U I I
        P U O G T L

        iron 2 5 w ne w
        wedge 3 4 e e n n
        driver 2 1 n e s s s
        putter 8 1 e n w n e
        chipper 4 5 e s s nw w n
        utility 7 4 se n se n nw w
        golfclubs 8 4 w n n n n n n n
        """
    ]
    with pytest.raises(ValueError):
        StrandsGame(txt_variations[0].split("\n"))
    with pytest.raises(ValueError):
        StrandsGame(txt_variations[1].split("\n"))
    with pytest.raises(ValueError):
        StrandsGame(txt_variations[2].split("\n"))

def test_play_game_fore_once() -> None:
    game = StrandsGame("boards/fore.txt")

    assert game.submit_strand(Strand(Pos(2, 0), [Step.S, Step.SE, \
                                                 Step.W])) == ("wood", True)
    assert len(game.found_strands()) == 1

    assert game.submit_strand(Strand(Pos(1, 4), [Step.W, Step.NE, \
                                                 Step.W])) == ("iron", True)
    assert len(game.found_strands()) == 2

    assert game.submit_strand(Strand(Pos(2, 3), [Step.E, Step.E, Step.N, \
                                                 Step.N])) == ("wedge", True)
    assert len(game.found_strands()) == 3

    assert game.submit_strand(Strand(Pos(1, 0), [Step.N, Step.E, Step.S, \
                                                 Step.S, Step.S])) == \
                                                 ("driver", True)
    assert len(game.found_strands()) == 4

    assert game.submit_strand(Strand(Pos(7, 0), [Step.E, Step.N, Step.W, \
                                                 Step.N, Step.E])) == \
                                                 ("putter", True)
    assert len(game.found_strands()) == 5

    assert game.submit_strand(Strand(Pos(3, 4), [Step.E, Step.S, Step.S, \
                                                 Step.NW, Step.W, Step.N])) == \
                                                    ("chipper", True)
    assert len(game.found_strands()) == 6

    assert game.submit_strand(Strand(Pos(6, 3), [Step.SE, Step.N, Step.SE, \
                                                 Step.N, Step.NW, Step.W])) == \
                                                    ("utility", True)
    assert len(game.found_strands()) == 7

    assert game.submit_strand(Strand(Pos(7, 3), [Step.W, Step.N, Step.N, \
                                                 Step.N, Step.N, Step.N, \
                                                    Step.N, Step.N])) == \
                                                        ("golfclubs", True)
    assert len(game.found_strands()) == 8

    assert game.game_over()

def test_play_game_fore_twice() -> None:
    game = StrandsGame("boards/fore.txt")

    assert game.submit_strand(Strand(Pos(2, 0), [Step.S, Step.SE, \
                                                 Step.W])) == ("wood", True)

    assert game.submit_strand(Strand(Pos(1, 4), [Step.W, Step.NE, \
                                                 Step.W])) == ("iron", True)

    assert game.submit_strand(Strand(Pos(2, 3), [Step.E, Step.E, Step.N, \
                                                 Step.N])) == ("wedge", True)

    assert game.submit_strand(Strand(Pos(1, 0), [Step.N, Step.E, Step.S, \
                                                 Step.S, Step.S])) == \
                                                 ("driver", True)

    assert game.submit_strand(Strand(Pos(7, 0), [Step.E, Step.N, Step.W, \
                                                 Step.N, Step.E])) == \
                                                 ("putter", True)

    assert game.submit_strand(Strand(Pos(3, 4), [Step.E, Step.S, Step.S, \
                                                 Step.NW, Step.W, Step.N])) == \
                                                    ("chipper", True)

    assert game.submit_strand(Strand(Pos(6, 3), [Step.SE, Step.N, Step.SE, \
                                                 Step.N, Step.NW, Step.W])) == \
                                                    ("utility", True)

    assert game.submit_strand(Strand(Pos(7, 3), [Step.W, Step.N, Step.N, \
                                                 Step.N, Step.N, Step.N, \
                                                    Step.N, Step.N])) == \
                                                        ("golfclubs", True)

    assert game.game_over()

def test_play_game_fore_three_times() -> None:
    game = StrandsGame("boards/fore.txt")

    assert game.submit_strand(Strand(Pos(2, 0), [Step.S, Step.SE, \
                                                 Step.W])) == ("wood", True)
    
    assert game.submit_strand(Strand(Pos(2, 0), [Step.S, Step.SE, \
                                                 Step.W])) == "Already found"

    assert game.submit_strand(Strand(Pos(1, 4), [Step.W, Step.NE, \
                                                 Step.W])) == ("iron", True)

    assert game.submit_strand(Strand(Pos(2, 3), [Step.E, Step.E, Step.N, \
                                                 Step.N])) == ("wedge", True)

    assert game.submit_strand(Strand(Pos(1, 0), [Step.N, Step.E, Step.S, \
                                                 Step.S, Step.S])) == \
                                                 ("driver", True)

    assert game.submit_strand(Strand(Pos(7, 0), [Step.E, Step.N, Step.W, \
                                                 Step.N, Step.E])) == \
                                                 ("putter", True)

    assert game.submit_strand(Strand(Pos(3, 4), [Step.E, Step.S, Step.S, \
                                                 Step.NW, Step.W, Step.N])) == \
                                                    ("chipper", True)

    assert game.submit_strand(Strand(Pos(6, 3), [Step.SE, Step.N, Step.SE, \
                                                 Step.N, Step.NW, Step.W])) == \
                                                    ("utility", True)
    
    assert game.submit_strand(Strand(Pos(6, 3), [Step.SE, Step.N, Step.SE, \
                                                 Step.N, Step.NW, Step.W])) == \
                                                    "Already found"

    assert game.submit_strand(Strand(Pos(7, 3), [Step.W, Step.N, Step.N, \
                                                 Step.N, Step.N, Step.N, \
                                                    Step.N, Step.N])) == \
                                                        ("golfclubs", True)

    assert game.game_over()

def test_play_game_fore_more() -> None: #incorrect test 
    game = StrandsGame("boards/fore.txt")

    assert game.use_hint() == "No hint yet"
    assert game.active_hint() is None

    game._hint_threshold = 0

    assert game.use_hint() == (0, False)
    assert game.active_hint() == (0, False)
    assert game.use_hint() == (0, True)
    assert game.active_hint() == (0, True)
    assert game.use_hint() == "Use your current hint"
    assert game.active_hint() == (0, True)

    assert game.submit_strand(Strand(Pos(2, 0), [Step.S, Step.SE, \
                                                 Step.W])) == ("wood", True)

    assert game.submit_strand(Strand(Pos(1, 4), [Step.W, Step.NE, \
                                                 Step.W])) == ("iron", True)
    assert game.use_hint() == (2, False)
    assert game.active_hint() == (2, False)

    assert game.submit_strand(Strand(Pos(2, 3), [Step.E, Step.E, Step.N, \
                                                 Step.N])) == ("wedge", True)

    assert game.submit_strand(Strand(Pos(1, 0), [Step.N, Step.E, Step.S, \
                                                 Step.S, Step.S])) == \
                                                 ("driver", True)

    assert game.submit_strand(Strand(Pos(7, 0), [Step.E, Step.N, Step.W, \
                                                 Step.N, Step.E])) == \
                                                 ("putter", True)

    assert game.submit_strand(Strand(Pos(3, 4), [Step.E, Step.S, Step.S, \
                                                 Step.NW, Step.W, Step.N])) == \
                                                    ("chipper", True)

    assert game.submit_strand(Strand(Pos(6, 3), [Step.SE, Step.N, Step.SE, \
                                                 Step.N, Step.NW, Step.W])) == \
                                                    ("utility", True)

    assert game.submit_strand(Strand(Pos(7, 3), [Step.W, Step.N, Step.N, \
                                                 Step.N, Step.N, Step.N, \
                                                    Step.N, Step.N])) == \
                                                        ("golfclubs", True)
    assert game.active_hint() is None

def test_is_not_cyclic() -> None:
    assert not Strand(Pos(0, 0), [Step.N, Step.E]).is_cyclic()
    assert not Strand(Pos(0, 0), [Step.N, Step.E, Step.S]).is_cyclic()
    assert not Strand(Pos(0, 0), [Step.N, Step.E, Step.S, Step.S, \
                                  Step.W]).is_cyclic()
    assert not Strand(Pos(0, 0), [Step.N, Step.E, Step.S, Step.S, \
                                  Step.W, Step.W, Step.N]).is_cyclic()

def test_is_cyclic() -> None:
    assert Strand(Pos(0, 0), [Step.N, Step.E, Step.SW]).is_cyclic()
    assert Strand(Pos(0, 0), [Step.N, Step.E, Step.S, Step.W]).is_cyclic()
    assert Strand(Pos(0, 0), [Step.N, Step.E, Step.S, Step.S, Step.W, \
                              Step.N]).is_cyclic()
    assert Strand(Pos(0, 0), [Step.N, Step.E, Step.S, Step.S, Step.W, \
                              Step.W, Step.N, Step.E]).is_cyclic()

def test_overlapping() -> None:
    game = StrandsGame("boards/fore.txt")
    path1 = [Step.E, Step.N, Step.W, Step.N, Step.E]
    path2 = [Step.E, Step.NW, Step.E, Step.NW, Step.E]
    assert game.submit_strand(Strand(Pos(7, 0), path1)) == ("putter", True)
    assert game.submit_strand(Strand(Pos(7, 0), path2)) == "Already found"

    game = StrandsGame("boards/its-in-the-stars.txt")
    path1 = [Step.E, Step.E, Step.N, Step.E, Step.S]
    path2 = [Step.E, Step.NE, Step.S, Step.NE, Step.S]
    assert game.submit_strand(Strand(Pos(7, 1), path1)) == ("dipper", True)
    assert game.submit_strand(Strand(Pos(7, 1), path2)) == "Already found"

def test_load_game_its_in_the_stars_file() -> None:
    game = StrandsGame("boards/its-in-the-stars.txt")

    assert game.theme() == '"It\'s in the stars"'

    assert game.board().num_rows() == 8
    assert game.board().num_cols() == 6

    answers = [
        ("swan", Strand(Pos(1, 5), [Step.W, Step.SE, Step.S])),
        ("cross", Strand(Pos(5, 4), [Step.NE, Step.S, Step.S, Step.S])),
        ("hunter", Strand(Pos(0, 5), [Step.W, Step.W, Step.S, Step.W, Step.N])),
        ("maiden", Strand(Pos(3, 4), [Step.S, Step.NW, Step.NE, Step.W, \
                                      Step.W])),
        ("dipper", Strand(Pos(7, 1), [Step.E, Step.E, Step.N, Step.E, Step.S])),
        ("centaur", Strand(Pos(3, 2), [Step.S, Step.S, Step.NE, Step.S, \
                                       Step.SW, Step.W])),
        ("constellations", Strand(Pos(0, 0), [Step.E, Step.S, Step.W, Step.SE, \
                                              Step.W, Step.S, Step.E, Step.SW, \
                                                Step.E, Step.S, Step.W, Step.S,\
                                                      Step.S]))
    ]

    assert game.answers() == answers

def test_load_game_its_in_the_stars_variations() -> None:
    txt_variations = [
        """
        "It's in the stars"

        C O R N U H
        S N E T W S
        E T N E D A
        L L C I M N
        A T E T A R
        O I N A C O
        N R U P E S
        S D I P R S

        swan            2 6  w se s
        cross           6 5  ne s s s
        hunter          1 6  w w s w n
        maiden          4 5  s nw ne w w
        dipper          8 2  e e n e s
        centaur         4 3  s s ne s sw w
        constellations  1 1  e s w se w s e sw e s w s s
        """,
        """
        "It's in the stars"

        C   O   R   N   U   H
        S   N   E   T   W   S
        E   T   N   E   D   A
        L   L   C   I   M   N
        A   T   E   T   A   R
        O   I   N   A   C   O
        N   R   U   P   E   S
        S   D   I   P   R   S

        swan            2 6  w se s
        cross           6 5  ne s s s
        hunter          1 6  w w s w n
        maiden          4 5  s nw ne w w
        dipper          8 2  e e n e s
        centaur         4 3  s s ne s sw w
        constellations  1 1  e s w se w s e sw e s w s s
        """,
        """
        "It's in the stars"

        C O R N U H
        S N E T W S
        E T N E D A
        L L C I M N
        A T E T A R
        O I N A C O
        N R U P E S
        S D I P R S

        swan 2 6 w se s
        cross 6 5 ne s s s
        hunter 1 6 w w s w n
        maiden 4 5 s nw ne w w
        dipper 8 2 e e n e s
        centaur 4 3 s s ne s sw w
        constellations 1 1 e s w se w s e sw e s w s s
        """,
        """
        "It's in the stars"

        C O R N U H
        S N E T W S
        E T N E D A
        L L C I M N
        A T E T A R
        O I N A C O
        N R U P E S
        S D I P R S

        swan      2 6     w se s
        cross                       6 5  ne     s s s
        hunter          1    6  w w s w n
        maiden              4 5  s nw    ne w w
        dipper            8 2  e e n e s
            centaur         4 3        s s   ne s sw w
        constellations  1 1  e s    w se   w s e sw e s w    s s
        """,
        """
        "It's in the stars"

        C O R N U H
        S N E T W S
        E T N E D A
        L L C I M N
        A T E T A R
        O I N A C O
        N R U P E S
        S D I P R S

        swAn            2 6  w se s
        CROSS           6 5  ne s s s
        huntEr          1 6  w w s w n
        maIden          4 5  s nw ne w w
        DiPper          8 2  e e n e s
        centauR         4 3  s s ne s sw w
        consteLLations  1 1  e s w se w s e sw e s w s s
        """
    ]

    answers = [
        ("swan", Strand(Pos(1, 5), [Step.W, Step.SE, Step.S])),
        ("cross", Strand(Pos(5, 4), [Step.NE, Step.S, Step.S, Step.S])),
        ("hunter", Strand(Pos(0, 5), [Step.W, Step.W, Step.S, Step.W, Step.N])),
        ("maiden", Strand(Pos(3, 4), [Step.S, Step.NW, Step.NE, Step.W, \
                                      Step.W])),
        ("dipper", Strand(Pos(7, 1), [Step.E, Step.E, Step.N, Step.E, Step.S])),
        ("centaur", Strand(Pos(3, 2), [Step.S, Step.S, Step.NE, Step.S, \
                                       Step.SW, Step.W])),
        ("constellations", Strand(Pos(0, 0), [Step.E, Step.S, Step.W, Step.SE, \
                                              Step.W, Step.S, Step.E, Step.SW, \
                                                Step.E, Step.S, Step.W, Step.S,\
                                                      Step.S]))
    ]

    for txt in txt_variations:
        lines = txt.split("\n")
        lines = lines[1:]
        game = StrandsGame(lines)

        assert game.theme() == '''"It\'s in the stars"'''
        assert game.board().num_rows() == 8
        assert game.board().num_cols() == 6
        assert game.board().get_letter(Pos(0, 4)) == "u"
        assert game.answers() == answers
        assert len(game.found_strands()) == 0
        assert not game.game_over()

def test_load_game_its_in_the_stars_invalid() -> None:
    txt_variations = [
        """
        "It's in the stars"

        C O R N  H
        S N E T W S
        E T N E D A
        L L C I M N
        A T E T A R
        O I N A C O
        N R U P E S
        S D I P R S

        swan            2 6  w se s
        cross           6 5  ne s s s
        hunter          1 6  w w s w n
        maiden          4 5  s nw ne w w
        dipper          8 2  e e n e s
        centaur         4 3  s s ne s sw w
        constellations  1 1  e s w se w s e sw e s w s s
        """,
        """
        "It's in the stars"

        C O R N U H
        S N E T W S
        E T N E D A
        L L C I M N
        A T E T A R
        O I N A C O
        N R U P E S
        S D I P R S

        swaan            2 6  w se s
        cross           6 5  ne s s s
        hunter          1 6  w w s w n
        maiden          4 5  s nw ne w w
        dipper          8 2  e e n e s
        centaur         4 3  s s ne s sw w
        constellations  1 1  e s w se w s e sw e s w s s
        """,
        """
        "It's in the stars"

        C O R N U H
        S N E T W S
        E T N E D A
        L L C I M N
        A T E T A R
        O I N A C O
        N R U P E S
        S D I P R S

        cross           6 5  ne s s s
        hunter          1 6  w w s w n
        maiden          4 5  s nw ne w w
        dipper          8 2  e e n e s
        centaur         4 3  s s ne s sw w
        constellations  1 1  e s w se w s e sw e s w s s
        """
    ]
    with pytest.raises(ValueError):
        StrandsGame(txt_variations[0].split("\n"))
    with pytest.raises(ValueError):
        StrandsGame(txt_variations[1].split("\n"))
    with pytest.raises(ValueError):
        StrandsGame(txt_variations[2].split("\n"))

def test_play_game_its_in_the_stars_once() -> None:
    game = StrandsGame("boards/its-in-the-stars.txt")

    assert game.submit_strand(Strand(Pos(1, 5), [Step.W, Step.SE, \
                                                 Step.S])) == ("swan", True)
    assert len(game.found_strands()) == 1

    assert game.submit_strand(Strand(Pos(5, 4), [Step.NE, Step.S, \
                                                 Step.S, Step.S])) == \
                                                    ("cross", True)
    assert len(game.found_strands()) == 2

    assert game.submit_strand(Strand(Pos(0, 5), [Step.W, Step.W, Step.S, \
                                                 Step.W, Step.N])) == \
                                                    ("hunter", True)
    assert len(game.found_strands()) == 3

    assert game.submit_strand(Strand(Pos(3, 4), [Step.S, Step.NW, Step.NE, \
                                                 Step.W, Step.W])) == \
                                                    ("maiden", True)
    assert len(game.found_strands()) == 4

    assert game.submit_strand(Strand(Pos(7, 1), [Step.E, Step.E, Step.N, \
                                                 Step.E, Step.S])) == \
                                                    ("dipper", True)
    assert len(game.found_strands()) == 5

    assert game.submit_strand(Strand(Pos(3, 2), [Step.S, Step.S, Step.NE, \
                                                 Step.S, Step.SW, Step.W])) == \
                                                    ("centaur", True)
    assert len(game.found_strands()) == 6

    assert game.submit_strand(Strand(Pos(0, 0), [Step.E, Step.S, Step.W, \
                                                 Step.SE, Step.W, Step.S, \
                                                    Step.E, Step.SW, Step.E, \
                                                        Step.S, Step.W, Step.S,\
                                                              Step.S])) == \
                                                                ("constellations", True)
    assert len(game.found_strands()) == 7

    assert game.game_over()

def test_play_game_its_in_the_stars_twice() -> None:
    game = StrandsGame("boards/its-in-the-stars.txt")

    assert game.submit_strand(Strand(Pos(1, 5), [Step.W, Step.SE, \
                                                 Step.S])) == ("swan", True)

    assert game.submit_strand(Strand(Pos(5, 4), [Step.NE, Step.S, \
                                                 Step.S, Step.S])) == \
                                                    ("cross", True)

    assert game.submit_strand(Strand(Pos(0, 5), [Step.W, Step.W, Step.S, \
                                                 Step.W, Step.N])) == \
                                                    ("hunter", True)

    assert game.submit_strand(Strand(Pos(3, 4), [Step.S, Step.NW, Step.NE, \
                                                 Step.W, Step.W])) == \
                                                    ("maiden", True)

    assert game.submit_strand(Strand(Pos(7, 1), [Step.E, Step.E, Step.N, \
                                                 Step.E, Step.S])) == \
                                                    ("dipper", True)

    assert game.submit_strand(Strand(Pos(3, 2), [Step.S, Step.S, Step.NE, \
                                                 Step.S, Step.SW, Step.W])) == \
                                                    ("centaur", True)

    assert game.submit_strand(Strand(Pos(0, 0), [Step.E, Step.S, Step.W, \
                                                 Step.SE, Step.W, Step.S, \
                                                    Step.E, Step.SW, Step.E, \
                                                        Step.S, Step.W, Step.S,\
                                                              Step.S])) == \
                                                                ("constellations", True)
 
    assert game.game_over()

def test_play_game_its_in_the_stars_three_times() -> None:
    game = StrandsGame("boards/its-in-the-stars.txt")

    assert game.submit_strand(Strand(Pos(1, 5), [Step.W, Step.SE, \
                                                 Step.S])) == ("swan", True)
    assert game.submit_strand(Strand(Pos(1, 5), [Step.W, Step.SE, \
                                                 Step.S])) == "Already found"


    assert game.submit_strand(Strand(Pos(5, 4), [Step.NE, Step.S, \
                                                 Step.S, Step.S])) == \
                                                    ("cross", True)

    assert game.submit_strand(Strand(Pos(0, 5), [Step.W, Step.W, Step.S, \
                                                 Step.W, Step.N])) == \
                                                    ("hunter", True)

    assert game.submit_strand(Strand(Pos(3, 4), [Step.S, Step.NW, Step.NE, \
                                                 Step.W, Step.W])) == \
                                                    ("maiden", True)

    assert game.submit_strand(Strand(Pos(7, 1), [Step.E, Step.E, Step.N, \
                                                 Step.E, Step.S])) == \
                                                    ("dipper", True)

    assert game.submit_strand(Strand(Pos(3, 2), [Step.S, Step.S, Step.NE, \
                                                 Step.S, Step.SW, Step.W])) == \
                                                    ("centaur", True)

    assert game.submit_strand(Strand(Pos(3, 2), [Step.S, Step.S, Step.NE, \
                                                 Step.S, Step.SW, Step.W])) == \
                                                 "Already found"

    assert game.submit_strand(Strand(Pos(0, 0), [Step.E, Step.S, Step.W, \
                                                 Step.SE, Step.W, Step.S, \
                                                    Step.E, Step.SW, Step.E, \
                                                        Step.S, Step.W, Step.S,\
                                                              Step.S])) == \
                                                                ("constellations", True)
 
    assert game.game_over()

def test_play_game_its_in_the_stars_more() -> None:
    game = StrandsGame("boards/its-in-the-stars.txt")

    assert game.use_hint() == "No hint yet"
    assert game.active_hint() is None

    game._hint_threshold = 0

    assert game.use_hint() == (0, False)
    assert game.active_hint() == (0, False)
    assert game.use_hint() == (0, True)
    assert game.active_hint() == (0, True)
    assert game.use_hint() == "Use your current hint"
    assert game.active_hint() == (0, True)

    assert game.submit_strand(Strand(Pos(1, 5), [Step.W, Step.SE, Step.S])) == ("swan", True)
    assert game.submit_strand(Strand(Pos(5, 4), [Step.NE, Step.S, Step.S, Step.S])) == ("cross", True)
    assert game.use_hint() == (2, False)
    assert game.active_hint() == (2, False)

    assert game.submit_strand(Strand(Pos(0, 5), [Step.W, Step.W, Step.S, Step.W, Step.N])) == ("hunter", True)
    assert game.submit_strand(Strand(Pos(3, 4), [Step.S, Step.NW, Step.NE, Step.W, Step.W])) == ("maiden", True)
    assert game.submit_strand(Strand(Pos(7, 1), [Step.E, Step.E, Step.N, Step.E, Step.S])) == ("dipper", True)
    assert game.submit_strand(Strand(Pos(3, 2), [Step.S, Step.S, Step.NE, Step.S, Step.SW, Step.W])) == ("centaur", True)
    assert game.submit_strand(Strand(Pos(0, 0), [Step.E, Step.S, Step.W, Step.SE, Step.W, Step.S, Step.E, Step.SW, Step.E, Step.S, Step.W, Step.S, Step.S])) == ("constellations", True)
    assert game.active_hint() is None


def test_valid_game_files() -> None:
    with pytest.raises(ValueError):
        StrandsGame("boards/shine-on.txt")

    StrandsGame("boards/two-thumbs-up.txt")
    StrandsGame("boards/the-feeling-is-mutual.txt")
    StrandsGame("boards/on-the-hunt.txt")
    StrandsGame("boards/cs-142.txt")
    StrandsGame("boards/step-on-it.txt")
    StrandsGame("boards/coarse-material.txt")
    StrandsGame("boards/buzzing-in.txt")
    StrandsGame("boards/join-the-chorus.txt")
    StrandsGame("boards/directions.txt")
    StrandsGame("boards/kitty-corner.txt")
    StrandsGame("boards/fore.txt")
    StrandsGame("boards/face-time.txt")
    StrandsGame("boards/sleep-tight.txt")
    StrandsGame("boards/the-movies.txt")
    StrandsGame("boards/___-a-___.txt")
    StrandsGame("boards/wetland-patrol.txt")
    StrandsGame("boards/best-in-class.txt")
    StrandsGame("boards/ive-got-you-covered.txt")
    StrandsGame("boards/counter-offers.txt")
    StrandsGame("boards/in-stitches.txt")
    StrandsGame("boards/i-get-around.txt")
    StrandsGame("boards/what-a-trill.txt")
    StrandsGame("boards/what-a-softie.txt")
    StrandsGame("boards/a-good-roast.txt")
    StrandsGame("boards/thats-quite-a-tasty-mouthful.txt")
    StrandsGame("boards/my-bad.txt")
    StrandsGame("boards/its-in-the-stars.txt")
    StrandsGame("boards/grrr.txt")
    StrandsGame("boards/free-for-all.txt")
    StrandsGame("boards/what-talent.txt")

def test_play_game_a_hints_0() -> None:
    game = StrandsGame("boards/___-a-___.txt")
    game._hint_threshold = 0

    assert game.use_hint() == (0, False)
    assert game.use_hint() == (0, True)

    game.submit_strand(Strand(Pos(2,5), [Step.S, Step.NW, Step.NE]))
    assert game.use_hint() == (1, False)
    assert game.use_hint() == (1, True)

def test_play_game_a_hints_0() -> None:
    game = StrandsGame("boards/___-a-___.txt")
    game._hint_threshold = 1

    game.submit_strand(Strand(Pos(0,0), [Step.S, Step.E, Step.S]))#SEAL
    game.submit_strand(Strand(Pos(0,0), [Step.S, Step.E, Step.N]))#SEAT
    game.submit_strand(Strand(Pos(0,2), [Step.SW, Step.N, Step.SW]))#HATE
    game.submit_strand(Strand(Pos(0,1), [Step.S, Step.S, Step.W]))#TALE

    assert game.use_hint() == (0, False)
    assert game.use_hint() == (0, True)

    game.submit_strand(Strand(Pos(2,5), [Step.S, Step.NW, Step.NE]))
    assert game.use_hint() == (1, False)
    assert game.use_hint() == (1, True)

def test_play_game_a_good_roast_hints_0() -> None:
    game = StrandsGame("boards/a-good-roast.txt")
    game._hint_threshold = 0

    assert game.use_hint() == (0, False)
    assert game.use_hint() == (0, True)
    game.submit_strand(Strand(Pos(7,5), [Step.W, Step.NE, Step.W]))
    assert game.use_hint() == (1, False)
    assert game.use_hint() == (1, True)

def test_play_game_a_good_roast_hints_0() -> None:
    game = StrandsGame("boards/a-good-roast.txt")
    game._hint_threshold = 1

    game.submit_strand(Strand(Pos(2,4), [Step.E, Step.N, Step.NW]))#HARK
    game.submit_strand(Strand(Pos(2,4), [Step.NW, Step.N, Step.W]))#HELP
    game.submit_strand(Strand(Pos(2,4), [Step.N, Step.NE, Step.W]))#HUCK
    game.submit_strand(Strand(Pos(0,3), [Step.SE, Step.NE, Step.W]))#LUCK

    assert game.use_hint() == (0, False)
    assert game.use_hint() == (0, True)

    game.submit_strand(Strand(Pos(7,5), [Step.W, Step.NE, Step.W]))
    assert game.use_hint() == (1, False)
    assert game.use_hint() == (1, True)