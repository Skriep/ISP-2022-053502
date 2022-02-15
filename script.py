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

if __name__ == '__main__':
    main()
