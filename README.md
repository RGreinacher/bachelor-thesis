# Efficiency Evaluation of an Assistance System for Text Annotations

Introduction: Smart personal assistants like Siri or Alexa use machine learning based text analysis to understand commands and questions. Underlying technologies require a huge amount of training data, and their production often involves human annotators doing repetitive and monotonous work.Objectives: The purpose of the present study is to identify possibilities to support the text annotation task with automated assistance. Since these annotation assistance systems cannot be perfectly accurate, the influence of reliability is analyzed, too.Methods: An assistance for making annotation suggestions was simulated. Subjects accomplished annotation tasks with and without the system in a counterbalanced order. Three levels of reliability (10, 50, or 90% correct suggestions) of the system were benchmarked. Dimensions measured were correct annotations (hits), misses of annotations, and total task time. A 2 (assistance present) x 3 (reliability, between) mixed design (N = 66) was used.Results: An assistance system providing a reliability of 50% or 90% improves accuracy and reduces misses of the human annotations significantly. Suggestions with a reliability of 90% lead to a significant decrease of human processing time.Conclusions: Supporting the task of text annotation using an automated assistance will improve human’s performance, if the suggestions of the system are mature.

***

## This Repo

This repo contains all relevant data of my Thesis I wrote to get my Bachelor of Science degree in Computer Science at the Technische Universität Berlin.

### Uploading not done yet

All files will be uploaded here after I released this work. Currently this repo only provides an URL which I use to link to.

### Files & folders to come

- **Thesis** folder with all the tex files, references and assets - and of course the PDF of the thesis
- **Data set** of the study
- **Slides** I used for my colloquium
### What is missing

The model evaluation (`Apps/Model Evaluation/*.py`) won't run out of the box. These scripts need several dependencies I won't provide. But they are free and can be found here:

- [German dictionary](https://sourceforge.net/projects/germandict/files/)
- [German NER Training Corpus](https://sites.google.com/site/germeval2014ner/data)
- [NLTK Classifier Based German Tagger](https://github.com/ptnplanet/NLTK-Contributions/tree/master/ClassifierBasedGermanTagger)
