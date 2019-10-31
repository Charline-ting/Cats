"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    index = 0
    while index < len(paragraphs):
        if select(paragraphs[index]):
            result = paragraphs[index]
            k -= 1
        if k == -1:
            return result
        index += 1
    return ''
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def check(paragraph):
        list_of_paragraph = split(remove_punctuation(lower(paragraph)))
        for i in topic:
            for k in list_of_paragraph:
                if i == k:
                    return True
        return False
    return check
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    count = 0
    index = 0
    if len(typed_words) != 0:
        while index < len(typed_words) and index < len(reference_words):
            if typed_words[index] == reference_words[index]:
                count += 1
            index += 1
        return count / len(typed_words) * 100
    else:
        return 0.0
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    return (len(typed)/5) / (elapsed/60)
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    diction = {x:diff_function(user_word, x, limit) for x in valid_words if diff_function(user_word, x, limit) <= limit}
    if user_word in diction or len(diction) < 1:
        return user_word
    else:
        return min(diction, key = lambda x: diction[x])
    # END PROBLEM 5


def swap_diff(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    if limit < 0:
        return 1
    elif len(start) == 0 or len(goal) == 0:
            return abs(len(goal) - len(start))
    else:
        if start[0] == goal[0]:
            return swap_diff(start[1:], goal[1:], limit)
        else:
            return 1 + swap_diff(start[1:], goal[1:], limit - 1)
    # END PROBLEM 6

def edit_diff(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""

    def leven(start, s, goal, g, limit):
        
        if limit < 0: # Fill in the condition
            # BEGIN
            "*** YOUR CODE HERE ***"
            return 1
            # END

        if s == 0 or g == 0:
            return s + g
        
        if start[s - 1] == goal[g - 1]:
            # BEGIN
            "*** YOUR CODE HERE ***"
            cost = 0
        else:
            cost = 1
            # END

        
        add_diff = leven(start, s, goal, g - 1, limit - 1) + 1   # Fill in these lines
        remove_diff = leven(start, s - 1, goal, g, limit - 1) + 1
        substitute_diff = leven(start, s - 1, goal, g - 1, limit - cost) + cost
        # BEGIN
        "*** YOUR CODE HERE ***"
        return min(add_diff, remove_diff, substitute_diff)
        # END


    return leven(start, len(start), goal, len(goal), limit)

def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'




###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    count, index, pointer = 0, 0, True
    while index < len(typed) and index < len(prompt) and pointer:
        if typed[index] == prompt[index]:
            count += 1
        else:
            pointer = False
        index += 1 
    send({'id': id, 'progress': count / len(prompt)})
    return count / len(prompt)
    # END PROBLEM 8


def fastest_words_report(word_times):
    """Return a text description of the fastest words typed by each player."""
    fastest = fastest_words(word_times)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def fastest_words(word_times, margin=1e-5):
    """A list of which words each player typed fastest."""
    n_players = len(word_times)
    n_words = len(word_times[0]) - 1
    assert all(len(times) == n_words + 1 for times in word_times)
    assert margin > 0
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    num_word = 1
    result = [[] for x in range(n_players)]
    while num_word <= n_words:
        player = 0
        min = elapsed_time(word_times[0][num_word])
        while player < n_players:
            time = elapsed_time(word_times[player][num_word]) - elapsed_time(word_times[player][num_word - 1])
            if time < min:
                min = time
            player += 1
        player = 0
        while player < n_players:
            time = elapsed_time(word_times[player][num_word]) - elapsed_time(word_times[player][num_word - 1])
            if time - min <= margin:
                result[player].append(word(word_times[player][num_word]))
            player += 1
        num_word += 1
    return result
    # END PROBLEM 9


def word_time(word, elapsed_time):
    """A data abstrction for the elapsed time that a player finished a word."""
    return [word, elapsed_time]


def word(word_time):
    """An accessor function for the word of a word_time."""
    return word_time[0]


def elapsed_time(word_time):
    """An accessor function for the elapsed time of a word_time."""
    return word_time[1]


enable_multiplayer = True  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
