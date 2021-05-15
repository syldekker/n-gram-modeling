import sys
import random
import re
import math
from collections import defaultdict


# Initial word boundaries are represented by '#', and final word boundaries are represented by '##'.
PHONE_LIST = (
    '#', 'AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'B', 'CH', 'D', 'DH', 'EH', 'ER', 'EY', 'F', 'G', 'HH', 'IH', 'IY', 'JH',
    'K', 'L', 'M', 'N', 'NG', 'OW', 'OY', 'P', 'R', 'S', 'SH', 'T', 'TH', 'UH', 'UW', 'V', 'W', 'Y', 'Z', 'ZH', '##'
)


# Reads in 'word_transcriptions.txt' and returns diphone dictionary of items containing each
# first phone paired with all possible second phones and their corresponding probabilities.
def di_training():
    phone_count = defaultdict(lambda: 0)
    diphone_count = defaultdict(lambda: 0)
    train_f = open(sys.argv[1], encoding='utf-8')

    if len(sys.argv) == 4:
        add_1_diph(diphone_count)

    for line in train_f.readlines():
        line = re.sub(u'^[a-z\']+', '#', line.strip()) + ' ##'  # Discard all orthographic word forms, append '##'.
        phonemes = line.split()  # Convert line to list of phonemes.
        for i in range(len(phonemes) - 1):
            phone_count[phonemes[i]] += 1  # Keep count of each phoneme's frequency.
            diphone = tuple(phonemes[i:i + 2])  # Create diphone (bigram) as tuple of 1st & 2nd phonemes.
            diphone_count[diphone] += 1  # Keep count of each diphone's frequency.
        phone_count['##'] += 1  # Count word final boundary, '##'.

    train_f.close()

    master_dict = defaultdict(dict)  # Create empty dictionary described above.

    for diphone in diphone_count.keys():  # P (x|x-1) (Fill that dictionary up, baby.)
        master_dict[diphone[0]][diphone[1]] = diphone_count[diphone] / phone_count[diphone[0]]

    return master_dict


# Set all possible diphones' counts to 1.
def add_1_diph(diph_ct):
    for phone1 in PHONE_LIST:
        for phone2 in PHONE_LIST:
            diph_ct[tuple([phone1] + [phone2])] += 1


# Generate pseudo words with respect to diphone frequencies.
def di_gen(p_diph):
    for i in range(25):
        while True:  # This loop ensures that only words of a sufficient length and composition will be printed.
            gen_phone = ''
            gen_word = []
            while gen_phone != '##':  # Phonemes are added until '##' is generated.
                gen_word.append(gen_phone)  # Adds generated phoneme to word being generated (1st addition is '').
                if gen_phone == '':
                    gen_phone = '#'
                gen_phone = gen_phone2(gen_phone, p_diph)  # 2nd half of diphone returned.
            word = ' '.join(gen_word)  # Assembles list of phonemes (gen_word) into string separated by ' '.
            if not re.search(r'[AEIOU]', word):  # If generated word has no vowel, re-do this
                continue                         # iteration of for loop (generate new word).
            print(word)  # Print final word at the end of each for loop.
            break  # Breaks outer while loop to proceed to next iteration of for loop.


# Generate phonemes on a diphone (bigram) basis.
def gen_phone2(phone1, p_diph):
    rand = random.random()  # Generate random float between 0 and 1.
    for phone2 in p_diph[phone1]:  # Go through all possible diphone configurations (and probs) given phone1.
        rand -= p_diph[phone1][phone2]  # Subtract probability of given phone2 from random float.
        if rand < 0.0:  # Return 1st phone2 that brings rand below 0.
            return phone2
    return '##'


# Reads in 'word_transcriptions.txt' and returns triphone dictionary of items containing each
# first diphone paired with all possible third phones and their corresponding probabilities.
def tri_training():
    diphone_count = defaultdict(lambda: 0)
    triphone_count = defaultdict(lambda: 0)
    train_f = open(sys.argv[1], encoding='utf-8')

    if len(sys.argv) == 4:
        add_1_diph(diphone_count)
        add_1_triph(triphone_count)

    for line in train_f.readlines():
        line = re.sub(u'^[a-z\']+', '#', line.strip()) + ' ##'  # Discard all orthographic word forms, append '##'.
        phonemes = line.split()  # Convert line to list of phonemes.
        for i in range(len(phonemes) - 2):
            diphone = tuple(phonemes[i:i+2])
            diphone_count[diphone] += 1  # Keep count of each diphone's frequency.
            triphone = tuple(phonemes[i:i+3])  # Create triphone (trigram) as tuple of 1st, 2nd, & 3rd phonemes.
            triphone_count[triphone] += 1  # Keep count of each triphone's frequency.
        diphone_count[(phonemes[-2], '##')] += 1  # Count word final boundary, '##'.

    train_f.close()

    master_dict = defaultdict(dict)  # Create empty dictionary described above.

    for triphone in triphone_count.keys():  # P (x|x-1) (Fill that dictionary up, baby.)
        master_dict[triphone[:2]][triphone[2]] = triphone_count[triphone] / diphone_count[triphone[:2]]

    return master_dict


