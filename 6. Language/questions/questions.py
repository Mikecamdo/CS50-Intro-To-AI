import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    data = { }

    for file in os.listdir(directory):
        with open(os.path.join(directory, file), 'r', encoding='utf-8') as file_content:
            data[file] = file_content.read()

    return data

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens = nltk.word_tokenize(document)

    omitted_words = nltk.corpus.stopwords.words("english")
    for character in string.punctuation:
        omitted_words.append(character)

    valid_words = [ ]

    for token in tokens:
        token = token.lower()
        if token not in omitted_words:
            valid_words.append(token)

    return valid_words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idf_values = { }
    words_to_documents = { }

    for document_name in documents:
        for word in documents[document_name]:
            if word in words_to_documents:
                current_documents = words_to_documents[word]
                if document_name not in current_documents:
                    words_to_documents[word].append(document_name)
            else:
                words_to_documents[word] = [ ]
                words_to_documents[word].append(document_name)

    num_documents = len(documents)
    for word in words_to_documents:
        idf_values[word] = math.log(num_documents) / len(words_to_documents[word])
    
    return idf_values


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    file_names = [ ] #TODO what happens if word not in idfs???

    tf_idf_values = { }
    for file in files: # loops through every .txt file
        tf_idf_values[file] = 0
        file_words = files[file]
        for word in query: # only searches for words in the query
            if word in idfs: # if word is not in idfs, tf-idf = 0
                term_frequency = file_words.count(word) # get the word's term frequency for the current file
                tf_idf_values[file] += (term_frequency * idfs[word]) # update the total tf_idf value

    for i in range(n): # gets the top n file names
        highest_value_key = max(tf_idf_values, key=tf_idf_values.get)
        file_names.append(highest_value_key)
        tf_idf_values.pop(highest_value_key)

    return file_names


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_idf_values = { }
    for sentence in sentences:
        sentence_idf_values[sentence] = 0
        sentence_words = sentences[sentence]
        for word in query:
            if word in sentence_words and word in idfs:
                sentence_idf_values[sentence] += idfs[word]

    top_sentences = [ ]

    for i in range(n):
        highest_value = -1
        highest_key = ""

        for key, value in sentence_idf_values.items():
            if value > highest_value:
                highest_value = value
                highest_key = key
            elif value == highest_value: # if there is a tie, find query term density
                query_term_density_1 = 0
                query_term_density_2 = 0

                sentence_1 = sentences[key] # the current sentence
                sentence_2 = sentences[highest_key] # the highest value sentence (so far)

                for word in sentence_1:
                    if word in query:
                        query_term_density_1 += 1

                for word in sentence_2:
                    if word in query:
                        query_term_density_2 += 1

                query_term_density_1 /= len(sentence_1)
                query_term_density_2 /= len(sentence_2)

                if query_term_density_1 > query_term_density_2: # if query term density of the new sentence is higher
                    highest_value = value
                    highest_key = key

        top_sentences.append(highest_key)
        sentence_idf_values.pop(highest_key)

    return top_sentences


if __name__ == "__main__":
    main()
