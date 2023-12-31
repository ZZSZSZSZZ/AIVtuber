from typing import List
from document.document import BaseLoader
from document.document import Document


class TestLoader(BaseLoader):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> List[Document]:
        return [Document(page_content='text1', metadata={'test': 111}),
                Document(page_content='text2', metadata={'test': 222})]
