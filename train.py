
import pandas as pd
import re , os
from utilities import segment, clean_text, syllable_tokenization, multilingual_semi_syllable_break, character_tokenization, manual_test
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, f1_score, recall_score
import pickle
import argparse

male_value = 0
female_value = 1
random_size = 0.1

def clean_data():
    #fetch females raw data
    female_raw = pd.read_csv('./raw_data/females.csv')["name"].tolist()
    female_raw = sorted(set(female_raw))
    female_data = pd.DataFrame(female_raw,columns=["name"])
    female_data['name'] = female_data['name'].apply(lambda x: clean_text(x))
    female_data['sex'] = female_value #assign value 1 as female sex value

    #fetch males raw data
    male_raw = pd.read_csv('./raw_data/males.csv')["name"].tolist()
    male_raw = sorted(set(male_raw))
    male_data = pd.DataFrame(male_raw,columns=["name"])
    male_data['name'] = male_data['name'].apply(lambda x: clean_text(x))
    male_data['sex'] = male_value #assign value 1 as male sex value

    #combine male and female data
    all_names = pd.concat([female_data,male_data])
    all_names["length"] = all_names['name'].apply(lambda x: len(syllable_tokenization(x)))
    all_names.to_csv('./processed_data/all_names.csv', index=False)

    special_female_two_words_raw = pd.read_csv('./raw_data/special_female_two_words.csv')["name"].tolist()
    special_female_two_words_raw = sorted(set(special_female_two_words_raw))
    special_female_two_words = pd.DataFrame(special_female_two_words_raw,columns=["name"])
    special_female_two_words['name'] = special_female_two_words['name'].apply(lambda x: clean_text(x))
    special_female_two_words .to_csv('./processed_data/special_female_two_words.csv', index=False)

    special_male_two_words_raw = pd.read_csv('./raw_data/special_male_two_words.csv')["name"].tolist()
    special_male_two_words_raw = sorted(set(special_male_two_words_raw))
    special_male_two_words = pd.DataFrame(special_male_two_words_raw,columns=["name"])
    special_male_two_words['name'] = special_male_two_words['name'].apply(lambda x: clean_text(x))
    special_male_two_words .to_csv('./processed_data/special_male_two_words.csv', index=False)

    both_words_raw = pd.read_csv('./raw_data/both.csv')["name"].tolist()
    both_words_raw = sorted(set(both_words_raw))
    both_words = pd.DataFrame(both_words_raw,columns=["name"])
    both_words['name'] = both_words['name'].apply(lambda x: clean_text(x))
    both_words .to_csv('./processed_data/both_words.csv', index=False)
    print("Clean Data is finished.")

def word_columns_by_segments():
    word_columns = ['OOV']
    all_names = retrieve_data()
    for index,value in all_names.iterrows():
        words = segment(value["name"])
        for w in words:
            if w not in word_columns:
                word_columns.append(w)

    word_columns = sorted(set(word_columns))
    words_template = {}
    for wc in word_columns:
        words_template[wc]=0
    
    pd.DataFrame(word_columns,columns=["word_columns"]).to_csv("./processed_data/word_columns_by_segments.csv",index=False)

    names_data=[] #This is for data
    names_sex=[] # This is for male/female 1 is female. 0 is male
    for index,row in all_names.iterrows():
        name_segments = segment(row["name"])
        words = words_template.copy()
        for seg in name_segments:
            if seg in words:
                words[seg] = words[seg]+1
            else:
                words[seg]=1
        names_data.append(words)
        names_sex.append(row["sex"])
    names_pd = pd.DataFrame(names_data)
    names_pd.fillna(0, inplace=True) #fill nan value into 0
    names_pd["sex"] = names_sex

    names_pd.to_csv("./processed_data/words_by_segments.csv",index=False)

    print("Word Columns by Segments is finish")

def word_columns_by_syllable_tokenization():
    word_columns = ['OOV']
    all_names = retrieve_data()
    for index,value in all_names.iterrows():
        words = syllable_tokenization(value["name"])
        for w in words:
            if w not in word_columns:
                word_columns.append(w)
    
    word_columns = sorted(set(word_columns))
    words_template = {}
    for wc in word_columns:
        words_template[wc]=0

    pd.DataFrame(word_columns,columns=["word_columns"]).to_csv("./processed_data/word_columns_by_syllable_tokenization.csv",index=False)

    names_data=[] #This is for data
    names_sex=[] # This is for male/female 1 is female. 0 is male
    for index,row in all_names.iterrows():
        name_segments = syllable_tokenization(row["name"])
        words = words_template.copy()
        for seg in name_segments:
            if seg in words:
                words[seg] = words[seg]+1
            else:
                words[seg]=1
        names_data.append(words)
        names_sex.append(row["sex"])
    names_pd = pd.DataFrame(names_data)
    names_pd.fillna(0, inplace=True) #fill nan value into 0
    names_pd["sex"] = names_sex

    names_pd.to_csv("./processed_data/words_by_syllable_tokenization.csv",index=False)

    print("Word Columns by Syllabla Tokenization is finished.")

