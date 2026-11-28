---
name: compose
description: Ghost-write one chapter of a RAMA book from its approved beats, following the style guide to the letter. Asks any remaining questions as a survey first, drafts the full chapter into its own Claude Doc, self-checks it, runs /rama:check on it, then presents the Doc and adds the chapter to the manuscript file. Usage /rama:compose 5. Run after /rama:beats 5.
---

# RAMA: Compose

Writes the chapter. The beats say what happens, and the style guide says how
it reads. Your job is prose the author would sign.

Before starting, read `references/project-files.md` and `references/survey.md`.

## Arguments

`/rama:compose <n>`. With no number, use the first chapter that has beats and
no draft, and say which.

If chapter `n` has no beats in the Beats file, ask in a survey: **Run beats
first (Recommended) / Compose straight from the outline / Cancel.**

If chapter `n` is already in the manuscript, ask: **Write a fresh draft to
compare / Revise the existing text against the beats / Cancel.** Never
overwrite written text without that answer.

## Step 1: Read

Say right away: `Composing Chapter <n>: <chapter head>. Reading…`

1. **Style guide**: **in full, every time.** It is the governing document. Pay
   special attention to banned constructions, punctuation quotas, POV limits,
   register samples and the revision checklist.
2. **Beats**: this chapter's section, including *For compose* and [ASSUMED].
3. **RAMA Log**: Decisions, Continuity Ledger and Open Threads.
4. **Outline**: this chapter's entry and its Tracking rows.
5. **Story bible**: characters, places and facts the beats touch.
6. **Manuscript**: the **full text of the previous chapter** (for voice,
   rhythm and the exact handoff), plus the opening of the first chapter as a
   voice anchor. Look up the earlier passage behind every Continuity Ledger
   fact the beats rely on.

## Step 2: Last questions

Survey only what's still open: the beats' *For compose* list, [ASSUMED] items
the author hasn't confirmed, and anything the read turned up (a beat that now
conflicts with the Ledger, say). Use up to two batches. If nothing is open,
skip straight to drafting and say so in one line.

## Step 3: Draft

Write the whole chapter in one pass, in the manuscript format from
`project-files.md`:

- Heading: `## <Designation>: <Chapter head>` exactly as the RAMA Log
  specifies. If this chapter opens a Part, put the Part heading (and any frame
  passage the outline puts there) above it.
- One scene per beat group. Use the style guide's scene-break mark between
  scenes, with no break before the first scene.
- Hit the target length within ±10%.
- Follow every beat, in order. If the prose needs a beat changed, change it,
  and report the change in Step 7. Don't drop one silently.

Prose discipline:
- **The style guide wins** over your own habits, the outline's wording and
  genre convention. When it bans a construction, don't use it even once.
- Match the voice of the written chapters, not a generic version of the genre.
  Reread the register samples if the book has them.
- Concrete and specific: names, objects, weather, tools and period detail
  from the bible and outline. Never invent a fact that contradicts the Ledger.
  When you must invent one (a minor name, a distance), log it in Step 8.
- End on the image or line the beats give for *Ends on*.
- Avoid the stock AI tells: not-X-but-Y contrasts, triads by reflex, one-line
  zingers closing paragraphs, staged openers, stacked em dashes, abstract
  emotional summary after a concrete moment, and "something shifted"
  vagueness. If the style guide has its own list, it covers these too.

## Step 4: Self-check

Go through the draft against the style guide's **Revision Checklist** (or, if
there is none, its stated rules) and against the beats. Fix what you find
before going on. Count anything the guide quantifies (em dashes per 1,000
words, addresses to the reader per chapter). Don't carry a draft you know
breaks a rule into the next step.

## Step 5: Chapter Doc

