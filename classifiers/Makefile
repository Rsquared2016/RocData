model_bin = $(model_dir)/svm_bin
model_dat = $(model_dir)/svm_data
model_mod = $(model_dir)/svm_model
model_dir = SVMs/$(model)

all: train

train: 
	mkdir -p $(model_bin) $(model_mod) $(model_dat)
	
	# Process training data and create a .words file
	@echo "\n Processing training data ..."
	python -OO src/createTrainingDataSVM.py $(model_dir)/training_data.txt 1
	
	# Learn SVM
	@echo "\n Learning SVM ..."
	# I have no idea what these parameters are.	
	# svm_perf_learn -w 3 -c 16.533 -l 10 --b 1 -t 0 -p 1 training_data.dat svm
	svm_perf/svm_perf_learn -w 3 -c 754 -l 10 --b 1 -t 0 -p 1 $(model_mod)/training_data.dat $(model_bin)/svm
	
	@echo "\n SVM features:"
	python src/inspect_SVM.py $(model_mod)/training_data.words $(model_bin)/svm
	
	# Process testing data
	@echo "\n Processing testing data ..."
	python -OO src/createTestingDataSVM.py $(model_dir)/nyc.trim.sort $(model_mod)/training_data.words
	
	# Classify testing data
	@echo "\n Classifying ..."
	svm_perf/svm_perf_classify -v 0 $(model_mod)/testing_data.dat $(model_bin)/svm $(model_bin)/predictions_svm
	
	# Interpret results
	@echo "\n Classification results:"
	python -OO src/interpret_results.py $(model_bin)/predictions_svm $(model_dir)/nyc.trim.sort 0.8
	
	@echo "\n Joined lines:"
	paste $(model_bin)/predictions_svm $(model_mod)/testing_data.dat | head

svm_perf:
	mkdir -p ../svm_perf/
	wget http://download.joachims.org/svm_perf/current/svm_perf.tar.gz
	mv svm_perf.tar.gz ../svm_perf/
	cd ../svm_perf/ && gunzip  svm_perf.tar.gz &&  tar xvf svm_perf.tar  && make && rm *.tar

clean:
		rm -rf *.pyo $(model_bin) svm_model
