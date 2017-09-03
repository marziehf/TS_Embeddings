"""
Generate the document-word-frequency matrix, using a list of words (wordstream.txt), and a 
list of vocabs (vocab.txt)

Usage:          MakeDocword.py <wordstream> <vocab> <doc-word-freq matrix>
Stdin:          N/A
Stdout:         N/A
Other input:    wordstream.txt, vocab.txt
Other output:   docword.txt, docword.txt.empty
Author:         Jey Han Lau
Date:           Oct 10
"""

import sys
import os
import subprocess
from collections import defaultdict

if len(sys.argv) < 4:
    print "Usage: MakeDocword.py <wordstream> <vocab> <docword_output> " + \
        "[doc_label_input, doc_label_output, num_topics]"
    raise SystemExit

#global variables
wordstream_file = open(sys.argv[1], "r")
vocabs_file = open(sys.argv[2], "r")
docword_file = open(sys.argv[3], "w")
docword_empty_file = open(sys.argv[3] + ".empty", "w")
tmp_file = open(sys.argv[3] + ".tmp", "w")
doc_label_input = None
doc_label_output = None
num_topics = 0
if len(sys.argv) == 7:
    doc_label_input = open(sys.argv[4], "r")
    doc_label_output = open(sys.argv[5], "w")
    num_topics = int(sys.argv[6])
pageboundary = "<PAGEBOUNDARY>"

#process the vocabs file, generating a reverse index (word: index_number)
vocabs = {}
vocab_id = 1
for line in vocabs_file:
    vocabs[line.strip()] = vocab_id
    vocab_id += 1

#get 3 header values for docword: number of documents, number of vocabs and
#total number of vocabs in documents
num_docs = 0
num_vocabs = len(vocabs)
total_lines = 0

#get number of documents
p = subprocess.Popen("grep \"" + pageboundary + "\" "+sys.argv[1]+" | wc -l", \
    stdout=subprocess.PIPE, shell=True)
command_output = p.stdout.readlines()
if len(command_output) == 1:
    num_docs = int(command_output[0])
else:
    print "Error finding number of files in document collection"
    raise SystemExit

#process the doc label file if it exists
doc_labels = defaultdict(list)
if doc_label_input != None:
    doc_index = 1
    total_labels = 0
    for line in doc_label_input:
        labels = [ int(item) for item in line.strip().split() ]
        total_labels += len(labels)
        doc_labels[doc_index] = labels
        doc_index += 1

    #print the header for doc_label file (D,T,N)
    doc_label_output.write(str(doc_index-1) + "\n")
    doc_label_output.write(str(num_topics) + "\n")
    doc_label_output.write(str(total_labels) + "\n")

#scan through word stream and calculate the vocab frequency
#the doc-word-frequency is stored in the following structure:
#{ 1:{ 39:1, 58:2, 405:1, 500: 4 }, 2:{ 96:2, 50:3 } }
#It is dictionary of document (key) and vocab frequencies (value), with the vocab frequency
#being another dictionary of vocab (key) and frequency (value)

doc_index = 1
vocabfreq = {}
for word in wordstream_file:
    word = word.strip()
    if word == pageboundary:
        if len(vocabfreq) == 0:
            docword_empty_file.write(str(doc_index) + "\n")
        else:
            sorted_vocabfreq = sorted(vocabfreq.items())
            for freq in sorted_vocabfreq:
                tmp_file.write(str(doc_index) + " " + str(freq[0]) + " " + \
                    str(freq[1]) + "\n")

        #output the document labels if it's supervised
        if doc_label_input != None:
            for label in sorted(doc_labels[doc_index]):
                doc_label_output.write(str(doc_index) + " " + str(label) + " 1\n")

        doc_index += 1
        vocabfreq = {}
            
    else:
        if word in vocabs:
            vocab_index = vocabs[word]
            if vocab_index in vocabfreq:
                vocabfreq[vocab_index] += 1
            else:
                vocabfreq[vocab_index] = 1
                total_lines += 1

#print the 3 header values first
docword_file.write(str(num_docs) + "\n")
docword_file.write(str(num_vocabs) + "\n")
docword_file.write(str(total_lines) + "\n")

#copy the content of the tmp file and append it to the docword file
tmp_file.close()
tmp_file = open(sys.argv[3] + ".tmp")
for line in tmp_file:
    docword_file.write(line)

#remove the temporary file
os.remove(sys.argv[3] + ".tmp")
