"""Builds julneree.com: optimises images and videos, then writes index.html and the article pages.

    python build/build.py            # build everything (processed media are cached)
    python build/build.py --force    # re-encode all media

Needs Pillow, pillow-heif and ffmpeg. Originals stay outside the repo (see ROOTS);
once a file is processed its output and dimensions are cached in build/manifest.json,
so the site can be rebuilt without the originals as long as the outputs exist.
"""
import hashlib
import html
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageOps

try:
    import pillow_heif

    pillow_heif.register_heif_opener()
except ImportError:  # only needed for the two .HEIC files
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
import content as C  # noqa: E402

BUILD = Path(__file__).resolve().parent
ROOT = BUILD.parent
DL = Path.home() / "Downloads"
ROOTS = {
    "Ryder": DL / "julneree.com images" / "Ryder",
    "Soundbrenner": DL / "julneree.com images" / "Soundbrenner",
    "Transcelestial": DL / "julneree.com images" / "Transcelestial",
    "c2m": DL / "julneree-concept-to-manufacturing" / "videos",
    "larkin": BUILD / "sources" / "larkin",
    "writing": BUILD / "sources" / "writing",
    "dl": DL,
}
IMG = ROOT / "img"
VID = ROOT / "video"
MANIFEST = BUILD / "manifest.json"
WIDTHS = [640, 1280, 2048]
FORCE = "--force" in sys.argv

manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
used = set()


def esc(s):
    return html.escape(s or "", quote=True)


def resolve(src):
    head, _, rest = src.partition("/")
    return ROOTS[head] / rest


def slugify(src):
    head, _, rest = src.partition("/")
    stem = Path(rest).stem.lower()
    stem = re.sub(r"[^a-z0-9]+", "-", stem).strip("-")
    stem = re.sub(r"-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", "", stem)
    stem = re.sub(r"screenshot-(\d{4}-\d{2}-\d{2})-at-", r"\1-", stem)
    parent = Path(rest).parent.as_posix()
    parent = "" if parent == "." else re.sub(r"[^a-z0-9]+", "-", parent.lower()) + "-"
    return f"{head.lower()}-{parent}{stem[:48]}".strip("-")


# ---------------------------------------------------------------- media


def save_widths(im, slug):
    w, h = im.size
    widths = [x for x in WIDTHS if x < w] + [min(w, WIDTHS[-1])]
    widths = sorted(set(widths))
    for W in widths:
        out = IMG / f"{slug}-{W}.webp"
        if out.exists() and not FORCE:
            continue
        r = im if W == w else im.resize((W, round(h * W / w)), Image.LANCZOS)
        r.save(out, "WEBP", quality=78, method=5)
    return widths


def process_image(src, crop=None):
    slug = slugify(src) + ("-crop" if crop else "")
    m = manifest.get(slug)
    if m and not FORCE and all((IMG / f"{slug}-{W}.webp").exists() for W in m["widths"]):
        return m
    path = resolve(src)
    im = Image.open(path)
    im = ImageOps.exif_transpose(im)
    if crop:
        im = im.crop(crop)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, "white")
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")
    widths = save_widths(im, slug)
    m = {"slug": slug, "kind": "img", "w": im.size[0], "h": im.size[1], "widths": widths}
    manifest[slug] = m
    print("img", slug, im.size)
    return m