# Set all possible triphones' counts to 1.
def add_1_triph(triph_ct):
    for phone1 in PHONE_LIST:
        for phone2 in PHONE_LIST:
            for phone3 in PHONE_LIST:
                triph_ct[tuple([phone1] + [phone2] + [phone3])] += 1


# Generate pseudo words with respect to triphone frequencies.
def tri_gen(p_triph):
    for i in range(25):
        while True:  # This loop ensures that only words of a sufficient length and composition will be printed.
            gen_phone = ''
            gen_diphone = ('', '')
            gen_word = []
            while gen_phone != '##':  # Phonemes are added until '##' is generated.
                gen_word.append(gen_phone)  # Adds generated phoneme to word being generated (1st addition is '').
                if gen_diphone == ('', ''):
                    gen_diphone = ('#', random.choice(PHONE_LIST[1:-1]))  # Assigns random 1st phoneme (excludes '##').
                    gen_word.append(gen_diphone[1])
                gen_phone = gen_phone3(gen_diphone, p_triph)  # 2nd half of diphone returned.
                gen_diphone = (gen_diphone[1], gen_phone)
            word = ' '.join(gen_word)  # Assembles list of phonemes (gen_word) into string separeated by ' '.
            if not re.search(r'[AEIOU]', word):  # If generated word has no vowel, re-do this
                continue                         # iteration of for loop (generate new word).
            print(word)  # Print final word at the end of each for loop.
            break  # Breaks outer while loop to proceed to next iteration of for loop.


# Generate phonemes on a triphone (trigram) basis.
def gen_phone3(diphone, p_triph):
    rand = random.random()  # Generate random float between 0 and 1.
    for phone3 in p_triph[diphone]:  # Go through all possible triphone configurations (and probs) given diphone.
        rand -= p_triph[diphone][phone3]  # Subtract probability of given phone3 from random float.
        if rand < 0.0:  # Return 1st phone3 that brings rand below 0.
            return phone3
    return '##'


# Normalize probability distributions in master.
def normalize(master):
    for ph_dist in master.values():
        sum = 0
        for p in ph_dist.values():
            sum += p
        for ph in ph_dist:
            ph_dist[ph] /= sum


def test_perplexity_diph(master):
    test_f = open(sys.argv[3], encoding='utf-8')
    log_sum = 0
    N = 0
    for word in test_f.readlines():
        sum = 0
        word = '# ' + word.strip() + ' ##'  # Prepend '#', append '##'.
        phonemes = word.split()  # Convert line to list of phonemes.
        for i in range(len(phonemes) - 1):
            diphone = tuple(phonemes[i:i + 2])  # Create diphone (bigram) as tuple of 1st & 2nd phonemes.
            sum += math.log(master[diphone[0]][diphone[1]], 2)
        N += len(phonemes)
        log_sum += sum
        print(word.strip('#') + '\t', 2**sum)

    test_f.close()

    perplexity = 2**(log_sum*((-1)/N))
    print('\n Perplexity:\t', perplexity)


def test_perplexity_triph(master):
    test_f = open(sys.argv[3], encoding='utf-8')
    log_sum = 0
    N = 0
    for word in test_f.readlines():
        sum = 0
        word = '# ' + word.strip() + ' ##'
        phonemes = word.split()  # Convert line to list of phonemes.
        for i in range(len(phonemes) - 2):
            triphone = tuple(phonemes[i:i+3])  # Create triphone (trigram) as tuple of 1st, 2nd, & 3rd phonemes.
            sum += math.log(master[triphone[:2]][triphone[2]], 2)
        N += len(phonemes)
        log_sum += sum
        print(log_sum)
        print(N)
        print('{}\t{}'.format(word.strip('#'), 2 ** sum))

    test_f.close()

    perplexity = 2 ** (log_sum * ((-1) / N))
    print('\n Perplexity:\t{}'.format(perplexity))


def main():
    n = int(sys.argv[2])

    if len(sys.argv) > 2:
        if n == 2:
            master = di_training()  # Create dictionary of all diphones and corresponding probabilities.
            normalize(master)
            if len(sys.argv) ==3:
                di_gen(master)
            if len(sys.argv) == 4:
                test_perplexity_diph(master)
        elif n == 3:
            master = tri_training()  # Create dictionary of all triphones and corresponding probabilities.
            normalize(master)
            if len(sys.argv) ==3:
                tri_gen(master)
            elif len(sys.argv) == 4:
                test_perplexity_triph(master)
        else:
            print('Invalid argument. N must be 2 or 3.')
            sys.exit(1)
    else:
        print('Invalid arguments.')
        sys.exit(1)


if __name__ == '__main__':
    main()
