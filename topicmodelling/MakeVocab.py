"""
Create a list of vocabs (unique words) from a list of words (wordstream)
Also outputs the frequency of words to freqwords.txt

Usage:          Makevocab.py <wordstream> <output dir> <freq_threshold> [ascii,symbol (filters)]
Stdin:          N/A
Stdout:         N/A
Other input:    wordstream
Other output:   vocabs, freqwords.txt
Author:         Jey Han Lau
Date:           Oct 10
"""

import sys
from operator import itemgetter

if len(sys.argv) < 4:
    print "Usage: Makevocab.py <wordstream> <output dir> <freq_threshold> [ascii,symbol (filters)]"
    raise SystemExit

#parameters
min_threshold = int(sys.argv[3]) #any vocabs with count <= min_threshold is removed
pageboundary = "<PAGEBOUNDARY>"
filter_ascii = False
filter_symbol = False
if len(sys.argv) == 5:
    options = sys.argv[4].split(",")
    for option in options:
        if option == "ascii":
            filter_ascii = True
        if option == "symbol":
            filter_symbol = True
    
wordstream_file = open(sys.argv[1])
vocabs_file = open(sys.argv[2] + "/vocabs.txt", "w")
wordfreq_file = open(sys.argv[2] + "/freqwords.txt", "w")

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def contain_symbol(s):
    symbols = set(["!", "@", "#", "*", "(", ")", "_", "+", "=", "[", "]", "{", "}", "|", "\\", \
        ":", ";", "<", ">", "/"])

    for symbol in symbols:
        if symbol in s:
            return True

    return False
        

######
#main#
######

#scan through word stream
wordfreq = {}
for word in wordstream_file:
    #remove trailing white spaces
    word = word.strip()
    if word != pageboundary:
        if word in wordfreq:
            wordfreq[word] += 1
        else:
            wordfreq[word] = 1

#filter vocabs that occur less than a defined minimum value
for word in wordfreq.keys():
    if (wordfreq[word] <= min_threshold) or (filter_ascii and (not is_ascii(word))) or \
        (filter_symbol and contain_symbol(word)):
        del wordfreq[word]

#print the vocabs (vocab.txt), sorted alphabetically
for word in sorted(wordfreq.items()):
    vocabs_file.write(word[0] + "\n")

#print the vocab frequency
sorted_wordfreq = sorted(wordfreq.items(), key=itemgetter(1), reverse=True)
for word in sorted_wordfreq:
    wordfreq_file.write(str(word[1]).rjust(9) + " " + word[0] + "\n")
