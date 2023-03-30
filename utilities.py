import streamlit as st
import pickle
import re
import json
import pandas as pd
import os
import csv
from difflib import SequenceMatcher

def clean_text(text):
    text = text.replace("\u200c","")
    text = text.replace(" ","")
    text = text.replace("ျ","ြ")
    text = text.replace("ည်","ီ")
    text = text.replace("ဏ်","န်")
    text = text.replace("မ်","န်")
    text = text.replace("ါ","ာ")
    text = text.replace("အူး","ဦး")
    return text

def multilingual_semi_syllable_break(user_input):
    #source : https://github.com/SaPhyoThuHtet/nlp-tool/blob/main/utilities.py
    # Multilingual Semi Syllabe Break (Lao, Kannada, Oriya, Gujarati, Malayalam, Khmer, Bengali, Sinhala, Tamil, Shan, Mon, Pali and Sanskrit, Sagaw Karen, Western Poh Karen, Eastern Poh Karen, Geba Karen, Kayah, Rumai Palaung, Khamathi Shan, Aiton and Phake, Burmese (Myanmar), Paoh, Rakhine Languages)
    #original -> result = re.sub(r"([a-zA-Z]+|[຀-ຯຽ-໇ໜ-ໟ][ະ-ຼ່-໏]{0,}|[಄-಻ೞ-ೡ][಼ಀ-ಃಾ-ೝೢ-೥]{0,}|[ଅ-଻ଡ଼-ୡୱ][଼଀-଄ା-୛ୢ-୥]{0,}|[અ-઻ૐ-૟ૠ-ૡ૰ૹ][઀-઄઼ા-૏-ૣૺ-૿]{0,}|[അ-ഺ൏-ൡ൰-ൿ][ഀ-ഄ഻-഼ാ-ൎൢ-൥]{0,}|[ក-ឳ។-៚ៜ][ា-៓៝]{0,}|[అ-ఽౘ-ౡ౷౸-౿][ఀ-ఄా-౗ౢ-౥]{0,}|[অ-঻ড়-ৡৰ-৽][ঁ-঄়-৛ৢ-৥৾-৿্]{0,}|[අ-෉][්-෥ෲ-ෳ඀-඄ි]{0,}|[அ-஽][஀-஄ா-௏ௗ]{0,}|[က-ဪဿ၌-၏ၐ-ၕၚ-ၝၡၥၦၮ-ၰၵ-ႁႎ႐-႙႟][ါ-ှၖ-ၙၞ-ၠၢ-ၤၧ-ၭၱ-ၴႂ-ႍႏႚ-႞ꩻ]{0,}|.)",r"\1.....", user_input)
    result = re.sub(r"([a-zA-Z]+|[຀-ຯຽ-໇ໜ-ໟ][ະ-ຼ່-໏]{0,}|[಄-಻ೞ-ೡ][಼ಀ-ಃಾ-ೝೢ-೥]{0,}|[ଅ-଻ଡ଼-ୡୱ][଼଀-଄ା-୛ୢ-୥]{0,}|[અ-઻ૐ-૟ૠ-ૡ૰ૹ][઀-઄઼ા-૏-ૣૺ-૿]{0,}|[അ-ഺ൏-ൡ൰-ൿ][ഀ-ഄ഻-഼ാ-ൎൢ-൥]{0,}|[ក-ឳ។-៚ៜ][ា-៓៝]{0,}|[అ-ఽౘ-ౡ౷౸-౿][ఀ-ఄా-౗ౢ-౥]{0,}|[অ-঻ড়-ৡৰ-৽][ঁ-঄়-৛ৢ-৥৾-৿্]{0,}|[අ-෉][්-෥ෲ-ෳ඀-඄ි]{0,}|[அ-஽][஀-஄ா-௏ௗ]{0,}|[က-ဪဿ၌-၏ၐ-ၕၚ-ၝၡၥၦၮ-ၰၵ-ႁႎ႐-႙႟][ါ-ှၖ-ၙၞ-ၠၢ-ၤၧ-ၭၱ-ၴႂ-ႍႏႚ-႞ꩻ]{0,}|.)",r"\1 ", user_input)
    result = re.sub(r" +", " ", result)
    return result.strip().split(" ")

def character_tokenization(input:str)->str:
    #source : https://github.com/SaPhyoThuHtet/nlp-tool/blob/main/utilities.py
    #original -> return re.sub(r"([^\s])",r"\1      ", input)   
    return re.sub(r"([^\s])",r"\1 ", input).strip().split(" ")

def syllable_tokenization(input:str)->str:
    #source : https://github.com/SaPhyoThuHtet/nlp-tool/blob/main/utilities.py
    return re.sub(r"(([A-Za-z0-9]+)|[က-အ|ဥ|ဦ](င်္|[က-အ][ှ]*[့း]*[်]|္[က-အ]|[ါ-ှႏꩻ][ꩻ]*){0,}|.)",r"\1 ", input).strip().split(" ")

