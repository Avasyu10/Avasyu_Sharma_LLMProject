from flask import request, jsonify, current_app
from app import processing
from app.utils import allowed_file, handle_errors
import os
from app.main import app

@app.route('/')
def index():
    return "Hello, this is the PanScience Innovations LLM Specialist Application!"

@app.route('/upload', methods=['POST'])
@handle_errors
def upload_files():
    if 'files' not in request.files:
        return jsonify({'error': 'No files part'}), 400
    files = request.files.getlist('files')
    metadata = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            doc_metadata = processing.process_document(filename, current_app.db)
            metadata.append(doc_metadata)
        else:
            return jsonify({'error': f'File type not allowed for {file.filename}'}), 400
    return jsonify({'message': 'Files uploaded successfully', 'metadata': metadata}), 201

@app.route('/query', methods=['POST'])
@handle_errors
def query_documents():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    results = processing.query_documents(query, current_app.db)
    return jsonify({'results': results}), 200

@app.route('/metadata', methods=['GET'])
@handle_errors
def get_metadata():
    documents = list(current_app.db.documents.find({}))
    
    for doc in documents:
        doc['_id'] = str(doc['_id'])
    return jsonify({'documents': documents}), 200
