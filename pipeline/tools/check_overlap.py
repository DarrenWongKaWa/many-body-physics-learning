"""Check that a topic's narration, labels and documents do not repeat the source text word for word.

Run from a topic folder, pointing at your local copy of the source (sources are never committed):

    python ../../pipeline/tools/check_overlap.py ~/papers/source.pdf          # passages of 10+ shared words
    python ../../pipeline/tools/check_overlap.py source.txt --n 8 narration.py

By default it reads narration.py, i18n_en.py, scenes/*.py, *.md and notes/*.md of the topic. A PDF is read with
pymupdf (optional in requirements.txt). Titles and citations of the source are expected hits; any other passage
should be reworded before the topic is published.
"""
import argparse, re
from pathlib import Path


def words(s):
    return re.findall(r"[a-z]+", s.lower())


def source_text(path):
    p = Path(path).expanduser()
    if p.suffix.lower() == '.pdf':
        import pymupdf
        return '\n'.join(page.get_text() for page in pymupdf.open(p))
    return p.read_text(errors='ignore')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('source', help='your local copy of the source text (.pdf or .txt)')
    ap.add_argument('files', nargs='*', help='files to check (default: narration, labels, scenes and docs)')
    ap.add_argument('--n', type=int, default=10, help='shortest shared passage to report, in words')
    a = ap.parse_args()
    sw = words(source_text(a.source))
    grams = {tuple(sw[i:i + a.n]) for i in range(len(sw) - a.n + 1)}
    here = Path('.')
    files = [Path(f) for f in a.files] or sorted({*here.glob('narration.py'), *here.glob('i18n_en.py'),
                                                 *here.glob('scenes/*.py'), *here.glob('*.md'), *here.glob('notes/*.md')})
    hits = 0
    for f in files:
        w = words(f.read_text(errors='ignore'))
        i = 0
        while i <= len(w) - a.n:
            if tuple(w[i:i + a.n]) in grams:
                j = i + a.n                       # extend to the whole shared passage
                while j < len(w) and tuple(w[j - a.n + 1:j + 1]) in grams:
                    j += 1
                print(f'{f}: "{" ".join(w[i:j])}"')
                hits += 1
                i = j
            else:
                i += 1
    print(f'{hits} shared passage(s) of {a.n}+ words in {len(files)} file(s)')


if __name__ == '__main__':
    main()