def process_video(src, start=0, dur=None):
    slug = slugify(src)
    if start or dur:
        slug += f"-{int(start)}-{int(dur or 0)}"
    out = VID / f"{slug}.mp4"
    m = manifest.get(slug)
    if m and not FORCE and out.exists() and all((IMG / f"{slug}-{W}.webp").exists() for W in m["widths"]):
        return m
    path = resolve(src)
    cmd = ["ffmpeg", "-y", "-v", "error"]
    if start:
        cmd += ["-ss", str(start)]
    cmd += ["-i", str(path)]
    if dur:
        cmd += ["-t", str(dur)]
    vf = ("scale='min(1280,iw)':'min(1280,ih)':force_original_aspect_ratio=decrease,"
          "scale=trunc(iw/2)*2:trunc(ih/2)*2,fps=30")
    cmd += ["-map", "0:v:0", "-an", "-vf", vf, "-c:v", "libx264", "-preset", "slow", "-crf", "28",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    with tempfile.TemporaryDirectory() as tmp:
        png = Path(tmp) / "poster.png"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "0.2", "-i", str(out), "-frames:v", "1", str(png)],
                       check=True)
        im = Image.open(png).convert("RGB")
        widths = save_widths(im, slug)
    m = {"slug": slug, "kind": "vid", "w": im.size[0], "h": im.size[1], "widths": widths,
         "kb": out.stat().st_size // 1024}
    manifest[slug] = m
    print("vid", slug, im.size, f"{m['kb']}KB")
    return m


def process_youtube(vid_id):
    slug = f"yt-{vid_id.lower()}"
    m = manifest.get(slug)
    if m and not FORCE and all((IMG / f"{slug}-{W}.webp").exists() for W in m["widths"]):
        return m
    import urllib.request

    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "t.jpg"
        for name in ("maxresdefault", "hqdefault"):
            try:
                urllib.request.urlretrieve(f"https://i.ytimg.com/vi/{vid_id}/{name}.jpg", p)
                break
            except Exception:
                continue
        im = Image.open(p).convert("RGB")
        widths = save_widths(im, slug)
    m = {"slug": slug, "kind": "img", "w": im.size[0], "h": im.size[1], "widths": widths}
    manifest[slug] = m
    return m


def media(item):
    src = item["src"]
    if item["type"] == "vid" or src.lower().endswith(".gif"):
        m = process_video(src, item.get("start", 0), item.get("dur"))
    else:
        m = process_image(src, item.get("crop"))
    used.add(m["slug"])
    return m


# ---------------------------------------------------------------- markup


def srcset(m, p):
    return ", ".join(f"{p}img/{m['slug']}-{W}.webp {W}w" for W in m["widths"])


def largest(m, p):
    return f"{p}img/{m['slug']}-{m['widths'][-1]}.webp"


def img_tag(m, p, sizes, alt="", eager=False, cls=""):
    mid = [W for W in m["widths"] if W <= 1280][-1]
    cls_attr = f' class="{cls}"' if cls else ""
    return (f'<img{cls_attr} src="{p}img/{m["slug"]}-{mid}.webp" '
            f'srcset="{srcset(m, p)}" sizes="{sizes}" width="{m["w"]}" height="{m["h"]}" '
            f'alt="{esc(alt)}" {"fetchpriority=high" if eager else "loading=lazy"} decoding="async">')


def video_tag(m, p, controls=False):
    poster = f"{p}img/{m['slug']}-{[W for W in m['widths'] if W <= 1280][-1]}.webp"
    if controls:
        return (f'<video controls playsinline preload="none" poster="{poster}" width="{m["w"]}" height="{m["h"]}">'
                f'<source src="{p}video/{m["slug"]}.mp4" type="video/mp4"></video>')
    return (f'<video class="loop" muted loop playsinline preload="none" poster="{poster}" '
            f'data-src="{p}video/{m["slug"]}.mp4" width="{m["w"]}" height="{m["h"]}"></video>')


def lb_attrs(m, p, cap):
    if m["kind"] == "vid":
        return (f'data-lb="vid" data-src="{p}video/{m["slug"]}.mp4" '
                f'data-poster="{largest(m, p)}" data-cap="{esc(cap)}"')
    return (f'data-lb="img" data-src="{largest(m, p)}" data-srcset="{srcset(m, p)}" '
            f'data-w="{m["w"]}" data-h="{m["h"]}" data-cap="{esc(cap)}"')


def tile(item, p=""):
    m = media(item)
    ar = m["w"] / m["h"]
    inner = video_tag(m, p) if m["kind"] == "vid" else img_tag(m, p, f"{min(round(300 * ar), 1400)}px", item["alt"])
    badge = '<span class="badge mono">Video</span>' if m["kind"] == "vid" else ""
    cls = "tile wide" if item.get("wide") else "tile"
    return (f'<figure class="{cls}" style="--ar:{ar:.4f}">'
            f'<button class="zoom" type="button" {lb_attrs(m, p, item["cap"])} aria-label="Enlarge: {esc(item["cap"])}">'
            f'{inner}{badge}</button>'
            f'<figcaption>{esc(item["cap"])}</figcaption></figure>')


def strip(items, p=""):
    return (f'<div class="strip-wrap"><div class="strip" data-gallery>{"".join(tile(i, p) for i in items)}</div>'
            '<button class="nudge prev" type="button" aria-label="Scroll left">←</button>'
            '<button class="nudge next" type="button" aria-label="Scroll right">→</button></div>')


CAT = dict(C.CATEGORIES)


def company(co):
    hero = media(co["hero"])
    facts = "".join(
        f'<div class="fact"><h3 class="label">{esc(t)}</h3><ul>{"".join(f"<li>{esc(x)}</li>" for x in xs)}</ul></div>'
        for t, xs in co["facts"])
    loops = ""
    if co.get("loops"):
        loops = '<div class="loops" data-gallery>' + "".join(
            f'<figure><button class="zoom" type="button" {lb_attrs(media(v), "", v["cap"])} '
            f'aria-label="Enlarge: {esc(v["cap"])}">{video_tag(media(v), "")}</button>'
            f'<figcaption>{esc(v["cap"])}</figcaption></figure>'
            for v in co["loops"]) + "</div>"
    phases = []
    for phase, keys in C.PHASES:
        rows = []
        # A row key can hold several categories ("production team"); it sits in the phase of the first one.
        for k in keys:
            for rk, items in co["rows"].items():
                if rk.split()[0] != k or not items:
                    continue
                label = co.get("row_labels", {}).get(rk) or CAT[k]
                rows.append(
                    f'<div class="row" data-cat="{rk}">'
                    f'<div class="row-head"><h4>{esc(label)}</h4></div>'
                    f'{strip(items)}</div>')
        if rows:
            phases.append(f'<div class="phase"><h3 class="phase-label">{phase}</h3>{"".join(rows)}</div>')
    return f'''
<section class="co" id="{co["id"]}" data-section>
  <header class="co-head wrap">
    <p class="label co-meta">{esc(co["years"])}</p>
    <h2 class="co-name">{esc(co["name"])}</h2>
    <p class="co-role">{esc(co["role"])}<span>{esc(co["place"])}</span></p>
    {site_link(co["url"])}
  </header>
  <figure class="co-hero wrap"><button class="zoom" type="button" {lb_attrs(hero, "", co["hero"]["cap"])} aria-label="Enlarge: {esc(co["hero"]["cap"])}">{img_tag(hero, "", "(max-width: 1320px) 100vw, 1280px", co["hero"]["alt"])}</button></figure>
  <div class="co-body wrap">
    <p class="co-intro">{esc(co["intro"])}</p>
    <div class="facts">{facts}</div>
  </div>
  {f'<div class="wrap">{loops}</div>' if loops else ""}
  <div class="work">{"".join(phases)}</div>
</section>'''


def site_link(url):
    domain = url.split("//")[1].strip("/").replace("www.", "")
    return f'<a class="site-link" href="{url}" rel="noopener" target="_blank">{domain}<span aria-hidden="true">↗</span></a>'


def now_section():
    n = C.NOW
    return f'''
<section class="now" id="{n["id"]}" data-section>
  <div class="wrap now-grid">
    <div>
      <p class="label"><span class="dot"></span>Now · {esc(n["years"])}</p>
      <h2 class="now-name">{esc(n["name"])}</h2>
      <p class="co-role">{esc(n["role"])}<span>{esc(n["place"])}</span></p>
      {site_link(n["url"])}
    </div>
    <p class="now-intro">{esc(n["intro"])}</p>
  </div>
  <div class="work"><div class="row">{strip(n["items"])}</div></div>
</section>'''


def counts():
    c = {k: 0 for k, _ in C.CATEGORIES}
    for co in C.COMPANIES:
        for rk, items in co["rows"].items():
            for k in rk.split():
                c[k] += len(items)
    c["photo"] = len(C.PHOTOS)
    return c


def index_section():
    c = counts()
    chips = "".join(
        f'<button class="chip" type="button" data-filter="{k}"><span>{esc(label)}</span><span class="n">{c[k]}</span></button>'
        for k, label in C.CATEGORIES)
    return f'''
<section class="index wrap" aria-label="What I do">
  <div class="index-head"><h2 class="label">What I do</h2><p class="muted small">Pick one to see that work across every company.</p></div>
  <div class="chips">{chips}</div>
</section>
<div class="filterbar" hidden><div class="wrap"><span class="label">Showing</span> <strong class="fb-name"></strong><button class="fb-clear" type="button">Show everything ×</button></div></div>'''


def videos_section():
    cards = ""
    for vid_id, title in C.VIDEOS:
        m = process_youtube(vid_id)
        used.add(m["slug"])
        cards += (f'<figure class="yt"><button type="button" class="yt-play" data-yt="{vid_id}" aria-label="Play: {esc(title)}">'
                  f'{img_tag(m, "", "(max-width: 700px) 100vw, 420px", "")}<span class="play" aria-hidden="true"></span></button>'
                  f'<figcaption>{esc(title)}</figcaption></figure>')
    return f'''
<section class="videos wrap" id="video" data-section>
  <div class="sec-head"><h2 class="sec-title">On video</h2><p class="muted">Design, manufacturing and launch of Ryder One, on the Ryder channel.</p></div>
  <div class="yt-grid">{cards}</div>
</section>'''


def writing_section():
    rows = "".join(
        f'<a class="post" href="{a["slug"]}/"><span class="label">{a["date"].split()[-1]}</span>'
        f'<span class="post-title">{esc(a["title"])}</span><span class="label post-kind">{esc(a["kind"])}</span></a>'
        for a in C.ARTICLES)
    return f'''
<section class="writing wrap" id="writing" data-section>
  <div class="sec-head"><h2 class="sec-title">Writing</h2></div>
  <div class="posts">{rows}</div>
</section>'''


def photos_section():
    figs = ""
    for it in C.PHOTOS:
        m = media(it)
        figs += (f'<figure><button class="zoom" type="button" {lb_attrs(m, "", it["cap"])} aria-label="Enlarge: {esc(it["cap"])}">'
                 f'{img_tag(m, "", "(max-width: 700px) 100vw, (max-width: 1100px) 50vw, 430px", it["alt"])}</button></figure>')
    return f'''
<section class="photos" id="photography" data-section>
  <div class="wrap">
    <div class="sec-head"><h2 class="sec-title">Product photography</h2><p>I shoot the products I make. Studio, close-ups and live shots, all by me.</p></div>
    <div class="masonry" data-gallery>{figs}</div>
  </div>
</section>'''


def about_section():
    a = C.ABOUT
    pm = media(a["portrait"])
    before = "".join(
        f'<li><span class="label">{y}</span><span><strong>{esc(o)}</strong> {esc(t)}</span></li>' for y, o, t in a["before"])
    links = " ".join(f'<a href="{u}" rel="noopener" target="_blank">{n} ↗</a>' for n, u in C.SITE["links"])
    return f'''
<section class="about wrap" id="about" data-section>
  <div class="about-grid">
    <div class="portrait">{img_tag(pm, "", "220px", "Julien Nérée")}</div>
    <div class="about-text">{"".join(f"<p>{esc(t)}</p>" for t in a["text"])}
      <p class="links">{links}</p></div>
    <div class="before"><h3 class="label">Before</h3><ul>{before}</ul></div>
  </div>
</section>'''


def asset_version():
    h = hashlib.md5()
    for f in ("assets/site.css", "assets/site.js"):
        h.update((ROOT / f).read_bytes())
    return h.hexdigest()[:8]


def page(title, description, body, p="", og_image="img/og.jpg", canonical=""):
    v = asset_version()
    nav = "".join(f'<a href="{p}#{i}">{n}</a>' for i, n in [
        ("larkin", "Larkin"), ("ryder", "Ryder"), ("transcelestial", "Transcelestial"),
        ("soundbrenner", "Soundbrenner"), ("video", "Video"), ("writing", "Writing"),
        ("photography", "Photography")])
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{C.SITE["url"]}{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:image" content="{C.SITE["url"]}{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}assets/site.css?v={v}">
<script defer src="{p}assets/site.js?v={v}"></script>
</head>
<body>
<header class="top">
  <div class="wrap top-inner">
    <a class="brand" href="{p or "#"}">Julien Nérée</a>
    <nav class="nav" aria-label="Sections">{nav}</nav>
  </div>
</header>
<main>{body}</main>
<footer class="foot wrap">
  <span>© 2026 Julien Nérée</span>
  <span>{" ".join(f'<a href="{u}" rel="noopener" target="_blank">{n}</a>' for n, u in C.SITE["links"])}</span>
</footer>
<dialog class="lb" aria-label="Image viewer">
  <div class="lb-stage"></div>
  <p class="lb-cap"><span class="lb-n label"></span><span class="lb-t"></span></p>
  <button class="lb-btn lb-close" type="button" aria-label="Close">×</button>
  <button class="lb-btn lb-prev" type="button" aria-label="Previous">←</button>
  <button class="lb-btn lb-next" type="button" aria-label="Next">→</button>
</dialog>
</body>
</html>
'''


def build_index():
    s = C.SITE
    hm = media(s["hero_image"])
    stats = "".join(f'<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>' for a, b in s["stats"])
    intro = f'''
<section class="intro wrap">
  <div class="intro-text">
    <h1>{esc(s["statement"])}</h1>
    <p class="lede">{esc(s["sub"])}</p>
    <dl class="stats">{stats}</dl>
  </div>
  <figure class="intro-img">{img_tag(hm, "", "(max-width: 900px) 100vw, 420px", s["hero_image"]["alt"], eager=True)}<figcaption>{esc(s["hero_image"]["cap"])}</figcaption></figure>
</section>'''
    body = (intro + index_section() + now_section() + "".join(company(c) for c in C.COMPANIES)
            + videos_section() + writing_section() + photos_section() + about_section())
    (ROOT / "index.html").write_text(page(s["title"], s["description"], body))


PH = re.compile(r"\{\{(img|video):([^|}]+)\|?([^}]*)\}\}")


def build_articles():
    for a in C.ARTICLES:
        src = (BUILD / "articles" / f"{a['slug']}.html").read_text()
        cover = re.search(r"<!-- cover: (\S+) -->", src)
        src = re.sub(r"<!-- cover: \S+ -->\n?", "", src)
        p = "../"

        def repl(mt):
            kind, path, cap = mt.group(1), mt.group(2), mt.group(3).strip()
            m = media({"type": "vid" if kind == "video" else "img", "src": path})
            if m["kind"] == "vid":
                inner = video_tag(m, p, controls=(kind == "video"))
            else:
                inner = img_tag(m, p, "(max-width: 760px) 100vw, 720px", re.sub("<[^>]+>", "", cap))
            fc = f"<figcaption>{cap}</figcaption>" if cap else ""
            plain = re.sub("<[^>]+>", "", cap)
            if kind == "video":
                return f'<figure class="a-fig">{inner}{fc}</figure>'
            return f'<figure class="a-fig"><button class="zoom" type="button" {lb_attrs(m, p, plain)} aria-label="Enlarge">{inner}</button>{fc}</figure>'

        body_html = PH.sub(repl, src)
        cover_html = ""
        if cover:
            cm = media({"type": "img", "src": cover.group(1)})
            cover_html = f'<figure class="a-cover">{img_tag(cm, p, "(max-width: 1100px) 100vw, 1080px", a["title"], eager=True)}</figure>'
        body = f'''
<article class="article">
  <header class="a-head wrap-narrow">
    <a class="back label" href="../#writing">← All writing</a>
    <p class="label">{esc(a["kind"])} · {esc(a["date"])}</p>
    <h1>{esc(a["title"])}</h1>
  </header>
  <div class="wrap-wide">{cover_html}</div>
  <div class="a-body wrap-narrow" data-gallery>{body_html}</div>
  <p class="wrap-narrow a-end"><a href="../#writing">← All writing</a> · <a href="../">Home</a></p>
</article>'''
        out = ROOT / a["slug"]
        out.mkdir(exist_ok=True)
        (out / "index.html").write_text(
            page(f"{a['title']} — Julien Nérée", a["description"], body, p=p, canonical=f"{a['slug']}/"))
        print("article", a["slug"])


def build_og():
    out = IMG / "og.jpg"
    if out.exists() and not FORCE:
        return
    im = ImageOps.exif_transpose(Image.open(resolve(C.COMPANIES[0]["hero"]["src"]))).convert("RGB")
    ImageOps.fit(im, (1200, 630), Image.LANCZOS).save(out, "JPEG", quality=84)


def main():
    IMG.mkdir(exist_ok=True)
    VID.mkdir(exist_ok=True)
    build_index()
    build_articles()
    build_og()
    # Drop outputs of media that content.py no longer uses.
    for slug in [s for s in manifest if s not in used]:
        for W in manifest[slug]["widths"]:
            (IMG / f"{slug}-{W}.webp").unlink(missing_ok=True)
        (VID / f"{slug}.mp4").unlink(missing_ok=True)
        del manifest[slug]
        print("removed", slug)
    MANIFEST.write_text(json.dumps(manifest, indent=1, sort_keys=True))
    total = sum(f.stat().st_size for f in list(IMG.iterdir()) + list(VID.iterdir()))
    print(f"done. media: {total / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
