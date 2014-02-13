Building Classifiers
=======================================

```bash
make train model=<SVM-NAME> # this builds an SVM against data provided.
-------------------------------------------------------------------------------
# TODO: configure      # TODO: should look through any system and find all dependencies for each machine
# TODO: make           # TODO: should generate appropriate makefile
# TODO: make install   # TODO: should compile and install all components necessary
# TODO: make run       # TODO: start all the services necessary for the given software.
```


This guide will help you train a SVM, run it against a data set, and then output labels for data.

#Prerequisites
We will make use of the following:
- [PIP](https://pypi.python.org/pypi/pip)
  - simplejson
  
#Directory Structure

    |-- README.md
    |-- Makefile
    |   |-- src           # Contains source code for training a classifier
    |   |-- svm_perf      # Contains source code for Cornell's SVMperf
    |   |-- SVMs          # Contains the different classifiers
    |       |-- <model-1> # Folder that your SVM will live in
    |         |-- training_data.txt  # input for creatTrainingDataSVM.py
    |         |-- model/             # contains .dat for the SVM
    |         |-- bin/               # contains binary data needed for SVM
    |         |-- data/
    |       |-- <model-2>
    |         |-- training_data.txt 
    |         |-- model/            
    |         |-- bin/              
    |         |-- data/

# Training
The first step in training a classifier is supplying the SVM classifier with training data. 
You will use a simple text file constructed like so:

```CSV
# model/training_data.txt
#
# tweet id | label | tweet text
10708877913  sick    Sick and Tired of being sick and tired 
4969488000   sick    i think i have freshers flu. which is quite a feat even for me. and makes me want to be back at uni sooo badly...
6050366908   health  Does this cold,dreary weather affect YOUR joints? What do U do to comfort yourself when cold, stiff & in pain??!? 
11869412900  health  Ian Dury died of cancer WAY before Malcolm Maclaren did. 
4798522704   no      should TEACH. And seriously I hate repubs and dems both. I'm just sick of Nobama being canonized because he's a good speaker. 
17158395602  no      i want more doctor who now 
10588865414  no      stupid blisters. What are your new shoes? 
22690177204  no      A Kite in the sky ! Alone n alone ! Have no one to share the pain 
24330120800  notenglish lalalalalalalalalala,no soy pica &lt;3 
```

# Output
You will be returned a flat file that looks like this.

```bash
# Output will look like this : 
# Score     | class | tokens                                |#| text
-0.30509016     0     797:1   6479:1 12609:1                 #  @Layce305 bless my people
-0.26440957     0     5735:1  7842:1 14426:1 14872:1 15766:1 #  #Nowplaying Kings of Leon- Use somebody
```


# Under the Hood
TODO: document the pipeline.

```bash
# Running : 
python -OO src/createTrainingDataSVM.py SVMs/flu/training_data.txt 1 
```
Prepares the model's training data for SVMlight from the labeled tweets, outputting 2 files :
  - `model/<classifier_name>.words` : a file listing all unique tokens appearing in the training data
  - `model/train.dat`               : each line contains tweet's class, representation in the feature space ( defined by the presence of a token word ) , #, and the name of the class

```
# example line of model/train.dat : 
#  -1 1175:1 1550:1 1859:1 1874:1 2872:1 3104:1 3488:1 3562:1 3853:1 4030:1 5637:1 6295:1 6679:1 6935:1 6942:1 7152:1 9016:1 # no
```


# Miscellaneous info
An old copy of all these files are located at `/p/twitter/SadilekAll/TwitterHealth2.0/SVM-starter-code`.
