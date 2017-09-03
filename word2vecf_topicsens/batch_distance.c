//
// Modified by Marzieh Fadaee, Aug 2017
// Added:
//    - support for batch distance calculation
//
/////////////////////////////////////////////////////////////////
//
//  Copyright 2013 Google Inc. All Rights Reserved.
//
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.

#include <stdio.h>
#include <string.h>
#include <math.h>
#include <malloc.h>
#include <stdlib.h>
#include <assert.h>

const long long max_size = 2000;         // max length of strings
const long long N = 20;                  // number of closest words that will be shown
const long long max_w = 50;              // max length of vocabulary entries

int main(int argc, char **argv) {
    FILE *f, *f2;
    char st1[max_size];
    char *bestw[N];
    char file_name[max_size], st[100][max_size], file_name2[max_size];
    float dist, len, bestd[N], vec[max_size];
    long long words, size, a, b, c, d, cn, bi[100];
    char ch;
    float *M;
    char *vocab;
    if (argc < 2) {
        printf("Usage: ./distance <FILE>\nwhere FILE contains word projections in the BINARY FORMAT\n");
        return 0;
    }
    strcpy(file_name, argv[1]);
    strcpy(file_name2, argv[2]);
    f = fopen(file_name, "rb");
    f2 = fopen(file_name2, "r");
    if (f == NULL) {
        printf("Input file not found\n");
        return -1;
    }
    fscanf(f, "%lld", &words);
    fscanf(f, "%lld", &size);
    vocab = (char *)malloc((long long)words * max_w * sizeof(char));
    for (a = 0; a < N; a++) bestw[a] = (char *)malloc(max_size * sizeof(char));
    M = (float *)malloc((long long)words * (long long)size * sizeof(float));
    if (M == NULL) {
        printf("Cannot allocate memory: %lld MB    %lld  %lld\n", (long long)words * size * sizeof(float) / 1048576, words, size);
        return -1;
    }
    for (b = 0; b < words; b++) {
        fscanf(f, "%s%c", &vocab[b * max_w], &ch);
        //printf("%s\n",&vocab[b * max_w]);
        //char* newWordSense = strtok(&vocab[b * max_w], "___");
        //if(newWordSense != NULL) {
        //  strcpy(&vocab[b * max_w], newWordSense);
        //}
        //printf("%s\n",&vocab[b * max_w]);
        for (a = 0; a < size; a++) fread(&M[a + b * size], sizeof(float), 1, f);
        len = 0;
        for (a = 0; a < size; a++) len += M[a + b * size] * M[a + b * size];
        len = sqrt(len);
        for (a = 0; a < size; a++) M[a + b * size] /= len;
    }
    fclose(f);
    while(!feof(f2)) {
        char wword[1000];  
        int inv;
        int inv2;
        //printf("HERE \n");
        fscanf(f2, "%s", &wword);
        fscanf(f2, "%d", &inv);
        fscanf(f2, "%d", &inv2);
        printf("%s %d %d: ", wword, inv, inv2);
        // printf("Enter word or sentence (EXIT to break): ");
        int current_topic;
//        printf("%s\n", wword);
        for(current_topic=0 ; current_topic<100 ; current_topic+=1) {
            for (a = 0; a < N; a++) bestd[a] = 0;
            for (a = 0; a < N; a++) bestw[a][0] = 0;
           //create word_sense tokens
            char newWordSense[1000];
            strcpy(newWordSense, wword);
            // printf("%s\n",newWordSense);
            strcat(newWordSense, "___");
  //           printf("%s\n",newWordSense);
             char strr[1000];
             sprintf(strr, "%d", current_topic);
            strcat(newWordSense, strr);
    //         printf("%s\n",newWordSense);
            strcpy(st1, newWordSense);
    //        printf("%s: ", st1);
            int x = 0;
           for (b = 0; b < words; b++) { 
//                printf("%s ---- %s\n", &vocab[b * max_w], st1);
               if (strcmp(&vocab[b * max_w], st1) == 0) {
                   x=1;
               //    printf("%s ---- %s\n", &vocab[b * max_w], st1);
               }
           }
           if(x == 0) break;
        cn = 0;
        b = 0;
        c = 0;
        while (1) {
            st[cn][b] = st1[c];
            b++;
            c++;
            st[cn][b] = 0;
            if (st1[c] == 0) break;
            if (st1[c] == ' ') {
                cn++;
                b = 0;
                c++;
            }
        }
        cn++;
        for (a = 0; a < cn; a++) {
           if (b == words) b = -1;
            bi[a] = b;
            //printf(st[a]);
            //printf("\nWord: %s  Position in vocabulary: %lld\n", st[a], bi[a]);
            if (b == -1) {
            //    printf("Out of dictionary word!\n");
                break;
            }
        }
        if (b == -1) continue;
        //  printf("\n                                              Word       Cosine distance\n------------------------------------------------------------------------\n");
        for (a = 0; a < size; a++) vec[a] = 0;
        for (b = 0; b < cn; b++) {
            if (bi[b] == -1) continue;
            for (a = 0; a < size; a++) vec[a] += M[a + bi[b] * size];
        }
        len = 0;
        for (a = 0; a < size; a++) len += vec[a] * vec[a];
        len = sqrt(len);
        for (a = 0; a < size; a++) vec[a] /= len;
        for (a = 0; a < N; a++) bestd[a] = -1;
        for (a = 0; a < N; a++) bestw[a][0] = 0;
        for (c = 0; c < words; c++) {
            a = 0;
            for (b = 0; b < cn; b++) if (bi[b] == c) a = 1;
            if (a == 1) continue;
            dist = 0;
            for (a = 0; a < size; a++) dist += vec[a] * M[a + c * size];
            for (a = 0; a < N; a++) {
                if (dist > bestd[a]) {
                    for (d = N - 1; d > a; d--) {
                        bestd[d] = bestd[d - 1];
                        strcpy(bestw[d], bestw[d - 1]);
                    }
                    bestd[a] = dist;
                    strcpy(bestw[a], &vocab[c * max_w]);
                    break;
                }
            }
        }
        for (a = 0; a < N; a++) printf("%s ", bestw[a]);// bestd[a]);
        printf("\n");           
    }
    printf("\n");
    }
    fclose(f2);
    return 0;
}

