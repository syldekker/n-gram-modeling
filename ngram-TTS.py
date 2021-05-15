import sys
import random
import re
from collections import defaultdict
import pyttsx3


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

    for line in train_f.readlines():
        line = re.sub(u'^[a-z\']+', '#', line) + ' ##'  # Discard all orthographic word forms, append '##'.
        phonemes = line.split()  # Convert line to list of phonemes.
        for i in range(len(phonemes) - 1):
            phone_count[phonemes[i]] += 1  # Keep count of each phoneme's frequency.
            diphone = tuple(phonemes[i:i + 2])  # Create diphone (bigram) as tuple of 1st & 2nd phonemes.
            diphone_count[diphone] += 1  # Keep count of each diphone's frequency.
        phone_count['##'] += 1  # Count word final boundary, '##'.

    train_f.close()

    master_dict = defaultdict(dict)  # Create empty dictionary described above.

    for diphone in diphone_count.keys():  # P (x|x-1) (Fill that dictionary up, baby.)
        master_dict[diphone[0]][diphone[1]] = diphone_count[diphone] / phone_count[(diphone[0])]

    return master_dict


# Generate pseudo words with respect to diphone frequencies.
def di_gen(p_diph):
    speaker = pyttsx3.init()
    voices = speaker.getProperty('voices')
    speaker.setProperty('voice', voices[1].id)
    speaker.setProperty('rate', 140)
    for i in range(25):
        while True:  # This loop ensures that only words of a sufficient length and composition will be printed.
            gen_phone = ''
            gen_word = []
            while gen_phone != '##':  # Phonemes are added until '##' is generated.
                gen_word.append(gen_phone)  # Adds generated phoneme to word being generated (1st addition is '').
                if gen_phone == '':
                    gen_phone = '#'
                gen_phone = gen_phone2(gen_phone, p_diph)  # 2nd half of diphone returned.
            word = ' '.join(gen_word)  # Assembles list of phonemes (gen_word) into string separeated by ' '.
            if not re.search(r'[AEIOU]', word):  # If generated word has no vowel, re-do this
                continue                         # iteration of for loop (generate new word).
            print(word)  # Print final word at the end of each for loop.
            gen_word = (''.join(gen_word)).lower()
            speaker.say(gen_word)
            print(gen_word)
            speaker.runAndWait()
            break  # Breaks outer while loop to proceed to next iteration of for loop.


# Generate phonemes on a diphone (bigram) basis.
def gen_phone2(phone1, p_diph):
    rand = random.random()  # Generate random float between 0 and 1.
    for phone2 in p_diph[phone1]:  # Go through all possible diphone configurations (and probs) given phone1.
        rand -= p_diph[phone1][phone2]  # Subtract probability of given phone2 from random float.
        if rand < 0.0:  # Return 1st phone2 that brings rand below 0.
            return phone2
    return '#'


# Reads in 'word_transcriptions.txt' and returns triphone dictionary of items containing each
# first diphone paired with all possible third phones and their corresponding probabilities.
def tri_training():
    diphone_count = defaultdict(lambda: 0)
    triphone_count = defaultdict(lambda: 0)
    train_f = open(sys.argv[1], encoding='utf-8')

    for line in train_f.readlines():
        line = re.sub(u'^[a-z\']+', '#', line) + ' ##'  # Discard all orthographic word forms, append '##'.
        phonemes = line.split()  # Convert line to list of phonemes.
        for i in range(len(phonemes) - 2):
            diphone = tuple(phonemes[i:i+2])
            diphone_count[diphone] += 1  # Keep count of each diphone's frequency.
            triphone = tuple(phonemes[i:i+3])  # Create triphone (trigram) as tuple of 1st, 2nd, & 3rd phonemes.
            if triphone == ('#', 'NG', 'L'):
                print(phonemes)
                breakpoint()
            triphone_count[triphone] += 1  # Keep count of each triphone's frequency.
        diphone_count[(phonemes[-2], '##')] += 1  # Count word final boundary, '##'.

    train_f.close()

    master_dict = defaultdict(dict)  # Create empty dictionary described above.

    for triphone in triphone_count.keys():  # P (x|x-1) (Fill that dictionary up, baby.)
        master_dict[triphone[:2]][triphone[2]] = triphone_count[triphone] / diphone_count[(triphone[:2])]

    return master_dict


# Generate pseudo words with respect to triphone frequencies.
def tri_gen(p_triph):
    speaker = pyttsx3.init()
    voices = speaker.getProperty('voices')
    speaker.setProperty('voice', voices[1].id)
    speaker.setProperty('rate', 140)
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
                gen_phone = gen_triphone3(gen_diphone, p_triph)  # 2nd half of diphone returned.
                gen_diphone = (gen_diphone[1], gen_phone)
            word = ' '.join(gen_word)  # Assembles list of phonemes (gen_word) into string separeated by ' '.
            if not re.search(r'[AEIOU]', word):  # If generated word has no vowel, re-do this
                continue                         # iteration of for loop (generate new word).
            print(word)  # Print final word at the end of each for loop.
            gen_word = (''.join(gen_word)).lower()
            speaker.say(gen_word)
            print(gen_word)
            speaker.runAndWait()
            break  # Breaks outer while loop to proceed to next iteration of for loop.


# Generate phonemes on a triphone (trigram) basis.
def gen_triphone3(diphone, p_triph):
    rand = random.random()  # Generate random float between 0 and 1.
    for phone3 in p_triph[diphone]:  # Go through all possible triphone configurations (and probs) given diphone.
        rand -= p_triph[diphone][phone3]  # Subtract probability of given phone3 from random float.
        if rand < 0.0:  # Return 1st phone3 that brings rand below 0.
            return phone3
    return '##'


def main():
    n = int(sys.argv[2])

    if n == 2:
        master = di_training()  # Create dictionary of all diphones and corresponding probabilities.
        di_gen(master)
    elif n == 3:
        master = tri_training()  # Create dictionary of all triphones and corresponding probabilities.
        tri_gen(master)
    else:
        print('Invalid argument.')


if __name__ == '__main__':
    main()
