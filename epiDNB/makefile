# clean:
# 	rm -f *.o a.out *~ *.trifile

# EMTRAIN=gmtkEMtrain

clean:
	rm -f *.o a.out *~

clean_parse:
	@rm -f parse *.o a.out *~

all_clean:
	rm -f *.o a.out *~ parse init_trigram_pmfs

parse: clean_parse
	gcc -o parse parse.c parser.c

parse_peptides: parse
	./parse riptide_peptides.txt peptides.txt pep_count.txt

triangulate_trigram:
	gmtkTriangulate -str trigram.str [-verb 100]

trigram_pmfs:
	gcc -o init_trigram_pmfs init_trigram_distr.c

init_trigram: trigram_pmfs
	./init_trigram_pmfs
	rm init_trigram_pmfs

train_trigram:
	./train_cmd.sh > gmtk_train_out.txt

parse2: clean_parse
	gcc -o parse2 test_parse.c parser.c

parse_test_peps: parse2
	./parse2 test_peptides.txt test_peps.txt test_peps_count.txt

test_trigram:
	./test_cmd.sh > gmtk_test_out.txt

run_trigram: triangulate_trigram train_trigram test_trigram
