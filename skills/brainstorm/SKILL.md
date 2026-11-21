---
name: brainstorm
description: RAMA generates ideas for you. Give it a chapter, a scene, a story problem, a character, an open thread, or something to name (title, chapter heads, characters, places), and it reads the project files, then offers a wide spread of options grounded in the book, sorted by approach. You pick, combine and push back over a few rounds until one idea holds, and RAMA turns it into a Decision, beats, or outline and bible proposals. Usage /rama:brainstorm 7, /rama:brainstorm "how does Keziah learn about the key", /rama:brainstorm names, /rama:brainstorm title.
---

# RAMA: Brainstorm

Read `references/project-files.md` and `references/survey.md` first.

`freeflow` is for when the author has the ideas and needs them sorted.
`brainstorm` is for when the author needs ideas: RAMA proposes, the author
chooses. It works before anything is written (a stuck outline entry, a
chapter with no clear shape) and after (a turn that demolish showed was
unearned, a thread with no payoff).

## Rules

- **Quantity first, judgment second.** The first round is wide. Don't filter
  out an idea for being odd; filter it out only if it breaks the book.
- **Every idea comes from this book.** Use its characters, places, objects,
  period and register. No generic craft-manual options ("add a ticking
  clock") unless they're dressed in the book's own material.
- **Ideas are distinct, not variations.** Ten versions of the same move count
  as one idea. Spread across different approaches.
- **Flag conflicts; don't hide good ideas because of them.** If an idea breaks
  a Decision, the outline, the bible or the Continuity Ledger, show it anyway
  and mark the conflict, unless it breaks a fact already fixed in the written
  text and the author hasn't asked to revise.
- **The author decides.** Recommend when there's a reason, and never settle a
  question of taste for them.
- **Nothing goes into the manuscript.** Brainstorm can write to the RAMA Log,
  the Beats file and the Brainstorm file, and propose changes to the outline
  or bible. It never changes prose.

## Arguments

`/rama:brainstorm <target>`. The target can be:

| Target | Example | What RAMA generates |
|---|---|---|
| A chapter | `7` | Shapes for the chapter: openings, turns, endings, what to dramatize or hold back |
| A scene or moment | `7 the landing` | Ways to play the moment |
| A problem or question | `"why doesn't Sharp just leave?"` | Answers, each with its cost to the rest of the book |
| A character | `character Keziah` | Wants, secrets, contradictions, scenes that would test them |
| An open thread | `thread the second key` | Payoffs, and where each one would land |
| Names | `names`, `names a ship` | Character, place or object names fit to the period and setting |
| Title or chapter heads | `title`, `heads 5-9` | Titles, or chapter heads in the style guide's form |
| Anything else | `"what's the book's last image?"` | Whatever fits |

With no target, ask with a survey. Build the three options from the project:
the next chapter without beats, the oldest Open Thread with no payoff, and the
most recent `deferred` item from a Demolition Log or review (fall back to
whatever is most stuck if any of these doesn't exist).

If no RAMA Log exists, say so and suggest `/rama:config`. Brainstorm still
works from whatever files are there, or from the author's description alone
if there are none.

## Phase 1: Read

Say: `Brainstorming <target>. Reading…`

Read what the target touches, not the whole book by default:

- **Always**: the RAMA Log (Decisions, Continuity Ledger, Open Threads, and
  any Demolition or Review Log entries on the target), the synopsis, and the
  style guide's sections on voice, register, POV and naming.
- **The Brainstorm file**, if it exists: earlier sessions on the same or a
  nearby target. Don't offer an idea the author already rejected unless you
  can say what has changed. Build on ideas they starred.
- **Chapter or scene**: its outline entry and the ones on either side, its
  beats if any, and the written text of the chapters around it.
- **Problem or thread**: every place in the outline, bible and manuscript
  where it's raised or touched (search for the names and objects involved).
- **Character**: their bible entry, `characters/<Name>.md` if it exists, and
  every scene they're in so far.
- **Names**: the bible's existing names (to avoid clashes of sound and
  initial), the period and place, and any naming rules or banned names in the
  style guide or RAMA Log.
- **Title or chapter heads**: the synopsis, the style guide's chapter-head
  form, and the existing heads in the outline and manuscript.

## Phase 2: Frame

Write the question back in one line, as RAMA understands it, with the
constraints the files impose:

> **The question:** How does Keziah learn the key has come back, given that
> Harold has sworn not to tell her (ch 3) and she can't read (bible)?
> **Must keep:** her ignorance through ch 8 · the moon calendar.
> **Open:** who tells her, and whether she lets on.

If the framing depends on something the files don't settle (how far the
author will let the outline move, whether the written chapters can be
revised, the tone they're after), ask up to three survey questions first.
Otherwise go straight to Phase 3; the author will correct the framing in
their reply if it's wrong.

## Phase 3: Diverge

Offer **12–15 ideas** (8–10 for a narrow target like a single beat; 20–30 for
names or titles), grouped under **three to five approaches**. An approach is a
different kind of answer, e.g. for "how does she learn": *someone tells her ·
she finds evidence · she's known all along · she never learns, and that's the
point*.

```
BRAINSTORM: How does Keziah learn the key has come back?

A. Someone tells her
  1. Sharp lets it slip, thinking she already knows. — Puts Sharp in her debt;
     gives ch 9 its quarrel.
  2. …

B. She finds evidence
  4. The salt crust on Harold's boots is the wrong color for the home shore.
     ⚠ Needs the bible to say where the key was found.
  5. …

C. She knew all along
  8. She saw it in ch 3 and has been waiting for Harold to say so. — Reframes
     her silence in ch 4–6 as a test. ⚠ Conflicts with Decision 2026-11-16
     ("Keziah learns in ch 7").

WILD CARD
  14. …

My pick: 4, because …  (only if there's a reason beyond taste)
```

Each idea gets **one line of what happens** and **one line of what it does to
the book**: what it opens, costs, pays off or makes possible. Mark any
conflict with `⚠` and name what it conflicts with. Always include at least
one **wild card**: the idea that breaks the author's assumption about the
target.

For names and titles, give each one a few words on why (period, meaning,
sound against the other names), and group by flavor rather than by approach.

Then ask, in plain text so the author can answer freely:

> Star the ones with life in them, strike the dead ones, or combine numbers
> ("4 + 8"). Say "more like B" for another round in one direction, or "none of
> these" and tell me why.

## Phase 4: Develop

Work from the author's reply. Run **at most three rounds** before Phase 5.

- **Starred or combined ideas**: develop each into a short paragraph: how it
  plays on the page, the scene it lands in, what changes downstream (later
  chapters, threads, the Ledger), and what it costs. If two starred ideas
  pull against each other, say how.
- **"More like X"**: a fresh round of 6–8 ideas in that direction, none
  repeating earlier ones.
- **"None of these"**: take the reason seriously. Restate the question with
  the new constraint and go wide again from a different angle. Don't offer
  the same ideas in new words.
- **The author adds their own idea**: treat it as a starred idea and develop
  it on equal terms with RAMA's.

When the field is down to two or three, present them side by side with a
survey: three options (the finalists, or the two finalists plus a combination),
the recommended one first if there's a reason, plus the write-in.

## Phase 5: Land

Once the author picks, write the result in two or three sentences, as it
would sit in the book. Then hand off with a survey built from the target,
e.g. for a chapter: **Build beats for Chapter <n> with this (Recommended) /
Log it as a Decision and stop / Keep it as a note, not decided yet.** Other
hand-offs, as they fit:

- **Decision**: log it in the RAMA Log under Decisions:
  `2026-11-21 · ch 7 · Keziah learns of the key from the salt on Harold's boots (brainstorm).`
- **Beats**: run the `beats` procedure for the chapter with the result as a
  settled input, and tag the beats it produces `(From brainstorm)`.
- **Outline or bible change**: propose each change as current text versus
  proposed text, one at a time, and apply only with the author's OK.
- **Names or title**: once chosen, offer to add them to the bible (names) or
  log the title in the RAMA Log's Project section.
- **Note**: save to the Brainstorm file only, undecided.

Whatever the hand-off, save the session to the Brainstorm file.

## The Brainstorm file

`<Title> — Brainstorm.md` keeps every session, so good ideas that lost one
round aren't lost for good. Create it if needed, with `# <Title> — Brainstorm`
as its first line. Add each session at the end:

```markdown
## 2026-11-21 · ch 7 · How does Keziah learn the key has come back?

**Chosen:** The salt on Harold's boots (idea 4), logged as a Decision.
**Starred, not used:** 1 (Sharp's slip; maybe for ch 9) · 8
**Struck:** 2, 5, 11 (author: "she'd never go through his things")

<the full idea list from the last round, as shown>
```

Record why the author struck ideas when they said why, so later sessions
don't offer them again. In a read-only claude.ai Project, write the full file
to outputs as `project-files.md` describes.

Finish with one line naming the files that changed, and the next step:

> Logged a Decision and saved the session to the Brainstorm file. Next: `/rama:beats 7`.
