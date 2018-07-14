#!/usr/bin/python
# -*- coding: utf-8 -*-
import math,re,time,pickle
from nltk.stem.snowball import RussianStemmer
'''
def freq_dict_old(filename):
    # подcчет встречаемости слова в тексте
    try:
        with open(filename,'r') as file:
            d = dict()
            for line in file:
                if line not in d:
                    d[line] = 1
                else:
                    d[line] += 1
            return d
    except:
        return 'Вы ввели неверное имя файла чтения'
'''

'''
def tfidf(list1):
    #list1 = [term, filename,*files]
    # вычисление веса слова по формуле
    count = 0
    try:
        for file in list1[2:]:
            with open(file,'r') as file:
                result = file.readlines()
                if list1[0] in result:
                    count += 1
        freq = freq_dict(list1[1])
        tf = freq[list1[0]]/len(freq)
        tfidf = tf*math.log(len(list1[2:])/count)
        return tfidf
    except FileNotFoundError:
        return 'Вы ввели неверное имя файла чтения'
'''

'''
def tfidf_dict(list1):
    #list1 = [filename, *files]
    # генерация словаря из слово : вес
    try:
        with open(list1[0],'r') as file:
            d = dict()
            result = file.readlines()
            set1 = set(result)
            for line in set1:
                list2=[line]
                list2.extend(list1)
                d[line] = tfidf(list2)
        return d
    except FileNotFoundError:
        return 'Вы ввели неверное имя файла чтения'
'''

'''
def similarity(list0):
    #list0 = [file1, file2, *files]
    #  в files нужно включить file1 и file2
    try:
        cur = [list0[0]]
        cur.extend(list0[2:])
        tfdict1 = tfidf_dict(cur)

        cur=[list0[1]]
        cur.extend(list0[2:])
        tfdict2 = tfidf_dict(cur)

        tfidf1 = set(tfdict1.keys())
        tfidf2 = set(tfdict2.keys())

        intersection = tfidf1.intersection(tfidf2)
        if intersection == set():
            return 0
        else:
            list1 = [tfdict1[key] for key in intersection]
            list2 = [tfdict2[key] for key in intersection]

            cosine = (sum([i*j for (i, j) in zip(list1, list2)]))/(math.sqrt(sum([i*i for i in list1]))*math.sqrt(sum([i*i for i in list2])))
            return cosine
    except FileNotFoundError:
        return 'Вы ввели неверное имя файла чтения'
'''

def freq_dict(list_of_words):
    d=dict()
    for word in list_of_words:
        if word not in d:
            d[word] = 1
        else:
            d[word] += 1
    return d

def stemmed_words_dict(words_list):
    stemmed_dict = dict()
    for word in words_list:
        stemmed = RussianStemmer().stem(word)
        if stemmed not in stemmed_dict:
            stemmed_dict[stemmed] = [word]
        else:
            stemmed_dict[stemmed].append(word)
    return stemmed_dict

def stemmed_freq_dict(words_list):
    d = dict()
    for word in words_list:
        stemmed = RussianStemmer().stem(word)
        if stemmed not in d:
            d[stemmed] = 1
        else:
            d[stemmed] += 1
    return d

def tfidf_high_level(term,cur_text,texts):
    count=0
    for text in texts:
        if term in text:
            count += 1
    freq = freq_dict(cur_text)
    tf = freq[term]/len(freq)
    try:
        tfidf = tf*(math.log(len(texts)/(count)))
    except ZeroDivisionError:
        tfidf = 0
    return tfidf

def tfidf_high_level_with_stemming(term,cur_text,texts):
    count=0
    for text in texts:
        if term in [RussianStemmer().stem(word) for word in text]:
            count += 1
    freq = stemmed_freq_dict(cur_text)
    tf = freq[term]/len(freq)
    tfidf = tf*(math.log(len(texts)/count))
    return tfidf

