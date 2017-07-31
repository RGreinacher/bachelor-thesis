#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import python libs

import json
import copy
import numpy as np
import matplotlib as mpl
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from pprint import pprint as pp

# import project libs

from constants import *
from helper import *

# defining globals & constants
# -

# methods

def plot_correct_answers_per_paragraph(annotation_classes, subjects_table):
    data_per_level = create_data_structure()
    reference_annotations = empty_subjects_table(subjects_table)
    paragraphs_per_block = count_paragraphs_per_block(reference_annotations)
    print('paragraphs_per_block', paragraphs_per_block)

    for subject_id, annotation_classes_per_subject in enumerate(annotation_classes):
        absolute_paragraph_index = 0

        for block_index, block in enumerate(annotation_classes_per_subject):
            subject_table_block = subjects_table[subject_id][block_index]
            if not subject_table_block_is_annotated(subject_table_block):
                level = 1 + (subject_id % 3)
            else:
                level = 0

            for paragraph_index, paragraph in enumerate(block):
                subject_annotations_per_paragraph = [item for sublist in paragraph for item in sublist]
                correct_annotations = subject_annotations_per_paragraph.count(0)
                total_number_of_annotations = count_annotations_per_paragraph(reference_annotations[block_index][paragraph_index])
                correctness_per_paragraph = correct_annotations / total_number_of_annotations

                data_per_level[level][absolute_paragraph_index].append(correctness_per_paragraph)
                absolute_paragraph_index = absolute_paragraph_index + 1

    plot_barchart(data_per_level, paragraphs_per_block)

# helpers

def create_data_structure():
    paragraphs = []
    for i in range(0, 73): paragraphs.append([])
    return [
        copy.deepcopy(paragraphs),
        copy.deepcopy(paragraphs),
        copy.deepcopy(paragraphs),
        copy.deepcopy(paragraphs)
    ]

def count_paragraphs_per_block(reference_annotations):
    return list(map(lambda x: len(x), reference_annotations))

def count_annotations_per_paragraph(paragraph):
    return sum(map(lambda x: len(x) , paragraph))

def add_spaces_between_blocks(data, paragraphs_per_block):
    absolute_paragraph_index = -1
    for index, number_of_paragraphs in enumerate(paragraphs_per_block):
        absolute_paragraph_index += number_of_paragraphs + 1

        if index < 3:
            data.insert(absolute_paragraph_index, 0)
    return data

def means_per_block(data, paragraphs_per_block):
    means = []
    standard_deviations = []
    block_start_index = 0
    for number_of_paragraphs in paragraphs_per_block:
        block_data = np.array(data[block_start_index:(block_start_index + number_of_paragraphs)])
        means.append(np.mean(block_data)) # * 100.0)
        standard_deviations.append(np.std(block_data))
        block_start_index += number_of_paragraphs + 1
    return (means, standard_deviations)

def plot_barchart(data_per_level, paragraphs_per_block):
    mpl.rc("figure", facecolor='1')
    fig = plt.figure()

    # relative_data_per_level = [list(map(lambda x: (sum(x) / len(x)) * 100, correct_annotations)) for correct_annotations in data_per_level]
    relative_data_per_level = [list(map(lambda x: np.mean(x) * 100, correct_annotations)) for correct_annotations in data_per_level]

    for plot_level in range(0, 4):
        title = "Korrekte Annotationen %s (%s annotierte Texte)" % (ASSISTANCE_SYSTEM_LEVELS_AS_TEXT[plot_level], len(data_per_level[plot_level][0]))
        data = add_spaces_between_blocks(relative_data_per_level[plot_level], paragraphs_per_block) # this data is per paragraph!
        # (means, standard_deviations) = means_per_block(data_per_level[plot_level], paragraphs_per_block)
        (means, standard_deviations) = means_per_block(relative_data_per_level[plot_level], paragraphs_per_block)

        # calculate standard deviantions per bar
        raw_data = add_spaces_between_blocks(data_per_level[plot_level], paragraphs_per_block)
        same_shaped_data = [[0] * len(raw_data[plot_level]) if x == 0 else x for x in raw_data]
        # pp(same_shaped_data)
        standard_deviations_per_bar = np.std(same_shaped_data, axis=1) * 100.0

        ax = fig.add_subplot(2, 2, plot_level + 1)
        plt.title(title)
        ax.set_axis_bgcolor((0.95, 0.95, 0.95))

        # coordinate system
        ax.set_xlim([-3, 78])
        # ax.set_xticklabels([])
        plt.xlabel('Absätze in 4 Blöcken')

        ax.set_ylim([0, 107])
        plt.yticks(np.arange(min(ax.get_ylim()), max(ax.get_ylim())+1, 10))
        vals = ax.get_yticks()
        ax.set_yticklabels(['{:.0f}%'.format(x) for x in vals])
        plt.ylabel('durchschnittlich korrekte Annotationen pro Absatz')

        # bars
        index = np.arange(len(data))
        error_config = {'ecolor': '0.3'}
        ax.grid(zorder=0)
        barlist = ax.bar(
            index,
            data,
            width = 0.9,
            align = 'center',
            error_kw=error_config,
            yerr = standard_deviations_per_bar,
            edgecolor = 'none',
            color = (0.56, 0.79, 0.99),
            alpha = 0.6,
            # label='A',
            zorder = 3
        )

        # color of groups
        for bar_index, bar in enumerate(barlist):
            if bar_index in range(15, 37) or bar_index in range(56, 76):
                bar.set_color((0.56, 0.79, 0.99))

        # average per block
        block_start_index = 0
        for index, number_of_paragraphs in enumerate(paragraphs_per_block):
            block_end_index = block_start_index + number_of_paragraphs
            mean = means[index]
            plt.plot(
                (block_start_index, block_end_index - 1),
                (mean, mean),
                linewidth = 2,
                color = 'r',
                zorder = 5
            )
            std = standard_deviations[index]
            plt.plot(
                (block_start_index, block_end_index - 1),
                (mean - std, mean - std),
                linewidth = 1,
                color = (0.8, 0.2, 0.2),
                zorder = 5
            )
            plt.plot(
                (block_start_index, block_end_index - 1),
                (mean + std, mean + std),
                linewidth = 1,
                color = (0.8, 0.2, 0.2),
                zorder = 5
            )
            block_start_index += number_of_paragraphs + 1

    plt.legend()
    plt.show()


# entry point as a stand alone script
if __name__ == '__main__':
    annotation_classes = read_json_file(JSON_ANNOTATION_CLASSES_FILE_NAME)
    subjects_table = read_subject_table()

    plot_correct_answers_per_paragraph(annotation_classes, subjects_table)
