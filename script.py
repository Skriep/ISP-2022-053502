import string

def main():
    K = 10
    N = 4
    K_string = input(f'Enter K (the number of top N-grams to be printed) or nothing for the default value of {K}: ')
    if K_string.isnumeric():
        K = int(K_string)
    else:
        print(f'The string for K is not numeric. Using the default value of {K}.')
    N_string = input(f'Enter N or nothing for the default value of {N}: ')
    if N_string.isnumeric():
        K = int(K_string)
    else:
        print(f'The string for N is not numeric. Using the default value of {N}.')

    text = input('Enter the text:\n')

    split_text = text.split()
    word_frequencies = {}
    sentence_word_counts = []
    biggest_word_length = 0
    curr_sentence_word_count = 0

    punctuation = tuple(string.punctuation)
    for word in split_text:
        clean_word = word.lower()
        while clean_word.endswith(punctuation):
            clean_word = clean_word[:-1]
        while clean_word.startswith(('"', "'", '(', '{', '[')):
            clean_word = clean_word[1:]
        clean_word_length = len(clean_word)
        if clean_word_length > 0:
            curr_sentence_word_count += 1
            if clean_word not in word_frequencies:
                word_frequencies[clean_word] = 1
            else:
                word_frequencies[clean_word] += 1
            
            if clean_word_length > biggest_word_length:
                biggest_word_length = clean_word_length
        if word.endswith(('.', '!', '?')):
            sentence_word_counts.append(curr_sentence_word_count + 1)
            curr_sentence_word_count = 0

    if curr_sentence_word_count > 0 or len(sentence_word_counts) == 0:
        sentence_word_counts.append(curr_sentence_word_count)
    
    print('\nFrequencies of words in text:')
    for word in word_frequencies:
        freq = word_frequencies[word]
        print(f'{word:<{biggest_word_length}s}\t{freq}')
    print()

    sentence_word_counts = sorted(sentence_word_counts)
    sentence_word_counts_len = len(sentence_word_counts)
    average_words_in_sentence = sum(sentence_word_counts) / sentence_word_counts_len
    if sentence_word_counts_len % 2 == 1:
        median_words_in_sentence = sentence_word_counts[sentence_word_counts_len // 2]
    else:
        median_words_in_sentence = (sentence_word_counts[sentence_word_counts_len // 2] +
                                    sentence_word_counts[sentence_word_counts_len // 2 - 1]) / 2
    print(f'Average amount of words in a sentence:\t{average_words_in_sentence:.3f}')
    print(f'Median amount of words in a sentence:\t{median_words_in_sentence:.1f}')

if __name__ == '__main__':
    main()
