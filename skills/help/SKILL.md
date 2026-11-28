---
name: help
description: Quick reference for every RAMA command, grouped by stage of the book, with a one-line description and usage for each. If a RAMA Log exists, marks where the book stands and the logical next command. Read-only. Usage /rama:help, or /rama:help compose for one command in detail.
---

# RAMA: Help

*Adapted from ghost-writer's `help` (MIT, Simone Di Roma).*

Shows what RAMA can do. Changes no files.

Read `references/project-files.md` first, only to find the RAMA Log.

## Arguments

- `/rama:help`: the full reference below.
- `/rama:help <command>` (e.g. `/rama:help check`): that command's usage,
  options, what it reads, what it writes, and what normally comes before and
  after it. Take this from the command's own skill if you can read it;
  otherwise from the table below.

## Before showing

Look for the RAMA Log. If it exists, read its Project and Chapter Status
sections only, and work out the next step with the same rules as
`/rama:resume`. If it doesn't exist, the next step is `/rama:brainstorm` (no
concept yet) or `/rama:config` (project files exist).

## The reference

Show this, with the usage forms exactly as written:

```
RAMA · COMMAND REFERENCE

START A BOOK
  /rama:brainstorm [seed]         From nothing or a seed to one story concept
  /rama:config                    Check the project files, fill gaps, write the RAMA Log
  /rama:character-interview Name  Deep profile for an important character (optional)

WRITE EACH CHAPTER
  /rama:beats 5                   Story beats for chapter 5, from the outline and what's written
  /rama:compose 5                 Draft chapter 5 into its own Claude Doc, run check on it,
                                  then add it to the manuscript
  /rama:freeflow 5                Stuck? Dump everything; RAMA turns it into beats or decisions
  /rama:retune 5                  "This isn't my voice": realign to a rough sample

CHECK AND REVISE
  /rama:check 5 · 5-7 · all       Style guide, beats, continuity, timeline, characters,
                                  accuracy, copy, repetition and rhythm, craft; fixes with your OK
  /rama:character-check 5 Name    One character's voice, behavior and knowledge in a chapter
  /rama:demolish 5                Hostile read for logic, motivation, stakes, POV cheats
  /rama:review 5 editor · all     Persona reads: editor, target reader, hostile reader,
                                  period expert, out-of-target, custom
  /rama:integrate 5               Turn demolish/review answers into approved text changes
  /rama:corrections [print]       Review PDF with paragraph IDs, then apply your annotations

FINISH
  /rama:compile [docx|epub|md]    Build the book: .md, .docx and .epub

ANY TIME
  /rama:resume                    Where the book stands and the one next step
  /rama:help [command]            This reference
```

Then, if a RAMA Log exists, one line on where the book stands and one on the
next command, e.g.:

```
The Shape of the Sea · 9 of 25 chapters drafted · last checked: 9
→ Next: /rama:beats 10
```

Places are cited as `ch.para` (`5.12` is chapter 5, paragraph 12) in every
report. Mention that once, at the end, only when the author asked for the full
reference.
