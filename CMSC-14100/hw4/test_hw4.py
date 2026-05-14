"""
CMSC 14100
Updated Winter 2025

Test code for Homework #4
"""

import hw4
import hw4_texts
import json
import os

import sys
import pytest
import helpers


# Handle the fact that the test code may not
# be in the same directory as the solution code
sys.path.insert(0, os.getcwd())

# Don't complain about the position of the import
# pylint: disable=wrong-import-position

MODULE = "hw4"


@pytest.mark.parametrize("word, expected",
                            [
                                ("", ""),
                                ("a", "a"),
                                ("I", "I"),
                                ("in", "in"),
                                ("Chicago", "Chcgo"),
                                ("apothecary", "apthcry"),
                                ("cOmPuTeR", "cmPTR"),
                                ("deinstitutionalization", "dnstttnlztn"),
                                ("coUNTErReVolutIoNARIES", "cNTrRVltNRS"),
                                ("HYDROCHLOROFLUOROCARBON", "HYDRCHLRFLRCRBN")
                            ])
def test_compress_word(word, expected):
    """ Test code for compress_word """
    steps = [f"actual = hw4.compress_word('{word}')"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw4.compress_word(word)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


@pytest.mark.parametrize("text, seq, expected",
                            [
                                ("winter", "000000", ["winter"]),
                                ("winter", "001000", ["win","ter"]),
                                ("winter", "101010", ["w", "in", "te", "r"]),
                                ("combination", "01001000000", ['co', 'mbi', 'nation']),
                                ("counterclockwise",
                                 "0000001000000000",
                                 ["counter", "clockwise"]),
                                ("counterclockwise",
                                 "0101000010100011",
                                 ['co', 'un', 'tercl', 'oc', 'kwis', 'e', '']),
                                ("chicagohasagreatlake",
                                 "00000000100000000000",
                                 ['chicagoha', 'sagreatlake']),
                                ("chicagohasagreatlake",
                                 "00000010011000010000", 
                                 ['chicago', 'has', 'a', 'great', 'lake']),
                                ("chicagohasagreatlake",
                                 "01010001000011101010",
                                 ['ch', 'ic', 'agoh', 'asagr', 'e', 'a', 'tl', 'ak', 'e']),
                                ("Updateswererejectedbecausethetipofyourcurrentbranchisbehinditsremotecounterpart.",
                                 "00000010001000000010000001001001010001000000100000101000001001000001000000000010",
                                ['Updates',
                                 'were',
                                 'rejected',
                                 'because',
                                 'the',
                                 'tip',
                                 'of',
                                 'your',
                                 'current',
                                 'branch',
                                 'is',
                                 'behind',
                                 'its',
                                 'remote',
                                 'counterpart',
                                 '.'])
                            ])
def test_segment_text(text, seq, expected):
    """ Test code for segment_text """
    steps = [f"actual = hw4.segment_text('{text}', '{seq}')"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw4.segment_text(text, seq)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)



@pytest.mark.parametrize("wordlist, text, expected",
                            [
                                (["bork"],
                                 "bork bork bork borka bork borky bork",
                                 [("bork", 5)]),
                                (["post", "begins", "when"],
                                 'tape post line when post begins tape post easily post post when begins begins tape when line line begins tape',
                                 [('post', 5), ('begins', 4), ('when', 3)]),
                                (["new", "few"],
                                 'new reducing new new marvelous marvelous new rather few reducing and and new few marvelous new rather new marvelous rather rather reducing few new few new new few few rather',
                                 [('new', 10), ('few', 6)]),
                                (["new", "few"],
                                 'tape post line when post begins tape post easily post post when begins begins tape when line line begins tape',
                                  [('new', 0), ('few', 0)]),
                                (['a', 'b', 'd'],
                                 'b b b a a a a a a a b c a a c b a c c b b b c c b c b c a c a b',
                                 [('a', 12), ('b', 11), ('d', 0)]),
                                (['c', 'b'],
                                 'b b b a a a a a a a b c a a c b a c c b b b c c b c b c a c a b',
                                 [('c', 9), ('b', 11)]),
                                (["buzz", "bee", "buzzing", "buzzing-noise", "noise"],
                                 'If there\'s a buzzing-noise, somebody\'s making a buzzing-noise, and the only reason for making a buzzing-noise that _I_ know of is because you\'re a bee." Then he thought another long time, and said: "And the only reason for being a bee that I know of is making honey." And then he got up, and said: "And the only reason for making honey is so as _I_ can eat it." So he began to climb the tree. He climbed and he climbed and he climbed, and as he climbed he sang a little song to himself. It went like this: Isn\'t it funny How a bear likes honey? Buzz! Buzz! Buzz! I wonder why he does? Then he climbed a little further ... and a little further ... and then just a little further.',
                                 [('buzz', 3), ('bee', 2), ('buzzing', 0), ('buzzing-noise', 3), ('noise', 0)]),
                                (['computer', 'ibm', 'program', 'modern', 'customer'],
                                 hw4_texts.IBM,
                                 [('computer', 10), ('ibm', 18), ('program', 17), ('modern', 4), ('customer', 3)]),
                                (['computer', 'ibm', 'program', 'modern', 'customer'],
                                 hw4_texts.IBM,
                                 [('computer', 10), ('ibm', 18), ('program', 17), ('modern', 4), ('customer', 3)]),
                                (['functions', 'machine', 'industry', 'coding', 'algebraic', 'printer'],
                                 hw4_texts.IBM,
                                 [('functions', 3),
                                 ('machine', 7),
                                 ('industry', 2),
                                 ('coding', 1),
                                 ('algebraic', 1),
                                 ('printer', 1)]),
                            ])
def test_count_words(wordlist, text, expected):
    """ Test code for count_words """
    steps = [f"actual = hw4.count_words({wordlist}, '{text}')"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw4.count_words(wordlist, text)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


@pytest.mark.parametrize("text, expected",
                            [
                                ("word", 
                                 []),
                                ("two words", 
                                 [("two", "words")]),
                                ("The 1401 uses a stored program.'", 
                                [('the', '1401'),
                                 ('1401', 'uses'),
                                 ('uses', 'a'),
                                 ('a', 'stored'),
                                 ('stored', 'program')]),
                                ("Many other advantages might be enumerated.", 
                                [('many', 'other'),
                                 ('other', 'advantages'),
                                 ('advantages', 'might'),
                                 ('might', 'be'),
                                 ('be', 'enumerated')]
                                 ),
                                ('"What is the matter?" asked the Ghost.',
                                [('what', 'is'),
                                 ('is', 'the'),
                                 ('the', 'matter'),
                                 ('matter', 'asked'),
                                 ('asked', 'the'),
                                 ('the', 'ghost')]
                                 ),
                                ('The finger pointed from the grave to him, and back again.',
                                [('the', 'finger'),
                                 ('finger', 'pointed'),
                                 ('pointed', 'from'),
                                 ('from', 'the'),
                                 ('the', 'grave'),
                                 ('grave', 'to'),
                                 ('to', 'him'),
                                 ('him', 'and'),
                                 ('and', 'back'),
                                 ('back', 'again')]
                                 ),
                                ("Chicago has a great lake.", 
                                 [("chicago", "has"), ("has", "a"), ("a", "great"), ("great", "lake")]),
                                ("And then he feels that perhaps there isn't.",
                                [('and', 'then'),
                                 ('then', 'he'),
                                 ('he', 'feels'),
                                 ('feels', 'that'),
                                 ('that', 'perhaps'),
                                 ('perhaps', 'there'),
                                 ('there', "isn't")]
                                 ),
                                ("Printed by order of the House of Commons.", 
                                [('printed', 'by'),
                                 ('by', 'order'),
                                 ('order', 'of'),
                                 ('of', 'the'),
                                 ('the', 'house'),
                                 ('house', 'of'),
                                 ('of', 'commons')]
                                 ),
                                ('Well-tested programming languages for communication with computers must accompany the systems.', 
                                 [('well-tested', 'programming'),
                                 ('programming', 'languages'),
                                 ('languages', 'for'),
                                 ('for', 'communication'),
                                 ('communication', 'with'),
                                 ('with', 'computers'),
                                 ('computers', 'must'),
                                 ('must', 'accompany'),
                                 ('accompany', 'the'),
                                 ('the', 'systems')])
                            ])
def test_list_bigrams(text, expected):
    """ Test code for list_bigrams """
    steps = [f"actual = hw4.list_bigrams('{text}')"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw4.list_bigrams(text)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


@pytest.mark.parametrize("counts, expected",
                            [
                                ([("bork", 5)], [(5, "bork")]),
                                ([('c', 9), ('b', 11)], [(11, 'b'), (9, 'c')]),
                                ([('computer', 10), ('ibm', 18), ('program', 17), ('modern', 4), ('customer', 3)], 
                                 [(18, 'ibm'), (17, 'program'), (10, 'computer'), (4, 'modern'), (3, 'customer')]),
                                ([('buzz', 3), ('bee', 2), ('buzzing', 0), ('buzzing-noise', 3), ('noise', 0)], 
                                 [(3, 'buzzing-noise'), (3, 'buzz'), (2, 'bee'), (0, 'noise'), (0, 'buzzing')]),
                                ([('ufvvsrujc', 11),
                                 ('ywdzzqs', 72),
                                 ('omo', 11),
                                 ('csgtgdxyx', 81),
                                 ('lzqeaviw', 85),
                                 ('ukvevc', 64)], 
                                 [(85, 'lzqeaviw'),
                                 (81, 'csgtgdxyx'),
                                 (72, 'ywdzzqs'),
                                 (64, 'ukvevc'),
                                 (11, 'ufvvsrujc'),
                                 (11, 'omo')]),
                                ([('applying', 12), ('been', 26), ('getting', 35), ('than', 11)], [(35, 'getting'), (26, 'been'), (12, 'applying'), (11, 'than')]),
                                ([('symbolic', 86),
                                 ('explains', 85),
                                 ('this', 94),
                                 ('provides', 77),
                                 ('itself', 90),
                                 ('because', 70),
                                 ('cut', 5)], 
                                 [(94, 'this'),
                                 (90, 'itself'),
                                 (86, 'symbolic'),
                                 (85, 'explains'),
                                 (77, 'provides'),
                                 (70, 'because'),
                                 (5, 'cut')]),
                                ([('page', 96),
                                 ('its', 80),
                                 ('stores', 53),
                                 ('just', 42),
                                 ('take', 57),
                                 ('generate', 47),
                                 ('solves', 75),
                                 ('aid', 14),
                                 ('been', 9),
                                 ('words', 94)], 
                                 [(96, 'page'),
                                 (94, 'words'),
                                 (80, 'its'),
                                 (75, 'solves'),
                                 (57, 'take'),
                                 (53, 'stores'),
                                 (47, 'generate'),
                                 (42, 'just'),
                                 (14, 'aid'),
                                 (9, 'been')]),
                                ([('yhojwifowkhft', 98), ('bwb', 56), ('aybuvkmob', 91)], [(98, 'yhojwifowkhft'), (91, 'aybuvkmob'), (56, 'bwb')]),
                                ([('yhpsuohtno', 32),
                                 ('wicpbhw', 52),
                                 ('ckcx', 52),
                                 ('lxshibni', 98),
                                 ('jqg', 15),
                                 ('hzlzuixoof', 94),
                                 ('jhzfmbkok', 8)], 
                                 [(98, 'lxshibni'),
                                 (94, 'hzlzuixoof'),
                                 (52, 'wicpbhw'),
                                 (52, 'ckcx'),
                                 (32, 'yhpsuohtno'),
                                 (15, 'jqg'),
                                 (8, 'jhzfmbkok')])
                            ])
def test_term_frequency(counts, expected):
    """ Test code for term_frequency """
    steps = [f"actual = hw4.term_frequency({counts})"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw4.term_frequency(counts)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


@pytest.mark.parametrize("pos, neg, text, expected",
                            [
                                (["good"], ["bad"], "good neutral good bad good", 2),
                                (["good"], ["bad"], "bad bad good bad other", -2),
                                (["bad"], ["good"], "good neutral good bad good", -2),
                                (['a', 'b'],
                                 ['c', 'd'],
                                 'b b b a a a a a a a b c a a c b a c c b b b c c b c b c a c a b',
                                 14),
                                (['a'],
                                 ['c', 'b'],
                                 'b b b a a a a a a a b c a a c b a c c b b b c c b c b c a c a b',
                                 -8),
                                (["programs"],
                                 ["expense"],
                                 'after after programs programs expense programs programs methods expense keep methods keep methods programs programs high high expense programs expense keep after keep methods methods high methods methods after expense',
                                 2),
                                (["programs", "marvelous"],
                                 ["expense", "road", "page"],
                                 'system road system marvelous usable road marvelous road page page system marvelous page marvelous road usable page page usable usable road road road page marvelous usable page marvelous system page',
                                 -9),
                                (['ibm', '1401'],
                                 ['management', 'requirements'],
                                 hw4_texts.IBM,
                                 24),
                                (["program", "programming", "customers"],
                                 ["instructions", "the", "reports", "requirements"],
                                 hw4_texts.IBM,
                                 -34),
                                (["children", "child", "thousand"],
                                 ["work", "poor", "flesh"],
                                 hw4_texts.PROPOSAL,
                                 26)
                            ])
def test_sentiment_score(pos, neg, text, expected):
    """ Test code for sentiment_score """
    steps = [f"actual = hw4.sentiment_score({pos}, {neg}, '{text}')"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw4.sentiment_score(pos, neg, text)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


@pytest.mark.parametrize("abbr, text, expected",
                            [
                                ([], "This is a sentence. This is another sentence.", ["This is a sentence.", "This is another sentence."]),
                                (["sentence."], "This is a sentence. This is another sentence. Yeah!", ["This is a sentence. This is another sentence. Yeah!"]),
                                ([], 
                                 'Considering how many fools can calculate, it is surprising that it should be thought either a difficult or a tedious task for any other fool to learn how to master the same tricks. Some calculus-tricks are quite easy. Some are enormously difficult.',
                                 ['Considering how many fools can calculate, it is surprising that it should be thought either a difficult or a tedious task for any other fool to learn how to master the same tricks.',
                                  'Some calculus-tricks are quite easy.',
                                  'Some are enormously difficult.']),
                                ([], 
                                 'Well-tested programming languages for communication with computers must accompany the systems. It is through these languages that the computer itself is used to perform many of the tedious functions that the programmer would otherwise have to perform.', 
                                 ['Well-tested programming languages for communication with computers must accompany the systems.', 
                                  'It is through these languages that the computer itself is used to perform many of the tedious functions that the programmer would otherwise have to perform.']),
                                 (["Mr.", "Mrs."], 
                                 'Well-tested programming languages for communication with computers must accompany the systems. It is through these languages that the computer itself is used to perform many of the tedious functions that the programmer would otherwise have to perform.', 
                                 ['Well-tested programming languages for communication with computers must accompany the systems.', 
                                  'It is through these languages that the computer itself is used to perform many of the tedious functions that the programmer would otherwise have to perform.']),
                                ([],
                                 "There is no doubt whatever about that. The register of his burial was signed by the clergyman, the clerk, the undertaker, and the chief mourner. Scrooge signed it: and Scrooge's name was good upon 'Change, for anything he chose to put his hand to. Old Marley was as dead as a door-nail." ,
                                 ['There is no doubt whatever about that.', 
                                  'The register of his burial was signed by the clergyman, the clerk, the undertaker, and the chief mourner.', 
                                  "Scrooge signed it: and Scrooge's name was good upon 'Change, for anything he chose to put his hand to.", 
                                  'Old Marley was as dead as a door-nail.']),
                                ([],
                                 'At the ominous word "liberality," Scrooge frowned, and shook his head, and handed the credentials back. "At this festive season of the year, Mr. Scrooge," said the gentleman, taking up a pen, "it is more than usually desirable that we should make some slight provision for the Poor and destitute, who suffer greatly at the present time.',
                                 ['At the ominous word "liberality," Scrooge frowned, and shook his head, and handed the credentials back.',
                                  '"At this festive season of the year, Mr.',
                                  'Scrooge," said the gentleman, taking up a pen, "it is more than usually desirable that we should make some slight provision for the Poor and destitute, who suffer greatly at the present time.']),
                                (["Mr."], 'At the ominous word "liberality," Scrooge frowned, and shook his head, and handed the credentials back. "At this festive season of the year, Mr. Scrooge," said the gentleman, taking up a pen, "it is more than usually desirable that we should make some slight provision for the Poor and destitute, who suffer greatly at the present time.', ['At the ominous word "liberality," Scrooge frowned, and shook his head, and handed the credentials back.',
 '"At this festive season of the year, Mr. Scrooge," said the gentleman, taking up a pen, "it is more than usually desirable that we should make some slight provision for the Poor and destitute, who suffer greatly at the present time.']),
                                ([], 'THERE is no position in society more enviable than that of the few who unite a moderate independence with high intellectual qualities. Liberated from the necessity of seeking their support by a profession, they are unfettered by its restraints, and are enabled to direct the powers of their minds, and to concentrate their intellectual energies on those objects exclusively to which they feel that their powers may be applied with the greatest advantage to the community, and with the most lasting reputation to themselves. On the other hand, their middle station and limited income rescue them from those allurements to frivolity and dissipation, to which rank and wealth ever expose their possessors.', ['THERE is no position in society more enviable than that of the few who unite a moderate independence with high intellectual qualities.',
 'Liberated from the necessity of seeking their support by a profession, they are unfettered by its restraints, and are enabled to direct the powers of their minds, and to concentrate their intellectual energies on those objects exclusively to which they feel that their powers may be applied with the greatest advantage to the community, and with the most lasting reputation to themselves.',
 'On the other hand, their middle station and limited income rescue them from those allurements to frivolity and dissipation, to which rank and wealth ever expose their possessors.']),
                                (["Mrs.", "Mr."],'And when old Fezziwig and Mrs. Fezziwig had gone all through the dance; advance and retire, both hands to your partner, bow and curtsey, corkscrew, thread-the-needle, and back again to your place; Fezziwig "cut"--cut so deftly, that he appeared to wink with his legs, and came upon his feet again without a stagger. When the clock struck eleven, this domestic ball broke up. Mr. and Mrs. Fezziwig took their stations, one on either side of the door, and shaking hands with every person individually as he or she went out, wished him or her a Merry Christmas.', ['And when old Fezziwig and Mrs. Fezziwig had gone all through the dance; advance and retire, both hands to your partner, bow and curtsey, corkscrew, thread-the-needle, and back again to your place; Fezziwig "cut"--cut so deftly, that he appeared to wink with his legs, and came upon his feet again without a stagger.',
 'When the clock struck eleven, this domestic ball broke up.',
 'Mr. and Mrs. Fezziwig took their stations, one on either side of the door, and shaking hands with every person individually as he or she went out, wished him or her a Merry Christmas.']),
                            ])
def test_str_to_sentences(abbr, text, expected):
    """ Test code for str_to_sentences """
    steps = [f"actual = hw4.str_to_sentences({abbr}, '{text}')"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw4.str_to_sentences(abbr, text)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)



@pytest.mark.parametrize("easy, text, expected",
                            [
                                (['a', 'b', 'c'], 
                                 'a c e b d b b e a c a a a. e b c d d b e a a a c. b e e b c a. d a d a d e e b d c c b b c. d e a d a c d a e d c. d e d c a a a e b d b e d a a.', 
                                 10.531166666666667),
                                (['d', 'e'], 
                                 'a c e b d b b e a c a a a. e b c d d b e a a a c. b e e b c a. d a d a d e e b d c c b b c. d e a d a c d a e d c. d e d c a a a e b d b e d a a.', 
                                 13.689166666666667),
                                (hw4_texts.EASY, 
                                 'rest companies who who. coded customer plus pleased. useful transfer key highly key. as only schools. with long algebraic.', 
                                 10.47340105263158),
                                (hw4_texts.EASY, 
                                 'And the first person he thought of was Christopher Robin.', 
                                 5.7115),
                                ([], 
                                 'And the first person he thought of was Christopher Robin.', 
                                 19.9225),
                                (["and", "the", "of", "was", "he"], 
                                 'And the first person he thought of was Christopher Robin.', 
                                 12.0275),
                                (hw4_texts.EASY, 
                                 "Foul weather didn't know where to have him.", 
                                 6.00705),
                                (hw4_texts.EASY, 
                                 'Well-tested programming languages for communication with computers must accompany the systems. It is through these languages that the computer itself is used to perform many of the tedious functions that the programmer would otherwise have to perform.', 
                                 10.528694594594596),
                                (hw4_texts.EASY, 
                                 'These mothers, instead of being able to work for their honest livelihood, are forced to employ all their time in stroling to beg sustenance for their helpless infants who, as they grow up, either turn thieves for want of work, or leave their dear native country, to fight for the Pretender in Spain, or sell themselves to the Barbadoes.', 
                                 10.30967966101695),
                                (hw4_texts.EASY, 
                                 'But it has been the fortune of this mathematician to surround himself with fame of another and more popular kind, and which rarely falls to the lot of those who devote their lives to the cultivation of the abstract sciences. This distinction he owes to the announcement, some years since, of his celebrated project of a Calculating Engine.', 
                                 9.703003448275862),
                            ])
def test_dale_chall(easy, text, expected):
    """ Test code for dale_chall """
    steps = [f"actual = hw4.dale_chall({easy}, '{text}')"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw4.dale_chall(easy, text)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)



