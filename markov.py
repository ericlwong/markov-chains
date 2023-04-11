"""Generate Markov text from text files."""

from random import choice
import sys

def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    file = open(file_path).read() 

    return file

def make_chains(text_string, n_gram):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains('hi there mary hi there juanita')

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """

    chains = {}

    words = text_string.split()
    # the first two words are going to create the key
    # the third word would determine the next pair of words
    # since we need to keep track of 3 words at a time, we need a loop
    # that can access three indices at the same time (index, index + 1, index + 2)
    # keys: first pair (0, 1) -> next pair (1, 2)
    # values: list of possible paths to take which creates the next pair
    # range(n): give us a range from (0, n exclusive)
    # range(start, stop): give us a range from (start, stop exclusive)
    # range(start, stop, step)
    # we can use a step of n_gram - 1
    # but the first key tuple in context of indices is always in sequential order from 0 to n_gram-1
    for index in range(len(words) - n_gram):
        # create a list of length n_gram containing the key words
        # once length of list is created, we can type cast it to a tuple using tuple()
        # Looking at index pairs for bigrams: (0, 1) -> (1, 2) -> (2, 3)    tuple(list[index:index+2])
        # For trigrams: (0, 1, 2) -> (1, 2, 3) -> (2, 3, 4)     tuple(list[index:index+3])
        # 4-gram: (0, 1, 2, 3) -> (1, 2, 3, 4) -> (2, 3, 4, 5)     tuple(list[index:index+4])
        # For n_grams: (0, 1, ..., n) -> (1, 2, ..., n +1)      tuple(list[index:index+n_grams])
        chain_key = tuple(words[index:index + n_gram])
        if chain_key in chains:
            # index = 0, chain_key = tuple(words[0:3]) -> tuple(['Would', 'you', 'could'])
            # chain_key = ('Would', 'you', 'could')
            # value would be the fourth word which is at index 3 (index + 3 for a trigram)
            chains[chain_key].append(words[index + n_gram])     
        else:
            chains[chain_key] = [words[index + n_gram]]

    return chains

def make_text(chains, n_gram):
    """Return text from chains."""

    words = []
    punct = ["." , "?" , "!"]

    # .keys() -> dict_keys[('Would', 'you'), ..., ]
    # We can type cast it to a list using the list() constructor --> list(dict.keys())
    # choice(sequence), this sequence is just a list --> a random elem, in our case it is a random tuple
    # Ex: random_elem = choice(list(dict.keys()))
    # We now need to get a random word from the list of words paired to the random key
    # Add this random word to the words list above 
    # .append() -> add the specified element to the end of a list
    # Ex: list = [1, 2, 3]
    # list.append([4, 5]) --> [1, 2, 3, [4, 5]]
    # .extend() -> adds the contents of the specified value to the end of a list
    # Note: If you use .extend(str), it will add each character as an elem to the end of the list
    # Ex: list2 = [1, 2, 3]
    # .extend([4, 5]) --> [1, 2, 3, 4, 5]
    # .extend("am?") --> [1, 2, 3, a, m, ?]
    random_key = choice(list(chains.keys()))

    # check if random_key's first word has a capital letter
    # if not, we should keep getting another random_key
    while not random_key[0][0].isupper():
        random_key = choice(list(chains.keys()))

    random_word = choice(chains[random_key])
    words.extend(random_key)
    words.append(random_word)       # We can potentially already have a list that begins with a capital letter and has punctuation

    # words = ['Sam', 'I', 'am?']
    if words[-1][-1] in punct:
        return ' '.join(words)
    
    # With n_gram, to make a new key, we want to take every word but the first from the original key
    # and include the value
    # to take every word but the first from original, random_key[1:] and then include random word
    # random_key[1:] -> ('you', 'could) -> convert to list using list(random_key[1:])
    # and then append random_word
    new_key = random_key[1:n_gram] + (random_word,)

    # Keep making a new key, getting a random word and adding to words list
    # as long as new key exists in our dictionary
    # .isupper() checks if all characters in a string are uppercase
    while new_key in chains:
        new_word = choice(chains[new_key])
        words.extend(new_key)
        words.append(new_word)

        if words[-1][-1] in punct:
            return ' '.join(words)

        new_key = new_key[1:n_gram] + (new_word,)

    return ' '.join(words)

# sys.argv -> list of command line arguments after the keyword python3
# sys.argv[0] -> the Python script name
# sys.argv[1:] -> the file name or any additional arguments to pass to the Python script
input_path = sys.argv[1]
print("You wil need to choose how many words you would like the program to use as a parameter to generate random text.")
users_choise = int(input("How many words would you like to use:  "))

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text, users_choise)

# Produce random text
random_text = make_text(chains, users_choise)

print(random_text)
