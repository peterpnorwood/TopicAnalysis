### Importing Pacakges
import pandas as pd
import sys
from matplotlib import pyplot as plt
import warnings
import sklearn as sk
import numpy as np
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import string
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF
import datetime as dt

emails = "" ## the file in this instance

### Creating a year and month variable from the dates variable and cleaning those up

emails["year"] = emails["dates"].str[:4]
emails["month"] = emails["dates"].str[5:7].str.replace('-','')
    
emails = emails[(emails.year != "NA") & (emails.month != "NA")]
emails["year"] = pd.to_numeric(emails["year"], downcast="integer")
emails["month"] = pd.to_numeric(emails["month"],downcast = "integer")

### NMF Topic Analysis

warnings.filterwarnings("ignore")

## Parameter Setting
no_features = 1000
no_topics = 10
no_top_words = 20
no_top_documents = 5

## Punctuation to exclude
exclude = set(string.punctuation)

## Stop Words, taken from other code, a few added
stop = ["ourselves", "hers", "between", "yourself", "but", "again", "there", "about", "once", "during", "out", "very", "having", "with", "they", "own", "an", "be", "some", "for", "do", "its", "yours", "such", "into", "of", "most", "itself", "other", "off", 
        "is", "s", "am", "or", "who", "as", "from", "him", "each", "the", "themselves", "until", "below", "are", "we", "these", "your", "his", "through", "don", "nor", "me", "were", "her", "more", "himself", "this", "down", "should", "our", "their", "while",
        "above", "both", "up", "to", "ours", "had", "she", "all", "no", "when", "at", "any", "before", "them", "same", "and", "been", "have", "in", "will", "on", "does", "yourselves", "then", "that", "because", "what", "over", "why", "so", "can", "did", "not",
        "now", "under", "he", "you", "herself", "has", "just", "where", "too", "only", "myself", "which", "those", "i", "after", "few", "whom", "t", "being", "if", "theirs", "my", "against", "a", "by", "doing", "it", "how", "further", "was", "here", "than",
        "com", "www", "http", "https", "ve","pgp","signed", "redhat"]


## Thanks to Aneesh Bakha for providing these next to functions
## found at https://towardsdatascience.com/improving-the-interpretation-of-topic-models-87fd2ee3847d

## Function to remove stop words and punctuation
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    return punc_free

## Function to Display Top Topics
def display_topics(H, W, feature_names, documents, no_top_words, no_top_documents):
    for topic_idx, topic in enumerate(H):
        print "Topic %d:" % (topic_idx)
        print " ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]])
        top_doc_indices = np.argsort( W[:,topic_idx] )[::-1][0:no_top_documents]
        for doc_index in top_doc_indices:
            print documents[doc_index]

            
## Dropping the duplicate subjects
cond_emails = emails.drop_duplicates("subjects")

## Making the subject line lowercase
cond_emails["subjects"] = cond_emails["subjects"].str.lower()

## Removing "RedHat" and "Red Hat" from the subject lines, creates for more diverse topics, not just a bunch of "Red Hat _____" unrelated topics
cond_emails["subjects"] = cond_emails["subjects"].str.replace('red hat', ' ')
cond_emails["subjects"] = cond_emails["subjects"].str.replace("redhat", ' ')

## Looping through each year
for i in range(1998,2019):
    
    ## Subsetting the current year and cleaning the subjects up
    year = cond_emails[cond_emails.year == i].fillna(' ')
    year_clean = list(year["subjects"])

    # NMF is able to use tf-idf
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words=stop)
    tfidf = tfidf_vectorizer.fit_transform(year_clean)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()
    
    # Run NMF
    nmf_model = NMF(n_components=no_topics, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(tfidf)
    nmf_W = nmf_model.transform(tfidf)
    nmf_H = nmf_model.components_

    print("\r\n Year %d" % (i))
    display_topics(nmf_H, nmf_W, tfidf_feature_names, year_clean, no_top_words, no_top_documents)
