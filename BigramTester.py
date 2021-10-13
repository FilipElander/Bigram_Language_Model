#  -*- coding: utf-8 -*-
import math
import argparse
import nltk
import codecs
from collections import defaultdict
import json
import requests



class BigramTester(object):
    def __init__(self):
        """
        This class reads a language model file and a test file, and computes
        the entropy of the latter.
        """
        # The mapping from words to identifiers.
        self.index = {}

        # The mapping from identifiers to words.
        self.word = {}

        # An array holding the unigram counts.
        self.unigram_count = {}

        # The bigram log-probabilities.
        self.bigram_prob = defaultdict(dict)

        # Number of unique words (word forms) in the training corpus.
        self.unique_words = 0

        # The total number of words in the training corpus.
        self.total_words = 0

        # The average log-probability (= the estimation of the entropy) of the test corpus.
        # Important that it is named self.logProb for the --check flag to work
        self.logProb = 0

        # The identifier of the previous word processed in the test corpus. Is -1 if the last word was unknown.
        self.last_index = -1

        # The fraction of the probability mass given to unknown words.
        self.lambda3 = 0.000001

        # The fraction of the probability mass given to unigram probabilities.
        self.lambda2 = 0.01 - self.lambda3

        # The fraction of the probability mass given to bigram probabilities.
        self.lambda1 = 0.99

        # The number of words processed in the test corpus.
        self.test_words_processed = 0


    def read_model(self, filename):
        """
        Reads the contents of the language model file into the appropriate data structures.

        :param filename: The name of the language model file.
        :return: <code>true</code> if the entire file could be processed, false otherwise.
        """

        try:
            with codecs.open(filename, 'r', 'utf-8') as f:
                self.unique_words, self.total_words = map(int, f.readline().strip().split(' '))
                # YOUR CODE HERE
                text = open(filename,'r')
                dod = text.readline().strip().split(' ') # dödar första raden
                for i in range(self.unique_words):
                    plats,ord,antal = text.readline().strip().split(' ')
                    self.index[ord]=i
                    self.word[i] = ord
                    self.unigram_count[ord] = antal
                l = 3
                while l ==3:
                    vek = []
                    vek = text.readline().strip().split(' ')
                    if len(vek) > 1:
                        o = self.word[int(vek[0])]
                        fol = self.word[int(vek[1])]
                        self.bigram_prob[o][fol] = vek[2]
                    l = len(vek)
                return True
        except IOError:
            print("Couldn't find bigram probabilities file {}".format(filename))
            return False


    def compute_entropy_cumulatively(self, word):
        # YOUR CODE HERE
        N = len(self.tokens)                           # antal ord i test corpuset
        sum = 0                                        # initierar sumeringen
        for toknr in range(1,len(self.tokens),1):      # vilken token i tokens man är på (börjar på andra för att kunna kolla bakåt)
            self.test_words_processed += 1             # räknar räknare på ord som processats
            ord = self.tokens[toknr]                   # tokenet man kollar på
            prew = self.tokens[toknr -1]               # föregående token

            if ord in self.bigram_prob[prew]:          # om det är nollskild sannolikhet från modellen
                bip = self.lambda1*(math.exp(float(self.bigram_prob[prew][ord])))
                # lambda1*(P(w_i|w_i -1))
            else:        # om det är noll sannolikhet från modellen sätt faktorn till noll
                bip = 0

            if ord in self.unigram_count:           # om det är nollskild sannolikhet från modellen
                unip = self.lambda2*(int(self.unigram_count[ord])/self.unique_words)
                # lambda2 * P(antal w_i / antal unika ord )
            else:                                   # om ordet inte finns
                unip = 0

            # logaritmen av sannolikheten
            logp = math.log(bip + unip + self.lambda3)
            sum = sum + logp # summerar varje varv
        # beräknar entropy
        self.logProb = (sum/N)*-1

        pass #donou....

    def process_test_file(self, test_filename):
        """
        <p>Reads and processes the test file one word at a time. </p>

        :param test_filename: The name of the test corpus file.
        :return: <code>true</code> if the entire file could be processed, false otherwise.
        """
        try:
            with codecs.open(test_filename, 'r', 'utf-8') as f:
                self.tokens = nltk.word_tokenize(f.read().lower()) # Important that it is named self.tokens for the --check flag to work
                for token in self.tokens:
                    self.compute_entropy_cumulatively(token)
            return True
        except IOError:
            print('Error reading testfile')
            return False


def main():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description='BigramTester')
    parser.add_argument('--file', '-f', type=str,  required=True, help='file with language model')
    parser.add_argument('--test_corpus', '-t', type=str, required=True, help='test corpus')


    arguments = parser.parse_args()

    bigram_tester = BigramTester()
    bigram_tester.read_model(arguments.file)
    bigram_tester.process_test_file(arguments.test_corpus)

    print('Read {0:d} words. Estimated entropy: {1:.2f}'.format(bigram_tester.test_words_processed, bigram_tester.logProb))

if __name__ == "__main__":
    main()
