import os

import pandas as pd

current_file_directory = os.path.dirname(os.path.abspath(__file__))
dictionary = pd.read_csv(
    os.path.join(current_file_directory, "language_dictionary.csv"), delimiter=";"
)
dictionary = dictionary.set_index("Deutsch")


def translate(text, language):
    if language == "Deutsch":
        return text
    else:
        if text in dictionary.index:
            text_translated = dictionary.loc[text][language]
            return text_translated
        else:
            return text
