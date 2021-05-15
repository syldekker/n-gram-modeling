# n-grams

This program uses diphone (bigram) and triphone (trigram) models to represent Mainstream American English (MAE) phonotactics.

## Uses:

1. Generate random sequences of phonemes based on training data (CMU Pronouncing Dictionary)
2. When given test file of made-up "words" as argument, model scores each "word" based on similarity to MAE phonotactics

## Description:

The program takes either two or three command line arguments:
1. `training_file`
  1. CMU phonetic dictionary
2. `N`
  1. either `2` or `3`
  2. sets n-gram type (bigram or trigram)
3. `test_file` (optional)
  1. corpus for which to calculate perplexity
    1. `X.txt` or `Y.txt`

If the program is given only two command line arguments, it prints 25 "words" consisting of random phoneme sequences based on either a diphone or triphone model.

When given three arguments, the program processes the test file based on a smoothed di- or triphone model. The probability of each test "word" is calculated and printed. The perplexity of the test corpus is calculated based on the log probabilities of its constituent words.
