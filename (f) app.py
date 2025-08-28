from flask import Flask, render_template, request, jsonify
from newspaper import Article


# create a flask server
app = Flask(__name__)

# route index.html file as the home page
@app.route('/')
def index():
    return render_template('index.html')
    # return render_template('i.html')


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
    summary=article.summary

    return jsonify({'summary': summary})

# starting 
if __name__ == '__main__':
    app.run(debug=True)
