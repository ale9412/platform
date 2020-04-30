#Frecuency-Topic-Extractor
from os import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import json
import requests
import pandas as pd
import numpy as np
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.stem.snowball import SnowballStemmer
# Starting with the CountVectorizer/TfidfTransformer approach...
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from itertools import islice

import nltk
nltk.download('punkt')
# nltk.download('wordnet') 
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import requests
import urllib.request
import re

palabrasvac = ['a', 'about', 'above', 'across', 'after', 'afterwards']
palabrasvac += ['again', 'against', 'all', 'almost', 'alone', 'along']
palabrasvac += ['already', 'also', 'although', 'always', 'am', 'among']
palabrasvac += ['amongst', 'amoungst', 'amount', 'an', 'and', 'another']
palabrasvac += ['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere']
palabrasvac += ['are', 'around', 'as', 'at', 'back', 'be', 'became']
palabrasvac += ['because', 'become', 'becomes', 'becoming', 'been']
palabrasvac += ['before', 'beforehand', 'behind', 'being', 'below']
palabrasvac += ['beside', 'besides', 'between', 'beyond', 'bill', 'both']
palabrasvac += ['bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant']
palabrasvac += ['co', 'con', 'could', 'couldnt', 'cry', 'de',',','.','-']
palabrasvac += ['describe', 'detail', 'did', 'do', 'done', 'down', 'due']
palabrasvac += ['during', 'each', 'eg', 'eight', 'either', 'eleven', 'else']
palabrasvac += ['elsewhere', 'empty', 'enough', 'etc', 'even', 'ever']
palabrasvac += ['every', 'everyone', 'everything', 'everywhere', 'except']
palabrasvac += ['few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first']
palabrasvac += ['five', 'for', 'former', 'formerly', 'forty', 'found']
palabrasvac += ['four', 'from', 'front', 'full', 'further', 'get', 'give']
palabrasvac += ['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her']
palabrasvac += ['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers']
palabrasvac += ['herself', 'him', 'himself', 'his', 'how', 'however']
palabrasvac += ['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed']
palabrasvac += ['interest', 'into', 'is', 'it', 'its', 'itself', 'keep']
palabrasvac += ['last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made']
palabrasvac += ['many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine']
palabrasvac += ['more', 'moreover', 'most', 'mostly', 'move', 'much','/div']
palabrasvac += ['must', 'my', 'myself', 'name', 'namely', 'neither', 'never']
palabrasvac += ['nevertheless', 'next', 'nine', 'no', 'nobody', 'none']
palabrasvac += ['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of']
palabrasvac += ['off', 'often', 'on','once', 'one', 'only', 'onto', 'or']
palabrasvac += ['other', 'others', 'otherwise', 'our', 'ours', 'ourselves']
palabrasvac += ['out', 'over', 'own', 'part', 'per', 'perhaps', 'please']
palabrasvac += ['put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed']
palabrasvac += ['seeming', 'seems', 'serious', 'several', 'she', 'should']
palabrasvac += ['show', 'side', 'since', 'sincere', 'six', 'sixty', 'so']
palabrasvac += ['some', 'somehow', 'someone', 'something', 'sometime','way']
palabrasvac += ['sometimes', 'somewhere', 'still', 'such', 'system', 'take']
palabrasvac += ['ten', 'than', 'that', 'the', 'their', 'them', 'themselves']
palabrasvac += ['then', 'thence', 'there', 'thereafter', 'thereby']
palabrasvac += ['therefore', 'therein', 'thereupon', 'these', 'they']
palabrasvac += ['thick', 'thin', 'third', 'this', 'those', 'though', 'three']
palabrasvac += ['three', 'through', 'throughout', 'thru', 'thus', 'to']
palabrasvac += ['together', 'too', 'top', 'toward', 'towards', 'twelve']
palabrasvac += ['twenty', 'two', 'un', 'under', 'until', 'up', 'upon']
palabrasvac += ['us', 'very', 'via', 'was', 'we', 'well', 'were', 'what']
palabrasvac += ['whatever', 'when', 'whence', 'whenever', 'where']
palabrasvac += ['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon']
palabrasvac += ['wherever', 'whether', 'which', 'while', 'whither', 'who']
palabrasvac += ['whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with','[',']','{','}']
palabrasvac += ['within', 'without', 'would', 'yet', 'you', 'your','%','<','>','-','and/or','*','$',':',';',"'s",'``']
palabrasvac += ['yours', 'yourself', 'yourselves','1','2','3','4','5','6','7','8','9','0']

