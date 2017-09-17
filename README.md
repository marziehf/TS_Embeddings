# Topic-Sensitive Word Representations

This repository includes the codes and scripts for training topic-sensitive word embeddings proposed in [our paper](https://www.aclweb.org/anthology/P/P17/P17-2070.pdf).

![alt](https://user-images.githubusercontent.com/8711401/30002703-a936b914-90b0-11e7-94ea-209901e9bc2c.png)

## Citation

If you use this code, please cite:
```
@InProceedings{fadaee-bisazza-monz:2017:Short1,
  author    = {Fadaee, Marzieh  and  Bisazza, Arianna  and  Monz, Christof},
  title     = {Learning Topic-Sensitive Word Representations},
  booktitle = {Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)},
  month     = {July},
  year      = {2017},
  address   = {Vancouver, Canada},
  publisher = {Association for Computational Linguistics},
  pages     = {441--447},
  url       = {http://aclweb.org/anthology/P17-2070}
}
```

## Usage

### Step 0: Topic Modeling 

You'll need to learn the abstract *topics* in a collection of documents. To make it faster, this collection can be a sampled subset of the bigger collection that you'll use for training the embeddings.

```
topicmodelling/run_topicmodel.sh corpus TM_output_path
```
This script labels the words in the corpus with topics:

```
perl scripts/topic_labeling.pl corpus TM_output_path/mode-word-assignments.dat \
TM_output_path/vocabs.txt TM_output_path/docword.train.txt.empty \
EM_output_path/labeled_sample.txt
```
The output files are used to train the embeddings with the proposed models, explained in the following sections.

### HTLE / HTLEadd Model

#### Step 1: Preprocess

In order to run the Hard Topic-Labeled Representation Models (HTLE and HTLEadd) you'll need to prepare the topic-labeled corpus in the format used for the feed-forward network:

```
python topicsensitive_word2vec/scripts/extract_neighbours_htle.py \
EM_output_path/freq.txt EM_output_path/labeled_sample.txt > $EM_output_path/pairs.txt

topicsensitive_word2vec/count_and_filter -train EM_output_path/pairs.txt -cvocab EM_output_path/cv \
-wvocab EM_output_path/wv -min-count 100
```
`-wvocab` contains the word and `-cvocab` contains the context vocabulary and frequency information. Note that `-min-count` indicates the threshold for filtering out words with frequncy below this threshold. 

##### Step 2: Training the HTLE Model

To train the embeddings using the HTLE model you'll need to run this:

```
topicsensitive_word2vec/word2vecf_HTLE -train EM_output_path/pairs.txt -wvocab EM_output_path/wv \
-cvocab EM_output_path/cv -size 100 -negative 6 -threads 1 -iter 15 \
-output EM_output_path/vectors.txt -dumpcv EM_output_path/vectors.syn1neg.txt 
```
`-size` indicates the size of the embeddings, `-negative` is the size of negative sampling, and iteration is the number of iterations over the corpus you'll need.

The output is two sets of vectors: `-output` and `-dumpcv`. 

#### Step 2 alt: Training the HTLEadd Model

To train the embeddings using the HTLEadd model you'll need to run this:

```
topicsensitive_word2vec/word2vecf_HTLEadd -train EM_output_path/pairs.txt -wvocab EM_output_path/wv \
-cvocab EM_output_path/cv -size 100 -negative 6 -threads 1 -dumpcv -iter 15 \
 -output EM_output_path/vectors.txt -dumpcv EM_output_path/vectors.syn1neg.txt -dumpcv2 EM_output_path/vectors.gen.txt 
```
`-size` indicates the size of the embeddings, `-negative` is the size of negative sampling, and iteration is the number of iterations over the corpus you'll need.

The output is three sets of vectors; two topic-sensitive embeddings: `-output` and `-dumpcv`, and one generic (i.e. word) embeddings: `-dumpcv2`. 

### STLE Model

#### Step 1: Preprocess

In order to run the Soft Topic-Labeled Representation Model (STLE) you'll need to prepare the topic-labeled corpus in the format used for the feed-forward network:

```
python topicsensitive_word2vec/scripts/extract_neighbours_stle.py EM_output_path/freq.txt \
EM_output_path/labeled_sample.txt TM_output_path/topicsindocs.txt > EM_output_path/pairs.txt

topicsensitive_word2vec/count_and_filter -train EM_output_path/pairs.txt -cvocab EM_output_path/cv \
-wvocab EM_output_path/wv -min-count 100
```
`-wvocab` contains the word and `-cvocab` contains the context vocabulary and frequency information. Note that `-min-count` indicates the threshold for filtering out words with frequncy below this threshold. 


#### Step 2: Training the STLE Model

To train the embeddings using the STLE model you'll need to run this:

```
./topicsensitive_word2vec/word2vecf_STLE -train EM_output_path/pairs.txt -wvocab EM_output_path/wv \
-cvocab $EM_output_path/cv -size 100 -negative 6 -threads 1 -iter 15 \
 -output $EM_output_path/vectors.txt -dumpcv EM_output_path/vectors.syn1neg.txt 
```

## TODO
- Clean and push the inference script 

## Acknowledgments

In this work these codes are utilized:

- Jey Han Lau's [hdp-wsi](https://github.com/jhlau/hdp-wsi)
- Yoav Goldberg's [word2vecf](https://bitbucket.org/yoavgo/word2vecf/)
