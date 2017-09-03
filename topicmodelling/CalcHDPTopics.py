"""
Calculate the document-topic proportion using the output from hdp_lda (mode-word-assignments.dat)

Usage:          CalcHDPTopics.py <target_word> mode-word-assignments.dat docwords.txt.empty >
                topicsindocs.txt
Stdin:          N/A
Stdout:         topicsindocs.txt
Other Input:    mode-word-assignments.dat, docwords.txt.empty
Other Output:   N/A
Author:         Jey Han Lau
Date:           Jul 11
"""


import sys
import operator

target_word = -1
#if target_word (in word id) is given, use the topic (s) of the target_word instead
if len(sys.argv) != 4:
    print "CalcHDPTopics.py <target_word (-1 if no target word)> mode-word-assignments.dat " + \
        "docwords.txt.empty"
    raise SystemExit

#input
target_word = int(sys.argv[1])
topicdoc_file = open(sys.argv[2])
emptydoc_file = open(sys.argv[3])

#global variables
doc_topics = {} #doc_topics[doc_id][topic_id] = count
doc_tw_topics = {} #target word topics, doc_tw_topics[doc_id][topic_id] = count
empty_docs = []

def get_true_doc_id(n, values):
    doc_id = int(n) + 1
    for value in values:
        if doc_id >= value:
            doc_id += 1
        else:
            break

    return doc_id

######
#main#
######

#get the list of empty documents
for line in emptydoc_file:
    empty_docs.append(int(line.strip()))
empty_docs = sorted(empty_docs)

#topics in a document
topics = {}
tw_topics = {} #topics of the target word
doc_id = 0
line_id = 0
for line in topicdoc_file:
    if line_id > 0:
        data = line.strip().split()
        new_doc_id = get_true_doc_id(data[0], empty_docs)
        if (doc_id != 0) and (doc_id != new_doc_id):
            doc_topics[doc_id] = topics
            doc_tw_topics[doc_id] = tw_topics

            #reset the topics in a document (and the target word's)
            topics = {}
            tw_topics = {}

        #get the doc and topic id
        doc_id = new_doc_id
        word_id = int(data[1])
        topic_id = int(data[2])

        #increment the count for topic_id (initialize topic_id in topics if it's not found)
        if topic_id not in topics:
            topics[topic_id] = 0
        topics[topic_id] += 1

        #add the topic to the target word's list of topics if word id matches
        if word_id == target_word:
            if topic_id not in tw_topics:
                tw_topics[topic_id] = 0
            tw_topics[topic_id] += 1
            
    line_id += 1

#add the last document's topics
if len(topics) > 0:
    doc_topics[doc_id] = topics
    doc_tw_topics[doc_id] = tw_topics

#print the doc-topic proportion to stdout
prev_doc_id = 0
for [doc_id, topics_in_doc] in sorted(doc_topics.items()):

    for diff in range(1, doc_id - prev_doc_id):
        if ((prev_doc_id+diff) != 0):
            print "<doc " + str(prev_doc_id + diff) + ">"

    print "<doc " + str(doc_id) + ">",

    topics_count = topics_in_doc
    #use target word's topic proportions if there are topics recorded for it
    if len(doc_tw_topics[doc_id]) > 0:
        topics_count = doc_tw_topics[doc_id]

    #get the total number of topic counts
    total_count = sum(topics_count.values())
    for [topic_id, count] in sorted(topics_count.items(), key=operator.itemgetter(1), \
        reverse=True):
        print "t." + str(topic_id+1) + "/%.4f" % (float(count)/total_count),
    print

    prev_doc_id = doc_id

if len(empty_docs) > 0:
    if empty_docs[-1] > prev_doc_id:
        for i in range(0, (empty_docs[-1]-prev_doc_id)):
            print "<doc " + str(prev_doc_id+i+1) + ">"