def directed_tfidf_dict_high_level(text,texts):
    text_dict = []
    splited_texts = []
    important_clear_text = re.sub(r'[^а-яА-Я ]+', ' ', text)
    if not important_clear_text == '':
            words = important_clear_text.split(' ')
            words_list = []
            for word in words:
                if (word != '\n') and (word!=''):
                    words_list.append(word.lower())
    for txt in texts:
        clear_text = re.sub(r'[^а-яА-Я ]+', ' ', txt)
        if not clear_text == '':
            words = clear_text.split(' ')
            result=[]
            for word in words:
                if (word != '\n') and (word!=''):
                    result.append(word.lower())
            splited_texts.append(result)
    current_dict = dict()
    set_of_words = set(words_list)
    for word in set_of_words:
        current_dict[word] = tfidf_high_level(word,words_list,splited_texts)
    text_dict.append(current_dict)
    return text_dict


def directed_tfidf_dict_high_level_with_stemming(text,texts):
    text_dict = []
    splited_texts = []
    important_clear_text = re.sub(r'[^а-яА-Я ]+', ' ', text)
    if not important_clear_text == '':
            words = important_clear_text.split(' ')
            words_list = []
            for word in words:
                if (word != '\n') and (word!=''):
                    words_list.append(word.lower())
            words_list = [RussianStemmer().stem(word) for word in words_list]
    for txt in texts:
        clear_text = re.sub(r'[^а-яА-Я ]+', ' ', txt)
        if not clear_text == '':
            words = clear_text.split(' ')
            result=[]
            for word in words:
                if (word != '\n') and (word!=''):
                    result.append(word.lower())
            result = [RussianStemmer().stem(word) for word in result]
            splited_texts.append(result)
    current_dict = dict()
    set_of_words = set(words_list)
    for word in set_of_words:
        current_dict[word] = tfidf_high_level(word,words_list,splited_texts)
    text_dict.append(current_dict)
    return text_dict

def directed_tfidf_dict_high_level_with_stemming_for_two_texts(text1,text2,texts):
    text_dict = []
    splited_texts = []
    first_important_clear_text = re.sub(r'[^а-яА-Я ]+', ' ', text1)
    if not first_important_clear_text == '':
            words = first_important_clear_text.split(' ')
            first_words_list = []
            for word in words:
                if (word != '\n') and (word!=''):
                    first_words_list.append(word.lower())
            first_words_list = [RussianStemmer().stem(word) for word in first_words_list]
    second_important_clear_text = re.sub(r'[^а-яА-Я ]+', ' ', text2)
    if not second_important_clear_text == '':
            words = second_important_clear_text.split(' ')
            second_words_list = []
            for word in words:
                if (word != '\n') and (word!=''):
                    second_words_list.append(word.lower())
            second_words_list = [RussianStemmer().stem(word) for word in second_words_list]
    for txt in texts:
        clear_text = re.sub(r'[^а-яА-Я ]+', ' ', txt)
        if not clear_text == '':
            words = clear_text.split(' ')
            result = []
            for word in words:
                if (word != '\n') and (word!=''):
                    result.append(word.lower())
            result = [RussianStemmer().stem(word) for word in result]
            splited_texts.append(result)
    first_current_dict = dict()
    second_current_dict = dict()
    first_set_of_words = set(first_words_list)
    second_set_of_words = set(second_words_list)
    for word in first_set_of_words:
        first_current_dict[word] = tfidf_high_level(word,first_words_list,splited_texts)
    text_dict.append(first_current_dict)
    for word in second_set_of_words:
        second_current_dict[word] = tfidf_high_level(word,second_words_list,splited_texts)
    text_dict.append(second_current_dict)
    return text_dict

