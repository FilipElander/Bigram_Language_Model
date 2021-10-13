#  -*- coding: utf-8 -*-
from __future__ import unicode_literals
import math
import argparse
import nltk
import os
from collections import defaultdict
import codecs
import json
import requests


class BigramTrainer(object):
    """
    This class constructs a bigram language model from a corpus.
    """

    def process_files(self, f):
        """
        Processes the file @code{f}.
        """
        with codecs.open(f, 'r', 'utf-8') as text_file:
            text = reader = str(text_file.read()).lower()
        try :
            self.tokens = nltk.word_tokenize(text) # Important that it is named self.tokens for the --check flag to work
        except LookupError :
            nltk.download('punkt')
            self.tokens = nltk.word_tokenize(text)
        for token in self.tokens:
            self.process_token(token)



    def process_token(self, token):
        """
        Processes one word in the training corpus, and adjusts the unigram and
        bigram counts.

        :param token: The current word to be processed.
        """
        # YOUR CODE HERE

        self.total_words += 1                           # för varje token addera ett ord på totalen
        self.unigram_count[token] +=1                   # lägger till på unigramet eller gör ny om ordet inte finns
        self.unique_words = len(self.unigram_count)     # antal uinka ord är längden på unigram diktionary

        # går igenom varje ord i unigramet, lägger till ett index och pekar indexet på ordet
        i = 0
        for word in self.unigram_count:
            self.index[word] = i
            self.word[i] = word
            i += 1

        # håller koll på vilket token i ordningen vi går igenom så att vi inte
        # genererar n:gånger så många bigram.
        pos = self.unigram_count[token]                 # kollar vilken token i ordningen
        if self.last_index >= 0:
            self.bigram_count[self.tokens[self.last_index]][token] += 1
            self.last_index += 1
        else:
            self.last_index += 1



        """
        for index in range(0,len(self.tokens)-1):       # går från första till nästsista token i corpus
        # när vi kommer fram till korpus vi fått in i funktionen så lägger vi till bigrammet med följande ordet
        # i bigram_count och adderar på räknaren så att vi inte går in i lopen nästa varv och gör för många bigram
            if self.tokens[index] == token:
                if counter == pos:
                    self.bigram_count[token][self.tokens[index+1]] +=1
                    counter +=1
                counter += 1

        """



    def stats(self):
        """
        Creates a list of rows to print of the language model.

        """
        rows_to_print = []

        rows_to_print.append(str(self.unique_words) + " " + str(self.total_words)) # unika & totala ord

        for ord in self.unigram_count:  # lägger till indexet, unigramet
            rows_to_print.append(str(self.index[ord]) + " " + ord + " " + str(self.unigram_count[ord]))

        for ord in self.bigram_count: # för varje ord går igenom vad ordet pekar på och beräknar sanolikheten enligt given ekv
            for follow in self.bigram_count[ord]:
                p =format(math.log(self.bigram_count[ord][follow] / self.unigram_count[ord]),'.15f')
                rows_to_print.append(str(self.index[ord]) + " " + str(self.index[follow]) + " " + str(p))

        rows_to_print.append(str(-1)) # lägger till slutrad


        return rows_to_print

    def __init__(self):
        """
        <p>Constructor. Processes the file <code>f</code> and builds a language model
        from it.</p>

        :param f: The training file.
        """

        # The mapping from words to identifiers.
        self.index = {}

        # The mapping from identifiers to words.
        self.word = {}

        # An array holding the unigram counts.
        self.unigram_count = defaultdict(int)

        """
        The bigram counts. Since most of these are zero (why?), we store these
        in a hashmap rather than an array to save space (and since it is impossible
        to create such a big array anyway).
        """
        self.bigram_count = defaultdict(lambda: defaultdict(int))

        # The identifier of the previous word processed.
        self.last_index = -1

        # Number of unique words (word forms) in the training corpus.
        self.unique_words = 0

        # The total number of words in the training corpus.
        self.total_words = 0

        self.laplace_smoothing = False


def main():

    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description='BigramTrainer')
    parser.add_argument('--file', '-f', type=str,  required=True, help='file from which to build the language model')
    parser.add_argument('--destination', '-d', type=str, help='file in which to store the language model')
    parser.add_argument('--check', action='store_true', help='check if your alignment is correct')

    arguments = parser.parse_args()

    bigram_trainer = BigramTrainer()

    bigram_trainer.process_files(arguments.file)

    if arguments.check:
        results  = bigram_trainer.stats()
        payload = json.dumps({
            'tokens': bigram_trainer.tokens,
            'result': results
        })
        response = requests.post(
            'https://language-engineering.herokuapp.com/lab2_trainer',
            data=payload,
            headers={'content-type': 'application/json'}
        )
        response_data = response.json()
        if response_data['correct']:
            print('Success! Your results are correct')
            for row in results: print(row)
        else:
            print('Your results:\n')
            for row in results: print(row)
            print("The server's results:\n")
            for row in response_data['result']: print(row)
    else:
        stats = bigram_trainer.stats()
        if arguments.destination:
            with codecs.open(arguments.destination, 'w', 'utf-8' ) as f:
                for row in stats: f.write(row + '\n')
        else:
            for row in stats: print(row)


if __name__ == "__main__":
    main()