def segment(text):
    #source : https://github.com/swanhtet1992/ReSegment/blob/master/resegment.py
    text = re.sub(r'(?:(?<!္)([က-ဪဿ၊-၏]|[၀-၉]+|[^က-၏]+)(?![ှျ]?[့္်]))', r'𝕊\1', text).strip('𝕊').split('𝕊')
    return text

def list_to_csv(my_list,path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        # Create a CSV writer object
        writer = csv.writer(file)
        # Write each row in the list to the CSV file
        for row in my_list:
            writer.writerow(row)


def rule_base_match(test_word):
    test_word = clean_text(test_word)
    all_words = syllable_tokenization(test_word)
    two_words = "".join(all_words[0:2])

    if os.path.exists("./processed_data/both_words.csv"):
        both_list = pd.read_csv("./processed_data/both_words.csv")["name"].tolist()
        if test_word in both_list:
            return 0.5 , 6
    
    if os.path.exists("./processed_data/special_list.csv"):
        special_list = pd.read_csv("./processed_data/special_list.csv")
        special_list_dict = {}
        for index,row in special_list.iterrows():
            special_list_dict[row["name"]] = row["sex"]
    else:
        special_list_dict = {}
    
    if test_word in special_list_dict:
        return special_list_dict[test_word] , 0    
    
    special_female_two_words = pd.read_csv("./processed_data/special_female_two_words.csv")["name"].tolist()
    special_female_two_words_re = "("+"|".join(special_female_two_words)+")"
    re_result_female = re.search(special_female_two_words_re,test_word)
    if re_result_female != None:
        return 1 , 1

    special_male_two_words = pd.read_csv("./processed_data/special_male_two_words.csv")["name"].tolist()
    special_male_two_words_re = "("+"|".join(special_male_two_words)+")"
    re_result_male = re.search(special_male_two_words_re,test_word)

    if re_result_male !=None:
        return 0, 2

    leading_female_2word_include = pd.read_csv("./processed_data/leading_female_2word_include.csv")["name"].tolist()
    if two_words in leading_female_2word_include:
        return 1, 3

    leading_male_2word_include = pd.read_csv("./processed_data/leading_male_2word_include.csv")["name"].tolist()
    if two_words in leading_male_2word_include:
        return 0, 4

    return None , None
    

def manual_test(test_word, getMethod=False , model="multi"):
    test_word = clean_text(test_word)
    sex , method = rule_base_match(test_word)
    if sex !=None:
        if getMethod:
            return sex, method
        else:
            return sex
    else:
        if model == "multi":
            source_model="./models_and_results/mf_logistic_regression_by_multilingual_semi_syllable_break_model.pkl"
            source_word_columns="./processed_data/word_columns_by_multilingual_semi_syllable_break.csv"
        elif model == "character":
            source_model="./models_and_results/mf_logistic_regression_by_character_tokenization_model.pkl"
            source_word_columns="./processed_data/word_columns_by_character_tokenization.csv"
        elif model == "syllable":
            source_model="./models_and_results/mf_logistic_regression_by_syllable_tokenization_model.pkl"
            source_word_columns="./processed_data/word_columns_by_syllable_tokenization.csv"
        elif model == "segment":
            source_model="./models_and_results/mf_logistic_regression_by_segments_model.pkl"
            source_word_columns="./processed_data/word_columns_by_segments.csv"
        else:
            source_model="./models_and_results/mf_logistic_regression_by_multilingual_semi_syllable_break_model.pkl"
            source_word_columns="./processed_data/word_columns_by_multilingual_semi_syllable_break.csv"

        with open(source_model, 'rb') as f:
            clf = pickle.load(f)
        word_columns_raw = pd.read_csv(source_word_columns)["word_columns"].tolist()
        
        word_columns_raw = sorted(set(word_columns_raw))
        word_columns = {}
        for x in word_columns_raw:
                word_columns[x]=0
        test_word_2 = "".join(syllable_tokenization(test_word))
        name_segments = multilingual_semi_syllable_break(test_word_2)        
        for seg in name_segments:
            if seg in word_columns:
                word_columns[seg] = word_columns[seg]+1
            else:
                word_columns['OOV'] = word_columns['OOV'] + 1
        test_df = pd.DataFrame(data=[word_columns])
        sex = clf.predict(test_df)[0] # Predit Y Value with Test Datasets
        method = 5

        if getMethod:
            return sex, method
        else:
            return sex

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def convert_en_to_mm(test_word):
    test_word = test_word.upper()
    
    mapping_df = pd.read_csv("./raw_data/en_to_mm.csv")

    words = test_word.strip().split(" ")

    results = []

    for w in words:
        max_myanmar = ""
        find_result = mapping_df[mapping_df["english"]==w]["myanmar"].tolist()
        if len(find_result)>0:
            max_myanmar = find_result[0]
        if max_myanmar == "" or max_myanmar == None:
            max_score = 0
            for index, row in mapping_df.iterrows():
                score = similar(w,str(row["english"]))
                if score > max_score:
                    max_score = score
                    max_myanmar = str(row["myanmar"])
        results.append(max_myanmar)
    results = " ".join(results).strip()
    return results
