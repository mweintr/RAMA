---
name: brainstorm
description: Brainstorm a story idea to start a new RAMA book. Begins from nothing, or from whatever seed the author has (an image, a what-if, a character, a period, a genre, a feeling), offers a wide spread of distinct premises, and narrows them with the author over a few rounds into one concept: logline, protagonist, conflict, setting, ending direction, voice and working title. Saves it as the Concept file, which /rama:config then builds the synopsis, outline, style guide and story bible from. Usage /rama:brainstorm, or /rama:brainstorm "a lighthouse keeper who finds a key".
---

# RAMA: Brainstorm

Read `references/project-files.md` and `references/survey.md` first.

`brainstorm` comes before everything else. It turns "I want to write a
book" into a concept solid enough for `/rama:config` to build a project on.
RAMA proposes; the author chooses. (`freeflow` is the reverse: the author has
the material and RAMA sorts it.)

## Rules

- **Wide first, narrow later.** The first round of premises should spread
  across genuinely different books. Don't filter out an idea for being odd.
- **Distinct, not variations.** Three takes on the same premise count as one.
- **Specific, not generic.** Every premise names a person, a place, a time
  and a problem. "A woman confronts her past" is not a premise. "In 1887 a
  lighthouse keeper's widow finds the key her husband swore he threw into the
  sea" is.
- **Every premise needs an engine.** Say what keeps generating chapters
  through the middle of the book, not just how it opens.
- **The author's taste governs.** Recommend when there's a craft reason (a
  premise with no middle, an ending that undercuts the hook), never on taste.
- **Fresh names.** Avoid stock names that read as machine-made (Elara,
  Alara, Volkov, Priya, Kael, Lyra, Seraphina and the like) and any names
  the author bans. Fit names to the period and place.
- **Nothing is final until the Concept file is approved.** Don't create
  outline, synopsis or style guide files here; that's `config`'s job.

## Phase 0: Where the project goes

Find the working folder (see `project-files.md → Where the project lives`).

- **It already holds a RAMA project** (a RAMA Log, an outline or a
  manuscript): say so, and ask with a survey whether to start a new book in a
  new subfolder, brainstorm for this book anyway (the Concept file is then
  reference material, never canonical), or stop.
- **It's empty, or holds only notes**: use it. Read any notes, old style
  guides or earlier books there; they show the author's taste and voice.
  Tell the author in one line what you took from them.

## Phase 1: Seed

If the author gave a seed with the command, start from it. Otherwise ask
with one survey round (up to four questions). Ask only what the author hasn't
already said:

1. **What do you have?** A seed (image, what-if, character, setting) / The
   kind of book I want, not the story / Nothing yet: surprise me.
2. **What kind of book?** Three options for genre or shelf, built from any
   seed or notes; with none, spread them wide (e.g. literary historical /
   crime or suspense / speculative).
3. **When and where?** Three periods or settings that suit what's known so
   far.
4. **What should it feel like?** Three tones or comparable books.

If they answer "a seed," ask them to give it in their own words before going
on. Treat everything they say as constraints on Phase 2, and keep a short
list of what they said they love or won't write.

## Phase 2: Diverge

Offer **10–12 premises**, grouped under **three or four approaches**. An
approach is a different kind of book from the same seed, e.g. for "a
lighthouse keeper finds a key": *a mystery about what it opens · a marriage
story · a ghost story that may not be one · a story about the town*.

```
PREMISES

A. The mystery of what it opens
  1. THE SALT KEY · Historical suspense, Maine, 1887
     A keeper's widow finds the key her husband swore he threw into the sea,
     and the lock it fits is in the house of the man who drowned him.
     Engine: each door she opens costs her someone's trust in the town.
     Ends toward: she opens the last door and chooses not to look.
  2. …

B. A marriage story
  4. …

WILD CARD
  11. …

My pick: 1, because its engine runs to the last chapter.  (only with a craft reason)
```

Each premise gets a **working title**, a **genre and setting tag**, a
**logline** (one or two sentences with a protagonist, a want and an
obstacle), an **engine** line, and an **ends toward** line. Include at least
one **wild card** that breaks an assumption in the author's seed.

Then ask, in plain text so the author can answer freely:

> Star the ones with life in them, strike the dead ones, or combine numbers
> ("1 + 6"). Say "more like B" for another round in one direction, or "none
> of these" and tell me why.

## Phase 3: Develop

Work from the author's reply. Run **at most three rounds** before narrowing.

- **Starred or combined premises**: develop each into a pitch paragraph of
  about 150 words: the protagonist and what they want, what stands in the
  way, the turn at the middle, the ending, and why this story needs this
  period and place. Then test it in three lines:
  - **The middle:** what happens in chapters 8–15? If you can't say, the
    premise has no middle; say so.
  - **The ending:** does it answer the question the opening asks?
  - **The narrator:** who tells it, and what they know that the reader
    doesn't.
- **"More like X"**: 6–8 fresh premises in that direction, none repeating
  earlier ones.
- **"None of these"**: take the reason seriously, restate the constraints
  with it, and go wide again from a different angle.
- **The author's own idea**: develop it on equal terms with RAMA's.

When two or three remain, present them side by side and ask with a survey:
the finalists (or two finalists and a combination), recommended first only
with a craft reason, plus the write-in.

## Phase 4: Deepen

With one premise chosen, settle what `config` will need for the synopsis.
Ask in survey rounds (up to four questions a round, at most three rounds),
with three options for each that are built from the chosen premise. Skip
anything already settled:

- **Protagonist**: who they are, what they want, what they need instead.
- **Opposition**: the person or force in the way, and what it wants.
- **The central turn**: what changes everything at the middle.
- **The ending**: how it resolves, and what it costs.
- **Narrator and POV**: first or third, past or present, and the narrator's
  distance from events (retrospective, close, unreliable).
- **Voice and register**: give three short sample passages (three or four
  sentences each, same moment, different voices) and ask which is closest.
- **Scope**: length and audience, and whether it's standalone or a series.
- **Title**: three title options plus the working title.

Mark anything still open as `[OPEN]` in the Concept file rather than asking
a fourth round.

## Phase 5: The Concept file

Write the concept and show it for approval:

```markdown
# <Title> — Concept

**Logline.** One or two sentences.

**Genre and shelf.** Genre · comparable books · length · audience · standalone or series.

**Setting.** Period, place, and why the story needs them.

**Premise.** The pitch paragraph, revised with everything decided.

**Protagonist.** Name, age, situation; want; need; flaw.

**Opposition.** Who or what, and what they want.

**Shape.** Opening situation · inciting event · central turn · crisis · ending, one line each.

**Engine.** What generates chapters through the middle.

**Narrator and voice.** POV, tense, distance; the chosen sample passage, verbatim.

**Themes.** Two or three, in plain words.

**Open questions.** Every `[OPEN]` item, for config to settle.

## Ideas not used
Starred premises that lost, one line each, and anything struck with the
author's reason, so a later session doesn't offer it again.
```

Revise it on the author's notes until they approve. Then save it as
`<Title> — Concept.md` in the project folder (in a new subfolder named after
the working title if Phase 0 chose one). In a read-only claude.ai Project,
write it to `/mnt/user-data/outputs/` and ask the author to add it to the
Project.

Finish with:

> Concept saved: *<Title>*. Next: `/rama:config` builds the synopsis,
> outline, style guide and story bible from it.
