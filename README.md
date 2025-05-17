# LLM Specialist Assignment - PanScience Innovations

## Overview

This project implements a Retrieval-Augmented Generation (RAG) pipeline that allows users to upload documents and ask questions based on their content. The system utilizes:

* **Document Ingestion & Processing:** For handling user-uploaded documents (up to 20 files, max 1000 pages each), chunking their content, and generating text embeddings.
* **Vector Database (ChromaDB):** For efficient storage and retrieval of document embeddings.
* **LLM API (Hugging Face):** For generating contextual responses based on retrieved document chunks and user queries.
* **Flask:** As the REST API framework.
* **MongoDB:** For storing metadata about the processed documents.
* **Docker:** For containerizing the entire application for easy deployment.

## Setup and Installation Instructions

Follow these steps to set up and run the application on your local machine.

### Prerequisites

* **Docker:** Ensure you have Docker installed on your system. You can download it from [https://www.docker.com/get-started](https://www.docker.com/get-started).
* **Docker Compose:** Docker Compose is usually installed with Docker Desktop. If you installed Docker Engine separately, you might need to install Docker Compose as well.
* **Python:** Python 3.x is required.

### Installation Steps

1.  **Clone the Repository:**

    ```bash
    git clone <YOUR_GITHUB_REPOSITORY_LINK>
    cd <YOUR_REPOSITORY_NAME>
    ```

2.  **Set up a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    venv\Scripts\activate  # On Windows
    ```

3.  **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables:**

    Create a `.env` file in the root directory of the project and add the following environment variables:

    ```env
    MONGO_URI=<YOUR_MONGODB_CONNECTION_STRING>
    MONGO_DB_NAME=<YOUR_MONGODB_DATABASE_NAME>
    HUGGING_FACE_API_KEY=<YOUR_HUGGING_FACE_API_KEY> #  Hugging Face API Key
    # Add other API keys or configuration as needed
    ```

    **Note:** Replace the placeholder values with your actual connection strings and API keys.

5.  **Build and Run Docker Containers:**

    ```bash
    docker compose up --build -d
    ```

    This command will build the Docker image for the web application and start the containers in detached mode.

6.  **Access the Application:**

    The API will be accessible at `http://localhost:5000`.

## API Usage and Testing Guidelines

The application exposes the following REST API endpoints:

### 1. Uploading Documents (`/upload`)

* **Endpoint:** `/upload`
* **HTTP Method:** `POST`
* **Request Body (Form Data):**
    * Key: `files[]`
    * Value: One or more PDF files to upload. You can include multiple files with the same key.
* **Example using `curl`:**

    ```bash
    curl -X POST -F "files=@path/to/your/document1.pdf" -F "files=@path/to/your/document2.pdf" http://localhost:5000/upload
    ```

* **Example using Postman:**

    1.  Create a new `POST` request to `http://localhost:5000/upload`.
    2.  Go to the "Body" tab and select `form-data`.
    3.  Add a key named `files`. Set the "Type" to `File` and select your PDF file. You can add more `files` keys for multiple uploads.
* **Response (JSON):**

    ```json
    {
        "message": "Files uploaded successfully",
        "metadata": [
            {
                "filename": "document1.pdf",
                "page_count": 10,
                "chunk_count": 50
            },
            {
                "filename": "document2.pdf",
                "page_count": 5,
                "chunk_count": 25
            }
            // ... more metadata for each uploaded file
        ]
    }
    ```

### 2. Querying the System (`/query`)

* **Endpoint:** `/query`
* **HTTP Method:** `POST`
* **Request Body (JSON):**

    ```json
    {
        "query": "What are the key requirements of this project?"
    }
    ```

* **Example using `curl`:**

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"query": "What are the key requirements of this project?"}' http://localhost:5000/query
    ```

* **Example using Postman:**

    1.  Create a new `POST` request to `http://localhost:5000/query`.
    2.  Go to the "Body" tab and select `raw`.
    3.  Choose `JSON` from the dropdown menu.
    4.  Enter your query in the JSON format as shown above.
* **Response (JSON):**

    ```json
    {
        "results": "The key requirements of this project include document ingestion and processing, implementing a Retrieval-Augmented Generation (RAG) pipeline, building a REST API with specific endpoints, and containerizing the application using Docker for deployment."
    }
    ```

    **(Note:** The actual response will depend on the LLM and the content of your uploaded documents.)

### 3. Viewing Processed Document Metadata (`/metadata`)

* **Endpoint:** `/metadata`
* **HTTP Method:** `GET`
* **Request Body:** None
* **Example using `curl`:**

    ```bash
    curl http://localhost:5000/metadata
    ```

* **Example using Postman:**

    1.  Create a new `GET` request to `http://localhost:5000/metadata`.
    2.  Click the "Send" button.
* **Response (JSON):**

    ```json
    {
        "documents": [
            {
                "_id": "6464b7c8b3e09c7a1c8a2d3f",
                "filename": "document1.pdf",
                "page_count": 10,
                "chunk_count": 50
            },
            {
                "_id": "6464b811b3e09c7a1c8a2d40",
                "filename": "document2.pdf",
                "page_count": 5,
                "chunk_count": 25
            }
            // ... metadata for all processed documents
        ]
    }
    ```

    **(Note:** The `_id` is the MongoDB ObjectId, which has been converted to a string for JSON serialization.)

## Configuration Details for Using Hugging Face Models

To use a Hugging Face model:

1.  Ensure you have the `sentence-transformers` library installed:
    ```bash
    pip install sentence-transformers
    ```

2.  Set the `HUGGING_FACE_API_KEY` in your `.env` file.  While `sentence-transformers`  does not always require an API key, some models or operations might.

3.  The application is configured to use the `all-MiniLM-L6-v2` model by default.  If you want to use a different model, you can change the  `embedding_model = SentenceTransformer('your-model-name')`  line in  `app/processing.py`.

## Automated Tests


For example:

* Unit tests are located in the `tests/unit` directory. You can run them using `pytest tests/unit`.
* Integration tests are in the `tests/integration` directory and test the interaction between different modules. Run them with `pytest tests/integration`.

