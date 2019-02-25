import nltk
import re

nltk.download('punkt')


def tokenize_no_nltk_CACM(documents):
    """
    tokenization avec les instructions du projet (stoplist)
    """
    d = {}
    for i in range(len(documents)):
        document = documents[i]
        for text in document:
            if len(text) > 0:
                tokens = re.compile("[^0-9a-zA-Z]").split(text)
                for token in tokens:
                    if token.lower() not in forbidden_words and len(token) > 0:
                        if token.lower() in d:
                            d[token.lower()].append(i + 1)
                        else:
                            d[token.lower()] = [i + 1]
    return d


def tokenize_CACM(documents):
    """
    tokenization utilisant NLTK et la stoplist
    """
    d = {}
    for i in range(len(documents)):
        document = documents[i]
        for text in document:
            if len(text) > 0:
                tokens = nltk.word_tokenize(text)
                for token in tokens:
                    if token.lower() not in forbidden_words and len(token) > 0:
                        if token.lower() in d:
                            d[token.lower()].append(i + 1)
                        else:
                            d[token.lower()] = [i + 1]
    return d


def tokenize_CS276(documents):
    """
    returns a dictionnary -> key: token name, value: list of document ids where token appear
    """
    tokens = {}
    for i in range(len(documents)):
        for token in documents[i]:
            if token.lower() not in forbidden_words and len(token.lower()) > 0:
                if token.lower() not in tokens:
                    tokens[token.lower()] = [i]
                else:
                    tokens[token.lower()].append(i)
        if len(documents) > 5000 and i % 1000 == 0:
            print("Processing document {}/{}          ".format(str(i), str(len(documents))), end="\r")
    return tokens


def print_heap_law(tokens_full, tokens_half, collection_name):
    print("heap low for collection", collection_name)
    T1 = sum([len(L) for L in tokens_full])
    T2 = sum([len(L) for L in tokens_half])

    M1 = len(tokens_full)
    M2 = len(tokens_half)

    from math import log, pow
    b = log(M1 / M2) / log(T1 / T2)
    k = M1 / (pow(T1, b))
    print("K = {}, b = {}".format(k, b))

    print('Pour 1 million de tokens, vocabulaire :')
    print(int(k * pow(1e6, b)))


def word_frequency(tokens):
    """
    return dict: word -> count
    """
    freq = {}
    words = tokens.keys()
    for word in words:
        freq[word] = len(tokens[word])
    return freq


class Token_sorter():
    def __init__(self, word, frequency):
        self.word = word
        self.f = frequency

    def __lt__(self, other):
        return self.f > other.f

    def __repr__(self):
        return str(self.word) + " : " + str(self.f)


def read_forbidden_words():
    """
    returns stoplist
    """
    file_name = "./Data/CACM/common_words"
    file = open(file_name)
    words = []
    for word in file.readlines():
        words.append(word.strip().lower())
    file.close()
    return words


forbidden_words = read_forbidden_words()
