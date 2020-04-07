"""This module generates all the texts to be used in Lithar II"""

import csv, sys

def separe():
    """ Prints a separator to divide different section of the text flow."""
    print("\n" + 150 * "~" + "\n")

def create_texts(language):
    """IN: language as string. A 3 Letters code for the language, e.g. ENG
    OUT: a dict with all the texts used in the program."""

    file_name = "texts.csv"
    texts = {}
    try:
        with open(file_name) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                texts.update({row["ID"]: row[language]})

        return texts
    except FileNotFoundError:
        separe()
        print("There is no text file in Lithar directory.\n"
              "Please add a 'texts.csv' in Lithar directory, then launch "
              "the program again."
              )
        separe()
        sys.exit()

if __name__ == "__main__":
    texts = create_texts("ITA")
    print(texts["welcome"])
    print(texts)
