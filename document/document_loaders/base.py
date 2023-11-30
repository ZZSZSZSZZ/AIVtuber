from abc import ABC, abstractmethod
from document.document import Document
from typing import List, Optional


class BaseLoader(ABC):
    """
    加载文档的接口
    """

    @abstractmethod
    def load(self) -> List[Document]:
        """将数据加载到 Document对象中。"""

    def load_and_split(self, text_splitter: Optional[TextSplitter] = None) -> List[Document]:
        """Load Documents and split into chunks. Chunks are returned as Documents.

        Args:
            text_splitter: TextSplitter instance to use for splitting documents.
              Defaults to RecursiveCharacterTextSplitter.

        Returns:
            List of Documents.
        """
        if text_splitter is None:
            _text_splitter: TextSplitter = RecursiveCharacterTextSplitter()
        else:
            _text_splitter = text_splitter
        docs = self.load()
        return _text_splitter.split_documents(docs)
