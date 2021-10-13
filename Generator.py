import math
import argparse
import codecs
from collections import defaultdict
import random



class Generator(object) :
    """
    This class generates words from a language model.
    """
    def __init__(self):

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


    def read_model(self,filename):
        """
        Reads the contents of the language model file into the appropriate data structures.

        :param filename: The name of the language model file.
        :return: <code>true</code> if the entire file could be processed, false otherwise.
        """

        try:
            with codecs.open(filename, 'r', 'utf-8') as f:
                self.unique_words, self.total_words = map(int, f.readline().strip().split(' '))
                # min kod

                text = open(filename,'r')
                dod = text.readline().strip().split(' ') # dödar första raden med unika och tot
                # hämtar hem unigramet och indexen
                for i in range(self.unique_words):
                    plats,ord,antal = text.readline().strip().split(' ')  # indexet ordet och antalet från modellen
                    self.index[ord]=i   # sätter in indexet
                    self.word[i] = ord  # sätter in ordet
                    self.unigram_count[ord] = antal # fyller i unigrammet

                # resterande rader skall vara 3 olika data tills -1 dyker upp och har nått botten
                l = 3
                while l ==3:  # antal inlästa data från raden
                    vek = []        # en holder array som skrivs över varje varv
                    vek = text.readline().strip().split(' ')    # läser in datan
                    if len(vek) > 1:                            # om det är 3 rader som läses in
                        o = self.word[int(vek[0])]              # ordet
                        fol = self.word[int(vek[1])]            # följdordet
                        self.bigram_prob[o][fol] = vek[2]       # sannolikheten i log() läggs in i bigrammet
                    l = len(vek) # kör tills längden blir 1
                return True
        except IOError:
            print("Couldn't find bigram probabilities file {}".format(filename))
            return False

    def generate(self, w, n):
        """
        Generates and prints n words, starting with the word w, and following the distribution
        of the language model.
        """
        # YOUR CODE HERE
        print(w)  # första ordet som ges av användaren

        for N in range(n):  # antal ord som användaren ber en generera

            if self.bigram_prob[w] == {}:  # om det är noll sannolikhet att det följer ett ord
                ordindex = random.randint(0,len(self.unigram_count))    # slumpa ett ord ur modellen uniformellt
                w = self.word[ordindex]                                 # slumpa ett ord ur modellen uniformellt

            follwords = []          # hållare för följeord
            p = []                  # hållare för sannolikheter
            for f in self.bigram_prob[w]:   # för varje ord som har en sannolikhet att följa
                follwords.append(f)         #   sätter in fljeorden i en array
                chans = math.exp(float(self.bigram_prob[w][f])) # räknar om från log-chans
                p.append(chans)                 # sätter in sannolikheten i en array
            next = random.choices(follwords,p)  # slumpar följande ordet från följeorden och dess sannolikheter
            n =''.join(next)                    # list -> str()
            print(n)                            # skriver ut följeordet
            w = n                               # genererar nästa ord

def main():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description='BigramTester')
    parser.add_argument('--file', '-f', type=str,  required=True, help='file with language model')
    parser.add_argument('--start', '-s', type=str, required=True, help='starting word')
    parser.add_argument('--number_of_words', '-n', type=int, default=100)

    arguments = parser.parse_args()

    generator = Generator()
    generator.read_model(arguments.file)
    generator.generate(arguments.start,arguments.number_of_words)

if __name__ == "__main__":
    main()
