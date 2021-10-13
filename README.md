# Bigram_Language_Model-
First train a Bigram Language model with either a kafka-dataset or incorperate a custom dataset.
Then Test the Entropy of the Language model 

Trainer:
'--file', '-f, --> file from which to build the language model
'--destination', '-d', --> file in which to store the language model
example: python BigramTrainer.py -f data/kafka.txt -d kafka_model.txt

Tester: 
