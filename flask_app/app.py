from sklearn.datasets import fetch_20newsgroups
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from flask import Flask, render_template, request, jsonify ,send_file
import os

newsgroups = fetch_20newsgroups(subset='all')


def term_document_matrix(data , term_count):
    documents = data.data

    tfidf_matrix = term_count.fit_transform(documents)


    return tfidf_matrix


def qeury_matrix(input, term_count):
   
    tfidf_matrix = term_count.transform([input])

    return tfidf_matrix

def apply_svd(data , n , input):
    
    svd = TruncatedSVD(n_components=n)
    
    doc_matrix = svd.fit_transform(data)
    input_matrix = svd.transform(input)

    return doc_matrix , input_matrix


def calculating_cosine(Q_vector , D_vectors):

    query_norm = np.linalg.norm(Q_vector)
    normalized_query = (Q_vector / query_norm).flatten() 

    document_norms = np.linalg.norm(D_vectors, axis=1)
    normalized_documents = D_vectors / document_norms[:, np.newaxis]

    cosine_similarities = np.dot(normalized_documents, normalized_query)

    return cosine_similarities

def top5(cosine_similarities):

    print(f"Number of cosine similarities: {len(cosine_similarities)}")

    
    

    top_indices = np.argsort(cosine_similarities)[-5:][::-1]  
    print(f"Top indices: {top_indices}")
    top5_texts = [newsgroups.data[i] for i in top_indices]
    cosine_doc = [(float(cosine_similarities[i]), int(i)) for i in top_indices]
    
    return top5_texts , cosine_doc
    
    



app = Flask(__name__)
app.secret_key = os.urandom(24)

tfidf_matrix = []
term_count = []

@app.route('/')
def index():
    global tfidf_matrix , term_count

    term_count = TfidfVectorizer(stop_words='english', max_features=1000)
    tfidf_matrix = term_document_matrix(newsgroups, term_count)
   
    
    return render_template('index.html')

@app.route('/search' , methods = ['POST'])
def query():
    global tfidf_matrix , term_count


    input_data = request.get_json()
    user_query = input_data.get('query', '')

    qeury = qeury_matrix(user_query , term_count)
    
    D_vectors , Q_vector = apply_svd( tfidf_matrix , 85 , qeury)
    cosine_similarities = calculating_cosine(Q_vector , D_vectors)
    top5_results , cosine_doc = top5(cosine_similarities)
    


    return jsonify({'top5_results': top5_results, 'cosine_doc': cosine_doc} )

if __name__ == '__main__':
    app.run(debug=True)

