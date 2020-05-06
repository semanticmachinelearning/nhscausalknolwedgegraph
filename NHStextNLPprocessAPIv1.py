#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Natural Language Processing Pipeline


# In[2]:


import NHSsearchv5 as nhs # the NHS web content crawler


# In[158]:


#import spacy
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import spotlight
from lxml import html
from lxml import html
#from collections import namedtuple
#from dateutil.parser import parse
#from collections import OrderedDict
#import urllib, json
#import urllib.request
import requests
import spotlight
import unicodedata
from nltk.stem import PorterStemmer 
ps = PorterStemmer()
#!python -m spacy download en_core_web_lg


# In[159]:


#nlp=spacy.load('en_core_web_lg/en_core_web_lg-2.2.5')


# In[160]:


sections = ['disease','overview','symptoms','affected','causes', 'prevention','treatment','diagnosis']


# In[167]:


#print('**overview:',_info[1])
#print('**symptoms:',_info[2])
#print('**affections:',_info[3])
#print('**cause:',_info[4])
#print('**prevention:',_info[5])
#print('**treatment:',_info[6])
#print('**diagnosis:',_info[7])
#testing 
#An example of crawling Pneumonia disease
#web_text_nlp_pipeline('pneumonia')
#The test passed!


# In[164]:


def web_text_nlp_pipeline(disease_name):
    terms=[]
    #Step 1: Crawling NHS information
    _info=crawling_nhs(disease_name)
    #Step 2 and 3: Sentence and word Segmentation and step 4 semantic tokenization and merge
    disease_tokens,dbp_tokens = disease_tokenlisation(_info)
    for i in range(1,8):
        final_list=merg_tag_semantic(disease_tokens[i],dbp_tokens[i])
        final_list = list(dict.fromkeys(final_list))
        print('*****',sections[i],'*****\n',final_list)
        terms.append(final_list)
    return terms


# In[108]:


def merg_tag_semantic(tag,sem):
    in_first = set(tag)
    in_second = set(sem)

    in_second_but_not_in_first = in_second - in_first

    return tag + list(in_second_but_not_in_first)


# In[140]:


def disease_tokenlisation(sects_text):
    word_list = []
    dbp_list = []
    for sect in sects_text:
        dbp_list.append(dbpedia_annoations(sect))
        stop_words = set(stopwords.words('english'))
        words=[]
        stoen = sent_tokens(sect)
        for s in stoen:
            tokenizer = RegexpTokenizer(r'\w+')
            new_s_list=tokenizer.tokenize(s)
            new_s = ' '.join(new_s_list)
            word_tokens = word_tokenize(new_s) 
            filtered_sentence = [w for w in word_tokens if not w in stop_words]
            nun_s = nltk.pos_tag(filtered_sentence)
            #nun_list=[]
            for n in nun_s:
                if n[1][:2]=='NN':
                    if n[1][:-1]=='S' or n[0].endswith('s'):
                        words.append(ps.stem(n[0]).capitalize())
                    else:
                        words.append(n[0].capitalize() )
                        
        #print(sect)
        #print('*********************************************************************************************************************')
        #print(words)
        word_list.append(words)
    #print(word_list)
    return word_list,dbp_list


# In[3]:


def crawling_nhs(dname):
    dname = dname.replace(' ','_')
    _data=[]
    _data.append(dname)
    question_list = ['overview','symptoms','affected','causes', 'prevention','treatment','diagnosis']
    for q in question_list:
        texts = nhs.NHS_pasering(dname,q)
        _data.append(texts)
    return _data


# In[35]:


def sent_tokens(p_text):
    return sent_tokenize(p_text)


# In[38]:


def word_tokens(s_text):
    return word_tokenize(s_text)


# In[153]:


def dbpedia_annoations(inp_db):
    restAPI='http://api.dbpedia-spotlight.org/en/annotate'
    reqk=[]
    inp_word = inp_db.split()
    try:
        #print('in')
        annotation = spotlight.annotate(restAPI,inp_db,confidence=0.20,support=10)
        for terms in annotation:
            uniterms = unicodedata.normalize('NFKD',terms['URI']).encode('ascii','ignore')
            #print(uniterms)
            sem_key = str(uniterms).split('/')[-1][0:-1].lower()
            #print (sem_key)
            if sem_key in inp_word and sem_key !='the_who':
                reqk.append(str(uniterms).split('/')[-1][0:-1])
            else:
                if sem_key !='the_who':
                    sem_key=sem_key.replace('_',' ')
                    for xs in inp_word:
                        if xs[-1]=='?' or xs[-1]=='.':
                            xs=xs[:-1]
                        #print('DBp anno: '+sem_key,xs)
                        if sem_key.startswith(xs.lower()) or xs.lower().startswith(sem_key) or sem_key.endswith(xs.lower()):
                            reqk.append(str(uniterms).split('/')[-1][0:-1])
                            break
    except: 
        e= 'no annoation find in DBpedia'
        #print (e)
    return reqk


# In[ ]:




