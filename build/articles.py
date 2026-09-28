"""One-time migration of the three Super.so (Notion) articles into clean HTML fragments.

Reads the saved Super.so pages in build/sources/page_<slug>.html, downloads every image
and video into build/sources/writing/<slug>/, and writes build/articles/<slug>.html.
Media are written as placeholders ({{img:...}} / {{video:...}}) that build.py turns into
optimised <figure> markup, so the fragments stay easy to edit by hand afterwards.

Run once:  python build/articles.py
"""
import html
import re
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / "sources"
OUT = ROOT / "articles"
SLUGS = ["4-key-lessons", "from-concept-phase-to-manufacturing", "ledger-nano-x"]

INLINE = {"strong": "strong", "b": "strong", "em": "em", "i": "em", "u": "u", "code": "code", "s": "s"}


def esc(s):
    return html.escape(s, quote=False)


def inline(node):
    out = []
    for c in node.children:
        if isinstance(c, NavigableString):
            out.append(esc(str(c)))
        elif isinstance(c, Tag):
            if c.name == "a":
                href = c.get("href", "")
                out.append(f'<a href="{html.escape(href)}">{inline(c)}</a>')
            elif c.name in INLINE:
                t = INLINE[c.name]
                inner = inline(c)
                out.append(f"<{t}>{inner}</{t}>" if inner.strip() else inner)
            elif c.name == "br":
                out.append("<br>")
            elif c.name in ("ul", "ol"):
                continue
            else:
                out.append(inline(c))
    return "".join(out)


class Converter:
    def __init__(self, slug):
        self.slug = slug
        self.n = 0
        self.dir = SOURCES / "writing" / slug
        self.dir.mkdir(parents=True, exist_ok=True)

    def download(self, url, ext):
        self.n += 1
        dest = self.dir / f"{self.n:02d}{ext}"
        if not dest.exists():
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            for attempt in range(3):
                try:
                    with urllib.request.urlopen(req, timeout=90) as r:
                        data = r.read()
                        ctype = r.headers.get("Content-Type", "")
                    break
                except Exception:
                    if attempt == 2:
                        self.n -= 1
                        raise
            if ext == ".img":
                real = {"image/png": ".png", "image/gif": ".gif", "image/webp": ".webp"}.get(ctype.split(";")[0], ".jpg")
                dest = dest.with_suffix(real)
                for old in self.dir.glob(f"{self.n:02d}.*"):
                    old.unlink()
            dest.write_bytes(data)
        return dest.relative_to(SOURCES).as_posix()

    def existing(self, ext_guess):
        hits = sorted(self.dir.glob(f"{self.n + 1:02d}.*"))
        return hits[0] if hits else None

    def media(self, url, kind):
        hit = self.existing(None)
        if hit is not None:
            self.n += 1
            return hit.relative_to(SOURCES).as_posix()
        return self.download(url, ".mp4" if kind == "video" else ".img")

    def image(self, node):
        span = node.find(attrs={"data-full-size": True})
        img = node.find("img")
        cap_el = node.find(class_="notion-caption")
        cap = inline(cap_el).strip() if cap_el else ""
        urls = ([span["data-full-size"]] if span else []) + [img["src"]]
        for i, url in enumerate(urls):
            try:
                path = self.media(url, "image")
                break
            except Exception as e:  # originals sometimes time out; the resized copy is enough
                print("  retry with resized copy:", e)
                if i == len(urls) - 1:
                    raise
        return f"{{{{img:{path}|{cap}}}}}"

    def video(self, node):
        # Super.so's video host is unreliable; the same six clips (in page order) are kept
        # locally in ~/Downloads/julneree-concept-to-manufacturing/videos.
        self.videos = getattr(self, "videos", 0) + 1
        local = sorted((Path.home() / "Downloads/julneree-concept-to-manufacturing/videos").glob(f"{self.videos}-*"))
        cap_el = node.find(class_="notion-caption")
        cap = inline(cap_el).strip() if cap_el else ""
        self.n += 1
        dest = self.dir / f"{self.n:02d}{local[0].suffix.lower()}"
        if not dest.exists():
            dest.write_bytes(local[0].read_bytes())
        return f"{{{{video:{dest.relative_to(SOURCES).as_posix()}|{cap}}}}}"

    def block(self, node):
        if isinstance(node, NavigableString):
            return esc(str(node)) if str(node).strip() else ""
        cls = node.get("class") or []
        if "notion-heading__anchor" in cls:
            return ""
        if "notion-heading" in cls:
            lvl = {"h1": 2, "h2": 2, "h3": 3, "h4": 4}.get(node.name, 3)
            return f"<h{lvl}>{inline(node).strip()}</h{lvl}>\n"
        if "notion-text" in cls:
            t = inline(node).strip()
            return f"<p>{t}</p>\n" if t else ""
        if "notion-bulleted-list" in cls or "notion-numbered-list" in cls or node.name in ("ul", "ol"):
            tag = "ol" if ("notion-numbered-list" in cls or node.name == "ol") else "ul"
            items = []
            for li in node.find_all("li", recursive=False):
                nested = "".join(self.block(x) for x in li.find_all(["ul", "ol"], recursive=False))
                items.append(f"<li>{inline(li).strip()}{nested}</li>")
            return f"<{tag}>\n" + "\n".join(items) + f"\n</{tag}>\n"
        if "notion-image" in cls:
            return self.image(node) + "\n"
        if "notion-video" in cls:
            return self.video(node) + "\n"
        if "notion-column-list" in cls:
            cols = [self.children(c) for c in node.find_all(class_="notion-column", recursive=False)]
            cols = [c for c in cols if c.strip()]
            if not cols:
                return ""
            return f'<div class="cols cols-{len(cols)}">\n' + "".join(f"<div>\n{c}</div>\n" for c in cols) + "</div>\n"
        if "notion-toggle" in cls:
            summary = node.find(class_="notion-toggle__summary")
            content = node.find(class_="notion-toggle__content")
            title = inline(summary).replace("‣", "").strip() if summary else ""
            return f"<h4>{title}</h4>\n" + (self.children(content) if content else "")
        if "notion-divider" in cls:
            return "<hr>\n"
        if "notion-quote" in cls or node.name == "blockquote":
            return f"<blockquote>{inline(node).strip()}</blockquote>\n"
        if "notion-callout" in cls:
            return f'<aside class="callout">{self.children(node)}</aside>\n'
        return self.children(node)

    def children(self, node):
        return "".join(self.block(c) for c in node.children)


def tidy(body):
    for t in ("strong", "em", "u"):
        while f"<{t}><{t}>" in body:
            body = body.replace(f"<{t}><{t}>", f"<{t}>").replace(f"</{t}></{t}>", f"</{t}>")
    body = re.sub(r"<(h[2-4])>(.*?)</\1>",
                  lambda m: f"<{m[1]}>{re.sub(r'</?strong>', '', m[2])}</{m[1]}>", body)
    soup = BeautifulSoup(body, "html.parser")
    for div in soup.select("div.cols-1"):
        inner = div.find("div", recursive=False)
        if inner:
            inner.unwrap()
        div.unwrap()
    for div in soup.select("div.cols-2"):
        first = div.find("div", recursive=False)
        kids = [k for k in first.children if isinstance(k, Tag)] if first else []
        if len(kids) == 1 and kids[0].name in ("h2", "h3", "h4"):
            div["class"] = ["split"]
    return re.sub(r"\n{3,}", "\n\n", str(soup))


def main():
    OUT.mkdir(exist_ok=True)
    for slug in SLUGS:
        soup = BeautifulSoup((SOURCES / f"page_{slug}.html").read_text(), "html.parser")
        conv = Converter(slug)
        cover = soup.select_one(".notion-header__cover span[data-full-size]")
        body = conv.children(soup.select_one(".notion-root"))
        body = tidy(body)
        cover_ph = ""
        if cover:
            conv_cover = Converter(slug + "-cover")
            cover_ph = conv_cover.media(cover["data-full-size"], "image")
        (OUT / f"{slug}.html").write_text(
            (f"<!-- cover: {cover_ph} -->\n" if cover_ph else "") + body
        )
        print(slug, conv.n, "media", len(body), "chars")


if __name__ == "__main__":
    main()
