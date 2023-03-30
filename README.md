# **Myanmar Male Female Classification**

Demo Link : https://myanmar-names-male-female.streamlit.app



**Purpose**  
To classify Myanmar Names by sex (male or female or both).  
**Description**  
This is the school project of Team Binary Brigade from Simbolo - AI Batch 9. We try various method including scikit-learn logistic regression and tensorflow. After many task, we use rule base plus logistic regression. All various train type include at following train options are all based on logistic regression.  
**Use Cases**  
It may be able to use to classify Myanmar Names. It may able to use Myanmar NER projects  
**Limitation**  
Till to this documentaiton time, there are total 6357 names in dataset. It was good to use for testing purposes. But for production use we may need to put more name to cover more names.  

## **Folder Structure**

Folder raw_data is for new data inputs.  
> boths.csv use for names which can be both male and female.  
> en_to_mm.csv This is mapping file to help convert from myanglish to myanmar  
> females.csv This file is for female names  
> males.csv This file is for male names  
> special_female_two_words.csv is include female names. if that two words include in name, that can be female names.  
> special_male_two_words.csv is include male names. if that two words include in name, that can be female names.  

Folder processed_data include auto generated file which will later use for program to train or to use.
Folder model_and_results include models and result note.

File app.py is use for streamlit. Just use following code to run that file.  
(before that make sure you install requirement libraries. python -m pip install -r requirements.txt)
>streamlit run app.py

File train.py is use to train the datasets and to generate model file.
File utilities.py include most reused library file.

## **How to retrain the model**

There are total four ways to train the model. Accuracy results are vary, between 88 to 94 in general. Normally Segment and Multilingual Semi Syllable Break. Got the good results. Character Tokenization is worst. 

#### To train all

> python ./train.py -t all

#### By Segment ['ခိုင်', 'သန္တာ', 'ထွန်း']

> python ./train.py -t segment

#### By Character ['ခ', 'ိ', 'ု', 'င', '်', 'သ', 'န', '္', 'တ', 'ာ', 'ထ', 'ွ', 'န', '်', 'း']

> python ./train.py -t character

#### By Syllable Tokenization ['ခိုင်', 'သ', 'န္တာ', 'ထွန်း']

> python ./train.py -t syllable

#### By Multilingual Semi Syllable Break ['ခို', 'င်', 'သ', 'န္', 'တာ', 'ထွ', 'န်း']

> python ./train.py -t multi

## **How to use by import**

```python
from utilities import manual_test

#This is default test, you will only got male value as 0, female value as 1, both is 0.5
manual_test("ခိုင်သန္တာထွန်း")

#It will response tuple first one is sex, second one is method type. Method 0,1,2,3,4,6 is rule base, 5 is from model
# method 0: special list exact value taken
# method 1: include by two syllabus, female
# method 2: include by two syllabus, male
# method 3: leading by first two syllabus, female
# method 4: leading by first two syllabus, male
# method 6: name which can be both male and female dictionary
manual_test(test_word="ခိုင်သန္တာထွန်း",getMethod=True)

#assign model type to manual_test function. default is Multilingual Semi Syllable Break
# All options : multi,character,syllable,segment
manual_test(test_word="ခိုင်သန္တာထွန်း",model="multi")

```

## **Sources**

### English to Myanmar Source
https://docs.google.com/spreadsheets/d/1FRWeY1QMEsyDTOGjk4Jj5hGXQekQb0-uURDbuAKe3Cs/edit#gid=1461949965

### Most of Burmese Names are got from following Source
https://github.com/L16H7/Myanmar_Names

### Source of Segmentation
https://github.com/swanhtet1992/ReSegment/blob/master/resegment.py

### Source of Multilingual Semi Syllable Break, Character Tokenization, Syllable Tokenization
https://github.com/SaPhyoThuHtet/nlp-tool/blob/main/utilities.py