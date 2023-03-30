# Myanmar Male Female Classification

This is the school project of Team Binary Brigade from Simbolo - AI Batch 9

Purpose    : To classify Myanmar Names by sex (male or female or both).  
Use Cases  : It may be able to use to classify Myanmar Names. It may able to use Myanmar NER projects  
Limitation : Till to this documentaiton time, there are total 6357 names in dataset. It was good to use for testing purposes. But for production use we may need to put more name to cover more names.  


## How to retrain the model

There are total four ways to train the model

To train all, just type as follow:

> python ./train.py -t all

#### By Segment ['ခိုင်', 'သန္တာ', 'ထွန်း']

> python ./train.py -t segment

#### By Character ['ခ', 'ိ', 'ု', 'င', '်', 'သ', 'န', '္', 'တ', 'ာ', 'ထ', 'ွ', 'န', '်', 'း']

> python ./train.py -t character

#### By Syllable Tokenization ['ခိုင်', 'သ', 'န္တာ', 'ထွန်း']

> python ./train.py -t syllable

#### By Multilingual Semi Syllable Break ['ခို', 'င်', 'သ', 'န္', 'တာ', 'ထွ', 'န်း']

> python ./train.py -t multi

## Sources

### English to Myanmar Source
https://docs.google.com/spreadsheets/d/1FRWeY1QMEsyDTOGjk4Jj5hGXQekQb0-uURDbuAKe3Cs/edit#gid=1461949965

### Most of Burmese Names are got from following Source
https://github.com/L16H7/Myanmar_Names

### Source of Segmentation
https://github.com/swanhtet1992/ReSegment/blob/master/resegment.py

### Source of Multilingual Semi Syllable Break, Character Tokenization, Syllable Tokenization
https://github.com/SaPhyoThuHtet/nlp-tool/blob/main/utilities.py