"""
Simple python script.

This script can calculate the following parameters for an arbitrary text:
- how many times does each word repeat in the text;
- average amount of words in a sentence;
- median amount of words in a sentence;
- top-K most frequent N-grams with default values of K = 10 and N = 4.

If imported as a module, the following functions can be used:
- get_input - returns values entered by the user: N, K, text;
- get_words_in_sentences - splits the text into words grouped by sentences;
- get_word_frequencies - returns all words' frequencies;
- get_average_words_in_sentence - returns average amount
of words in a sentence;
- get_median_words_in_sentence - returns median amount of words in a sentence;
- get_all_ngrams - returns all the n-grams;
- main - the main function.

The following global variables are used:
- K_DEFAULT - the default value for K (used in function get_input);
- N_DEFAULT - the default value for N (used in function get_input).
"""
import string

K_DEFAULT = 10
N_DEFAULT = 4


def get_input() -> 'tuple[int, int, str]':
    """
    Return a tuple of values K, N, text.

    Ask the user to enter values of K, N, text.
    K must be a non-negative integer.
    N must be an integer greater than 0.
    text may be an arbitrary string.

    If some of the values K, N are entered incorrectly,
    the default values are used.
    Default values for K, N must be stored in global variables
    K_DEFAULT and N_DEFAULT respectively.
    """
    k_string = input('Enter K (the number of top N-grams to be printed) '
                     f'or nothing for the default value of {K_DEFAULT}: ')
    if k_string.isnumeric():
        k = int(k_string)
    else:
        k = K_DEFAULT
        print('The string for K is not numeric. '
              f'Using the default value of {k}.')

    n_string = input(
        f'Enter N or nothing for the default value of {N_DEFAULT}: ')
    if n_string.isnumeric():
        n = int(n_string)
    else:
        n = N_DEFAULT
        print('The string for N is not numeric. '
              f'Using the default value of {n}.')

    if n <= 0:
        n = N_DEFAULT
        print(f'N can only be greater than 0. Using the default value of {n}.')

    text = input('Enter the text:\n')
    return (k, n, text)


def get_words_in_sentences(text: str) -> 'list[list[str]]':
    """
    Return lists of words grouped into sentences.

    If the text is an empty string, return a list containing an empty list:
    [[]];
    Otherwise, return a list in the following form:
    [['word', 'word'], ['word'], ...].

    If any word ends in '.', '!' or '?',
    it is considered the end of a sentence.
    All trailing punctuation (as defined in string.punctuation)
    in words is stripped.
    Leading characters '"', "'", '(', '{', '[' in words are also stripped.
    """
    sentences: list[list[str]] = [[]]
    for word in text.split():
        clean_word = word.lower()
        clean_word = clean_word.rstrip(string.punctuation)
        clean_word = clean_word.lstrip("\"'({[")
        if len(clean_word) > 0:
            sentences[-1].append(clean_word)
        if word.endswith(('.', '!', '?')) and len(sentences[-1]) > 0:
            sentences.append([])
    if len(sentences[-1]) == 0 and len(sentences) > 1:
        del sentences[-1]
    return sentences


def get_word_frequencies(sentences: 'list[list[str]]') -> 'dict[str, int]':
    """
    Return a dictionary of word frequencies of occurrence in the text.

    Dictionary's keys are words (strings),
    and values are their frequencies of occurence.

    The text must be split into lists of words grouped into sentences.
    """
    word_frequencies = {}
    for sentence in sentences:
        for word in sentence:
            if word not in word_frequencies:
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    return word_frequencies


def get_average_words_in_sentence(sentences: 'list[list[str]]') -> float:
    """
    Return an average amount of words in a sentence of the text.

    If text contains no words, return 0.

    The text must be split into lists of words grouped into sentences.
    """
    sentence_word_counts = {len(sentence) for sentence in sentences}
    if len(sentence_word_counts) == 0:
        return 0
    else:
        return sum(sentence_word_counts) / len(sentence_word_counts)


def get_median_words_in_sentence(sentences: 'list[list[str]]') -> float:
    """
    Return a median amount of words in a sentence of the text.

    If text contains no words, return 0.
    If text contains an odd amount of words,
    return the middle value in the center of the list of sentences' lengths.
    If text contains an even amount of words,
    return an average of the two middle values in the center
    of the list of sentences' lengths.

    The text must be split into lists of words grouped into sentences.
    """
    sentence_word_counts = sorted([len(sentence) for sentence in sentences])
    word_counts_len = len(sentence_word_counts)
    if word_counts_len == 0:
        return 0
    elif word_counts_len % 2 == 1:
        median_words_in_sentence = float(
            sentence_word_counts[word_counts_len // 2])
    else:
        median_words_in_sentence = (
            sentence_word_counts[word_counts_len // 2]
            + sentence_word_counts[word_counts_len // 2 - 1]
        ) / 2
    return median_words_in_sentence


def get_all_ngrams(sentences: 'list[list[str]]', n) -> 'dict[str, int]':
    """
    Return a dictionary with all n-grams and their frequencies in the text.

    Dictionary's keys are words (n-grams),
    and values are their frequencies of occurence in text.

    The text must be split into lists of words grouped into sentences.
    """
    n_grams: dict[str, int] = {}
    for sentence in sentences:
        for word in sentence:
            word_len = len(word)
            if word_len >= n:
                for i in range(word_len - n + 1):
                    word_slice = word[i:i+n]
                    if word_slice not in n_grams:
                        n_grams[word_slice] = 1
                    else:
                        n_grams[word_slice] += 1
    return n_grams


def main():
    """
    Print some information about the text entered by the user.

    First, the function get_input() is called.
    Then, the entered text is processed
    and the following information is printed:
    - how many times does each word repeat in the text;
    - average amount of words in a sentence;
    - median amount of words in a sentence;
    - top-K most frequent N-grams and their frequencies of occurence.
    """
    k, n, text = get_input()
    sentences = get_words_in_sentences(text)

    word_frequencies = get_word_frequencies(sentences)
    if len(word_frequencies) == 0:
        print('\nThe text contains no words.')
    else:
        biggest_word_length = max(
            {len(word) for word in word_frequencies.keys()}, default=0)
        print('\nFrequencies of words in text:')
        for word in word_frequencies:
            freq = word_frequencies[word]
            print(f'{word:<{biggest_word_length}s}\t{freq}')

    print()
    median_words_in_sentence = get_median_words_in_sentence(sentences)
    average_words_in_sentence = get_average_words_in_sentence(sentences)
    print('Average amount of words in a sentence:\t'
          f'{average_words_in_sentence:.3f}')
    print('Median amount of words in a sentence:\t'
          f'{median_words_in_sentence:.1f}')

    if k > 0:
        print()
        n_grams = get_all_ngrams(sentences, n)
        n_grams_items = list(n_grams.items())
        n_grams_items.sort(key=lambda item: item[1], reverse=True)
        if len(n_grams_items) == 0:
            print(f'No {n}-grams found.')
        else:
            print(f'Top {k} most frequent {n}-grams:')
            for item in n_grams_items[:k]:
                print(item[0], item[1], sep='\t')


if __name__ == '__main__':
    main()
