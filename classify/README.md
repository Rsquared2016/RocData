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
