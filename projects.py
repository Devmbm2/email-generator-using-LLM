import pandas as pd
import chromadb
import uuid


class ProjectCollection:
    def __init__(self, file_path="resource/portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorDB')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_projects(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def search_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
