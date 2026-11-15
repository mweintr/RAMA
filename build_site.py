#!/usr/bin/env python3
"""Ghost Writer — book website.

One pre-generated page (docs/index.html) ready for GitHub Pages: opening, the book
(+ download), featured characters / ideas, podcast episodes, and the explorable book
graph. Every section except the opening and the book is optional and appears only
when its source exists. All content is written into the HTML; JavaScript only draws
the graph and navigates between cards.

  python3 build_site.py            # build docs/index.html
  python3 build_site.py --init     # write a site.yaml skeleton from book.config.json
  python3 build_site.py --check    # validate site.yaml and sources, write nothing

Sources (book root):
  site.yaml                 texts of the page (book language)
  cover.jpg / cover.png     cover (optional; Pillow makes the 720 px version if installed)
  graph/cards/**            book graph (optional) — see graph.py
  podcast/scripts/*.md + podcast/episodes/*.mp3 + podcast/feed.xml   (optional)

Only the standard library + PyYAML (Pillow optional).
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from html import escape as e
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("build_site.py needs PyYAML. Install it with:  pip install pyyaml")

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import graph as G  # noqa: E402

PALETTE = ["#6ee7a0", "#7aa2f7", "#c9a0ff", "#5fd4d4", "#f2cc60", "#f28fb8", "#9aa4b2", "#ff8c69", "#a3d977"]

LABELS = {
    "en": {
        "book": "The book", "podcast": "Podcast", "graph": "Graph", "listen": "Listen to the podcast",
        "read": "Read the book", "explore": "Explore the graph", "by": "by", "cover_of": "Cover of",
        "open_card": "Open the card in the graph →", "episodes": "episodes", "rss": "RSS feed to follow it in your app.",
        "rss_short": "RSS feed", "cards": "cards", "events": "events", "open_points": "open points",
        "chapters_n": "chapters", "tab_graph": "Graph", "tab_chapters": "Chapters", "tab_open": "Open points",
        "only_open": "Only with open points", "search": "Search the graph", "search_eg": "Search",
        "zoom_in": "Zoom in", "zoom_out": "Zoom out",
        "help": "Drag to move · Ctrl + wheel or the buttons to zoom · click a node",
        "tap": "Tap to explore the graph", "read_card": "Read the card ↓", "chapter": "Chapter",
        "event_chain": "Chain of events", "cards_in_chapter": "Cards in this chapter",
        "how_to_read": "How to read it",
        "how_to_read_text": "Every node is a card. Click a node, or search a name: the facts, relations and chain of "
                            "events appear here, with chapter and line of the text.",
        "start_from": "Where to start", "all_cards": "All {n} cards, in full",
        "open_intro": "{n} open points in {m} cards: small inconsistencies of the text still to be fixed.",
        "no_results": "No results", "min": "min", "ch": "ch.", "l": "l.", "aka": "Also called",
        "offstage": "off stage", "where_who": "Where and who", "where": "Where", "involved": "Involved",
        "chain": "Chain", "comes_from": "Comes from", "leads_to": "Leads to", "traits": "Traits", "facts": "Facts",
        "state": "State, chapter by chapter", "not_said": "What the text does not say",
        "notes": "Reading notes", "relations": "Relations", "this_card": "this card", "open_title": "Open points",
        "graph_title": "The book graph",
        "graph_text": "Everything that exists in the book, linked. Every fact gives chapter and line of the text.",
        "spoiler": "Warning: the graph tells the whole book, up to the last chapter shown.",
        "open_notice": "Nodes with an orange ring have open points: small inconsistencies of the text still to "
                       "be fixed. The book is a work in progress and shows them too.",
        "podcast_title": "The podcast", "podcast_text": "One chapter per episode, read aloud.",
        "chapters_upto": "chapters 1–{n}", "download": "Download the book",
        "featured_fiction": "Characters", "featured_people": "People", "featured_ideas": "Key ideas",
    },
    "it": {
        "book": "Il libro", "podcast": "Podcast", "graph": "Grafo", "listen": "Ascolta il podcast",
        "read": "Leggi il libro", "explore": "Esplora il grafo", "by": "di", "cover_of": "Copertina di",
        "open_card": "Apri la scheda nel grafo →", "episodes": "puntate", "rss": "Feed RSS per seguirlo dalla tua app.",
        "rss_short": "Feed RSS", "cards": "schede", "events": "eventi", "open_points": "punti aperti",
        "chapters_n": "capitoli", "tab_graph": "Grafo", "tab_chapters": "Capitoli", "tab_open": "Punti aperti",
        "only_open": "Solo con punti aperti", "search": "Cerca nel grafo", "search_eg": "Cerca",
        "zoom_in": "Ingrandisci", "zoom_out": "Riduci",
        "help": "Trascina per spostare · Ctrl + rotella o i pulsanti per lo zoom · clicca un nodo",
        "tap": "Tocca per esplorare il grafo", "read_card": "Leggi la scheda ↓", "chapter": "Capitolo",
        "event_chain": "Catena degli eventi", "cards_in_chapter": "Schede del capitolo",
        "how_to_read": "Come si legge",
        "how_to_read_text": "Ogni nodo è una scheda. Clicca un nodo, oppure cerca un nome: qui compaiono i fatti, "
                            "le relazioni e la catena degli eventi, con capitolo e riga del testo.",
        "start_from": "Da dove partire", "all_cards": "Tutte le {n} schede, per esteso",
        "open_intro": "{n} punti aperti in {m} schede: piccole incongruenze del testo ancora da sistemare.",
        "no_results": "Nessun risultato", "min": "min", "ch": "cap.", "l": "r.", "aka": "Detto anche",
        "offstage": "fuori scena", "where_who": "Dove e chi", "where": "Dove", "involved": "Coinvolti",
        "chain": "Catena", "comes_from": "Viene da", "leads_to": "Porta a", "traits": "Caratteristiche",
        "facts": "Fatti", "state": "Stato, capitolo per capitolo", "not_said": "Cosa il testo non dice",
        "notes": "Osservazioni di lettura", "relations": "Relazioni", "this_card": "questa scheda",
        "open_title": "Punti aperti", "graph_title": "Il grafo del libro",
        "graph_text": "Tutto ciò che esiste nel libro, collegato. Ogni fatto riporta capitolo e riga del testo.",
        "spoiler": "Attenzione: il grafo racconta tutto il libro, fino all'ultimo capitolo mostrato.",
        "open_notice": "I nodi con il bordo arancione hanno punti aperti: piccole incongruenze del testo ancora "
                       "da sistemare. Il libro è in lavorazione e si vedono anche quelle.",
        "podcast_title": "Il podcast", "podcast_text": "Un capitolo per puntata, letto ad alta voce.",
        "chapters_upto": "capitoli 1–{n}", "download": "Scarica il libro",
        "featured_fiction": "Personaggi", "featured_people": "Persone", "featured_ideas": "Idee chiave",
    },
}
FEATURED_KIND = {"fiction": "featured_fiction", "fable": "featured_fiction", "childrens-book": "featured_fiction",
                 "biography": "featured_people", "essay": "featured_ideas", "manual": "featured_ideas"}


def load_site(book):
    p = book.root / "site.yaml"
    if not p.exists():
        sys.exit("site.yaml not found: run  python3 build_site.py --init  (or /ghost-writer:site)")
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def labels(book, site):
    L = dict(LABELS["en"])
    L.update(LABELS.get(book.lang, {}))
    L.update(site.get("labels") or {})
    return L


# ─── Graph (with spoiler limit) ───────────────────────────────────────────────

def graph_data(book, upto):
    """Validated cards, trimmed to chapters <= upto (None = all)."""
    errors, warnings = [], []
    chs = G.load_graph_chapters(book)
    cards = G.load_cards(book, errors)
    G.validate(book, cards, chs, errors, warnings)
    if errors:
        sys.exit("Graph errors — run  python3 graph.py build  first:\n  " + "\n  ".join(errors[:20]))
    if upto is None:
        return cards, chs

    def ok_src(item):
        if not item.get("source"):
            return True
        return all(r[0] <= upto for r in G.parse_refs(item["source"]))

    keep = {}
    for i, c in cards.items():
        if c["_type"] == "event" and c.get("chapter", 0) > upto:
            continue
        c = dict(c)
        for k in ("traits", "facts", "relations"):
            if c.get(k):
                c[k] = [x for x in c[k] if ok_src(x)]
        for k in ("notes", "open", "not_said"):  # often unsourced: shown only if sourced within the limit
            if c.get(k):
                c[k] = [x for x in c[k] if x.get("source") and ok_src(x)]
        c["state"] = [x for x in c.get("state", []) or [] if (x.get("chapter") or 0) <= upto and ok_src(x)]
        if c.get("chapters"):
            c["chapters"] = [n for n in c["chapters"] if n <= upto]
        has = c["_type"] == "event" or c.get("chapters") or any(
            c.get(k) for k in ("traits", "facts", "state", "relations"))
        if has:
            keep[i] = c
    for c in keep.values():  # drop links to cards that are not shown
        c["relations"] = [r for r in c.get("relations", []) or [] if r.get("to") in keep]
        for k in ("involved", "after"):
            if c.get(k):
                c[k] = [x for x in c[k] if x in keep]
        if c.get("where") not in keep:
            c.pop("where", None)
    return keep, {n: v for n, v in chs.items() if n <= upto}


def chapters_of(c):
    s = set(c.get("chapters", []) or [])
    if c.get("chapter") is not None:
        s.add(c["chapter"])
    for it in G.source_items(c):
        try:
            s.update(r[0] for r in G.parse_refs(it["source"]))
        except ValueError:
            pass
    return sorted(s)


def graph_html(book, site, L):
    gs = site.get("graph") or {}
    cards, chs = graph_data(book, gs.get("up_to_chapter"))
    types = [sing for _, sing in book.types]
    tidx = {t: i for i, t in enumerate(types)}
    plural = {sing: book.type_label(folder) for folder, sing in book.types}
    ev_i = tidx.get("event", -1)
    edges = []  # (from, to, kind)  0 relation · 1 event-entity · 2 event chain
    for i, n in cards.items():
        edges += [(i, r["to"], 0) for r in n.get("relations", []) or []]
        if n["_type"] == "event":
            edges += [(i, x, 1) for x in n.get("involved", []) or []]
            if n.get("where"):
                edges.append((i, n["where"], 1))
            edges += [(x, i, 2) for x in n.get("after", []) or []]
    events = sorted((n for n in cards.values() if n["_type"] == "event"), key=lambda x: x["order"])
    n_open = {i: len(n.get("open", []) or []) for i, n in cards.items()}
    tot_open = sum(n_open.values())

    def src(f):
        if not f:
            return ""
        txt = re.sub(r"c(\d+):", lambda m: f'{L["ch"]} {m.group(1)}, {L["l"]} ', str(f))
        return f' <span class="src">({e(txt)})</span>'

    def link(i):
        n = cards[i]
        b = f'<span class="badge" title="{e(L["open_points"])}">{n_open[i]}</span>' if n_open[i] else ""
        return f'<a href="#card={i}" data-id="{i}">{e(n["name"])}</a>{b}'

    def items(title, xs, cls=""):
        if not xs:
            return ""
        rows = "".join(
            f'<li>{"<b>" + e(L["chapter"]) + " %s</b> — " % x["chapter"] if x.get("chapter") else ""}'
            f'{e(x.get("text", ""))}{src(x.get("source"))}</li>' for x in xs)
        return f'<h4>{e(title)}</h4><ul class="{cls}">{rows}</ul>'

    def card(n):
        i, t = n["id"], n["_type"]
        h = [f'<article class="card" id="s-{i}"><div class="type t{tidx[t]}">{e(plural[t])}</div><h3>{e(n["name"])}</h3>']
        if t == "event":
            off = "" if n.get("on_stage", True) else f' · {e(L["offstage"])}'
            ct = chs.get(n["chapter"], {}).get("title", "")
            h.append(f'<div class="meta">{e(L["chapter"])} {n["chapter"]} — {e(ct)} · {e(str(n.get("when", "")))}{off}</div>')
        else:
            aka = f'{e(L["aka"])}: ' + ", ".join(map(e, map(str, n["aliases"]))) + " · " if n.get("aliases") else ""
            h.append(f'<div class="meta">{aka}{e(L["chapters_n"])} {", ".join(map(str, chapters_of(n)))}</div>')
        h.append(f'<p>{e(str(n.get("summary", "")).strip())}</p>')
        if n.get("open"):
            h.append(f'<div class="open"><h4>{e(L["open_title"])} ({len(n["open"])})</h4><ul>'
                     + "".join(f'<li>{e(a.get("text", ""))}</li>' for a in n["open"]) + "</ul></div>")
        if t == "event":
            before = ", ".join(link(x) for x in n.get("after", []) or []) or "—"
            then = ", ".join(link(x["id"]) for x in events if i in (x.get("after") or [])) or "—"
            where = f'<li>{e(L["where"])}: {link(n["where"])}</li>' if n.get("where") else ""
            h.append(f'<h4>{e(L["where_who"])}</h4><ul>{where}<li>{e(L["involved"])}: '
                     f'{", ".join(link(x) for x in n.get("involved", []) or [])}</li></ul>')
            h.append(f'<h4>{e(L["chain"])}</h4><ul><li>{e(L["comes_from"])}: {before}</li>'
                     f'<li>{e(L["leads_to"])}: {then}</li></ul>')
        h.append(items(L["traits"], n.get("traits")))
        h.append(items(L["facts"], n.get("facts")))
        h.append(items(L["state"], n.get("state")))
        h.append(items(L["not_said"], n.get("not_said"), "notsaid"))
        h.append(items(L["notes"], n.get("notes"), "notsaid"))
        out = [(r["to"], r) for r in n.get("relations", []) or []]
        inc = [(j, r) for j, m in cards.items() for r in m.get("relations", []) or [] if r["to"] == i]
        if out or inc:
            rows = [f'<li>{e(r.get("type", ""))} {link(a)}{" — " + e(r["note"]) if r.get("note") else ""}{src(r.get("source"))}</li>'
                    for a, r in out]
            rows += [f'<li>{link(j)} <span class="meta">{e(r.get("type", ""))}</span> {e(L["this_card"])}{src(r.get("source"))}</li>'
                     for j, r in inc]
            h.append(f'<h4>{e(L["relations"])}</h4><ul>{"".join(rows)}</ul>')
        if t != "event":
            mine = [x for x in events if i in (x.get("involved") or []) or x.get("where") == i]
            if mine:
                h.append(f'<h4>{e(L["event_chain"])} ({len(mine)})</h4><ul>'
                         + "".join(f'<li><span class="meta">{e(L["ch"])} {x["chapter"]}</span> {link(x["id"])}</li>' for x in mine)
                         + "</ul>")
        h.append("</article>")
        return "".join(h)

    first = min(chs) if chs else 0
    options = "".join(f'<option value="{k}">{e(L["chapter"])} {k} — {e(c["title"])}</option>' for k, c in sorted(chs.items()))
    if events:
        per = "".join(
            f'<div class="chev" data-ch="{k}"{"" if k == first else " hidden"}>' + "".join(
                f'<a class="row" href="#card={x["id"]}" data-id="{x["id"]}"><b>{e(x["name"])}</b>'
                f'<small>{e(str(x.get("when", "")))}{"" if x.get("on_stage", True) else " · " + e(L["offstage"])}</small>'
                f'{e(str(x.get("summary", "")))}</a>' for x in events if x["chapter"] == k) + "</div>" for k in sorted(chs))
    else:
        per = "".join(
            f'<div class="chev" data-ch="{k}"{"" if k == first else " hidden"}>' + "".join(
                f'<a class="row" href="#card={n["id"]}" data-id="{n["id"]}"><b>{e(n["name"])}</b>'
                f'<small>{e(plural[n["_type"]])}</small>{e(str(n.get("summary", "")))}</a>'
                for n in sorted(cards.values(), key=lambda n: str(n["name"]).lower()) if k in chapters_of(n)) + "</div>"
            for k in sorted(chs))
    with_open = sorted((n for n in cards.values() if n.get("open")), key=lambda n: -len(n["open"]))
    open_list = "".join(
        f'<h4><a class="t{tidx[n["_type"]]}" href="#card={n["id"]}" data-id="{n["id"]}">{e(n["name"])}</a>'
        f'<span class="badge">{len(n["open"])}</span></h4>'
        + "".join(f'<a class="row op" href="#card={n["id"]}" data-id="{n["id"]}">{e(a.get("text", ""))}</a>' for a in n["open"])
        for n in with_open)
    allc = "".join(
        f'<h3 class="group t{tidx[t]}">{e(plural[t])}</h3>' + "".join(
            card(n) for n in sorted((n for n in cards.values() if n["_type"] == t),
                                    key=(lambda n: n["order"]) if t == "event" else (lambda n: str(n["name"]).lower())))
        for t in types if any(n["_type"] == t for n in cards.values()))
    start_ids = gs.get("start") or [n["id"] for n in sorted(
        (n for n in cards.values() if n["_type"] != "event"),
        key=lambda n: -sum(1 for a, b, _ in edges if n["id"] in (a, b)))[:8]]
    start = "".join(f"<li>{link(i)}</li>" for i in start_ids if i in cards)
    chips = " ".join(f'<button class="chip{" off" if t == "event" else ""}" data-t="{tidx[t]}"><i class="b{tidx[t]}"></i>{e(plural[t])}</button>'
                     for t in types if any(n["_type"] == t for n in cards.values()))
    data = json.dumps({
        "types": [plural[t] for t in types], "event": ev_i, "noResults": L["no_results"],
        "nodes": [[i, tidx[n["_type"]], n["name"], n_open[i], " ".join(map(str, n.get("aliases", []) or []))] for i, n in cards.items()],
        "edges": [[a, b, k] for a, b, k in edges if a in cards and b in cards]},
        ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    notices = f'<div class="notice sp">{e(gs.get("spoiler", L["spoiler"]))}</div>'
    if tot_open:
        notices += f'<div class="notice op">{e(gs.get("open_notice", L["open_notice"]))}</div>'
    names = [str(cards[i]["name"]) for i in start_ids[:3] if i in cards]
    return {
        "GRAPH_TITLE": e(gs.get("title", L["graph_title"])), "GRAPH_TEXT": e(gs.get("text", L["graph_text"])),
        "NOTICES": notices, "N_CARDS": str(len(cards)),
        "EVENTS_META": f" · {len(events)} {e(L['events'])}" if events else "",
        "N_OPEN": str(tot_open), "CHAPTERS_META": e(L["chapters_upto"].format(n=max(chs) if chs else 0)),
        "CHIPS": chips, "CHAPTER_OPTIONS": options, "PER_CHAPTER": per,
        "CHAPTER_LIST_TITLE": e(L["event_chain"] if events else L["cards_in_chapter"]),
        "OPEN_INTRO": e(L["open_intro"].format(n=tot_open, m=len(with_open))), "OPEN_LIST": open_list,
        "START": start, "ALL_CARDS": e(L["all_cards"].format(n=len(cards))), "CARDS": allc, "DATA": data,
        "SEARCH_PLACEHOLDER": e(gs.get("search_placeholder", f'{L["search_eg"]}: ' + ", ".join(names) + "…")),
        "TYPE_VARS": "".join(f"--t{i}:{PALETTE[i % len(PALETTE)]};" for i in range(len(types))),
        "TYPE_CLASSES": "".join(f".t{i}{{color:var(--t{i})}}.b{i}{{background:var(--t{i})}}" for i in range(len(types))),
    }, cards


# ─── Podcast ──────────────────────────────────────────────────────────────────

def duration(mp3, bitrate):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp3)],
                             capture_output=True, text=True, timeout=20).stdout.strip()
        return float(out)
    except (OSError, ValueError, subprocess.SubprocessError):
        kbps = int(re.sub(r"\D", "", str(bitrate)) or 96)
        return mp3.stat().st_size * 8 / (kbps * 1000)


def episodes(book, out_dir):
    pod = book.root / "podcast"
    bitrate = (book.config.get("podcast") or {}).get("bitrate", "96k")
    out = []
    for f in sorted((pod / "scripts").glob("episode-*.md")):
        mp3 = pod / "episodes" / f"{f.stem}.mp3"
        if not mp3.exists():  # already published only
            mp3 = out_dir / "episodes" / f"{f.stem}.mp3"
        if not mp3.exists():
            continue
        meta = G.frontmatter(f.read_text(encoding="utf-8"))
        out.append({"mp3": mp3, "file": f"episodes/{mp3.name}", "title": str(meta.get("title", f.stem)),
                    "text": str(meta.get("description", "")), "min": round(duration(mp3, bitrate) / 60)})
    return out


# ─── Page ─────────────────────────────────────────────────────────────────────

def sections(html, present):
    for name in ("COVER", "SUBTITLE", "FEATURED", "PODCAST", "GRAPH"):
        pat = re.compile(rf"<!--IF:{name}-->(.*?)<!--END:{name}-->", re.S)
        html = pat.sub(lambda m: m.group(1) if present.get(name) else "", html)
    return html


def find_cover(book, site):
    for name in ([site["cover"]] if site.get("cover") else []) + ["cover.jpg", "cover.png", "docs/cover.jpg"]:
        p = book.root / name
        if p.exists():
            return p
    return None


def build(book, check_only=False):
    site = load_site(book)
    L = labels(book, site)
    out = book.root / site.get("output", "docs")
    cfg = book.config
    title = site.get("title") or cfg.get("title", "")
    subtitle = site.get("subtitle", cfg.get("subtitle", ""))
    full = f"{title}: {subtitle}" if subtitle else title
    author = site.get("author") or (cfg.get("author_profile") or {}).get("name") or (cfg.get("author") or {}).get("name", "")
    problems = []

    has_graph = book.dir.exists() and (site.get("graph") or {}).get("show", True) is not False and any(book.cards_dir.rglob("*.yaml"))
    gvals, cards = graph_html(book, site, L) if has_graph else ({}, {})
    eps = episodes(book, out) if (site.get("podcast") or {}).get("show", True) is not False else []

    feat = site.get("featured") or []
    for f in feat:
        if f.get("id") and has_graph and f["id"] not in cards:
            problems.append(f"featured: '{f['id']}' is not a card shown in the graph")
        if not f.get("id") and not f.get("name"):
            problems.append("featured: every entry needs 'id' (graph card) or 'name'")
    bk = site.get("book") or {}
    dl = bk.get("download") or {}
    if dl.get("file") and not (book.root / dl["file"]).exists():
        problems.append(f"book.download.file: {dl['file']} not found")
    cover = find_cover(book, site)
    if not cover:
        problems.append("no cover (cover.jpg / cover.png in the book root): the page is built without it")
    if eps and not (book.config.get("podcast") or {}).get("base_url"):
        problems.append("podcast.base_url is empty in book.config.json: set it to <site URL>/episodes and run "
                        "python3 export_podcast.py feed, or podcast apps will not find the MP3s")
    if check_only:
        for p in problems:
            print("WARNING:", p)
        print(f"OK: site.yaml readable · graph: {len(cards)} cards · podcast: {len(eps)} episodes · output: {out.name}/")
        return 0

    out.mkdir(parents=True, exist_ok=True)
    if cover:
        shutil.copyfile(cover, out / ("cover" + cover.suffix.lower()))
        small = out / "cover-720.jpg"
        if cover.resolve() != small.resolve():
            try:
                from PIL import Image
                img = Image.open(cover).convert("RGB")
                img.thumbnail((720, 720 * 2), Image.LANCZOS)
                img.save(small, quality=82)
            except ImportError:
                if cover.suffix.lower() in (".jpg", ".jpeg"):
                    shutil.copyfile(cover, small)
    download = ""
    if dl.get("file") and (book.root / dl["file"]).exists():
        src = book.root / dl["file"]
        dest = out / "download" / src.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        download = (f'<p><a class="button" href="download/{e(src.name)}" download>{e(dl.get("label", L["download"]))}</a></p>'
                    + (f'<p class="meta">{e(dl["note"])}</p>' if dl.get("note") else ""))
    if eps:
        (out / "episodes").mkdir(exist_ok=True)
        for p in eps:
            dest = out / p["file"]
            if dest.resolve() == p["mp3"].resolve():
                continue
            if not dest.exists() or dest.stat().st_size != p["mp3"].stat().st_size or dest.stat().st_mtime < p["mp3"].stat().st_mtime:
                shutil.copyfile(p["mp3"], dest)
        feed = book.root / "podcast" / "feed.xml"
        if feed.exists():
            shutil.copyfile(feed, out / "feed.xml")

    def feat_card(f):
        name = cards[f["id"]]["name"] if f.get("id") in cards else f.get("name", f.get("id", ""))
        inner = (f'<span class="role">{e(f.get("role", ""))}</span><h3>{e(str(name))}</h3><p>{e(f.get("text", ""))}</p>')
        if f.get("id") in cards:
            return f'<a class="feat" href="#card={f["id"]}" data-id="{f["id"]}">{inner}<span class="go">{e(L["open_card"])}</span></a>'
        return f'<div class="feat">{inner}</div>'

    kind = FEATURED_KIND.get(book.preset, "featured_fiction")
    pod = site.get("podcast") or {}
    menu = [("book", L["book"])] + ([("featured", site.get("featured_title", L[kind]))] if feat else []) \
        + ([("podcast", L["podcast"])] if eps else []) + ([("graph", L["graph"])] if has_graph else [])
    buttons = ([f'<a class="button" href="#podcast">{e(L["listen"])}</a>'] if eps else []) \
        + [f'<a class="button{" two" if eps else ""}" href="#book">{e(L["read"])}</a>'] \
        + ([f'<a class="button two" href="#graph">{e(L["explore"])}</a>'] if has_graph else [])
    vals = {
        "LANG": e(book.lang), "BG": site.get("colors", {}).get("background", "#0e1116"),
        "ACCENT": site.get("colors", {}).get("accent", "#6ee7a0"),
        "TITLE": e(full), "NAME": e(title), "SUBTITLE": e(subtitle), "AUTHOR": e(author),
        "KICKER": e(site.get("kicker", "")), "TAGLINE": e(site.get("tagline", "")),
        "TOP_COLS": "minmax(0,340px) 1fr" if cover else "1fr",
        "MENU": "".join(f'<a href="#{a}">{e(b)}</a>' for a, b in menu), "BUTTONS": "".join(buttons),
        "BOOK_TITLE": e(bk.get("title", L["book"])), "BOOK": "".join(f"<p>{e(p)}</p>" for p in bk.get("paragraphs", [])),
        "DOWNLOAD": download, "FEATURED_TITLE": e(site.get("featured_title", L[kind])),
        "FEATURED": "".join(feat_card(f) for f in feat),
        "PODCAST_TITLE": e(pod.get("title", L["podcast_title"])), "PODCAST_TEXT": e(pod.get("text", L["podcast_text"])),
        "N_EPISODES": str(len(eps)),
        "EPISODES": "".join(
            f'<li><h3>{e(p["title"])}</h3><p>{e(p["text"])}</p><div class="audio"><audio controls preload="none" '
            f'src="{e(p["file"])}"></audio><span class="meta">{p["min"]} {e(L["min"])}</span></div></li>' for p in eps),
        "TYPE_VARS": "", "TYPE_CLASSES": "",
    }
    vals.update({f"L_{k}": e(v) for k, v in L.items()})
    vals.update(gvals)
    tpl = None
    for base in (book.root, SCRIPT_DIR):
        if (base / "site" / "page.html").exists():
            tpl = (base / "site" / "page.html").read_text(encoding="utf-8")
            break
    page = sections(tpl, {"COVER": bool(cover), "SUBTITLE": bool(subtitle), "FEATURED": bool(feat),
                          "PODCAST": bool(eps), "GRAPH": has_graph})
    missing = set()
    page = re.sub(r"\{\{(\w+)\}\}", lambda m: vals[m.group(1)] if m.group(1) in vals else missing.add(m.group(1)) or "", page)
    if missing:
        sys.exit(f"template placeholders without a value: {', '.join(sorted(missing))}")
    (out / "index.html").write_text(page, encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    for p in problems:
        print("WARNING:", p)
    size = sum(f.stat().st_size for f in out.rglob("*") if f.is_file())
    if size > 900 * 1024 * 1024:
        print(f"WARNING: {out.name}/ is {size // 2**20} MB — GitHub Pages sites are limited to 1 GB")
    print(f"OK: {out.name}/index.html ({len(page) // 1024} KB) · {len(eps)} episodes · {len(cards)} graph cards"
          f" · {sum(len(c.get('open', []) or []) for c in cards.values())} open points")
    return 0


def init(book):
    p = book.root / "site.yaml"
    if p.exists():
        sys.exit("site.yaml already exists")
    cfg = book.config
    kind = FEATURED_KIND.get(book.preset, "featured_fiction")
    L = LABELS.get(book.lang, LABELS["en"])
    skel = {
        "title": cfg.get("title", ""), "subtitle": cfg.get("subtitle", ""),
        "author": (cfg.get("author_profile") or {}).get("name", ""), "kicker": "", "tagline": "",
        "book": {"title": L["book"], "paragraphs": [""],
                 "download": {"file": "", "label": L["download"], "note": ""}},
        "featured_title": L[kind], "featured": [{"id": "", "role": "", "text": ""}],
        "podcast": {"title": L["podcast_title"], "text": L["podcast_text"]},
        "graph": {"title": L["graph_title"], "text": L["graph_text"], "spoiler": L["spoiler"],
                  "up_to_chapter": None, "start": []},
        "output": "docs",
    }
    p.write_text("# Texts of the book website (docs/index.html). After a change: python3 build_site.py\n"
                 + yaml.safe_dump(skel, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")
    print(f"written {p.name}: fill it, then  python3 build_site.py")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Ghost Writer — book website")
    ap.add_argument("--book", default=None, help="book root (default: current dir)")
    ap.add_argument("--init", action="store_true", help="write a site.yaml skeleton")
    ap.add_argument("--check", action="store_true", help="validate, write nothing")
    a = ap.parse_args(argv)
    root = Path(a.book) if a.book else Path.cwd()
    if not a.book and not (root / "book.config.json").exists() and (SCRIPT_DIR / "book.config.json").exists():
        root = SCRIPT_DIR
    book = G.Book(root)
    if a.init:
        return init(book)
    return build(book, check_only=a.check)


if __name__ == "__main__":
    sys.exit(main())
