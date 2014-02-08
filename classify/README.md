Building a Classifier
=======================================

This guide should help you train a classifier, run it against a data set and output labels.
Data files in this tutorial are placed in `data/`.


#Prerequisites
For this you'll need the svm perf library. The documentation for it is [here](http://www.cs.cornell.edu/people/tj/svm_light/svm_perf.html)
We are going to use `svm_perf_learn` and `svm_perf_classify` from this library.


# Training
The hardest part in training a classifier is obtaining the training set.

For the flu model, we have created a text file of training data located at `data/training_data.txt`. 
This is a simple text file, where each line is comprised of the following : 
```
# a tweet id | tweet text
22690177204    no A Kite in the sky ! Alone n alone ! Have no one to share the pain
```

# Testing
Your test file should be comprised of json objects representing tweets. 

```json
{"id":"6f3acc1e75c817417f118d44596f33f6","key":"6f3acc1e75c817417f118d44596f33f6","value":{"rev":"1-e1e70bd847ff3a38f0bcc69da542cab8"},"doc":{"_id":"6f3acc1e75c817417f118d44596f33f6","_rev":"1-e1e70bd847ff3a38f0bcc69da542cab8","iso_language_code":"en","text":"@Layce305 bless my people","created_at":"Wed, 19 May 2010 00:40:00 +0000","lon":-73.918209000000004494,"profile_image_url":"http://a3.twimg.com/profile_images/317812083/n1294582050_215_normal.jpg","to_user":"Layce305","source":"&lt;a href=&quot;http://ubertwitter.com&quot; rel=&quot;nofollow&quot;&gt;UberTwitter&lt;/a&gt;","health":-0.10548193000000000152,"location":"ÜT: 40.664879,-73.918209","from_user":"kingraspedro","lat":40.66487899999999911,"from_user_id":16789049,"to_user_id":1542507,"geo":null,"id":14261124214,"metadata":{"result_type":"recent"}}}
```


All the necessary files are located at `/p/twitter/SadilekAll/TwitterHealth2.0/SVM-starter-code`
```
    # This is the input for creatTrainingDataSVM.py
    training_data.txt  
  
    # Outputs train.dat file, where each line contains tweet's class, representation of a tweet in the feature space defined by the presence of a token word, #, and the name of the class
    # Outputs WORDS_sys.argv[1] file with all the unique tokens that appear in the training data
    python -OO createTrainingDataSVM.py training_data.txt 1
  
    inspect_SVM.py  

    # contains json objects to create testing data for SVM
    test_file 
    
    # createTestingDataSVM.py creates testing_data.dat
    python -OO createTestingDataSVM.py ../test_file WORDS_training_data

    # interpret_results.py 
    python -OO interpret_results.py predictions_svm ../nyc.trim.sort 0.8
```


```bash
# run.sh

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
python -OO createTestingDataSVM.py ../test_file WORDS_training_data &&

### Classify testing data
echo
echo "Classifying ..."
svm_perf_classify -v 0 testing_data.dat svm predictions_svm &&

### Interpret results
echo
echo "Classification results:"
python -OO interpret_results.py predictions_svm ../test_file 0.8 &&

```

echo
echo "Joined lines:"
paste predictions_svm testing_data.dat | head

