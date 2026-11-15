#!/usr/bin/env python3
"""End-to-end tests for graph.py on a throw-away 2-chapter book.

  python3 tests/test_graph.py
"""
import contextlib
import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import graph  # noqa: E402
import build_site  # noqa: E402

CH1 = """---
title: Il faro
version: 1.0
claim: x
status: {status}
---

Marta salì le scale del faro alle sei del mattino, come ogni giorno da vent'anni.

In cima trovò la lanterna spenta e un biglietto piegato in due sotto la lente.

Il biglietto diceva soltanto: «Non accenderla stanotte».

Marta lo mise in tasca e scese a fare colazione con il gatto Ferro.

---

## Demolition Log
"""
CH2 = """---
title: La notte
version: 1.0
claim: y
status: {status}
---

Quella notte Marta non accese la lanterna.

Alle due una nave passò vicino agli scogli senza vederli.
"""
P1 = """@ characters/marta
name: "Marta"
summary: "La guardiana del faro."
traits: {text: "Sale al faro alle sei", source: "c1:8", quote: "alle sei del mattino, come ogni giorno"}
relations: {to: ferro, type: "vive con", source: "c1:14", quote: "con il gatto Ferro"}
@ characters/ferro
name: "Ferro"
summary: "Il gatto."
traits: {text: "È un gatto", source: "c1:14", quote: "il gatto Ferro"}
@ objects/biglietto
name: "Il biglietto"
summary: "Biglietto sotto la lente."
traits: {text: "Piegato in due", source: "c1:10", quote: "un biglietto piegato in due"}
traits: {text: "Dice: «Non accenderla stanotte»", source: "c1:12", quote: "Non accenderla stanotte"}
open: {text: "Chi l'ha scritto?"}
"""
P2 = """@ characters/marta
state: {chapter: 2, text: "Non accende la lanterna", source: "c2:8", quote: "Marta non accese la lanterna"}
@ objects/nave
name: "La nave"
summary: "Passa vicino agli scogli."
traits: {text: "Passa vicino agli scogli", source: "c2:10", quote: "passò vicino agli scogli"}
"""


class GraphTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "chapters").mkdir()
        (self.root / "book.config.json").write_text(json.dumps({"language": "it", "preset": "fiction"}))
        self.write(1, CH1.format(status="draft"))
        self.write(2, CH2.format(status="draft"))

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, n, text):
        name = {1: "01-il-faro.md", 2: "02-la-notte.md"}[n]
        (self.root / "chapters" / name).write_text(text, encoding="utf-8")

    def edit(self, n, old, new):
        name = {1: "01-il-faro.md", 2: "02-la-notte.md"}[n]
        p = self.root / "chapters" / name
        p.write_text(p.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")

    def run_graph(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            try:
                code = graph.main(["--book", str(self.root), *args])
            except SystemExit as e:  # refusals exit with a message
                print(e)
                code = 1
        return code, out.getvalue()

    def patch(self, text):
        p = self.root / "patch.txt"
        p.write_text(text, encoding="utf-8")
        self.assertEqual(self.run_graph("apply", str(p))[0], 0)

    def hashes(self, sub="graph"):
        base = self.root / sub
        return {p.relative_to(base).as_posix(): hashlib.sha1(p.read_bytes()).hexdigest()
                for p in base.rglob("*") if p.is_file()}

    def two_chapters(self):
        self.edit(1, "status: draft", "status: complete")
        self.run_graph("start")
        self.patch(P1)
        self.assertEqual(self.run_graph("commit", "1")[0], 0)
        self.edit(2, "status: draft", "status: complete")
        self.run_graph("start")
        self.patch(P2)
        self.assertEqual(self.run_graph("commit", "2")[0], 0)

    def test_1_birth_and_extension(self):
        _, out = self.run_graph("check")
        self.assertIn("not created yet", out)
        self.assertFalse((self.root / "graph").exists())
        self.edit(1, "status: draft", "status: complete")
        _, out = self.run_graph("start")
        self.assertIn("NEW", out)
        self.assertTrue((self.root / "graph").exists())
        self.patch(P1)
        code, out = self.run_graph("commit", "1")
        self.assertEqual(code, 0, out)
        self.assertIn("3 new cards", out)
        self.edit(2, "status: draft", "status: complete")
        self.run_graph("start")
        self.patch(P2)
        code, out = self.run_graph("commit", "2")
        self.assertEqual(code, 0, out)
        self.assertIn("1 new cards, 1 modified", out)
        self.assertIn("up to date", self.run_graph("check")[1])
        self.assertTrue((self.root / "graph/view/characters/marta.md").exists())

    def test_invalid_id_stops_and_rolls_back(self):
        self.edit(1, "status: draft", "status: complete")
        self.run_graph("start")
        self.patch(P1 + '@ objects/lente\nname: "Lente"\nrelations: {to: nessuno, type: "x"}\n')
        code, out = self.run_graph("commit", "1")
        self.assertEqual(code, 1)
        self.assertIn("'nessuno' does not exist", out)
        self.assertFalse((self.root / "graph/chapters.yaml").exists())
        self.assertIn("TO ANALYZE", self.run_graph("check")[1])

    def test_2_new_version_relocates(self):
        self.two_chapters()
        before = self.hashes("graph/cards")
        self.edit(1, "version: 1.0", "version: 1.1")
        self.edit(1, "Marta salì", "Il vento soffiava da nord.\n\nMarta salì")
        self.edit(1, "«Non accenderla stanotte»", "«Stanotte resta al buio»")
        _, out = self.run_graph("start")
        self.assertIn("TO RE-ANALYZE", out)
        self.assertIn("+ new c1:8: Il vento soffiava da nord.", out)
        self.assertIn("LOST  c1:12", out)
        code, out = self.run_graph("commit", "1")
        self.assertEqual(code, 1)          # lost source blocks the commit
        self.assertEqual(before, self.hashes("graph/cards"))
        self.patch('@ objects/biglietto\n-traits: "Dice:"\n'
                   'traits: {text: "Dice: «Stanotte resta al buio»", source: "c1:14", quote: "Stanotte resta al buio"}\n')
        code, out = self.run_graph("commit", "1")
        self.assertEqual(code, 0, out)
        after = self.hashes("graph/cards")
        self.assertEqual(before["objects/nave.yaml"], after["objects/nave.yaml"])  # untouched
        marta = (self.root / "graph/cards/characters/marta.yaml").read_text(encoding="utf-8")
        self.assertIn('source: "c1:10"', marta)   # 8 -> 10
        self.assertIn('source: "c1:16"', marta)   # 14 -> 16
        self.assertIn('source: "c2:8"', marta)    # other chapter untouched
        self.assertNotIn("Non accenderla", (self.root / "graph/cards/objects/biglietto.yaml").read_text(encoding="utf-8"))

    def test_4_drafts_and_suspended(self):
        self.edit(1, "status: draft", "status: complete")
        self.run_graph("start")
        self.patch(P1)
        self.run_graph("commit", "1")
        snap = self.hashes()
        self.edit(2, "version: 1.0", "version: 1.1")          # draft changes version
        self.assertIn("drafts ignored", self.run_graph("check")[1])
        self.run_graph("start")
        self.assertEqual(snap, self.hashes())
        self.assertEqual(self.run_graph("commit", "2")[0], 1)   # drafts are refused
        # chapter 1 goes back in progress and is edited
        self.edit(1, "status: complete", "status: in-review")
        self.edit(1, "version: 1.0", "version: 1.2")
        self.edit(1, "Marta lo mise in tasca", "Marta lo bruciò")
        _, out = self.run_graph("check")
        self.assertIn("SUSPENDED", out)
        self.assertEqual(self.run_graph("commit", "1")[0], 1)
        self.assertEqual(self.run_graph("validate")[0], 0)       # validated against the snapshot
        self.assertEqual(snap, self.hashes())
        self.edit(1, "status: in-review", "status: complete")
        self.assertIn("TO RE-ANALYZE", self.run_graph("check")[1])

    def test_site(self):
        self.two_chapters()
        (self.root / "site.yaml").write_text(
            'title: Prova\ntagline: "Un faro."\nbook: {paragraphs: ["Testo."]}\n'
            'featured: [{id: marta, role: Guardiana, text: "Sale al faro."}]\ngraph: {up_to_chapter: null}\n',
            encoding="utf-8")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(build_site.main(["--book", str(self.root)]), 0)
        html = (self.root / "docs/index.html").read_text(encoding="utf-8")
        self.assertIn('id="s-nave"', html)
        self.assertIn('href="#card=marta"', html)
        self.assertNotIn("{{", html)
        p = self.root / "site.yaml"
        p.write_text(p.read_text(encoding="utf-8").replace("up_to_chapter: null", "up_to_chapter: 1"), encoding="utf-8")
        with contextlib.redirect_stdout(out):
            build_site.main(["--book", str(self.root)])
        html = (self.root / "docs/index.html").read_text(encoding="utf-8")
        self.assertNotIn('id="s-nave"', html)       # chapter 2 only: hidden
        self.assertNotIn("Non accende la lanterna", html)  # chapter 2 state of Marta: hidden


if __name__ == "__main__":
    unittest.main(verbosity=2)
