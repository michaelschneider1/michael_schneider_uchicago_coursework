"""
CMSC 14100
Winter 2025
Homework #4

We will be using anonymous grading, so please do NOT include your name
in this file

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URL of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

# Global constants
PUNCTUATION = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

"""
CORRECTIONS MADE:

Exercise 1: 1) changed the for loop to be a "for val in list" rather than an 
index list. Able to do so by list slicing (line 84) 2) Utilized defined list 
vowels (line 81) to shorten code 3) removed if word == "" because it was 
unnecessary 
Exercise 2: 1) made the for loop have enumerate instead of doing a for loop by
using the text's length (line 105) 2) Used [-1] to reach the last number of seq 
instead of len(seq) - 1 (line 112)
Exercise 3: 1) used helper function string_to_list to reduce repeated code for 
future problems (line 129) 2) changed for loop variable names (line 132, 134) 
3) made code more efficent 4) followed criteria of only going through the text 
once
Exercise 4: 1) used helper function string_to_list to avoid repeating code 2) 
used enumerate on my for loop rather using range(line 158)
Exercise 5: 1) used enumerate in the for loop (line 174) 2) unpacked the tuple 
to increase efficency (line 176)
Exercise 6: 1) used count_words function to avoid repeated code (line 199, 200)
2) unpacked the tuples (line 205, 208)
Exercise 7: 1) changed function entirley to be less complex 2) did not use the
replace function
Exercise 8: 1) use helper function string_to_list to find number of words 
(line 259) 2) used str_to_sentence to find how many sentences are in the 
text (line 258) 3) used count_words to make counting the easy words easier 
(line 261)
"""

#helper function, turn strings to list words, lower case, no punctuation
def string_to_list(text):
    """
    Given a string, produces a list of each word in the string while making 
    all the words lower case and stripping the punctuation

    Input:
        text(str): a string
    Output(lst): list of the words in the string, lower case, no punctuation
    """
    lower_case = text.lower()
    temporary_list = lower_case.split()
    word_list = []
    for word in temporary_list:
        word_list.append(word.strip(PUNCTUATION))
    return word_list


# Exercise 1
def compress_word(word):
    """
    Given a word, produce a compressed version of the word, by stripping all
    interior vowels.

    Input:
        word (str): text to be compressed

    Output (str): compressed word without interior vowels
    """
    if len(word) <= 2:
        return word
    vowels = ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]

    compressed_word = word[0]
    for letter in word[1:-1]:
        if letter not in vowels:
            compressed_word += letter
    return compressed_word + word[-1]


# Exercise 2
def segment_text(text, seq):
    """
    Given a text and a binary sequence, segment the text into words according
    to the sequence.

    Input:
        text (str): the text to be segmented
        seq (str): binary sequence representing the locations of words

    Output (list[str]): list of words comprising the text
    """
    segments = []
    after_one = 0

    for index, _ in enumerate(text):
        if seq[index] == "1":
            segments.append(text[after_one:(index + 1)])
            after_one = index + 1

    if after_one < len(text):
        segments.append(text[after_one:len(text)])
    if seq[-1] == "1":
        segments.append("")
    return segments
            

# Exercise 3
def count_words(wordlist, text):
    """
    Given a list of words and a text, produce a count of the occurrences of
    each word from the word list in the text.

    Input:
        wordlist (list[str]): list of words to be counted
        text (str): text to search

    Output (list[tuple[str,int]]): list of (word, count) pairs
    """
    text_as_list = string_to_list(text)
    pair_list = []

    for desired_word in wordlist:
        occurences = 0
        for word in text_as_list:
            if desired_word == word:
                occurences += 1
        pair_list.append((desired_word, occurences))

    return pair_list


# Exercise 4
def list_bigrams(text):
    """
    Given a text, produce a list of all bigrams contained in the text, in the
    order that they appear.

    Input:
        text (str): the text

    Output (list[tuple[str,str]]): list of bigrams contained in text
    """
    text_as_list = string_to_list(text)
    bigram_list = []

    if len(text_as_list) < 2:
        return []
    for index, _ in enumerate(text_as_list[:-1]):
        bigram_list.append((text_as_list[index], text_as_list[index + 1]))
    return bigram_list


# Exercise 5
def term_frequency(counts):
    """
    Given a list of (word, count) pairs, produce a list of (count, word) pairs,
    ordered from greatest to least, then lexicographically.

    Input:
        counts (list[tuple[str,int]]): list of (word, count) pairs

    Output (list[tuple[int,str]]): sorted list of (count, word) pairs
    """
    reverse = []
    for tuple in counts:
        word, count = tuple
        reverse.append((count, word))
    reverse.sort(reverse = True)
    return reverse


# Exercise 6
def sentiment_score(pos, neg, text):
    """
    Given a list of positive words, a list of negative words, and a text,
    produce a sentiment score based on the number of occurrences of the given
    words in the text.

    Each occurrence of a "positive" word contributes +1 to the score and each
    "negative" word contributes -1 to the score.

    Input:
        pos (list[str]): list of positive words
        neg (list[str]): list of negative words
        text (str): the text

    Output (int): sentiment score for the text
    """
    good_list = count_words(pos, text)
    bad_list = count_words(neg, text)
    tot_good = 0
    tot_bad = 0

    for tuple in good_list:
        _, count = tuple
        tot_good += count
    for tuple in bad_list:
        _, count = tuple
        tot_bad += count
    
    return tot_good - tot_bad


# Exercise 7
def str_to_sentences(abbr, text):
    """
    Given a list of abbreviations and a text, produce a list containing the 
    sentences of the text, in order. A sentence is a sequence of words that 
    ends in one of the following punctuation marks: ".", "!", "?". Sentences
    should not end on any of the given abbreviations.

    Input:
        abbr (list[str]): list of abbreviations
        text (str): the text to be broken up

    Output (list[str]): list of sentences that comprise text
    """
    text_list = text.split()
    sentence_enders = [".", "!", "?"]
    final_list = []

    sentence = ''
    for word in text_list:
        if sentence == '':
            sentence += word
        else:
            sentence += " " + word
        if word[-1] in sentence_enders:
            if word not in abbr:
                final_list.append(sentence)
                sentence = ''

    return final_list


# Exercise 8
def dale_chall(easy, text):
    """
    Given a list of "easy" words and a text, compute the Dale-Chall readability
    score for the text, relative to the list of easy words.

    Input:
        easy (list[str]): list of easy words
        text (str): the text to be analyzed

    Output (float): Dale-Chall readability score for the text
    """
    num_sentences = len(str_to_sentences('', text))
    num_words = len(string_to_list(text))
    
    easy_list = count_words(easy, text)
    easy_words = 0
    for tuple in easy_list:
        _, num = tuple
        easy_words += num
    hard_words = num_words - easy_words

    percentage = (hard_words / num_words) * 100
    score = (0.1579 * percentage) + (.0496 * (num_words / num_sentences))
    if percentage > 5:
        return score + 3.6365
    return score
