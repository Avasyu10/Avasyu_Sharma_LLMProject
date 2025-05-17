
class DocumentMetadata:
    def __init__(self, filename, page_count, chunk_count):
        self.filename = filename
        self.page_count = page_count
        self.chunk_count = chunk_count

    def to_dict(self):
        return {
            'filename': self.filename,
            'page_count': self.page_count,
            'chunk_count': self.chunk_count
        }