Put the draft in its own **Claude Doc**, titled `<Title> - Chapter <n>`
(e.g. *The Shape of the Sea - Chapter 6*), with the chapter heading exactly as
it will stand in the manuscript and the full chapter text below it, scene
breaks included. Create it through the docs skill or the Claude Docs connector
(load its instructions first) and follow its rules for making a doc. This Doc
is the working copy of the chapter until it goes into the manuscript.

- If a Doc with that title already exists from an earlier session (the RAMA
  Log records it), update it in place when the author chose **Revise the
  existing text**. For **Write a fresh draft to compare**, make a new Doc
  titled `<Title> - Chapter <n> (new draft)` and leave the old one alone.
- Record the Doc's link in the RAMA Log, Chapter Status, as soon as it exists.
- If no docs tool is available, say so in one line and keep the draft as a
  file instead: `<Title> - Chapter <n>.md` in the project folder, or in
  outputs for a read-only Project. Every later step uses that file in place of
  the Doc.

Don't paste the chapter into chat at this stage. Say in one line that the Doc
exists and that the check comes next.

## Step 6: Check

Run **`/rama:check <n>`** on the draft before the author sees it. Invoke the
check skill (`Skill` tool in Claude Code / Cowork: `rama:check`; in claude.ai,
the **rama-check** skill) and follow it in full, with these differences, which
check's *Called from compose* section also states:

- The chapter is not in the manuscript yet. Check reads it from the Chapter
  Doc, and checks it against the manuscript chapters before it.
- Every fix the author approves goes into the Chapter Doc, not the manuscript.
- Check writes its report and Check History as usual, then hands back here
  instead of closing out on its own.

If the check skill isn't installed, run its passes yourself from the style
guide, beats, Ledger and earlier chapters, and say so.

## Step 7: Present and add to the manuscript

Once the check is complete:

1. **Present the Chapter Doc.** Open it for the author (or give its link).
   Don't paste the full chapter into chat. Then a short note, no more than
   eight lines:

   ```
   Chapter 5 · 3,640 words (target 3,600) · 4 scenes
   Doc: The Shape of the Sea - Chapter 5
   Beats changed: 3.2 (Sharp names the boat, not Harold; the POV rule required it)
   New facts: Sharp's skiff is the *Ruth*; the landing is the north cove
   Check: 9 findings, 8 fixed, 1 kept as intentional. Em dashes 3 (quota 3)
   Open: none
   ```

2. **Add it to the manuscript.** Insert the chapter, exactly as it stands in
   the Doc, into `<Title>.md` in outline order (after chapter `n−1` and before
   `n+1`, if that exists), or replace the existing chapter if the author chose
   revision. Create the manuscript with `Title:` / `Author:` lines first if it
   doesn't exist. Strip anything the Doc carries that the manuscript format
   forbids (comments, notes, word counts). In a read-only claude.ai Project,
   write the full updated manuscript to outputs and say which Project file to
   replace.

Then ask with a survey: **Done / Revise (I'll say what) / Retune the voice
(run /rama:retune).** Revise as many rounds as the author wants. Make each
revision in the Chapter Doc and the manuscript together, so the two never
differ, and report only the changed passages in chat. Every revised passage
must pass the style guide.

## Step 8: Update the log and beats

1. **RAMA Log**:
   - Chapter Status → Draft `✓ <date>`, Words, Last check `<date>`, Doc link.
   - Continuity Ledger → every new concrete fact this chapter establishes,
     including canonical values settled during the check.
   - Open Threads → mark payoffs and add threads opened.
   - Decisions → any choice made in this skill that changes the book.
2. **Beats file**: if beats changed in drafting, update the chapter's beats to
   match what was written and mark the changes `(Changed in compose)`.

In a read-only claude.ai Project, write the full updated RAMA Log and Beats
file to outputs too, and say which Project files to replace.

Finish with:

> Chapter <n> checked and added to the manuscript ([W] words; book total [T] / [target]). Doc: <Title> - Chapter <n>.
> Next: `/rama:beats <n+1>`.
