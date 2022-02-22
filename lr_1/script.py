import string

K_DEFAULT = 10
N_DEFAULT = 4

def get_input() -> 'tuple[int, int, str]':
	k_string = input(f'Enter K (the number of top N-grams to be printed) or nothing for the default value of {K_DEFAULT}: ')
	if k_string.isnumeric():
		k = int(k_string)
	else:
		k = K_DEFAULT
		print(f'The string for K is not numeric. Using the default value of {k}.')
	
	n_string = input(f'Enter N or nothing for the default value of {N_DEFAULT}: ')
	if n_string.isnumeric():
		n = int(n_string)
	else:
		n = N_DEFAULT
		print(f'The string for N is not numeric. Using the default value of {n}.')

	if n <= 0:
		n = N_DEFAULT
		print(f'N can only be greater than 0. Using the default value of {n}.')

	text = input('Enter the text:\n')
	return (k, n, text)

def get_words_in_sentences(text : str) -> 'list[list[str]]':
	sentences : list[list[str]] = [[]]
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

def get_word_frequencies(sentences : 'list[list[str]]') -> 'dict[str, int]':
	word_frequencies = {}
	for sentence in sentences:
		for word in sentence:
			if word not in word_frequencies:
				word_frequencies[word] = 1
			else:
				word_frequencies[word] += 1
	return word_frequencies

def get_average_words_in_sentence(sentences : 'list[list[str]]') -> float:
	sentence_word_counts = {len(sentence) for sentence in sentences}
	if len(sentence_word_counts) == 0:
		return 0
	else:
		return sum(sentence_word_counts) / len(sentence_word_counts)

def get_median_words_in_sentence(sentences : 'list[list[str]]') -> float:
	sentence_word_counts = sorted([len(sentence) for sentence in sentences])
	sentence_word_counts_len = len(sentence_word_counts)
	if sentence_word_counts_len == 0:
		return 0
	elif sentence_word_counts_len % 2 == 1:
		median_words_in_sentence = float(sentence_word_counts[sentence_word_counts_len // 2])
	else:
		median_words_in_sentence = (sentence_word_counts[sentence_word_counts_len // 2] +
									sentence_word_counts[sentence_word_counts_len // 2 - 1]) / 2
	return median_words_in_sentence

def get_all_ngrams(sentences : 'list[list[str]]', n) -> 'dict[str, int]':
	n_grams : dict[str, int] = {}
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
	k, n, text = get_input()
	sentences = get_words_in_sentences(text)
	
	word_frequencies = get_word_frequencies(sentences)
	if len(word_frequencies) == 0:
		print('\nThe text contains no words.')
	else:
		biggest_word_length = max({len(word) for word in word_frequencies.keys()}, default=0)
		print('\nFrequencies of words in text:')
		for word in word_frequencies:
			freq = word_frequencies[word]
			print(f'{word:<{biggest_word_length}s}\t{freq}')

	print()
	median_words_in_sentence = get_median_words_in_sentence(sentences)
	average_words_in_sentence = get_average_words_in_sentence(sentences)
	print(f'Average amount of words in a sentence:\t{average_words_in_sentence:.3f}')
	print(f'Median amount of words in a sentence:\t{median_words_in_sentence:.1f}')

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
