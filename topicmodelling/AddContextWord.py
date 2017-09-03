"""
Add left and right 3 neighbour words of a target word to the wordstream.

Usage:          AddContextWord.py <target_word> < wordstream.txt > modified_wordstream.txt
Stdin:          wordstream.txt
Stdout:         modified_wordstream.txt
Other Input:    N/A
Other Output:   N/A
Author:         Jey Han Lau
Date:           Jul 11
"""

import sys

if len(sys.argv) != 2:
    print "Usage: AddContextWord.py <target_word> < wordstream.txt > modified_wordstream.txt"
    raise SystemExit

#get the target word
target_word = sys.argv[1]

#constants
pageboundary = "<PAGEBOUNDARY>"

words_in_doc = [] #list of words in one document
target_word_pos = [] #list of positions of the target word in one document
word_pos = 0 #current word position in a document
doc_id = 1
for line in sys.stdin:
    word = line.strip()

    if word == pageboundary:
        #print context word
        for pos in target_word_pos:
            for i in range(1, 4):
                #left i'th neighbour
                if (pos-i) >= 0:
                    if words_in_doc[pos-i].count("#") != 2:
                        print words_in_doc[pos-i] + "_#" + str(-1*i)

                #right i'th neghbour
                if (pos+i) < word_pos:
                    if words_in_doc[pos+i].count("#") != 2:
                        print words_in_doc[pos+i] + "_#" + str(i)

        if len(target_word_pos) == 0:
            sys.stderr.write("WARNING: Target word <<" + target_word + ">> not found in "
                "document id = " + str(doc_id) + ".\n")

        words_in_doc = []
        target_word_pos = []
        word_pos = 0
        doc_id += 1
    else:
        words_in_doc.append(word)
        if word == target_word:
            target_word_pos.append(word_pos)

        word_pos += 1

    print word



