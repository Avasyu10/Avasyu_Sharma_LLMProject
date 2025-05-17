import unittest
from flask import Flask
from flask_testing import FlaskClient
from app.main import create_app
import json
import os

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        os.makedirs(self.app.config['UPLOAD_FOLDER'], exist_ok=True)

    def tearDown(self):
        
        import shutil
        if os.path.exists(self.app.config['UPLOAD_FOLDER']):
            shutil.rmtree(self.app.config['UPLOAD_FOLDER'])
        self.app_context.pop()

    def test_upload_route(self):
       
        with open(os.path.join(self.app.config['UPLOAD_FOLDER'], "test_file.txt"), "w") as f:
            f.write("test content")

        with open(os.path.join(self.app.config['UPLOAD_FOLDER'], "test_file.txt"), "rb") as f:
            response = self.client.post(
                "/upload",
                data={"files": (f, "test_file.txt")},
                content_type="multipart/form-data",
            )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode("utf-8"))
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Files uploaded successfully")
        self.assertIn("metadata", data)

    def test_query_route(self):
        
        response = self.client.post(
            "/query",
            json={"query": "What is the content of the document?"}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode("utf-8"))
        self.assertIn("results", data)

    def test_metadata_route(self):
        response = self.client.get("/metadata")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode("utf-8"))
        self.assertIn("documents", data)

if __name__ == "__main__":
    unittest.main()