def directed_tfidf_dict_high_level_with_stemming_for_two_texts_but_faster(text1,text2):
    text_dict = []
    first_important_clear_text = re.sub(r'[^а-яА-Я ]+', ' ', text1)
    if not first_important_clear_text == '':
            words = first_important_clear_text.split(' ')
            first_words_list = []
            for word in words:
                if (word != '\n') and (word!=''):
                    first_words_list.append(word.lower())
            first_words_list = [RussianStemmer().stem(word) for word in first_words_list]
    second_important_clear_text = re.sub(r'[^а-яА-Я ]+', ' ', text2)
    if not second_important_clear_text == '':
            words = second_important_clear_text.split(' ')
            second_words_list = []
            for word in words:
                if (word != '\n') and (word!=''):
                    second_words_list.append(word.lower())
            second_words_list = [RussianStemmer().stem(word) for word in second_words_list]

    with open('words.pickle','rb') as f:
        splited_texts = pickle.load(f)

    first_current_dict = dict()
    second_current_dict = dict()
    first_set_of_words = set(first_words_list)
    second_set_of_words = set(second_words_list)
    for word in first_set_of_words:
        first_current_dict[word] = tfidf_high_level(word,first_words_list,splited_texts)
    text_dict.append(first_current_dict)
    for word in second_set_of_words:
        second_current_dict[word] = tfidf_high_level(word,second_words_list,splited_texts)
    text_dict.append(second_current_dict)
    return text_dict

def get_corpus_tfidf(texts):
    splited_texts = []
    for txt in texts:
        clear_text = re.sub(r'[^а-яА-Я ]+', ' ', txt)
        if not clear_text == '':
            words = clear_text.split(' ')
            result=[]
            for word in words:
                if (word != '\n') and (word!=''):
                    result.append(word.lower())
            result = [RussianStemmer().stem(word) for word in result]
            splited_texts.append(result)
    return splited_texts

def tfidf_dict_high_level(texts):
    all_dicts=[]
    splited_texts=[]
    for text in texts:
        clear_text = re.sub(r'[^а-яА-Я ]+', ' ', text)
        if not clear_text == '':
            words = clear_text.split(' ')
            result=[]
            for word in words:
                if (word != '\n') and (word!=''):
                    result.append(word.lower())
            splited_texts.append(result)
    for cur_text in splited_texts:
        current_dict=dict()
        set_of_words = set(cur_text)
        for word in set_of_words:
            current_dict[word] = tfidf_high_level(word,cur_text,splited_texts)
        all_dicts.append(current_dict)
    return all_dicts


def true_similarity(first,second):
    first_keys = set(first.keys())
    second_keys = set(second.keys())
    keys_intersection = first_keys.intersection(second_keys)
    if keys_intersection == set():
        return 0
    else:
        list1 = [first[key] for key in keys_intersection]
        list2 = [second[key] for key in keys_intersection]
        try:
            cosine = (sum([i*j for (i, j) in zip(list1, list2)]))/(math.sqrt(sum([i*i for i in list1]))*math.sqrt(sum([i*i for i in list2])))
        except ZeroDivisionError:
            return 0
        return cosine,1-(hemming_distance(list(first.keys()),list(second.keys())))/len(common_vector([list(first.keys()),list(second.keys())]))


def common_vector(splited_texts):
    # input list
    all_words = []
    for text in splited_texts:
        all_words.extend(text)
    all_words=list(set(all_words))
    return all_words


def hemming_distance(first,second):
    # input lists
    all_words = common_vector([first,second])
    first_list=[]
    second_list=[]
    for word in all_words:
        if word in first:
            first_list.append(1)
        else:
            first_list.append(0)
        if word in second:
            second_list.append(1)
        else:
           second_list.append(0)
    distance = 0
    for i in range(len(first_list)):
        if first_list[i] != second_list[i]:
            distance+=1
    return distance


if __name__ == '__main__':

    all_texts = []
    for i in range(1,394):
        try:
            with open('XML\page'+str(i)+'.txt','r') as f:
                content = f.read()
                all_texts.append(content)
        except:
            continue
    print('ads'<0)
    #texts = get_corpus_tfidf(all_texts)
'''
    with open('page3.txt','r',encoding='utf-8') as f1:
        page3 = f1.read()
    with open('page4.txt','r',encoding='utf-8') as f2:
        page4 = f2.read()
    a = directed_tfidf_dict_high_level_with_stemming_for_two_texts_but_faster(page3,page4)
    b = directed_tfidf_dict_high_level_with_stemming_for_two_texts(page3,page4,all_texts)
    print(true_similarity(a[0],a[1]))
    print(true_similarity(b[0],b[1]))
'''

