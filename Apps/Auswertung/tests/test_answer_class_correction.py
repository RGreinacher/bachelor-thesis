#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import python libs

import sys
sys.path.append('../')

# import project libs

from answer_class_correction_analysis import *
from pprint import pprint as pp

test_cases =[
    { # 0
        'reference':    [0, 0, 0, 0, 0, 0],
        'annotation':   [0, 0, 0, 0, 0, 0],
        'target_output': [
            [6, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            0
        ]
    },
    { # 1
        'reference':    [5, 5, 3, 2, 1, 0],
        'annotation':   [0, 5, 0, 0, 2, 5],
        'target_output': [
            [0, 0, 0, 0, 0, 1],
            [0, 0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 1],
            0
        ]
    },
    { # 2
        'reference':    [4, 5],
        'annotation':   [4, 5],
        'target_output': [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1],
            0
        ]
    },
    { # 3
        'reference':    [4, 5],
        'annotation':   [4, 0],
        'target_output': [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [1, 0, 0, 0, 0, 0],
            0
        ]
    },
    { # 4
        'reference':    [4, 5],
        'annotation':   [   0],
        'target_output': [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            0
        ]
    },
    { # 5
        'reference':    [   0],
        'annotation':   [4, 0],
        'target_output': [
            [1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            1
        ]
    },
    { # 6
        'reference':    [   0, 5],
        'annotation':   [4, 0, 0],
        'target_output': [
            [1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            1
        ]
    },
    { # 7
        'reference':    [4, 5   ],
        'annotation':   [   0, 4],
        'target_output': [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            1
        ]
    },
    { # 8
        'reference':    [   0, 5, 5],
        'annotation':   [4, 0, 1, 0],
        'target_output': [
            [1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0],
            1
        ]
    },
    { # 9
        'reference':    [      0],
        'annotation':   [4, 4, 2],
        'target_output': [
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            2
        ]
    },
    { # 10
        'reference':    [      0, 2],
        'annotation':   [4, 4, 2, 0],
        'target_output': [
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            2
        ]
    },
    { # 11
        'reference':    [5, 4],
        'annotation':   [0],
        'target_output': [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            0
        ]
    },
    { # 12
        'reference':    [2, 4, 0],
        'annotation':   [0,    0],
        'target_output': [
            [1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            0
        ]
    },
    { # 13
        'reference':    [1, 5, 4, 5],
        'annotation':   [0, 0,    0],
        'target_output': [
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0],
            0
        ]
    },
    { # 14
        'reference':    [5, 4, 2],
        'annotation':   [0,    0],
        'target_output': [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            0
        ]
    },
]

for index, test in enumerate(test_cases):
    reference = [[test['reference']]]
    annotation = [[test['annotation']]]
    analyzed_annotations = quantitative_answer_class_correction_analysis_per_block(annotation, reference)
    if analyzed_annotations == test['target_output']:
        print('✓ Test', index)
    else:
        print('✗ Test', index, '- should be:')
        pp(test['target_output'])
        print('but is')
        pp(analyzed_annotations)
        break
