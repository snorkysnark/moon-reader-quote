from dataclasses import dataclass
from typing import TextIO
import re

BR_REGEX = re.compile("(<BR>)+")


@dataclass
class MrExptQuote:
    mr_id: str
    quote: str


def parse(file: TextIO) -> list[MrExptQuote]:
    results = []

    raw_text = file.read()
    for chunk in raw_text.split("#\n")[1:]:
        lines = chunk.splitlines()

        mr_id = lines[0]
        quote = BR_REGEX.sub(" ", lines[12])
        results.append(MrExptQuote(mr_id, quote))

    return results
