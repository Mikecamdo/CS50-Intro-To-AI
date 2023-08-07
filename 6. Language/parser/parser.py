import nltk
import sys
import re

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP
NP -> N | Det N | Det N PP | Det AdjP N | Det AdjP N Conj S | Det N Conj S | N Conj S | Det N Adv | Det AdjP N PP | N Conj VP
VP -> V | V NP | V NP PP | V PP | V Det NP | Adv V NP | V Adv Conj VP
PP -> P NP
AdjP -> Adj | Adj AdjP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = [ ]
    tokens = nltk.word_tokenize(sentence)

    for token in tokens:
        valid_word = bool(re.search('[a-zA-Z]', token))
        if valid_word:
            words.append(token.lower())

    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = [ ]

    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            valid = True
            counter = 0
            for subsubtree in subtree.subtrees():
                if counter == 0: # skips the first subsubtree (which is just the current subtree)
                    counter += 1
                    continue
                if subsubtree.label() == "NP": # if the subtree has a subtree with label "NP"
                    valid = False
                    break
            if valid: # if the subtree doesn't have a subtree with label "NP"
                chunks.append(subtree)
            
    return chunks


if __name__ == "__main__":
    main()
