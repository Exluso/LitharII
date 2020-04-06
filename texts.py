"""This module generates all the texts to be used in Lithar II"""

import csv

def create_texts(language):
    """IN: language as string. A 3 Letters code for the language, e.g. ENG
    OUT: a dict with all the texts used in the program."""

    file_name = "texts.csv"
    texts = {}
    with open(file_name) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            texts.update({row["ID"]: row[language]})

    return texts

# texts = create_texts("ITA")
# print(texts["welcome"])
