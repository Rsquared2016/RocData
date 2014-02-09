Building a Classifier
=======================================
This guide will help you train a SVM classifier, run it against a data set, and then output labels.
Data files in this tutorial are placed in `data/`.


#Prerequisites
We will make use of the following 
- [ SVMperf ](http://www.cs.cornell.edu/people/tj/svm_light/svm_perf.html) : SVM library from Cornell
- [PIP](https://pypi.python.org/pypi/pip)
  - simplejson
  
# Training
The hardest part in training a classifier is building the training set.

For a given model, you have to create , a text file of training data with the following structure.

located at `data/training_data.txt`. 
This is a simple text file, where each line is comprised of the following : 

```CSV
#  training_data.txt
#  tweet id | label |  tweet text
10708877913 sick   Sick and Tired of being sick and tired 
4969488000  sick   i think i have freshers flu. which is quite a feat even for me. and makes me want to be back at uni sooo badly...
23938723201 health ive had a tooth removed its not that pain full :) dont worry about it it will be ok 
20314009003 health I'm dying of heat stroke 
26390902605 health Woke up with a freaking headache today... And the biochemistry exam didn't really help to cure it... :( 
6050366908  health Does this cold,dreary weather affect YOUR joints? What do U do to comfort yourself when cold, stiff & in pain??!? 
11869412900 health Ian Dury died of cancer WAY before Malcolm Maclaren did. 
22690177204 no     A Kite in the sky ! Alone n alone ! Have no one to share the pain
9073622108  no     lithium!! 
20787350603 no     Wow Flushing smells like straight unwashed ass this morning chick next to me was trying not to gag 
4798522704  no     should TEACH. And seriously I hate repubs and dems both. I'm just sick of Nobama being canonized because he's a good speaker. 
17158395602 no     i want more doctor who now 
10588865414 no     stupid blisters. What are your new shoes? 
22690177204 no     A Kite in the sky ! Alone n alone ! Have no one to share the pain 
5362439308  no     so bored, thought i had swine flu last night. Turned out i just ate too much candy 
24330120800 notenglish lalalalalalalalalala,no soy pica &lt;3 
```

# Testing
Your test file should be comprised of json objects representing tweets. 

```json
{
    "id": "6f3acc1e75c817417f118d44596f33f6",
    "key": "6f3acc1e75c817417f118d44596f33f6",
    "value": {
        "rev": "1-e1e70bd847ff3a38f0bcc69da542cab8"
    },
    "doc": {
        "_i     d": "6f3acc1e75c817417f118d44596f33f6",
        "_rev": "1-e1e70bd847ff3a38f0bcc69da542cab8",
        "iso_language_code": "en",
        "text": "@Layce305 bless my people",
        "cr     eated_at": "Wed, 19 May 2010 00:40:00 +0000",
        "lon": -73.918209,
        "profile_image_url": "http://a3.twimg.com/profile_images/317812083/n12945     82050_215_normal.jpg",
        "to_user": "Layce305",
        "source": "&lt;a href=&quot;http://ubertwitter.com&quot; rel=&quot;nofollow&quot;&gt;UberTwitter&lt;/a&     gt;",
        "health": -0.10548193,
        "location": "ÜT: 40.664879,-73.918209",
        "from_user": "kingraspedro",
        "lat": 40.664879,
        "from_user_id": 16789049,
        "to_user_id": 1542507,
        "geo": null,
        "id": 14261124214,
        "metadata": {
            "result_type": "recent"
        }
    }
}
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

echo
echo "Joined lines:"
paste predictions_svm testing_data.dat | head

```
