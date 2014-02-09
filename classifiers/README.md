Building a Classifier
=======================================
This guide will help you train a SVM classifier, run it against a data set, and then output labels for data.

#Prerequisites
We will make use of the following:
- [PIP](https://pypi.python.org/pypi/pip)
  - simplejson
  
#Directory Structure
```
    |-- README.md
    |-- Makefile
    |   |-- src           # Contains source code for training a classifier
    |       |-- repositories
    |   |-- svm_perf      # Contains source code for Cornell's [ SVMperf ](http://www.cs.cornell.edu/people/tj/svm_light/svm_perf.html)
    |   |-- SVMs          # Contains the different classifiers
    |       |-- training_data.txt  # input for creatTrainingDataSVM.py [follows this](#training)
    |       |-- model/             # contains .dat for the SVM
    |       |-- bin/               # contains binary data needed for SVM
```

# Training
We begin building our SVM by supplying the model with training data. We will use a simple 
simple text file where each line follows the following pattern:

```CSV
#  training_data.txt
# tweet id | label |  tweet text
10708877913  sick   Sick and Tired of being sick and tired 
4969488000   sick   i think i have freshers flu. which is quite a feat even for me. and makes me want to be back at uni sooo badly...
6050366908   health Does this cold,dreary weather affect YOUR joints? What do U do to comfort yourself when cold, stiff & in pain??!? 
11869412900  health Ian Dury died of cancer WAY before Malcolm Maclaren did. 
4798522704   no     should TEACH. And seriously I hate repubs and dems both. I'm just sick of Nobama being canonized because he's a good speaker. 
17158395602  no     i want more doctor who now 
10588865414  no     stupid blisters. What are your new shoes? 
22690177204  no     A Kite in the sky ! Alone n alone ! Have no one to share the pain 
24330120800  notenglish lalalalalalalalalala,no soy pica &lt;3 
```

SVMperf will then do the following : 
### createTrainingDataSVM.py
This file prepares the model's training data for SVMlight from labeled tweets. It will output two files :
`model/sys.argv[1].words` this contains all the unique tokens that appear in the training data
`model/train.dat` each line contains tweet's class, representation of a tweet in the feature space defined by the presence of a token word, #, and the name of the class

```dat
# model/train.dat
# For example:
#  -1 1175:1 1550:1 1859:1 1874:1 2872:1 3104:1 3488:1 3562:1 3853:1 4030:1 5637:1 6295:1 6679:1 6935:1 6942:1 7152:1 9016:1 # no

# Run: 
# python -OO createTrainingDataSVM.py training_data.txt 1 
```

# Testing
TODO:

# Miscellaneous info
An old copy of all these files are located at `/p/twitter/SadilekAll/TwitterHealth2.0/SVM-starter-code`.
```
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
