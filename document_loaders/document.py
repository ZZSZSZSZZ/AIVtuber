from typing import NamedTuple


class Document(NamedTuple):
    """用于存储一段文本和相关元数据的类"""
    page_content: str
    """用于存储一段文本和相关元数据的类"""
    metadata: dict
    """Arbitrary metadata about the page content (e.g., source, relationships to other
            documents, etc.).
        """