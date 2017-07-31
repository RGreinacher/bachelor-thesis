import nltk
import pickle
import json
from nltk import Tree
from nltk import ChunkScore
from pprint import pprint as pp
from nltk.chunk.api import ChunkParserI
from os import listdir
from os.path import isfile, join
import maxent_chunker

POS_TAGGER_PATH = 'nltk_german_pos_classifier_data.pickle'
CHUNKER_PICKLE_NAME = 'implisense_ne_chunker_multiclass.pickle'
TEXT_SET = 'NER-de-test'

with open(POS_TAGGER_PATH, 'rb') as f:
  german_pos_tagger = pickle.load(f)

with open(CHUNKER_PICKLE_NAME, 'rb') as f:
  self_trained_chunker = pickle.load(f)

with open('training/germeval/' + TEXT_SET + '.pickle', 'rb') as f:
  germ_eval_corpus = pickle.load(f)

sentence = germ_eval_corpus[0]
text = sentence.leaves()
parsed = self_trained_chunker.parse(text)

print('RAW TEXT')
pp(text)

print('SENTENCE')
pp(sentence)

print('PARSED')
pp(parsed)

score = self_trained_chunker.evaluate(germ_eval_corpus)
print("Accuracy: %s" % score.accuracy())
print("F Score: %s" % score.f_measure())
print("Precision: %s" % score.precision())
print("Recall: %s" % score.recall())
