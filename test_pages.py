from html.parser import HTMLParser
from pathlib import Path

PAGES = [
    "pg1.html", "pg2.html", "pg3.html",
    "pg4-carlos.html", "pg4-fernanda.html", "pg4-julio.html",
    "pg4-marco.html", "pg4-patricia.html", "pg4-simone.html",
]

def test_pages_exist():
    for p in PAGES:
        assert Path(p).exists(), f"{p} missing"

def test_pages_valid_html():
    class Parser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.stack = []
            self.void = {"meta","link","br","hr","img","input","col","area","base","embed","param","source","track","wbr"}
        def handle_starttag(self, tag, attrs):
            if tag not in self.void:
                self.stack.append(tag)
        def handle_endtag(self, tag):
            if tag in self.void:
                return
            if self.stack and self.stack[-1] == tag:
                self.stack.pop()
            else:
                raise AssertionError(f"malformed: /{tag}")

    for p in PAGES:
        parser = Parser()
        parser.feed(Path(p).read_text(encoding="utf-8"))
        assert not parser.stack, f"{p} unclosed tags: {parser.stack}"
