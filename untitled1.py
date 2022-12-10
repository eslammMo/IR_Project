# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 18:43:04 2022

@author: EslamMo
"""

# Import Module
import os

# Folder Path
path = r"E:\&Uni\7S\ir\sec\testtt\Collection"

# Change the directory
os.chdir(path)

# Read text File
def read_text_file(file_path):
    with open(file_path, 'r') as fl:
        wordStr=fl.read()
        return wordStr
        
# iterate through all file
coll=""
for file in os.listdir():
        file_path = f"{path}\{file}"
        # call read text file function
        fileText=read_text_file(file_path)
        coll=coll+" "+(fileText)

# Tokenization
from nltk.tokenize import word_tokenize 

tokens=word_tokenize(coll)
#print(tokens)

# Apply Stop Words
from nltk.corpus import stopwords

def exclude_stop_words(terms):
        filtered_terms=[]
        stop_words = set(stopwords.words('english'))
        for term in terms :
            if term not in stop_words:
                 filtered_terms.append(term)
        return filtered_terms
final_tokens=exclude_stop_words(tokens)
final_tokens

def get_unique_terms(tokens):
        unique_terms=[]
        for t in tokens :
            if t not in unique_terms:
                 unique_terms.append(t)
        return unique_terms
#terms without stopwords
terms=get_unique_terms(final_tokens)
#terms with stopwords
disTokens=get_unique_terms(tokens)


#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------


# Part two => Postional Index

# importing libraries
import os
from natsort import natsorted
# Initialize the file no.
fileno = 0
# initialize postional index dict.
pos_index = {}

# get and sort files
file_names = natsorted(os.listdir())
# For every file.
for file in file_names:
    file_path = f"{path}\{file}"
    # call read text file function
    fileText=read_text_file(file_path)
    fileno=fileno+1		
    # Tokenization
    final_token_list=word_tokenize(fileText)
    
    #final_token_list = exclude_stop_words(file_tokens)
	# For position and term in the tokens.
    for pos, term in enumerate(final_token_list):
			# If term already exists in the positional index dictionary.
        if term in pos_index:
				# Increment total freq by 1.
            pos_index[term][0] = pos_index[term][0] + 1	
				# Check if the term has existed in that DocID before.
            if fileno in pos_index[term][1]:
                pos_index[term][1][fileno].append(pos)	
            else:
                pos_index[term][1][fileno] = [pos]
			# If term does not exist in the positional index dictionary
			# (first encounter).
        else:						
            # Initialize the list.
            pos_index[term] = []
            # The total frequency is 1.
            pos_index[term].append(1)
            # The postings list is initially empty.
            pos_index[term].append({})	
            # Add doc ID to postings list.
            pos_index[term][1][fileno] = [pos]
# example from positional index .
# ex = pos_index["antony"]
#print(ex)

#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------

# Part two => phrase Query
flag1=0

# Initialize the dictionary.
Query_index = {}
Query_revs = []

User_Query = input("Enter your value: ")
Qterms=word_tokenize(User_Query)
#Qterms=exclude_stop_words(Qtoken)
Qlen=len(Qterms)
if Qlen ==1:
    Q1=Qterms[0]
    if Q1 in pos_index:
        Query_index=pos_index[Q1][1]
    else:
        flag1=1
else:
    Q1=Qterms[0]
    Q2=Qterms[1]

    if not (Q2 in pos_index):
        flag1=1
    else:
        for idD in  pos_index[Q1][1]:
            if idD in pos_index[Q2][1]:
                for posTerm in pos_index[Q1][1][idD]:
                    if posTerm+1 in pos_index[Q2][1][idD]:
                        Query_index[idD]=[posTerm+1]
                        #loop in query if it have more than two words
        if Qlen > 2 :
            for x in range(2, Qlen):
                Qn=Qterms[x]
                #check if the query have a word dosen't exist in Docs
                if not (Qn in pos_index) :
                    Query_index.clear()
                    break
                else:
                    for idDQ in Query_index:
                        if idDQ in pos_index[Qn][1]:
                            for pos , term in enumerate( Query_index[idDQ]):
                                #check if the words are sequentially
                                if term+1 in pos_index[Qn][1][idDQ]:
                                    Query_index[idDQ][pos]=term+1
                                else:
                                    #get the docs that have the words but arent sequentially
                                    Query_revs.append(idDQ)
                        else:
                            #get the docs that haven't the words
                            Query_revs.append(idDQ)
                            
   #clear the result from wrong Docs
    if len(Query_revs) > 0:
      for Qrev in Query_revs:
          if Qrev in Query_index:
              Query_index.pop(Qrev)
#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------

# Part three 
#------------------------------------------------------------
#------------------------------------------------------------
#-------------------------------------------------------------
#-------------------------------------------------------------
#-------------------------------------------------------------
#-------------------------------------------------------------
#-------------------------------------------------------------
#---------------------------------------------------------------------
# create term freq dict
#dynamic
import pandas as pd
import math
#files number
files_num=len(file_names)
#intialize Term Frequency , w_Term Frequency,Df_idf and Tf*Idf tables
Term_Freq={}
df_and_idf={}
W_tf={}
tf_idf={}
filnum=0
for tok in disTokens:
    Term_Freq[tok]=[0]*files_num
    df_and_idf[tok]=[0,0]
    filnum=0
    for file in file_names:
        file_path = f"{path}\{file}"
                # call read text file function
        fileText=read_text_file(file_path)
        # Tokenization
        final_token_list=word_tokenize(fileText)
        #calc df
        if tok in final_token_list:
            df_and_idf[tok][0]= df_and_idf[tok][0]+1
        #calc TF
        for t in final_token_list:
            if tok == t:
                Term_Freq[tok][filnum]=Term_Freq[tok][filnum]+1 
        
        filnum=filnum+1
    #calc IDF
    df_and_idf[tok][1]=math.log10(files_num/df_and_idf[tok][0])
        
#calc weight_tf
for tok in Term_Freq:
    filnum=0
    W_tf[tok]=[0]*files_num
    for x in range(files_num):
        if Term_Freq[tok][x] >0:
           W_tf[tok][x]=1+ math.log10(Term_Freq[tok][x])
           
#clac tf*idf
for tok in Term_Freq:
    tf_idf[tok]=[0]*files_num
    for x in range(files_num):
           tf_idf[tok][x]=df_and_idf[tok][1] * W_tf[tok][x]


dt_W_tf   = pd.DataFrame.from_dict(W_tf, orient ='index')     
dt_df_idf = pd.DataFrame.from_dict(df_and_idf, orient ='index')     
dt_tf     = pd.DataFrame.from_dict(Term_Freq, orient ='index') 
dt_tf_idf = pd.DataFrame.from_dict(tf_idf, orient ='index') 

#--------------------------------------------------------------------
#calc length for each doc
length={}
for x in range(files_num):
    sq_len=0
    for tok in tf_idf:
        sq_len=sq_len+pow(tf_idf[tok][x],2)
    length[x]=math.sqrt(sq_len)
#-------------------------------------------------------------------
#calc normalize
norm={}
for tok in tf_idf:
    norm[tok]=[0]*files_num
    for x in range(files_num):
        norm[tok][x]=tf_idf[tok][x]/length[x]

dt_norm = pd.DataFrame.from_dict(norm, orient ='index')   
dt_len  = pd.DataFrame.from_dict(length, orient ='index')

#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#Calc query methods
Q_data={}
sq_Qlen=0
Qlength=0
cos_sim={}
if flag1==1 :
     print("no doc related to your search3")
elif len (Query_index) == 0 :
     print("no doc related to your search3")
else:
    #calc tf for Query tokens
    for qt in Qterms:
        if qt in Q_data:
            Q_data[qt][0]=Q_data[qt][0]+1
        else:
            Q_data[qt]=[]
            Q_data[qt].append(1)
    #calc Weight_tf for Query tokens
    for qt in Q_data:
        Q_data[qt].append(1+math.log10(Q_data[qt][0]))

    #calc tf_idf for Query tokens
    for qt in Q_data:
        Q_data[qt].append(Q_data[qt][1]*df_and_idf[qt][1])

    #calc Query length
    for qt in Q_data:
        sq_Qlen=sq_Qlen+pow(Q_data[qt][2],2)
        Qlength=math.sqrt(sq_Qlen)
    #calc normlize
    for qt in Q_data:
        Q_data[qt].append(Q_data[qt][2]/Qlength)
    #calc cosin sim
    for diD in Query_index:
        cos_sim[diD]=0
        for qt in Q_data:
            cos_sim[diD]=cos_sim[diD]+(norm[qt][diD-1]*Q_data[qt][3])
        #    print(qt ,':',diD,'=>',norm[qt][diD-1],' * ',Q_data[qt][3],' = ',cos_sim[diD],)
            
    cos_sim=dict(sorted(cos_sim.items(), key = lambda x: x[1], reverse = True))
    for doc in cos_sim:
        print("Doc ID",doc ,": postions =>",Query_index[doc])
       

dt_QData  = pd.DataFrame.from_dict(Q_data, orient ='index')
dt_QData.rename(columns = {'index':'Token', 0:'TF',1:'TF_Weight',2:'Tf_IDF',3:'normalize'}, inplace = True)


dtr_tf_idf  = pd.DataFrame.from_dict(tf_idf, orient ='index')

dtr_tf_idf.rename(columns = {'index':'Token', 0:'Doc1',1:'Doc2',2:'Doc3',3:'Doc4',4:'Doc5',5:'Doc6',6:'Doc7',7:'Doc8',8:'Doc9',9:'Doc10'}, inplace = True)






















