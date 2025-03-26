import os

import pandas as pd

current_file_directory = os.path.dirname(os.path.abspath(__file__))
dictionary = pd.read_csv(os.path.join(current_file_directory, "language_dictionary.csv"), delimiter=";")
dictionary = dictionary.set_index("key")


def translate(key, language):
    if language in dictionary.columns:
        return dictionary.loc[key][language]
    else:
        # default to English if language not found
        return dictionary.loc[key]["English"]