topicsAll=[]
frecuencyAll=[]
topicsSubjects=[]
frecuencySubjects=[]
sorterListTopics=[]
titulo_all=[]
#Dataframe of words, termFrecuency and ITF

def termFrecuency(topicsSubjects,frecuencySubjects,topicsAll,frecuencyAll):
    cont=0
    
    for topicList in topicsSubjects:
        
        #result=[w for w in topicList if w in topics_resultALL]
        i=0
        wordSubjectTF=[]
        wordIDF=[]
        for topic in topicList:   
            if topic in topicsAll:
                #Indice dentro de el array de la asignatura
                indexTopic=topicList.index(topic)
                #Valor en frecuencia del Topic dentro del docuemnto de la asignatura
                valueFrecuencyTopic=frecuencySubjects[cont][indexTopic]

                #Tomo el indice de las palabras de cada asignatura en el array de las palabras de todos los docuemtos
                indexTopicGeneral=topicsAll.index(topic)
                #print(indexFrecuencyTopicGeneral)
                
                
                #Tomo el valor de la frecuencia de esa palabra en todos los documentos
                valueFrecuencyTopicGeneral=frecuencyAll[indexTopicGeneral]
                
                termFrecuencyWordSubject=valueFrecuencyTopic/len(frecuencySubjects[cont])

                #Esto seria columna 1 de la matriz de topic, tf idf de cada palabra en la asignatura
                wordSubjectTF.append(termFrecuencyWordSubject)

                #Calculo de TF-IDF
                
                index=topicsAll.index(topic)
                idfWordSubject=np.log(len(frecuencyAll)/frecuencyAll[index])


                #Esto seria columna 2 de la matriz de topic, tf idf de cada palabra en la asignatura
                wordIDF.append(idfWordSubject)
                

                listaSubject=[topic,valueFrecuencyTopic]
                listaTotal=[topic,valueFrecuencyTopicGeneral]

                #
                # print(listaSubject)
                # print(listaTotal)
                
            else:
                continue
                #print(topic)
        #Muestra el orden total de las principales palabras d ecada asigantura
        wordSubjectTopics=list(zip(topicList,wordSubjectTF,wordIDF))
        wordSortSubjectTopics=sorted(wordSubjectTopics,key=lambda row: (row[1],row[2]), reverse=True)
        
        first=wordSortSubjectTopics[0][1]
        last=wordSortSubjectTopics[-1][1]
        diferencia=(first-last)*0.10
        # print("*******************************************************")
        # print(wordSortSubjectTopics)
        for wordx in wordSortSubjectTopics:
            t=0
            j=t+1
            for wordy in wordSortSubjectTopics:
                #diferencia_aCTUAL=wordy[1]-wordSortSubjectTopics[j][1]
                
                if wordy[2]<wordSortSubjectTopics[j][2]:
                    
                    if wordy[1]-wordSortSubjectTopics[j][1]<diferencia:
                        aux=wordy
                        wordSortSubjectTopics[t]=wordSortSubjectTopics[j]
                        wordSortSubjectTopics[j]=aux
                    else:
                        continue
                else:
                    continue
                t=t+1
                if j > len(wordSortSubjectTopics):
                    break
                else:
                    j=t+1
                
        #print(str(wordSortSubjectTopics))

       
        sorterListTopics.append(wordSortSubjectTopics)
        # print(sorterListTopics)
        # print("************************************   topics_subject  *******************************")
        # print(sorterListTopics[-1])

        list_word_frecuancySUBJECTS=list(zip(topicsSubjects[cont], frecuencySubjects[cont]))
        list_word_frecuancyAllDoc=list(zip(topicsAll, frecuencyAll))
        #print("Esto esta relacionado a la Asignatura "+str(cont))
        cont=cont+1
        # print("************************************   topics_subject  *******************************")
        # print(list_word_frecuancySUBJECTS)
        # print("************************************   topics_total  *******************************")
        # print(list_word_frecuancyAllDoc)
    return sorterListTopics
        

