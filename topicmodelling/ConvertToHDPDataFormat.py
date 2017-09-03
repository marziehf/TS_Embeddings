"""
Convert our docword file to hdp_lda's data format:
<num unique vocabs> <term id>:<term count> ...

Usage:          ConvertToHDPDataFormat.py < docword > hdpdata.txt
Stdin:          docword
Stdout:         hdpdata.txt
Other Input:    N/A
Other Output:   N/A
Author:         Jey Han Lau
Date:           Jul 11
"""


import sys

#parse the docword file and convert it to HDP's data format
line_id = 0
doc_id = 0
doc_terms = {}
for line in sys.stdin:
    if line_id > 2:
        data = line.strip().split()
        term_id = int(data[1])
        count = int(data[2])

        #new document
        if (int(data[0]) != doc_id):
            if (len(doc_terms) > 0):
                #print out the terms in HDP data format
                print len(doc_terms),
                for term, count in doc_terms.items():
                    print term + ":" + str(count),
                print

            doc_id = int(data[0])
            doc_terms = {}

        doc_terms[str(term_id)] = count

    #increment line_id
    line_id += 1

#end of docword, print out the terms of last document
print len(doc_terms),
for term, count in doc_terms.items():
    print term + ":" + str(count),
