#!/bin/bash

corpus="./sample.txt"
TM_output_path="./TM"
EM_output_path="./Embeddings"

# learn topics from the corpus
./topicmodelling/run_topicmodel.sh $corpus $TM_output_path

# label corpus with topics
perl ./scripts/topic_labeling.pl $corpus $TM_output_path/mode-word-assignments.dat $TM_output_path/vocabs.txt $TM_output_path/docword.train.txt.empty $EM_output_path/labeled_sample.txt

# prepare for embedding training
python ./topicsensitive_word2vec/scripts/extract_neighbours_htle.py $EM_output_path/freq.txt $EM_output_path/labeled_sample.txt > $EM_output_path/pairs.txt
./topicsensitive_word2vec/count_and_filter -train $EM_output_path/pairs.txt -cvocab $EM_output_path/cv -wvocab $EM_output_path/wv -min-count 100

# train embeddings: HTLE
./topicsensitive_word2vec/word2vecf_HTLE -train $EM_output_path/pairs.txt -wvocab $EM_output_path/wv -cvocab $EM_output_path/cv -output $EM_output_path/vectors.txt -size 100 -negative 6 -threads 1 -dumpcv $EM_output_path/vectors.syn1neg.txt -iter 15

# train embeddings: HTLEadd
./topicsensitive_word2vec/word2vecf_HTLEadd -train $EM_output_path/pairs.txt -wvocab $EM_output_path/wv -cvocab $EM_output_path/cv -output $EM_output_path/vectors.txt -size 100 -negative 6 -threads 1 -dumpcv $EM_output_path/vectors.syn1neg.txt -dumpcv2 $EM_output_path/vectors.gen.txt  -iter 15

# train embeddings: STLE
python ./topicsensitive_word2vec/scripts/extract_neighbours_stle.py $EM_output_path/freq.txt $EM_output_path/labeled_sample.txt $TM_output_path/topicsindocs.txt > $EM_output_path/pairs.txt
./topicsensitive_word2vec/count_and_filter -train $EM_output_path/pairs.txt -cvocab $EM_output_path/cv -wvocab $EM_output_path/wv -min-count 100
./topicsensitive_word2vec/word2vecf_STLE -train $EM_output_path/pairs.txt -wvocab $EM_output_path/wv -cvocab $EM_output_path/cv -output $EM_output_path/vectors.txt -size 100 -negative 6 -threads 1 -dumpcv $EM_output_path/vectors.syn1neg.txt -iter 15

# inference


