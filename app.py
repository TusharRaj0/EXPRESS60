# Final backend for Express60
import heapq
import re
from flask import Flask, render_template, request, jsonify
from newspaper import Article
from nltk.tokenize import sent_tokenize,word_tokenize

import nltk
nltk.download('punkt_tab')


# create a flask server
app = Flask(__name__)


# route index.html file as the home page
@app.route('/')
def index():
    return render_template('index.html')
    # return render_template('i.html')

# summarise Logic
@app.route('/summarize', methods=['POST'])
def summarize():
    # Extract the article URL from the POST request
    article_url = request.json.get('url')
    
    # Fetch the article using Newspaper3k
    article = Article(article_url)
    try:
        article.download()
    except:
        summary=""
        return jsonify({'summary': summary})
    article.parse()
    article.nlp() 
    # summary=article.summary    -using inbuilt functions
    text=article.text

# SUMMARISATION DONE MANUALLY
    # Step 1: Preprocess the text
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    sentences = sent_tokenize(text)  # Sentence tokenization
    words = word_tokenize(text.lower())  # Word tokenization (lowercased)

    # Manually defined stopwords
    manual_stopwords = {"is", "a", "of", "that", "the", "and", "it", "such", "as", "in"}

    # Remove manually defined stopwords & punctuation
    word_frequencies = {}
    for word in words:
        if word.isalnum() and word not in manual_stopwords:  # Exclude stopwords & punctuation
            word_frequencies[word] = word_frequencies.get(word, 0) + 1

    # Step 2: Normalize word frequency (DIVIDE EACH BY MAX-FREQUENCY)
    max_freq = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] /= max_freq  # Normalize values

    # Step 3: Score sentences based on word importance (ranking of sentences)
    sentence_scores = {}  #this will have sentences and its score(key,value pair)
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in word_frequencies:
                # add word frquencies of all words in a sentence 
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word]

    # Step 4: Extract top-ranked sentences as the summary
    summary_length = 4 #Here k=4
    # create a heap using sentence_scores and use the "value" to construct the heap  
    summary_sentences = heapq.nlargest(summary_length, sentence_scores, key=sentence_scores.get)

    # Final Summary
    summary = " ".join(summary_sentences)
    
    

    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)