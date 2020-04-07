import re
import nltk
import pandas
from matplotlib import pyplot as plt
#nltk.download('stopwords')
from nltk.corpus import stopwords

# nltk.download('wordnet') 
from nltk.stem.wordnet import WordNetLemmatizer

# Creating a vector of word counts
from sklearn.feature_extraction.text import CountVectorizer



##Creating a list of stop words and adding custom stopwords
stop_words = set(stopwords.words("english"))
##Creating a list of custom stopwords
new_words = ["following", "student", "course","using", "show", "result", "large", "also", "iv", "one", "two", "new", "previously", "shown"]
stop_words = stop_words.union(new_words)

def clean(data):
    #Remove punctuations
    text = re.sub('[^a-zA-Z]', ' ', data)

    #Convert to lowercase
    text = text.lower()

    #remove tags
    text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)

    # remove special characters and digits
    text=re.sub("(\\d|\\W)+"," ",text)

    ##Convert to list from string
    text = text.split()

    #Lemmatisation
    lem = WordNetLemmatizer()
    text = [lem.lemmatize(word) for word in text if not word in  
            stop_words] 
    text = " ".join(text)
    
    return text


def get_top_n_words(corpus, n=None):
    vec = CountVectorizer().fit(corpus)
    bag_of_words = vec.transform(corpus)
    
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in      
                   vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], 
                       reverse=True)
    top_words = words_freq[:n]
    top_df = pandas.DataFrame( top_words )
    top_df.columns=["Word", "Freq"]
    return top_df



def get_top_n2_words(corpus, n=None):
    vec1 = CountVectorizer(ngram_range=(2,2),  
            max_features=2000).fit(corpus)
    bag_of_words = vec1.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in     
                  vec1.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], 
                reverse=True)
    top2_words = words_freq[:n]
    top2_df = pandas.DataFrame( top2_words )
    top2_df.columns=["Word", "Freq"]
    return top2_df

# corpus = clean([data])
# top_words = get_top_n_words(corpus, n=10)

# # # #Barplot of most freq words
# import seaborn as sns
# sns.set(rc={'figure.figsize':(13,8)})
# g = sns.barplot(x="Word", y="Freq", data=top_words)
# g.set_xticklabels(g.get_xticklabels(), rotation=30)
# plt.show()