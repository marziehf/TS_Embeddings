CC = gcc
#The -Ofast might not work with older versions of gcc; in that case, use -O2
#CFLAGS = -lm -pthread -Ofast -march=native -Wall -funroll-loops -Wno-unused-result
CFLAGS = -lm -pthread -O3 -march=native -Wall -funroll-loops -Wno-unused-result

all: word2vecf_HTLE word2vecf_HTLEadd word2vecf_STLE batch_distance count_and_filter

word2vecf_HTLE : word2vecf_HTLE.c vocab.c io.c
	$(CC) word2vecf_HTLE.c vocab.c io.c -o word2vecf_HTLE $(CFLAGS)
word2vecf_HTLEadd : word2vecf_HTLEadd.c
	$(CC) word2vecf_HTLEadd.c vocab.c io.c -o word2vecf_HTLEadd $(CFLAGS)
word2vecf_STLE : word2vecf_STLE.c
	$(CC) word2vecf_STLE.c vocab.c io.c -o word2vecf_STLE $(CFLAGS)
batch_distance : batch_distance.c
	$(CC) batch_distance.c -o batch_distance $(CFLAGS)
count_and_filter: count_and_filter.c vocab.c io.c
	$(CC) vocab.c count_and_filter.c io.c -o count_and_filter $(CFLAGS)
