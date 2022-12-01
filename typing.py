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
    for x in paragraphs:
        if select(x):
            k-=1
        if k<0:
            return x
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
    def checker(paragraph):
        for x in topic:
            newparagraph = remove_punctuation(lower(paragraph))
            while newparagraph.find(x) != -1:
                bool1, bool2 = True,True
                if newparagraph.find(x) != 0:
                    bool1 = newparagraph[newparagraph.find(x)-1] == ' '
                if newparagraph.find(x) +len(x) != len(newparagraph):
                    bool2 = not newparagraph[newparagraph.find(x) + len(x)].isalnum()
                if bool1 and bool2:
                    return True
                newparagraph = newparagraph[newparagraph.find(x) +len(x):]
        return False
    return checker
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
    i, score, total_iterations=0,0.0, min(len(reference_words),len(typed_words))
    if typed=="":
        return score
    else:
        while i<total_iterations:
            if reference_words[i]==typed_words[i]:
                score +=1
            i+=1
        return score/len(typed_words)*100
            
        
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    return len(typed)/5*(60/elapsed)
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than or equal to LIMIT.
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    if user_word in valid_words:
        return user_word
    else:
        potential = limit
        replacement_word = user_word
        for x in valid_words:
            if diff_function(user_word, x, limit)<potential:
                potential= diff_function(user_word, x, limit)
                replacement_word = x
            if potential==diff_function(user_word, x, limit) and potential==limit:
                replacement_word=x
        return replacement_word
    # END PROBLEM 5


def swap_diff(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6

    if limit<0:
        return 1
    elif min(len(start), len(goal))==0:
           return 0
    else:
        if start[0]!=goal[0]:
            return 1+swap_diff(start[1:min(len(start), len(goal))], goal[1:min(len(start), len(goal))], limit-1) +abs(len(start)-len(goal))
        else:
            return swap_diff(start[1:min(len(start), len(goal))], goal[1:min(len(start), len(goal))], limit) +abs(len(start)-len(goal))
             
    
    # END PROBLEM 6

def edit_diff(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""

    w,h = len(start)+1, len(goal)+1
    dpMatrix = [[0 for x in range(w)]for y in range(h)]
    for x in range(w):
        dpMatrix[0][x] = x
    for y in range(h):
        dpMatrix[y][0] = y
    x = 1
    while x < w:
        y =1
        while y <h:
            if start[x-1] == goal[y-1]:
                dpMatrix[y][x] = dpMatrix[y-1][x-1]
            else:
                add_diff = 1+dpMatrix[y][x-1]
                remove_diff = 1+dpMatrix[y-1][x-1]
                substitute_diff = 1 + dpMatrix[y-1][x]
                dpMatrix[y][x] = min(add_diff,remove_diff,substitute_diff)
            y +=1
        x+=1
    return dpMatrix[h-1][w-1]


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
    not_wrong=True
    num_right, i = 0, 0
    while not_wrong and i<len(prompt) and i<len(typed):
        if prompt[i]==typed[i]:
            num_right +=1
            i+=1
        else:
            not_wrong = False
    send({'id': id, 'progress': num_right/len(prompt)})
    return num_right/len(prompt)
        
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
    lst_of_lst= [][]
    w=1
    while w<n_words:
        i = 1
        shortest_time = elapsed_time(word_times[0][w])-elapsed_time(word_times[0][w-1])
        fastest_player=0
        #once through to find shortest time
        while i<n_players:
            if (elapsed_time(word_times[i][w])-elapsed_time(word_times[i][w-1]))<shortest_time:
                shortest_time = elapsed_time(word_times[i][w])-elapsed_time(word_times[i][w-1])
                fastest_player=i
            i+=1
        
        i=1
        #second time through to check if others also fit margin
        while
        
            i+=1
        w+=1
    
    return lst_of_lst
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


enable_multiplayer = False  # Change to True when you


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