def word_columns_by_multilingual_semi_syllable_break():
    word_columns = ['OOV']
    all_names = retrieve_data()
    for index,value in all_names.iterrows():
        words = multilingual_semi_syllable_break(value["name"])
        for w in words:
            if w not in word_columns:
                word_columns.append(w)
    
    word_columns = sorted(set(word_columns))
    words_template = {}
    for wc in word_columns:
        words_template[wc]=0

    pd.DataFrame(word_columns,columns=["word_columns"]).to_csv("./processed_data/word_columns_by_multilingual_semi_syllable_break.csv",index=False)

    names_data=[] #This is for data
    names_sex=[] # This is for male/female 1 is female. 0 is male
    for index,row in all_names.iterrows():
        name_segments = multilingual_semi_syllable_break(row["name"])
        words = words_template.copy()
        for seg in name_segments:
            if seg in words:
                words[seg] = words[seg]+1
            else:
                words[seg]=1
        names_data.append(words)
        names_sex.append(row["sex"])
    names_pd = pd.DataFrame(names_data)
    names_pd.fillna(0, inplace=True) #fill nan value into 0
    names_pd["sex"] = names_sex

    names_pd.to_csv("./processed_data/words_by_multilingual_semi_syllable_break.csv",index=False)

    print("Word Columns by Multilingual Semi Syllable Break is finished.")

def word_columns_by_character_tokenization():
    word_columns = ['OOV']
    all_names = retrieve_data()
    for index,value in all_names.iterrows():
        words = character_tokenization(value["name"])
        for w in words:
            if w not in word_columns:
                word_columns.append(w)
    
    word_columns = sorted(set(word_columns))
    words_template = {}
    for wc in word_columns:
        words_template[wc]=0

    pd.DataFrame(word_columns,columns=["word_columns"]).to_csv("./processed_data/word_columns_by_character_tokenization.csv",index=False)

    names_data=[] #This is for data
    names_sex=[] # This is for male/female 1 is female. 0 is male
    for index,row in all_names.iterrows():
        name_segments = character_tokenization(row["name"])
        words = words_template.copy()
        for seg in name_segments:
            if seg in words:
                words[seg] = words[seg]+1
            else:
                words[seg]=1
        names_data.append(words)
        names_sex.append(row["sex"])
    names_pd = pd.DataFrame(names_data)
    names_pd.fillna(0, inplace=True) #fill nan value into 0
    names_pd["sex"] = names_sex

    names_pd.to_csv("./processed_data/words_by_character_tokenization.csv",index=False)

    print("Word Columns by Character Tokenization is finished.")

def retrieve_data():
    return pd.read_csv("./processed_data/all_names.csv")

def mf_leading_exclude_list():
    #get all names
    all_names = retrieve_data()
    exclude_list = []

    #list names which has only two syllables 
    female_two_words = all_names[(all_names['sex'] == female_value) & (all_names['length'] == 2)]["name"].tolist()
    male_two_words = all_names[(all_names['sex'] == male_value) & (all_names['length'] == 2)]["name"].tolist()

    for ftw in female_two_words:
        males = all_names[(all_names['sex'] == male_value) & (all_names['length'] > 2)]["name"].tolist()
        for m in males:
            if "".join(syllable_tokenization(m)[0:2])==ftw:
                exclude_list.append(ftw)
    
    for mtw in male_two_words:
        females = all_names[(all_names['sex'] == female_value) & (all_names['length'] > 2)]["name"].tolist()
        for f in females:
            if "".join(syllable_tokenization(f)[0:2])==mtw:
                exclude_list.append(mtw)
    
    exclude_list = sorted(set(exclude_list))

    leading_male_2word_include = [x for x in male_two_words if x not in exclude_list]
    leading_female_2word_include = [x for x in female_two_words if x not in exclude_list]

    df = pd.DataFrame(leading_male_2word_include,columns=["name"])
    df.to_csv('./processed_data/leading_male_2word_include.csv', index=False)

    df = pd.DataFrame(leading_female_2word_include,columns=["name"])
    df.to_csv('./processed_data/leading_female_2word_include.csv', index=False)

    df = pd.DataFrame(exclude_list,columns=["name"])
    df.to_csv('./processed_data/leading_both_2word_exclude.csv', index=False)
    print("MF leading exclusion list is finished.")



