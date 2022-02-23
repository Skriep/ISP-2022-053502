"""
Simple python script.

This script can calculate the following parameters for an arbitrary text:
- how many times does each word repeat in the text;
- average amount of words in a sentence;
- median amount of words in a sentence;
- top-K most frequent N-grams with default values of K = 10 and N = 4.
"""
from ui_utils import UIUtils


def main():
    """
    Print some information about the text entered by the user.

    Text entered by the user is processed
    and the following information is printed:
    - how many times does each word repeat in the text;
    - average amount of words in a sentence;
    - median amount of words in a sentence;
    - top-K most frequent N-grams and their frequencies of occurence.
    """
    usr_utils = UIUtils()
    print('\n')
    usr_utils.print_word_frequencies()
    print('\n')
    usr_utils.print_average_words_in_sentence()
    usr_utils.print_median_words_in_sentence()
    if usr_utils.k > 0:
        print('\n')
        usr_utils.print_top_ngrams()


if __name__ == '__main__':
    main()
