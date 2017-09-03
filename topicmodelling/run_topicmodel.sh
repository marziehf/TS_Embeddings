#!/bin/bash

#hdp parameters
gamma_b=0.1
alpha_b=1.0
#topic model output directory
output_dir=$2
#minimum vocab frequency to filter
voc_minfreq=10
#corpus
input_txt=$1
######
#main#
######

#create generated folder if it hasn't been created
if ! [ -d $output_dir ]
then
    mkdir $output_dir
fi

#generate word stream
python MakeWordStream.py $input_txt $output_dir 0

#generate vocabulary
python MakeVocab.py $output_dir/wordstream.train.txt $output_dir $voc_minfreq

#generate docword
python MakeDocword.py "$output_dir/wordstream.train.txt" \
    "$output_dir/vocabs.txt" "$output_dir/docword.train.txt"

#run hdp
#compile the code
cd hdp
make
cd ..

#convert docword to hdp's data format
python ConvertToHDPDataFormat.py < $output_dir/docword.train.txt > \
    $output_dir/hdpdata.train.txt
#run the topic model
./hdp/hdp --algorithm train --data $output_dir/hdpdata.train.txt --directory $output_dir \
    --max_iter 300 --save_lag -1 --gamma_b $gamma_b --alpha_b $alpha_b

#print the topic/sense distribution for each document
python CalcHDPTopics.py -1 $output_dir/mode-word-assignments.dat \
    $output_dir/docword.train.txt.empty > $output_dir/topicsindocs.txt

#print the induced topics/senses
#./hdp/print.topics.R $output_dir/mode-topics.dat $output_dir/vocabs.txt \
#   $output_dir/topics.txt 10
#python hdp/ConvertTopicDisplayFormat.py < $output_dir/topics.txt > \
#   $output_dir/topics.txt.tmp
#mv $output_dir/topics.txt.tmp $output_dir/topics.txt
 
#create the topic-word-probability pickle
#python hdp/CreateTopicWordProbPickle.py $output_dir/mode-topics.dat \
#   $output_dir/vocabs.txt $output_dir/topics.pickle
