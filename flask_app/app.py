from sklearn.datasets import fetch_20newsgroups
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from flask import Flask, render_template, request, jsonify ,send_file
import os

newsgroups = fetch_20newsgroups(subset='all')


def term_document_matrix(data):
    documents = data.data


    term_count = TfidfVectorizer(stop_words='english', max_features=1000)
    tfidf_matrix = term_count.fit_transform(documents)

    return tfidf_matrix


def qeury_matrix(input):
    term_count = TfidfVectorizer(stop_words='english', max_features=1000)
    tfidf_matrix = term_count.fit_transform(input)

    return tfidf_matrix

def apply_svd(data , n , input):
    
    svd = TruncatedSVD(n_components=n)
    input_matrix = svd.fit_transform(input)
    doc_matrix = svd.fit_transform(data)

    return doc_matrix , input_matrix


def calculating_cosine(Q_vector , D_vectors):

    query_norm = np.linalg.norm(Q_vector)
    normalized_query = Q_vector / query_norm

    document_norms = np.linalg.norm(D_vectors, axis=1)
    normalized_documents = D_vectors / document_norms[:, np.newaxis]

    cosine_similarities = np.dot(normalized_documents, normalized_query)

    return cosine_similarities

def top5(cosine_similarities):
    
    top5_index = []

    for _ in range(5):
        index = np.argmax(cosine_similarities)
        
        top5_index.append(index)
        
        cosine_similarities[index] = -np.inf

    top5_texts = [newsgroups.data[i] for i in top5_index]
    
    return top5_texts



app = Flask(__name__)
app.secret_key = os.urandom(24)

tfidf_matrix = []


@app.route('/')
def index():
    global tfidf_matrix
    tfidf_matrix = term_document_matrix(newsgroups)
    
    return render_template('index.html')


def query():
    global tfidf_matrix
    input = request.get_json()
    qeury_matrix = qeury_matrix(input)
    apply_svd( tfidf_matrix , 100 , qeury_matrix)


if __name__ == '__main__':
    app.run(debug=True)

