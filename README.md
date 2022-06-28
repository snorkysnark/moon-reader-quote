# Moon Reader Highlights to EPUB-CFI

## Usage

```bash
# Pre-build the js library
python build.py
# Run search
python -m moon_quote <book_path> <mrexpt_path> -o <output.json>
```

## Example output

```json
{
    "1263": {
        "original": "«Преподавать статистику как исследовательский процесс...",
        "found": [
            {
                "chapter_id": "note.xhtml",
                "chapter_name": "Примечания",
                "text": "«Преподавать статистику как исследовательский процесс...",
                "distance": 3,
                "cfi": "epubcfi(/6/54!/4/22[note-9]/2,/1:70,/3:174)"
            }
        ]
    },
    "1293": {
        "original": "Недостаток прозрачности.",
        "found": [
            {
                "chapter_id": "G6.xhtml",
                "chapter_name": "ГЛАВА 6. Алгоритмы, аналитика и прогнозирование",
                "text": "Недостаток прозрачности.",
                "distance": 0,
                "cfi": "epubcfi(/6/28!/4/200/8,/2/1:0,/1:0)"
            },
            {
                "chapter_id": "G6.xhtml",
                "chapter_name": "ГЛАВА 6. Алгоритмы, аналитика и прогнозирование",
                "text": "Недостаток робастности ",
                "distance": 6,
                "cfi": "epubcfi(/6/28!/4/200/2/2,/1:0,/1:23)"
            }
        ]
    }
}
```