def stop_wear(vocab,palabrasvac):
   
    return [s for s in vocab if s not in palabrasvac]
def wordCount(tokens):
   
    frecuenciaPalab=[]
    for n in tokens:
        frecuenciaPalab.append(tokens.count(n))
    return tokens, frecuenciaPalab

def vocabulario(tokens):
    stemmer= PorterStemmer()               
    
    for x in tokens:
        if ((x is int) or (len(x)<4)):            
            #print("**************   "+x+"  *************************")            
            tokens.remove(x)                  
        else:
            index=tokens.index(x)
            #Convert to lowercase           
            palabra1=x.lower()        
           
            #***********I think that is not necesary because STEM  limit the word an we need synonims
            
            # palabra3=stemmer.stem(palabra1)        
            # tokens[index]  = palabra3    
                    
            #Lemmatisation ***********I think that is not necesary because limit the word an we need synonims
            lem = WordNetLemmatizer()
            tokens[index]  = lem.lemmatize(palabra1)
                
    vocab = list(sorted(set(tokens)))
   
    words,frecuenciaPalab=wordCount(vocab)     
    
    

    list_word_frecuancy=list(zip(words, frecuenciaPalab))
    orden_lista=sorted(list_word_frecuancy,key=lambda row: row[1], reverse=True)
    # print("*************************************************")
    # print(orden_lista)
    
    return orden_lista
     
def writeTopics(sorterListTopics,subjects,titulo):
    contSubjects=0
    print(len(subjects))
    print(len(sorterListTopics))
    while len(sorterListTopics)>contSubjects:
        word,x,y=list(zip(*sorterListTopics[contSubjects]))
        finalTopicsSubjects=word
        if len(finalTopicsSubjects)<11:
            array=finalTopicsSubjects[:len(finalTopicsSubjects)]
            array_new=list(array)
            parte=titulo[contSubjects]
            array_new.extend(titulo[contSubjects])
            array=tuple(array_new)
            subjects[contSubjects]["topics"]=array
            with open('./data/subject-updated.json', 'w') as subjects_f:
            	subjects_f.write(json.dumps(subjects).encode("latin1"))                
        else:
            array=finalTopicsSubjects[:10]
            array_new=list(array)
            parte=titulo[contSubjects]
            array_new.extend(titulo[contSubjects])
            array=tuple(array_new)
            subjects[contSubjects]["topics"]=array
            with open('./data/subject-updated.json', 'w') as subjects_f:
                subjects_f.write(json.dumps(subjects).encode("latin1"))    
        contSubjects=contSubjects+1
       
        #print(finalTopicsSubjects)       
        
