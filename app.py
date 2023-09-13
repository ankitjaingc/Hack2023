from flask import Flask, request
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
from pathlib import Path
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

 

import os
os.environ["OPENAI_API_KEY"] = ""

 

app = Flask(__name__)
 
@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/post_json', methods=['POST'])
def process_json():
    content_type = request.headers.get('Content-Type')
    print(content_type)
    if (content_type == 'application/json'):
        json = request.get_json()

        print(json["name"])

        return json
    else:
        return 'Content-Type not supported!'

@app.route('/post_query', methods=['POST'])
def process_json():
    content_type = request.headers.get('Content-Type')
    print(content_type)
    if (content_type == 'application/json'):
        json = request.get_json()
        raw_text = ''
        for p in Path('data').glob('*.pdf'):
            reader = PdfReader('data\\' + p.name)
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    raw_text += text
        text_splitter = CharacterTextSplitter(        
            separator = "\n",
            chunk_size = 1000,
            chunk_overlap  = 200,
            length_function = len,
        )
        texts = text_splitter.split_text(raw_text)
        embeddings = OpenAIEmbeddings()
        docsearch = FAISS.from_texts(texts, embeddings)
        chain = load_qa_chain(OpenAI(), chain_type="stuff")
        query = json["name"]
        docs = docsearch.similarity_search(query)
        return chain.run(input_documents=docs, question=query)
    else:
        return 'Content-Type not supported!'    
 
# main driver function
if __name__ == '__main__':
    app.run(debug=True)