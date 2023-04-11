"""Generate Markov text from text files."""

from random import choice


def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    file = open(file_path).read() 

    return file

def make_chains(text_string):
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
    for index in range(len(words) - 2):
        chain_key = (words[index], words[index + 1])
        if chain_key in chains:
            chains[chain_key].append(words[index + 2])
        else:
            chains[chain_key] = [words[index + 2]]

    return chains

def make_text(chains):
    """Return text from chains."""

    words = []

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
    random_word = choice(chains[random_key])
    words.extend(random_key)
    words.append(random_word)
    new_key = (random_key[1], random_word)

    # Keep making a new key, getting a random word and adding to words list
    # as long as new key exists in our dictionary
    while new_key in chains:
        new_word = choice(chains[new_key])
        words.extend(new_key)
        words.append(new_word)
        new_key = (new_key[1], new_word)

    return ' '.join(words)

input_path = 'gettysburg.txt'

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text)

# Produce random text
random_text = make_text(chains)

print(random_text)
