from app import llm_api
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer  
import uuid
import os
import chromadb  


embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


chroma_client = chromadb.Client() 

vector_db = chroma_client.create_collection("my_rag_collection")

def process_document(filepath, db):
    text = extract_text(filepath)
    chunks = chunk_text(text)
    embeddings = generate_embeddings(chunks)
    ids = [str(uuid.uuid4()) for _ in chunks]

    
    vector_db.add(
        embeddings=embeddings,
        documents=chunks,
        ids=ids
    )

    metadata = {
        'filename': os.path.basename(filepath),
        'page_count': get_page_count(filepath),
        'chunk_count': len(chunks)
    }
    result = db.documents.insert_one(metadata)
    inserted_id = str(result.inserted_id)  
    metadata['_id'] = inserted_id 
    return metadata


def extract_text(filepath):
    if filepath.endswith('.pdf'):
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
   
    else:
        with open(filepath, 'r') as file:
            return file.read()


def get_page_count(filepath):
    if filepath.endswith('.pdf'):
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            return len(reader.pages)
        return 1



def chunk_text(text, chunk_size=500, chunk_overlap=100):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return text_splitter.split_text(text)



def generate_embeddings(texts):
    return embedding_model.encode(texts).tolist()



def query_documents(query, db):
    query_embedding = embedding_model.encode([query]).tolist()

    
    results = vector_db.query(
        query_embeddings=query_embedding,
        n_results=5  
    )
    relevant_chunks = results['documents'][0] 

    context = " ".join(relevant_chunks)  
    llm_response = llm_api.query_llm(context, query)
    return llm_response
