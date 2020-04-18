import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.stem.snowball import SnowballStemmer
# Starting with the CountVectorizer/TfidfTransformer approach...
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from itertools import islice

import nltk
nltk.download('punkt')
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
palabrasvac += ['some', 'somehow', 'someone', 'something', 'sometime']
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
palabrasvac += ['within', 'without', 'would', 'yet', 'you', 'your','%','<','>','-','and/or','*','$',':']
palabrasvac += ['yours', 'yourself', 'yourselves','1','2','3','4','5','6','7','8','9','0']

#def insert_topic_subject(topics,subject,subjects_f,):    
       
     

    #subjects_f.seek(0)
    #subjects_f.write(json.dumps(subject))
    #subjects_f.truncate()
    #del subject["topics"]

    #old_topics = subject["topics"]
    #print(old_topics)
    #for t in old_topics:
        #del old_topics[t]
    
    #page = requests.get(url)
    #print(page)
def stop_wear(vocab,palabrasvac):
   
    return [w for w in vocab if w not in palabrasvac]

def vocabulario(tokens):
    words = [w.lower() for w in tokens]
    #print(type(words))
    frecuenciaPalab=[]
    for w in words:
        frecuenciaPalab.append(words.count(w)) 
    
    vocab = list(sorted(set(words)))
    
    for w in vocab:
        if ((w is int) or (len(w)<4 )):
            
            print("**************   "+w+"  *************************")            
            vocab.remove(w)        
        else:
            pass

    vocab_need=stop_wear(vocab,palabrasvac)
    list_word_frecuancy=list(zip(vocab_need, frecuenciaPalab))
    orden_lista=sorted(list_word_frecuancy,key=lambda row: row[1], reverse=True)
    

    #print("Pares\n" +str(orden_lista))
    #print(type(vocab))
    #print(vocab)
    return orden_lista

def miner(subjects,subjects_f):
    # Function to extract the description of every subject
    i=0
    for subject in subjects:
        url = subject["url"]
        
        #page = urllib.request.urlopen(url)
        page=requests.get(url)
        
        status_code=page.status_code
        if status_code == 200:
            print(url)
            # print the source code
            #print(page.content)
                
            parsed_webpage = BeautifulSoup(page.content,"html.parser")
            #parsed_webpage=parsed_webpage.get_text()

            p_tag = parsed_webpage.find_all('div',attrs={'class': 'tarea'})
            if p_tag==[]:
                continue
            else:
                #p_tag = parsed_webpage.findAll('div')
                all_text=[]
                for div in p_tag:
                    print(div.text)
                    all_text.append(div)
                
                tokens = nltk.word_tokenize(str(all_text))
                
                unique_words=vocabulario(tokens)
                print(str(unique_words))
                topics_result, frecuency=zip(*unique_words[:10])

                print(str(topics_result))
                subject["topics"] = topics_result
                with open('data/subjects.json', 'w') as subjects_f:
                    subjects_f.write(json.dumps(subjects))    
        
       

if __name__ == "__main__":
    # Open subjects file and get subject object
    with open("data/subjects.json") as subjects_f:
        subjects =  json.load(subjects_f)
    
    miner(subjects,subjects_f)
    
    #clean_topics = cleaner(topics)
    #top_words = extract_kwargs(clean_topics)

    #top_words.to_json("topics.json", orient='records')