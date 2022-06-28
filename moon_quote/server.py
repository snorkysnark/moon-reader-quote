from multiprocessing import Process
from dataclasses import dataclass
import atexit

from flask import Flask
from ebooklib.epub import EpubBook
from selenium.webdriver import Chrome
import fuzzysearch

from moon_quote.book import Chapter


CUTOFF_FRACTION = 4


def map_id_to_content(book: EpubBook) -> dict[str, str]:
    spine_map = {}

    for spine_id, linear in book.spine:
        content = book.get_item_with_id(spine_id).content  # type:ignore
        spine_map[spine_id] = content

    return spine_map


def fuzzyfind(
    subsequence: str, sequence: str, max_distance: int
) -> list[fuzzysearch.Match]:
    distance = min(round(len(subsequence) / CUTOFF_FRACTION), max_distance)

    return fuzzysearch.find_near_matches(subsequence, sequence, max_l_dist=distance)


@dataclass
class SearchResult:
    text: str
    cfi: str
    distance: int


class BookServer:
    def __init__(self, book: EpubBook, port: int = 5000) -> None:
        app = Flask("moon-quote")

        spine_items = map_id_to_content(book)

        @app.route("/book/<path:filename>")
        def book_item(filename):
            return spine_items[filename]

        server = Process(target=app.run, args=(None, port))
        server.start()
        atexit.register(server.kill) # Kill flask when this process dies

        self.server = server
        self.browser = Chrome()
        self.base_url = f"http://127.0.0.1:{port}"
        self.chapter_path = ""

    def close(self):
        self.browser.close()
        self.server.terminate()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def open_chapter(self, spine_id: str, efi_path: str = ""):
        self.chapter_path = efi_path

        self.browser.get(f"{self.base_url}/book/{spine_id}")
        self.browser.execute_script(
            """moonQuote = await import('/static/moon-quote.es.js')
            taggedText = new moonQuote.TaggedText()"""
        )

    def open_chapter_object(self, chapter: Chapter):
        efi_path = "6/{}".format((chapter.order + 1) * 2)
        self.open_chapter(chapter.id, efi_path)

    def get_plain_text(self):
        return self.browser.execute_script("return taggedText.plainText")

    def select_range(self, offset_from: int, offset_to: int):
        return self.browser.execute_script(
            f"moonQuote.selectRange(taggedText.construcRange({offset_from}, {offset_to}))"
        )

    def cfi_from_range(self, offset_from: int, offset_to: int) -> str:
        cfi_parts = self.browser.execute_script(
            f"""return new moonQuote.EpubCFI(
    taggedText.construcRange({offset_from}, {offset_to})
).toString()"""
        ).split("!")

        return "{}{}!{}".format(cfi_parts[0], self.chapter_path, cfi_parts[1])

    def fuzzyfind(self, subsequence: str, max_distance: int = 10) -> list[SearchResult]:
        matches = fuzzyfind(subsequence, self.get_plain_text(), max_distance)

        def to_search_result(match: fuzzysearch.Match):
            return SearchResult(
                text=match.matched,
                cfi=self.cfi_from_range(match.start, match.end),
                distance=match.dist,
            )

        return list(map(to_search_result, matches))