def miner(subjects,subjects_f):
    # Function to extract the description of every subject
    #i=0
    for subject in subjects:
        #i=i+1
        #if i ==2: break
        url = subject["url"]
        all_text=[]
        #page = urllib.request.urlopen(url)
        page=requests.get(url)
        
        status_code=page.status_code
        if status_code == 200:
            #print(url)
            # print the source code
            #print(page.content)
            u=0
            parsed_webpage = BeautifulSoup(page.content,"html.parser")
            

            p_tag = parsed_webpage.find_all('div',attrs={'class': 'tarea'})
            if p_tag==[]:
                print("This page is not"+ url)
                
                all_text=nltk.word_tokenize("This text is a defuault text when this page is empty, sorry comunicate this with administrators")
                # print(all_text)
            else:
                                
                for div in p_tag:
                    u=u+1
                    #print("El div que se ve es este"+str(u))
                    #all_text = "\n".join(nltk.word_tokenize(str(div)))
                    all_text.extend(nltk.word_tokenize(str(div)))
                    #print(all_text)
                    
            data=all_text  

            #Made process to Title 
            name = subject["name"]
            titulo=nltk.word_tokenize(str(name))
            titulo = [word for word in titulo if word.isalpha()]
            titulo=stop_wear(titulo,palabrasvac)
            clean_titulo,frequency_title=zip(*vocabulario(titulo))
            titulo_all.append(clean_titulo)
            
            # symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
            # for k in symbols:
            #     text = np.char.replace(data, k, ' ')
            words = [word for word in data if word.isalpha()]
            tokensSubjects=stop_wear(words,palabrasvac) 
            #tokensSubjects = [x.replace('"!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n="','') for x in tokensSubjects]
            
            # tokensSubjects1 = [x.replace('\n','') for x in tokensSubjects0]
            # tokensSubjects2=[x.replace('\\n','') for x in tokensSubjects1]
            # tokensSubjects3=[x.replace('.-','') for x in tokensSubjects2]
            # tokensSubjects4=[x.replace('-','') for x in tokensSubjects3]
            # tokensSubjects5=[x.replace('.t','') for x in tokensSubjects4]
            # tokensSubjects6=[x.replace('\\','') for x in tokensSubjects5]
            # tokensSubjects7=[x.replace("''",'') for x in tokensSubjects6]
            # tokensSubjects8=[x.replace("  ",'') for x in tokensSubjects7]
            # tokensSubjects9=[x.replace("&lt;/?.*?&gt;"," &lt;&gt; ") for x in tokensSubjects0]
            # tokensSubjects10=[x.replace("(\\d|\\W)+><="," ") for x in tokensSubjects9]
            # tokensSubjects=[x.replace('[^a-zA-Z]', ' ') for x in tokensSubjects10]
           
            unique_words=vocabulario(tokensSubjects)
            

            topics_result,frecuency=zip(*unique_words)
                
            #Add todos las palabras de los documentos que no estan agragadas a un array final
            for chart in topics_result:
                if chart in topicsAll:
                    index=topics_result.index(chart)
                    chartFrecuency=frecuency[index]
                    indexTotal=topicsAll.index(chart)
                    frecuencyAll[indexTotal]=frecuencyAll[indexTotal]+chartFrecuency
                else:
                    topicsAll.append(chart)  
                    index=topics_result.index(chart)   
                            
                    frecuencyAll.append(frecuency[index])

            topicsSubjects.append(topics_result)

            frecuencySubjects.append(frecuency)    
                    #print(str(topics_result))
        else:
            print("This page is not"+ url)
                
    return topicsAll,frecuencyAll,topicsSubjects,frecuencySubjects,titulo_all



        
if __name__ == "__main__":
    
    # Open subjects file and get each subject object
    with open("./data/subject-updated.json") as subjects_f:
        subjects =json.load(subjects_f)
    
    #Scraping and data process information of all page web
    topicsAll,frecuencyAll,topicsSubjects,frecuencySubjects,titulo_all=miner(subjects,subjects_f)
  
    #get the general information of all topics possibles in all data get 
    listWordFrecuencyAll=list(zip(topicsAll,frecuencyAll))
   
    #Obtained a list for subjects where in each subject get the word acord the FT and IFT
    #  how many times the word is in the text and how important and popular is
    sorterListTopics=termFrecuency(topicsSubjects,frecuencySubjects,topicsAll,frecuencyAll)

    #Write the selections topics in the subjects json
    writeTopics(sorterListTopics,subjects,titulo_all)