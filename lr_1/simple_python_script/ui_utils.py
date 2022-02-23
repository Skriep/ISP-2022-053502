"""
UIUtils module.

This module can print the following parameters for the text
provided by the user:
- how many times does each word repeat in the text;
- average amount of words in a sentence;
- median amount of words in a sentence;
- top-K most frequent N-grams with default values of K = 10 and N = 4.

If imported as a module, the class UIUtils is available.
"""


from text_utils import TextUtils


class UIUtils:
    """
    The class provides functions for interaction with the user.

    Provided functions:
    - print_word_frequencies - print all words' frequencies;
    - print_average_words_in_sentence - print average amount
    of words in a sentence;
    - print_median_words_in_sentence - print median amount
    of words in a sentence;
    - print_top_ngrams - print top k n-grams;
    """

    def __init__(self, k_default=10, n_default=4):
        """
        Asks the user to enter k, n and text,\
        initializing the corresponding fields.

        Provided functions:
        - print_word_frequencies - print all words' frequencies;
        - print_average_words_in_sentence - print average amount
        of words in a sentence;
        - print_median_words_in_sentence - print median amount
        of words in a sentence;
        - print_top_ngrams - print top k n-grams;
        """
        self.k_default = k_default
        self.n_default = n_default
        self._get_user_input()
        self.text_utils = TextUtils(self.text)

    def _get_user_input(self):
        """
        Initialize values self.k, self.n and self.text.

        Ask the user to enter values of K, N, text.
        K must be a non-negative integer.
        N must be an integer greater than 0.
        text may be an arbitrary string.

        If some of the values K, N are entered incorrectly,
        the default values are used.
        """
        k_string = input('Enter K (the number of top N-grams to be printed) '
                         'or nothing for the default value '
                         f'of {self.k_default}: ')
        if k_string.isnumeric():
            self.k = int(k_string)
        else:
            self.k = self.k_default
            print('The string for K is not numeric. '
                  f'Using the default value of {self.k}.')

        n_string = input(
            f'Enter N or nothing for the default value of {self.n_default}: ')
        if n_string.isnumeric():
            self.n = int(n_string)
        else:
            self.n = self.n_default
            print('The string for N is not numeric. '
                  f'Using the default value of {self.n}.')

        if self.n <= 0:
            self.n = self.n_default
            print('N can only be greater than 0. '
                  f'Using the default value of {self.n}.')

        self.text = input('Enter the text:\n')

    def print_word_frequencies(self):
        """Print all words' frequencies."""
        word_frequencies = self.text_utils.get_word_frequencies()
        if len(word_frequencies) == 0:
            print('\nThe text contains no words.')
        else:
            biggest_word_length = max(
                {len(word) for word in word_frequencies.keys()}, default=0)
            print('\nFrequencies of words in text:')
            for word in word_frequencies:
                freq = word_frequencies[word]
                print(f'{word:<{biggest_word_length}s}\t{freq}')

    def print_average_words_in_sentence(self):
        """Print average amount of words in a sentence."""
        average_words_in_sentence = (
            self.text_utils.get_average_words_in_sentence())
        print('Average amount of words in a sentence:\t'
              f'{average_words_in_sentence:.3f}')

    def print_median_words_in_sentence(self):
        """Print median amount of words in a sentence."""
        median_words_in_sentence = (
            self.text_utils.get_median_words_in_sentence())
        print('Median amount of words in a sentence:\t'
              f'{median_words_in_sentence:.1f}')

    def print_top_ngrams(self):
        """
        Print top K N-grams.

        K and N are values of the corresponding variables self.k and self.n.
        """
        if self.k > 0:
            n_grams = self.text_utils.get_all_ngrams(self.n)
            n_grams_items = list(n_grams.items())
            n_grams_items.sort(key=lambda item: item[1], reverse=True)
            if len(n_grams_items) == 0:
                print(f'No {self.n}-grams found.')
            else:
                print(f'Top {self.k} most frequent {self.n}-grams:')
                for item in n_grams_items[:self.k]:
                    print(item[0], item[1], sep='\t')
