from dataclasses import dataclass
from typing import Optional
from ebooklib import epub


@dataclass
class Chapter:
    id: str
    order: int
    name: Optional[str]
    linear: str


def get_chapter_list(book: epub.EpubBook):
    # Convert TOC from href->name to id->name
    id_to_title = {}
    for link in book.toc:
        target_document = book.get_item_with_href(link.href)

        if not target_document:
            raise KeyError(f"Item with href {link.href} not found")

        id_to_title[target_document.id] = link.title

    chapters = []
    for order, (spine_id, linear) in enumerate(book.spine):
        chapters.append(
            Chapter(
                id=spine_id,
                order=order,
                name=id_to_title.get(spine_id, None),
                linear=linear,
            )
        )
    return chapters
