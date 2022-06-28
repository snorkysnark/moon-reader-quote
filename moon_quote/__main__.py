from argparse import ArgumentParser
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Optional
from dataclasses_json.api import dataclass_json

from ebooklib import epub

from . import get_chapter_list, parse_mrexpt, BookServer, MrExptQuote, Chapter


@dataclass_json
@dataclass
class FoundQuote:
    chapter_id: str
    chapter_name: Optional[str]
    text: str
    distance: int
    cfi: str


@dataclass_json
@dataclass
class QuoteMatches:
    original: str
    found: list[FoundQuote]


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("book", type=Path, help="epub book path")
    parser.add_argument("quotes", type=Path, help="mrexpt file path")
    parser.add_argument(
        "--max-distance", type=int, default=10, help="max levenstein distance"
    )
    parser.add_argument("-o", "--output", type=Path, required=True, help="output json")

    return parser.parse_args()


def find_quotes(
    server: BookServer,
    chapters: list[Chapter],
    quotes: list[MrExptQuote],
    max_distance: int,
):
    quote_results: dict[str, QuoteMatches] = {}

    # Initialize with empty lists
    for quote_item in quotes:
        quote_results[quote_item.mr_id] = QuoteMatches(quote_item.quote, [])

    # Search in all chapters
    for chapter in chapters:
        server.open_chapter_object(chapter)

        for quote_item in quotes:
            for match in server.fuzzyfind(quote_item.quote, max_distance):
                print(match)
                quote_results[quote_item.mr_id].found.append(
                    FoundQuote(
                        chapter_id=chapter.id,
                        chapter_name=chapter.name,
                        text=match.text,
                        distance=match.distance,
                        cfi=match.cfi,
                    )
                )

    # Sort by distance
    for match_list in quote_results.values():
        match_list.found.sort(key=lambda match: match.distance)

    return quote_results


def main():
    args = parse_args()

    book = epub.read_epub(args.book)
    chapters = get_chapter_list(book)

    with args.quotes.open() as file:
        quotes = parse_mrexpt(file)

    with BookServer(book) as server:
        results = find_quotes(
            server=server,
            chapters=chapters,
            quotes=quotes,
            max_distance=args.max_distance,
        )

    with Path(args.output).open("w") as output_file:
        dict_results = {
            key: value.to_dict() for key, value in results.items()  # type:ignore
        }
        json.dump(dict_results, output_file, indent=4, ensure_ascii=False)


main()
