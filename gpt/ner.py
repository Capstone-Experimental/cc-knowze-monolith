import nltk
import json
from nltk.corpus import stopwords

# nltk.download('punkt')
# nltk.download('stopwords')

def detect_entities(text):
    stop_words = set(stopwords.words('indonesian'))
    
    # test
    more_stopwords = [
        'bermimpi',
        'membuat',
        'tutorial',
        'cara',
        'membeli',
        'meningkatkan',
        'penjualan',
    ]

    words = nltk.word_tokenize(text=text)
    filtered_words = [word for word in words if word not in stop_words and word not in more_stopwords]

    tagged_words = nltk.pos_tag(filtered_words)

    nouns = []

    for word, tag in tagged_words:
        if tag.startswith('NN'):
            nouns.append(word)
            
    if len(nouns) == 1:
        nouns = nouns[0].strip()
            
    elif len(nouns) > 1:
        str_nouns = ""
        for noun in nouns:
            str_nouns += noun + " "
        nouns = str_nouns
    
    elif len(nouns) == 0:
        nouns = None
    
    return nouns