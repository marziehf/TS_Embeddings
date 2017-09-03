use strict;
use IO::File;

my $c=$ARGV[0];
my $v=$ARGV[1];
my $vv=$ARGV[2];
my $emp=$ARGV[3];
my $out=$ARGV[4];

my $corpus_file = IO::File->new($c, "r");
my $assignment_file = IO::File->new($v, "r");
my $vocab_file = IO::File->new($vv, "r");
my $empty_files = IO::File->new($emp, "r");

open(FILE_OUT, ">$out") || die "File not found";
open(FILE_OUT_FREQ, ">freq.txt") || die "File not found";

my %word_doc_senses;
my %vocab_id;
my %empty_docs;
my %freq;
my $current_word_id = 1; 
while (my $line = <$vocab_file>) {
    chomp $line;
    $vocab_id{$line} = $current_word_id;
    $current_word_id = $current_word_id + 1;
}

while (my $line = <$empty_files>) {
    chomp $line;
    $empty_docs{$line} = 1;
}

my $l = <$assignment_file>;
while ($l = <$assignment_file>) {
    chomp $l;   
    my @words = split(/\s/, $l); 
    if(exists $word_doc_senses{$words[0]}{$words[1]}) {
        $word_doc_senses{$words[0]}{$words[1]} = $word_doc_senses{$words[0]}{$words[1]}."_".$words[2];
    }
    else {
        $word_doc_senses{$words[0]}{$words[1]} = $words[2];
    }
}

my $corpus_current_doc_id = 0;
my $counter = 0;

while (my $line = <$corpus_file>) {
    chomp $line;
    if(exists $empty_docs{$corpus_current_doc_id}) {
        print FILE_OUT "$line";
    }
    else {
        my @words = split(/\s/, $line);
        foreach (@words) {
            my $word = $_;
            if(exists $vocab_id{$word}) {
                my $word_id = $vocab_id{$word};
                my $senses = $word_doc_senses{$counter}{$word_id};
                my @each_sense = split("_", $senses);
# assign max topic to the word
#                my(%count); 
#               foreach my $value (@each_sense) {     
#                   $count{$value}++; 
#               } 
#               my $max_value = (sort {$count{$b} <=> $count{$a}} @each_sense)[0];

# sample from topics
                my $currentlabel = $each_sense[rand @each_sense];
                my $newtoken = $word."___".$currentlabel;
                print FILE_OUT "$newtoken ";
                if(exists $freq{$newtoken}) {
                    $freq{$newtoken} = $freq{$newtoken} + 1;
                }
                else {
                    $freq{$newtoken} = 1;
                }
            }
            else {
                print FILE_OUT "$word ";
                 if(exists $freq{$word}) {
                    $freq{$word} = $freq{$word} + 1;
                 }
                 else {
                    $freq{$word} = 1;
                 }
            }
        }
        $counter = $counter + 1;
    }
    $corpus_current_doc_id = $corpus_current_doc_id + 1;
    print FILE_OUT "\n";
}

foreach my $key (sort { $freq{$b} <=> $freq{$a} } keys(%freq)) {
    print FILE_OUT_FREQ "$key $freq{$key}\n";
}

close($corpus_file);
close($vocab_file);
close($assignment_file);
