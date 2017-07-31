import nltk
import pickle
import json
from nltk import Tree
from nltk import ChunkScore
import pprint
from pprint import pprint as pp
from nltk.chunk.api import ChunkParserI
from os import listdir
from os.path import isfile, join
import maxent_chunker
import numpy as np
from sklearn.model_selection import KFold
import ner_pipeline
from time import gmtime, strftime

TEXT_SET = 'NER-de-train'
MANUAL_LOG_FILE = 'results.log'
K_FOLD = 10

def evaluation_summary(scores):
    labels = ['Accuracy', 'F Score', 'Precision', 'Recall']

    current_results_index = len(scores) - 1
    for i in range(0, 4):
        write_to_log("current %s: %s" % (labels[i], scores[current_results_index][i]))

    for i in range(0, 4):
        avg = sum(scores[i]) / float(len(scores[i]))
        result = "mean %s: %s" % (labels[i], avg)
        write_to_log(result)

    write_to_log(pprint.pformat(scores))
    write_to_log("\n")

def write_to_log(msg):
    datetime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    write_string = datetime + ": " + msg + "\n"

    file = open(MANUAL_LOG_FILE, 'a')
    file.write(write_string)
    file.close()



# entry point as a stand alone script
if __name__ == '__main__':
    print('load preprocessed corpus...')
    with open('training/germeval/' + TEXT_SET + '.pickle', 'rb') as f:
      germ_eval_corpus = pickle.load(f)
      print("corpus size: %s" % (len(germ_eval_corpus)))

    iteration = 0
    scores = [
        [],
        [],
        [],
        []
    ]

    write_to_log("start %s-fold cross validation..." % (K_FOLD))
    kf = KFold(n_splits=K_FOLD, shuffle=True)
    for train_index, test_index in kf.split(germ_eval_corpus):
        training_set = [germ_eval_corpus[i] for i in train_index]
        test_set = [germ_eval_corpus[i] for i in test_index]
        write_to_log("iteration %s: train size: %s, test size: %s" % (iteration, len(training_set), len(test_set)))
        iteration += 1

        currently_trained_chunker = ner_pipeline.train_maxent_chunker_with(training_set)
        print('start evaluating...')
        evaluation = currently_trained_chunker.evaluate(test_set)
        scores[0].append(evaluation.accuracy())
        scores[1].append(evaluation.f_measure())
        scores[2].append(evaluation.precision())
        scores[3].append(evaluation.recall())

        print('current scores:')
        evaluation_summary(scores)

    print('final scores:')
    evaluation_summary(scores)
    pp(scores)

    # scores = [
    #     [
    #         0.9476210489061913,
    #         0.9491465775118775,
    #         0.9458963879377003,
    #         0.9476252004990198,
    #         0.9493742889647326,
    #         0.9497946342742288,
    #         0.9498006725908109,
    #         0.9521216044284726,
    #         0.9442498733452279,
    #         0.9467618245489605
    #     ],
    #     [
    #         0.6077519379844961,
    #         0.6112736493075873,
    #         0.5861864239065901,
    #         0.5922953451043339,
    #         0.6136363636363636,
    #         0.5964563010153294,
    #         0.6181172291296625,
    #         0.6078759949727692,
    #         0.5553074893444286,
    #         0.5923062052967331
    #     ],
    #     [
    #         0.6784941583729988,
    #         0.6936697653829128,
    #         0.6567627494456763,
    #         0.6733576642335767,
    #         0.6905071521456437,
    #         0.6784420289855072,
    #         0.6926138876603273,
    #         0.6847569608305805,
    #         0.6404494382022472,
    #         0.6742957746478874
    #     ],
    #     [
    #         0.5503685503685504,
    #         0.546373779637378,
    #         0.5293066476054324,
    #         0.5286532951289399,
    #         0.5521663778162912,
    #         0.5321492007104796,
    #         0.5580898075552387,
    #         0.5465160075329567,
    #         0.4901469007524185,
    #         0.5280937607721475
    #     ]
    # ]
