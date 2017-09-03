"""
Create a stream of words for a text collection file (different file is separated 
by a designated page boundary symbol). 2 text files created, one for training 
and one for testing.
Default page boundary symbol = <PAGEBOUNDARY>
Parameter <num_test> controls how many test documents to be generated:
-1         = 10% docs as test docs
0          = no test docs
non-zero N = top-N as test docs

Usage:          Makewordstream.py <text_input_file> <wordstream_output_dir> <num_test> [colloc_file]
Stdin:          N/A
Stdout:         N/A
Other Input:    text collection input (separated by page boundary),
                stopwords.txt, includewords.txt
Other Output:   wordstream.train.txt, wordstream.test.txt
Author:         Jey Han Lau
Date:           Oct 10
"""

import sys
import codecs
import subprocess
import random
import os.path
import math

#parameters
debug = False
word_len_threshold = 2

if (len(sys.argv) != 4) and (len(sys.argv) != 5):
    print "Usage: Makewordstream.py <text_input_file> <wordstream_output_dir> <num_test> " + \
        "[colloc_file]"
    raise SystemExit

#global variables
pageboundary = "<PAGEBOUNDARY>"
text_input = open(sys.argv[1])
wordstream_train = open(sys.argv[2] + "/wordstream.train.txt", "w")
num_test = int(sys.argv[3]) #number of test documents to generate
if num_test != 0:
    wordstream_test = open(sys.argv[2] + "/wordstream.test.txt", "w")
replace_colloc = False
if (len(sys.argv) == 5):
    replace_colloc = True
    bigram_file = open(sys.argv[4])
stopwords = []
test_docs = []
include_words = [] #select only words from includewords.txt

def clean_token(token):
    return token.strip(",").strip(".").strip("'").strip("\"")

######
#main#
######

#first process the stopword file
for line in open("stopwords.txt").readlines():
    stopwords.append(line.strip())
#convert stopwords to a set (faster processing)
stopwords = set(stopwords)
if debug:
    print "Stopwords =", stopwords

#process the 'includewords' file
if os.path.isfile("includewords.txt"):
    for line in open("includewords.txt"):
        include_words.append(line.strip())
include_words = set(include_words)
if debug:
    print "Select only words from =", include_words

#if replace collocation, get the set of collocations
if replace_colloc:
    colloc = set([])
    for line in bigram_file:
        colloc.add(line.strip())

#first find out how many files in the document collection. Take a random 10%
#to be the test documents
num_docs = 0
p = subprocess.Popen("wc -l " + sys.argv[1], stdout=subprocess.PIPE, shell=True)
command_output = p.stdout.readlines()
if len(command_output) == 1:
    num_docs = int(command_output[0].split()[0])
else:
    print "Error finding number of files in document collection"
    raise SystemExit

test_docs = []
if num_test != 0:
    #generate top-N docs as test
    if num_test > 0:
        test_docs = range(0, num_test)
    #generate 10% of the docs to be test
    else:
        #deterministic way
        num_test_docs = 1 #at least 1 test doc
        if (num_docs/10) > 1:
            num_test_docs = num_docs/10

        interval = float(num_docs)/float(num_test_docs)
        i = 0
        while len(test_docs) < num_test_docs:
            test_docs.append(int(round(float(i)*interval)))
            i += 1
        #random
    #    num_list = range(0, num_docs)
    #    random.shuffle(num_list)
    #    test_docs = num_list[0:(num_docs/10)]

    if debug:
        print "\nTest docs (", len(test_docs), ") =", test_docs

doc_id = 0
for line in text_input:
    #first check to see which wordstream file to output
    if doc_id in test_docs:
        output_file = wordstream_test
    else:
        output_file = wordstream_train

    tokens = line.split()
    #tokens = line.strip()
    #tokens = [tokens]
    ignore_token = False
    for i in range(0, len(tokens)):
        token = tokens[i]

        #ignore this word (because it's used as a collocation with the previous word)
        if ignore_token:
            ignore_token = False
        else:
            #if replace collocation, check if it forms a collocation with the next word
            if replace_colloc and (i+1 < len(tokens)) and \
                ((tokens[i] + " " + tokens[i+1]) in colloc):
                token = tokens[i] + "_" + tokens[i+1]
                ignore_token = True
                
            #remove words of length <= word_len_threshold and stopwords
            if (len(token) > word_len_threshold) and (token not in stopwords) \
                and (token != "-rrb-") and (token != "-lrb-") and \
                (len(include_words) == 0 or token in include_words):
                if (i>0) and (tokens[i-1]) == "#":
                    token = tokens[i-1] + token

                #token_length = len(token.decode("utf-8"))
                #token_length = len(token)

                #if ((max_token_length == 0) or (token_length <= max_token_length)):
                output_file.write(token + "\n")
                #else:
                #    for char in token.decode("utf-8"):
                #        if len(char.encode("utf-8")) > 1:
                #            output_file.write(char.encode("utf-8") + "\n")

    #write pageboundary at end of document
    output_file.write(pageboundary + "\n")

    doc_id += 1
