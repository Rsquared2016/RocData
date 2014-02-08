### Process training data and create WORDS file
echo "Processing training data ..."
python -OO createTrainingDataSVM.py training_data.txt 1 &&

### Learn SVM
echo
echo "Learning SVM ..."
#svm_perf_learn -w 3 -c 16.533 -l 10 --b 1 -t 0 -p 1 training_data.dat svm &&
svm_perf_learn -w 3 -c 754 -l 10 --b 1 -t 0 -p 1 training_data.dat svm &&

echo
echo "SVM features:"
python inspect_SVM.py WORDS_training_data svm &&

### Process testing data
echo
echo "Processing testing data ..."
python -OO createTestingDataSVM.py ../nyc.trim.sort WORDS_training_data &&

### Classify testing data
echo
echo "Classifying ..."
svm_perf_classify -v 0 testing_data.dat svm predictions_svm &&

### Interpret results
echo
echo "Classification results:"
python -OO interpret_results.py predictions_svm ../nyc.trim.sort 0.8 &&

echo
echo "Joined lines:"
paste predictions_svm testing_data.dat | head