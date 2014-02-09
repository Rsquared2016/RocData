all: train

train: 
	mkdir -p svm_bin svm_model
	
	### Process training data and create WOR`:DS file
	echo "Processing training data ..."
	python -OO createTrainingDataSVM.py svm_data/training_data.txt 1 &&
	echo "Processing training data ..."
	
	#Learn SVM
	echo
	echo "Learning SVM ..."
	# I have no idea what these parameters are.	
	#svm_perf_learn -w 3 -c 16.533 -l 10 --b 1 -t 0 -p 1 training_data.dat svm &&
	svm_perf_learn -w 3 -c 754 -l 10 --b 1 -t 0 -p 1 svm_model/training_data.dat svm_bin/svm &&
	
	echo
	echo "SVM features:"
	python inspect_SVM.py svm_model/training_data.words svm_bin/svm &&
	
	### Process testing data
	echo
	echo "Processing testing data ..."
	python -OO createTestingDataSVM.py ../nyc.trim.sort svm_model/training_data.words &&
	
	### Classify testing data
	echo
	echo "Classifying ..."
	svm_perf_classify -v 0 svm_model/testing_data.dat svm_bin/svm svm_bin/predictions_svm &&
	
	### Interpret results
	echo
	echo "Classification results:"
	python -OO interpret_results.py svm_bin/predictions_svm ../nyc.trim.sort 0.8 &&
	
	echo
	echo "Joined lines:"
	paste predictions_svm svm_model/testing_data.dat | head

clean:
		rm -rf *.pyo svm_bin svm_model
