all: train

train: svm_perf
	mkdir -p svm_bin svm_model
	
	# Process training data and create a .words file
	@echo "\n Processing training data ..."
	python -OO src/createTrainingDataSVM.py svm_data/training_data.txt 1
	
	# Learn SVM
	@echo "\n Learning SVM ..."
	# I have no idea what these parameters are.	
	# svm_perf_learn -w 3 -c 16.533 -l 10 --b 1 -t 0 -p 1 training_data.dat svm
	svm_perf/svm_perf_learn -w 3 -c 754 -l 10 --b 1 -t 0 -p 1 svm_model/training_data.dat svm_bin/svm
	
	@echo "\n SVM features:"
	python src/inspect_SVM.py svm_model/training_data.words svm_bin/svm
	
	# Process testing data
	@echo "\n Processing testing data ..."
	python -OO src/createTestingDataSVM.py ../nyc.trim.sort svm_model/training_data.words
	
	# Classify testing data
	@echo "\n Classifying ..."
	svm_perf/svm_perf_classify -v 0 svm_model/testing_data.dat svm_bin/svm svm_bin/predictions_svm
	
	# Interpret results
	@echo "\n Classification results:"
	python -OO src/interpret_results.py svm_bin/predictions_svm ../nyc.trim.sort 0.8
	
	@echo "\n Joined lines:"
	paste predictions_svm svm_model/testing_data.dat | head

svm_perf:
	mkdir -p ../svm_perf/
	wget http://download.joachims.org/svm_perf/current/svm_perf.tar.gz
	mv svm_perf.tar.gz ../svm_perf/
	cd ../svm_perf/ && gunzip  svm_perf.tar.gz &&  tar xvf svm_perf.tar  && make && rm *.tar

clean:
		rm -rf *.pyo svm_bin svm_model
