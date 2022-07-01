from dataclasses import dataclass
from typing import Optional
from ebooklib.epub import EpubBook


@dataclass
class Document:
    id: str
    toc_parent: Optional[str]
    order: int
    linear: str


def map_id_to_href(book: EpubBook) -> dict[str, str]:
    id_to_href = {}
    for link in book.toc:
        document = book.get_item_with_href(link.href)

        if not document:
            raise KeyError(f"Item with href {link.href} not found")

        id_to_href[document.id] = link.href

    return id_to_href


def get_document_list(book: EpubBook) -> list[Document]:
    documents = []
    current_href = None
    id_to_href = map_id_to_href(book)

    for order, (spine_id, linear) in enumerate(book.spine):

        if spine_id in id_to_href:
            current_href = id_to_href[spine_id]

        documents.append(
            Document(
                id=spine_id,
                toc_parent=current_href,
                order=order,
                linear=linear,
            )
        )
    return documents
