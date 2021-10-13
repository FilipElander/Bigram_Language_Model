# Bigram_Language_Model-
Generate new words and sentences through Bigram language models
First train a Bigram Language model with either a kafka-dataset. Or, incorperate a custom dataset.
Then Test the Entropy of the Language model
Lastly, run the word generator to generate N following words from a START-word

Trainer:
'--file', '-f, --> file from which to build the language model
'--destination', '-d', --> file in which to store the language model
example: python BigramTrainer.py -f data/kafka.txt -d kafka_model.txt

Tester: 
'--file', '-f', type=str, --> file with language model
'--test_corpus', '-t', --> test corpus

Generator:
'--file', '-f, --> file with language model
'--start', '-s', --> starting word
'--number_of_words' --> default=100
