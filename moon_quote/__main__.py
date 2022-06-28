from argparse import ArgumentParser
from pathlib import Path
import json

from ebooklib import epub

from . import get_chapter_list, parse_mrexpt, BookServer, MrExptQuote


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("book", type=Path, help="epub book path")
    parser.add_argument("quotes", type=Path, help="mrexpt file path")
    parser.add_argument("-o", "--output", type=Path, required=True, help="output json")

    return parser.parse_args()


args = parse_args()

book = epub.read_epub(args.book)
chapters = get_chapter_list(book)

with args.quotes.open() as file:
    quotes = parse_mrexpt(file)


def make_output_template(quotes: list[MrExptQuote]):
    output = {}
    for quote_item in quotes:
        output[quote_item.mr_id] = {"original": quote_item.quote, "found": []}
    return output


output_dict = make_output_template(quotes)

with BookServer(book) as server:
    for chapter in chapters:
        server.open_chapter_object(chapter)

        quote_results = []
        for quote_item in quotes:
            for match in server.fuzzyfind(quote_item.quote, 20):
                print(match)
                output_dict[quote_item.mr_id]["found"].append(
                    {
                        "chapter_id": chapter.id,
                        "chapter_name": chapter.name,
                        "text": match.text,
                        "distance": match.distance,
                        "cfi": match.cfi,
                    }
                )

with Path(args.output).open("w") as output_file:
    json.dump(output_dict, output_file)