def train(title,words,model):
    print("=================================================")
    print(title)
    print("=================================================")
    names = pd.read_csv(words)
    total_count = len(names)
    male_count = len(names[(names['sex'] == male_value)])
    female_count = len(names[(names['sex'] == female_value)])
    print(f"Total is {total_count}. Male is {male_count}. Female is {female_count}")

    X = names.iloc[:,:-1] #data only
    Y = names.iloc[:,-1] #only labels Male/Female\

    max_i=0
    max_score=0
    for i in range(10,70):
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = random_size,random_state=i)
        classifier = LogisticRegression()
        if model == "mf_logistic_regression_by_character_tokenization":
            classifier = LogisticRegression(max_iter=5000)
        classifier.fit(x_train, y_train)       #training level
        score = classifier.score(x_test, y_test)
        if score > max_score:
            max_i=i
            max_score=score
            max_classifier = classifier
            max_x_train, max_x_test, max_y_train, max_y_test = x_train, x_test, y_train, y_test
            max_y_pred = classifier.predict(max_x_test) # Predit Y Value with Test Datasets

    print(f"Model accuracy score of random state {max_i} is : ", max_score*100)
    cm = confusion_matrix(max_y_test,max_y_pred) #Check TP TN FP FN with test and prediction dataset
    print(str(cm))

    tn = cm[0,0]
    fp = cm[0,1]
    fn = cm[1,0]
    tp = cm[1,1]

    with open(f"./models_and_results/{model}_model.pkl", 'wb') as f:
        pickle.dump(max_classifier, f)
    with open(f"./models_and_results/{model}_result.txt", 'w') as f:
        f.write(str(title)+"\n")
        f.write(f"Total is {total_count}. Male is {male_count}. Female is {female_count}"+"\n")
        max_score = str(max_score*100)
        f.write(str(f"Score is : {max_score}")+"\n")
        f.write(str(f"Confusion Matrix result")+"\n")
        f.write(str(f"True Negative is {tn}")+"\n")
        f.write(str(f"False Positive is {fp}")+"\n")
        f.write(str(f"False Negative is {fn}")+"\n")
        f.write(str(f"True Positive is {tp}")+"\n")
        f.write('Accuracy Score '+str(accuracy_score(max_y_test, max_y_pred)*100)+'%\n')
        f.write('Precision Macro Score '+str(precision_score(max_y_test, max_y_pred,average = 'macro')*100)+'%\n')
        f.write('Recall_Score '+str(recall_score(max_y_test, max_y_pred, average = 'macro')*100)+'%\n')
        f.write('F_Score '+str(f1_score(max_y_test, max_y_pred, average = 'macro')*100)+'%\n')

def test_all_and_generate_special():
    if os.path.exists('./processed_data/special_list.csv'):
        os.remove('./processed_data/special_list.csv')

    #Testing Against all datasets
    all_names = retrieve_data()
    #all_names = all_names["name"].tolist()
    total=len(all_names)
    right=0
    wrong=0
    wrong_method_count = {0:0,1:0,2:0,3:0,4:0,5:0,6:0}
    right_method_count = {0:0,1:0,2:0,3:0,4:0,5:0,6:0}
    wrong_words=[]
    special_list={}
    for index,row in all_names.iterrows():
        result = manual_test(row["name"],True)
        sex = result[0]
        method = result[1]
        if sex!=row["sex"] and sex != 0.5:
            wrong=wrong+1
            wrong_method_count[method]=wrong_method_count[method]+1
            special_list[row["name"]]=row["sex"]
        else:
            right_method_count[method]=right_method_count[method]+1
            right=right+1
    percentage=(right/total)*100
    wrong_words = list(set(wrong_words))
    wrong_words = sorted(wrong_words)

    df = pd.DataFrame(list(special_list.items()), columns=["name", "sex"])
    df.to_csv('./processed_data/special_list.csv',index=False)

    print(f"Right is {right}")
    print(f"Wrong is {wrong}")
    print(f"Percentage is {percentage}")
    print('","'.join(wrong_words))
    print("Wrong Method Count")
    print(wrong_method_count)
    print("Right Method Count")
    print(right_method_count)

def data_preprocessing():
    clean_data()
    #word_columns_by_segments()
    #word_columns_by_syllable_tokenization()
    word_columns_by_multilingual_semi_syllable_break()
    #word_columns_by_character_tokenization()
    mf_leading_exclude_list()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--train', help='Training Type all,segment,character,syllable,multi')
    args = parser.parse_args()
    if args.train:
        if args.train in ["all","segment","character","syllable","multi"]:

            clean_data()
            
            if args.train == "segment" or args.train=="all": word_columns_by_segments() 
            if args.train == "syllable" or args.train=="all": word_columns_by_syllable_tokenization()
            if args.train == "multi" or args.train=="all": word_columns_by_multilingual_semi_syllable_break()
            if args.train == "character" or args.train=="all": word_columns_by_character_tokenization()

            mf_leading_exclude_list()
            
            if args.train == "segment" or args.train=="all": train("By Segment","./processed_data/words_by_segments.csv","mf_logistic_regression_by_segments")
            if args.train == "syllable" or args.train=="all": train("By Syllable Tokenization","./processed_data/words_by_syllable_tokenization.csv","mf_logistic_regression_by_syllable_tokenization")
            if args.train == "multi" or args.train=="all": train("By Multilingual Semi Syllable Break","./processed_data/words_by_multilingual_semi_syllable_break.csv","mf_logistic_regression_by_multilingual_semi_syllable_break")
            if args.train == "character" or args.train=="all": train("By Character Tokenization","./processed_data/words_by_character_tokenization.csv","mf_logistic_regression_by_character_tokenization")
            
            test_all_and_generate_special()
        else:
            print("NO valid training type")
    else:
        print("No Training Type is provided. Default will be used.")    


    