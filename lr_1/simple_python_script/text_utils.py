"""
TextUtils module.

This module can calculate the following parameters for an arbitrary text:
- how many times does each word repeat in the text;
- average amount of words in a sentence;
- median amount of words in a sentence;
- top-K most frequent N-grams with default values of K = 10 and N = 4.

If imported as a module, the class TextUtils is available.
"""
import string


class TextUtils:
    """
    The class provides functions for text statistics.

    Provided functions:
    - get_words_in_sentences - splits the text into words grouped by sentences;
    - get_word_frequencies - returns all words' frequencies;
    - get_average_words_in_sentence - returns average amount
    of words in a sentence;
    - get_median_words_in_sentence - returns median amount
    of words in a sentence;
    - get_all_ngrams - returns all the n-grams;
    """

    def __init__(self, text):
        """Initialize the class with the text."""
        self.set_text(text)

    def _get_words_in_sentences(self) -> 'list[list[str]]':
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
        for word in self.text.split():
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

    def set_text(self, text):
        """Replace text with the provided one."""
        self.text = text
        self.sentences = self._get_words_in_sentences()

    def get_word_frequencies(self) -> 'dict[str, int]':
        """
        Return a dictionary of word frequencies of occurrence in the text.

        Dictionary's keys are words (strings),
        and values are their frequencies of occurence.

        The text must be split into lists of words grouped into sentences.
        """
        word_frequencies = {}
        for sentence in self.sentences:
            for word in sentence:
                if word not in word_frequencies:
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1
        return word_frequencies

    def get_average_words_in_sentence(self) -> float:
        """
        Return an average amount of words in a sentence of the text.

        If text contains no words, return 0.

        The text must be split into lists of words grouped into sentences.
        """
        sentence_word_counts = {len(sentence) for sentence in self.sentences}
        if len(sentence_word_counts) == 0:
            return 0
        else:
            return sum(sentence_word_counts) / len(sentence_word_counts)

    def get_median_words_in_sentence(self) -> float:
        """
        Return a median amount of words in a sentence of the text.

        If text contains no words, return 0.
        If text contains an odd amount of words,
        return the middle value in the center
        of the list of sentences' lengths.
        If text contains an even amount of words,
        return an average of the two middle values in the center
        of the list of sentences' lengths.

        The text must be split into lists of words grouped into sentences.
        """
        sentence_word_counts = sorted(
            [len(sentence) for sentence in self.sentences])
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

    def get_all_ngrams(self, n) -> 'dict[str, int]':
        """
        Return a dictionary with all n-grams and their frequencies in the text.

        Dictionary's keys are words (n-grams),
        and values are their frequencies of occurence in text.

        The text must be split into lists of words grouped into sentences.
        """
        n_grams: dict[str, int] = {}
        for sentence in self.sentences:
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
