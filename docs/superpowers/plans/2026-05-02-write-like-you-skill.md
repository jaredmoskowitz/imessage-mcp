# write-like-you-skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Claude Code skill repo that mines iMessages and generates a personalized writing voice skill.

**Architecture:** Pure markdown repo — no code, no dependencies. A SKILL.md bootstrapping prompt drives the entire flow using iMessage MCP tools. Template files exist for human reference; the skill embeds its output structure inline.

**Tech Stack:** Claude Code skills (markdown), iMessage MCP (external dependency, not bundled)

---

## File Structure

```
write-like-you-skill/
├── README.md                          # Install guide, prerequisites, privacy, usage
├── SKILL.md                           # The bootstrapping skill (/build-my-voice)
├── templates/
│   ├── SKILL.md.template              # Human-readable reference for voice skill output
│   └── corpus.md.template             # Human-readable reference for corpus output
├── examples/
│   └── README.md                      # Annotated good/bad examples
└── .gitignore
```

---

### Task 1: Initialize the repo

**Files:**
- Create: `write-like-you-skill/.gitignore`

This task creates the repo in a new directory alongside the imessage-mcp project.

- [ ] **Step 1: Create the repo directory and subdirectories**

```bash
mkdir -p ~/workspace/write-like-you-skill/{templates,examples}
cd ~/workspace/write-like-you-skill
git init
```

- [ ] **Step 2: Create .gitignore**

Write to `~/workspace/write-like-you-skill/.gitignore`:

```
.DS_Store
*.swp
*~
```

- [ ] **Step 3: Initial commit**

```bash
cd ~/workspace/write-like-you-skill
git add .gitignore
git commit -m "chore: initialize write-like-you-skill repo"
```

---

### Task 2: Write the corpus template

**Files:**
- Create: `templates/corpus.md.template`

This is the human-readable reference showing what a completed corpus looks like. The bootstrapping skill generates this structure — this file is for people who want to understand or customize the output format.

- [ ] **Step 1: Write the corpus template**

Write to `~/workspace/write-like-you-skill/templates/corpus.md.template`:

```markdown
# Corpus — samples of [Name]'s writing

Real samples, grouped by surface. When drafting for [Name], find the nearest analog here and match its tempo, structure, and register before worrying about individual word choices. Each entry opens with a one-line note on what's distinctive about the sample.

Add new samples here as they come in. When a pattern repeats across three or more samples, promote it into `../SKILL.md` under "Phrases and patterns you actually use."

---

## iMessage / Texting

<!-- This section is populated automatically by /build-my-voice -->
<!-- Each sample should have: -->
<!-- ### Sample title -->
<!-- *Distinctive: one line on what's characteristic* -->
<!-- ``` -->
<!-- The verbatim message(s) -->
<!-- ``` -->
<!-- **Patterns to notice:** -->
<!-- - What should a writer imitate? -->

---

## Slack DMs

<!-- Not yet populated. To add samples: -->
<!-- 1. Copy a real DM exchange that shows your voice -->
<!-- 2. Add a "Distinctive:" note above it -->
<!-- 3. Add "Patterns to notice:" below it -->
<!-- 4. If a pattern appears 3+ times across samples, promote it to SKILL.md -->

---

## Slack public posts

<!-- Same format as above. -->

---

## Emails (short / transactional)

<!-- Same format as above. -->

---

## Emails (long-form / pitch)

<!-- Same format as above. -->

---

## LinkedIn posts

<!-- Same format as above. -->

---

## Technical docs

<!-- Same format as above. -->

---

## PR descriptions / commit messages

<!-- Same format as above. -->

---

## Cross-corpus observations

**Promoted patterns:**
<!-- Patterns confirmed across 3+ independent samples. These are reflected in SKILL.md. -->

**Patterns to watch:**
<!-- Patterns seen once or twice. Watch for more before promoting. -->

---

## How to add to this corpus

When you have a new writing sample:

1. Figure out the surface (DM? Tech doc? Pitch email?).
2. Paste the verbatim sample under the matching heading.
3. Write a one-line "Distinctive:" note above the sample naming what's characteristic about it.
4. Add a "Patterns to notice:" section under the sample — what should a writer imitate?
5. If the sample introduces a new pattern not yet reflected in SKILL.md, flag it in "Cross-corpus observations → Patterns to watch." Once the pattern appears in ~3 independent samples, promote it.
6. If the sample contradicts existing guidance, update SKILL.md — don't just stack rules on top.

Keep the corpus organized by surface, not by date. The goal is fast retrieval when matching voice to context.
```

- [ ] **Step 2: Commit**

```bash
cd ~/workspace/write-like-you-skill
git add templates/corpus.md.template
git commit -m "feat: add corpus template with surface headings and instructions"
```

---

### Task 3: Write the voice skill template

**Files:**
- Create: `templates/SKILL.md.template`

The human-readable reference for what a completed voice skill looks like. Shows the full section structure with comments explaining each section's purpose.

- [ ] **Step 1: Write the voice skill template**

Write to `~/workspace/write-like-you-skill/templates/SKILL.md.template`:

```markdown
---
name: [name]-voice
description: Write in [Name]'s voice across any surface — texts, Slack, emails, docs, PRs.
---

# [Name]'s Voice

This skill captures how [Name] writes across different contexts so Claude can draft under their name. Voice is not a single setting — it shifts with audience, stakes, and surface. This skill codifies those shifts.

## How to use this skill

1. **Identify the surface first.** Before writing a word, determine which context you're in: text message, Slack DM, Slack public post, email, LinkedIn, tech doc, PR description. Each has different rules. The wrong register is worse than the wrong word.
2. **Pull the cross-context invariants** — those hold everywhere.
3. **Layer on the context-specific rules** from the matching subsection.
4. **Before shipping, run the "Before sending" checklist.**
5. **When in doubt, read the corpus.** `references/corpus.md` has real samples — matching tone to a similar piece is better than reasoning from rules.

## Cross-context invariants (true everywhere)

<!-- These are the 5-8 rules that hold regardless of surface. -->
<!-- Derived from patterns that appear across ALL your writing, not just one context. -->
<!-- Examples of what might go here: -->
<!-- - How you open messages (point-first vs. preamble) -->
<!-- - How you express opinions (hedged vs. direct) -->
<!-- - How you handle uncertainty (admit vs. avoid) -->
<!-- - Fragment vs. full-sentence threshold -->
<!-- - Humor style -->

## Context-specific voice

### Text messages (iMessage)

<!-- Populated by /build-my-voice. Rules specific to how you text: -->
<!-- - Acknowledgment style (fragments, specific word choices) -->
<!-- - Enthusiasm markers (extended vowels? emoji? caps?) -->
<!-- - Multi-message burst patterns -->
<!-- - When full sentences appear vs. fragments -->
<!-- - Self-correction style -->
<!-- - Story-sharing framing -->

### Slack DMs

<!-- Not yet populated. Add samples to corpus.md, identify patterns, write rules here. -->

### Slack public posts

<!-- Not yet populated. -->

### Short emails

<!-- Not yet populated. -->

### Long-form / pitch emails

<!-- Not yet populated. -->

### LinkedIn posts

<!-- Not yet populated. -->

### Technical docs

<!-- Not yet populated. -->

### PR descriptions / commit messages

<!-- Not yet populated. -->

## Phrases and patterns you actually use

<!-- Organized by function. Real phrases pulled from your writing. -->
<!-- Example categories: -->

<!-- **Acknowledgments:** -->
<!-- - "Bet", "Sounds good", etc. -->

<!-- **Enthusiasm:** -->
<!-- - "Hell yeah", extended vowels, etc. -->

<!-- **Staking a position:** -->
<!-- - "I think...", "I strongly believe...", etc. -->

<!-- **Admitting limits:** -->
<!-- - "Not sure", "I could be wrong", etc. -->

<!-- **Closings:** -->
<!-- - Sign-off patterns by surface -->

## Phrases and patterns to avoid

These are anti-patterns regardless of context:

- "I hope this message finds you well."
- "Just wanted to reach out to..."
- "Per my last message..."
- "Circling back..."
- "Leverage" as a verb (unless literal).
- "Synergy," "stakeholders," "value-add," "low-hanging fruit."
- Apology pile-ups ("so sorry to bother you," "apologies for the delay").
- Overly hedged claims ("it might perhaps be worth considering whether we could possibly...").
- Starting with weather, wishing, or vibes.

<!-- Add any personal anti-patterns the user identifies during setup. -->

## Before sending (checklist)

1. Does the first sentence state the point? If not, rewrite.
2. Is the register right for the surface? (A DM shouldn't read like a memo. A pitch email shouldn't read like a text.)
3. Have I hedged where I should stake a position?
4. Have I stated opinions without backing them up?
5. Is there filler? Kill it unless it earns its keep.
6. Does anything sound like it was written by a committee?
7. Is there a clear close? A next step, an ask, or a deliberate open end.
8. Does it sound like [Name] — or like "a generally competent writer"? If the latter, go back to the corpus.

## Corpus and updating this skill

The real examples live in `references/corpus.md`. When the voice judgment is close, read the nearest analog sample before writing. Matching a pattern beats following a rule.

**To update this skill as more writing comes in:**

1. Add new sample(s) to `references/corpus.md` under the correct context heading.
2. If the new sample contradicts or extends guidance here, update the relevant section — don't just stack rules.
3. When a pattern has appeared in three or more independent samples, promote it to "Phrases and patterns you actually use."
4. Periodically do a consolidation pass: prune rules that aren't earning their spot.
5. Keep this file under ~500 lines. Push longer analysis into `references/`.
```

- [ ] **Step 2: Commit**

```bash
cd ~/workspace/write-like-you-skill
git add templates/SKILL.md.template
git commit -m "feat: add voice skill template with section structure and guidance"
```

---

### Task 4: Write the examples README

**Files:**
- Create: `examples/README.md`

Annotated examples showing what good voice skill output looks like vs. common mistakes. Uses fictional examples — not real voice data.

- [ ] **Step 1: Write the examples README**

Write to `~/workspace/write-like-you-skill/examples/README.md`:

```markdown
# Examples — What Good Output Looks Like

This directory shows annotated examples of what `/build-my-voice` should produce. These use fictional patterns — not real voice data.

## Good cross-context invariant vs. bad

**Good — specific and actionable:**
> "Lead with the point, not with preamble. The first sentence says what the message is about. If you find yourself writing 'I wanted to reach out about...' — delete it. Start with the thing."

This works because it names the pattern, gives a concrete anti-example, and tells you what to do instead.

**Bad — too vague:**
> "Be direct and concise."

This doesn't help. Every writing guide says this. It doesn't capture anything unique about *your* voice.

**Bad — too specific to one surface:**
> "Always use extended vowels for enthusiasm."

This is an iMessage convention, not a universal rule. It belongs in the "Text messages" section, not in cross-context invariants.

---

## Good corpus sample vs. bad

**Good — real sample with analysis:**

> ### Reacting to good news
>
> *Distinctive: extended vowels, single-line burst, no context needed.*
>
> ```
> Yooooo that's incredible
> ```
>
> **Patterns to notice:**
> - "Yooooo" not "Yo" — letter extension is the emphasis move, not caps or emoji.
> - Single line. The excitement is the whole message.
> - No follow-up explanation. The reaction stands alone.

This works because the sample is verbatim, the "Distinctive" note is one specific observation, and "Patterns to notice" tells a writer what to imitate.

**Bad — too short to learn from:**

> ### Quick response
>
> *Distinctive: short.*
>
> ```
> ok
> ```
>
> **Patterns to notice:**
> - It's short.

"ok" by itself doesn't teach anything. The corpus should capture messages that reveal *how you're different from a generic writer* — not messages anyone would send.

---

## Good "phrases you actually use" entry vs. bad

**Good — phrase with context:**

> **Enthusiasm:**
> - "I'm down" — the universal yes for plans, invitations, proposals. Sometimes bare, sometimes with context ("I'm down to check it out if you want company").
> - "Yooooo" / "Daaaaamn" — extended vowels as the primary excitement marker, not emoji.

Each entry names the phrase AND when/how it's used. A writer can pattern-match from this.

**Bad — list without context:**

> **Enthusiasm:**
> - "Cool"
> - "Nice"
> - "Awesome"

These are generic. Everyone says these. If the user actually says "cool" as their default acknowledgment, the entry should note that: "cool — the default acknowledgment, lowercase, no punctuation. Not 'Cool!' or 'That's cool' — just 'cool'."

---

## Common mistakes

1. **Rules that are too vague to act on.** "Be authentic" is not a rule. "Use 'I think' when staking a position, not 'it seems like'" is a rule.

2. **Samples that are too short.** A single "ok" or "yes" doesn't reveal voice. Include messages where the person is actually *writing* — explaining something, reacting with personality, telling a story.

3. **Confusing surface-specific patterns with universal ones.** Extended vowels in texts ≠ extended vowels in emails. Check whether a pattern holds across surfaces before putting it in cross-context invariants.

4. **Not enough contrast.** The skill should capture what makes this person's writing *different* from a generic competent writer. If a rule applies to anyone ("use correct grammar"), it doesn't belong.

5. **Privacy leaks.** Strip phone numbers, reduce contact names, exclude private content. The corpus should demonstrate voice mechanics, not expose personal life details.
```

- [ ] **Step 2: Commit**

```bash
cd ~/workspace/write-like-you-skill
git add examples/README.md
git commit -m "feat: add annotated examples of good vs. bad voice skill output"
```

---

### Task 5: Write the bootstrapping skill (SKILL.md)

**Files:**
- Create: `SKILL.md`

This is the core of the repo — the prompt that drives `/build-my-voice`. It contains the full 5-stage flow: permissions check, mining, analysis, generation, and output. The template structures are embedded inline as instructions for what to generate.

- [ ] **Step 1: Write the bootstrapping skill**

Write to `~/workspace/write-like-you-skill/SKILL.md`:

````markdown
---
name: build-my-voice
description: Mine your iMessages and build a personalized writing voice skill. Run this once — it creates a skill that writes in your voice.
---

# Build My Voice

This skill mines your iMessage history, analyzes how you write, and generates a Claude Code voice skill that captures your writing patterns across different surfaces.

**What you get:** A ready-to-use skill at `~/.claude/skills/<name>-voice/` with a populated SKILL.md and corpus of real writing samples.

**What you need:** macOS, an iMessage MCP server, and Full Disk Access for your terminal.

## Stage 1: Permissions & Prerequisites

Before doing anything else, verify that the iMessage MCP is working.

**Step 1:** Try calling `list_chats` with a limit of 5.

**If it works** (returns a list of chats): Tell the user "iMessage access is working" and skip to Stage 2.

**If it fails or the tool doesn't exist:**

Tell the user they need an iMessage MCP server. Say:

"To mine your messages, I need an iMessage MCP server. Here's how to set one up:

1. Install an iMessage MCP server. One option: https://github.com/jaredmoskowitz/imessage-mcp

   ```
   git clone https://github.com/jaredmoskowitz/imessage-mcp.git ~/workspace/imessage-mcp
   cd ~/workspace/imessage-mcp
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

2. Add it to your Claude Code settings. Add this to `~/.claude/settings.json` under `mcpServers`:

   ```json
   \"imessage\": {
     \"command\": \"$HOME/workspace/imessage-mcp/.venv/bin/python\",
     \"args\": [\"-m\", \"imessage_mcp\"]
   }
   ```

3. Grant Full Disk Access to your terminal app:
   - Open **System Settings**
   - Go to **Privacy & Security → Full Disk Access**
   - Click the **+** button
   - Add your terminal app (Terminal, iTerm2, Ghostty, Warp — whichever you use for Claude Code)

4. Restart Claude Code after granting access.

Once that's done, come back and run `/build-my-voice` again."

**Stop here.** Do not proceed to Stage 2 until the prerequisites are met. The user needs to restart Claude Code after configuring the MCP.

## Stage 2: Mining

Now mine the user's iMessage history. Be methodical — the quality of the voice skill depends on the quality of the samples.

**Step 1: Get active chats.**
Call `list_chats` with a limit of 25. Note which are 1:1 chats vs. group chats (group chats have multiple participants).

**Step 2: Pull recent messages from the top 10-15 most active chats.**
For each chat, call `get_messages` with a limit of 100 and `since` set to 3 months ago (calculate the ISO date). Collect ONLY messages where `sender` is `"Me"`.

**Step 3: Search for signal-rich messages.**
Run `search_messages` for each of these phrases (limit 30 each):
- "I think"
- "I believe"
- "honestly"
- "I'm down"
- "not gonna lie"

Filter results to only messages where `sender` is `"Me"`.

**Step 4: Bucket the collected messages.**
Organize into three groups:
- **Ultra-short** (1-5 words): acknowledgments, reactions, one-word responses
- **Medium** (1-2 sentences): coordination, quick opinions, brief reactions with context
- **Long** (3+ sentences): stories, explanations, substantive thoughts, multi-message narratives

Keep track of which messages came from 1:1 chats vs. group chats.

**Do not show all messages to the user.** This is background work. Proceed directly to analysis.

## Stage 3: Analysis

Analyze the collected messages across these dimensions. For each, identify the specific pattern with real examples from the mined messages.

1. **Default acknowledgment style.** Look at the ultra-short messages. What words does this person use for "yes", "ok", "sounds good"? Are they playful or standard? List the top 5-8 most common acknowledgments with frequency.

2. **Enthusiasm markers.** How do they express excitement? Look for: extended vowels/letters ("sickkkk"), emoji usage, caps, specific phrases ("hell yeah"), exclamation patterns. Quote real examples.

3. **Signal-carrying register.** In the medium and long messages, how do they structure real thoughts? Do they lead with the point? Use "I think" framing? Build arguments? Look at sentence structure and opening patterns.

4. **Self-assessment style.** Search for messages where they talk about their own work, performance, or decisions. Are they hedged ("I think I did ok?"), direct ("nailed it"), or self-deprecating ("probably messed that up")?

5. **Humor patterns.** Look for jokes, dry observations, playful register shifts, absurdist comments. Note whether humor is frequent or rare.

6. **Punctuation and formatting habits.** Do they drop periods? Use trailing ellipses? Send rapid-fire multi-message bursts or composed paragraphs? Lowercase everything or capitalize normally?

7. **Group chat vs. 1:1 behavior.** Compare their messages in group chats vs. 1:1. Are they quieter in groups? Different register?

**Present findings to the user.** Format as a summary:

"Here's what I found in your messages. Let me know if this sounds right or if I'm off on anything:

**Your acknowledgment style:** [summary with examples]
**How you show enthusiasm:** [summary with examples]
**When you write full sentences:** [summary with examples]
**How you talk about yourself/your work:** [summary with examples]
**Your humor:** [summary with examples]
**Formatting habits:** [summary with examples]
**Group vs. 1:1:** [summary with examples]

Does this sound like you? Anything I'm getting wrong?"

**Wait for user feedback.** Adjust the analysis based on their corrections before proceeding.

## Stage 4: Generation

Generate two files: the voice skill SKILL.md and the corpus.

### Generate the voice skill SKILL.md

Write a complete SKILL.md with these sections, filled in from the analysis:

**Frontmatter:**
```yaml
---
name: <name>-voice
description: Write in <Name>'s voice across any surface — texts, Slack, emails, docs, PRs.
---
```

**Section: "How to use this skill"**
Include the 5-step process:
1. Identify the surface
2. Pull cross-context invariants
3. Layer context-specific rules
4. Run the before-sending checklist
5. Consult the corpus when the judgment is close

**Section: "Cross-context invariants"**
Write 5-8 rules that hold across ALL surfaces, derived from the analysis. Each rule should be:
- Specific enough to act on (not "be direct")
- Backed by a real example from their messages
- Something that distinguishes THIS person from a generic writer

**Section: "Context-specific voice → Text messages (iMessage)"**
Write 8-12 detailed rules covering:
- Acknowledgment words and style
- Enthusiasm markers (with examples)
- Multi-message burst patterns
- When fragments vs. full sentences appear
- Self-correction patterns (if any)
- Story-sharing framing (if any)
- No greetings / no sign-offs
- Group chat behavior differences (if any)

**Section: "Context-specific voice" for other surfaces**
For each of these surfaces, write a stub:
- Slack DMs
- Slack public posts
- Short emails
- Long-form / pitch emails
- LinkedIn posts
- Technical docs
- PR descriptions / commit messages

Each stub should say: "Not yet populated. Add samples to `references/corpus.md` under the [Surface] heading, identify patterns, then fill in rules here."

**Section: "Phrases and patterns you actually use"**
Organize by function with real phrases from the analysis:
- Acknowledgments
- Enthusiasm
- Staking a position
- Admitting limits
- Any other functional categories that emerged

Each entry should include the phrase AND when/how it's used.

**Section: "Phrases and patterns to avoid"**
Include the standard anti-patterns:
- Corporate filler ("synergy", "stakeholders", "leverage" as verb)
- Preamble padding ("I hope this finds you well", "Just wanted to reach out")
- Apology pile-ups
- Overly hedged claims

Plus any personal anti-patterns the user flagged during the review.

**Section: "Before sending checklist"**
8 items checking: point-first, right register, position-staking, opinions backed up, filler killed, committee-voice eliminated, clear close, sounds like the person.

**Section: "Corpus and updating"**
Pointer to `references/corpus.md` with instructions for adding samples and promoting patterns.

### Generate the corpus

Write a complete `references/corpus.md` with:

**iMessage / Texting section:** 8-12 curated samples from the mined messages. For each sample:
- A descriptive title
- A one-line "Distinctive:" note
- The verbatim message(s)
- A "Patterns to notice:" section with 2-4 bullet points

Choose samples that cover different aspects of their voice: acknowledgments, enthusiasm, substantive thoughts, humor, self-assessment, coordination, storytelling. Prioritize samples that show what makes this person distinctive.

**Privacy pass before writing samples:**
- Strip all phone numbers
- Replace contact names with first names only or generic labels
- Exclude messages with clearly private content (medical, financial, intimate, others' personal information)
- When in doubt, leave it out

**Other surface sections:** Empty with instructions (same as the template).

**Cross-corpus observations:** Seed "Promoted patterns" with the patterns confirmed across 3+ samples during analysis. Seed "Patterns to watch" with patterns seen only once or twice.

**How to add to this corpus:** The standard 6-step process.

## Stage 5: Output

**Step 1: Ask for the skill name.**
"What do you want your voice skill to be called? This determines the slash command. Default: `<firstname>-voice` (invoked as `/<firstname>-voice`)."

**Step 2: Create the directory and write the files.**
Create `~/.claude/skills/<name>-voice/` and `~/.claude/skills/<name>-voice/references/`.
Write the generated SKILL.md and corpus.md to these paths.

**Step 3: Confirm and instruct.**
Tell the user:

"Your voice skill is ready at `~/.claude/skills/<name>-voice/`.

**To use it:** Next time you need to write something — a text, a Slack post, a LinkedIn post, a README — invoke `/<name>-voice` and tell Claude what you're writing and who it's for.

**Try it now:** Ask me to draft a text to a friend about weekend plans using `/<name>-voice`.

**To expand it:** Right now your skill only covers iMessage. To add more surfaces:
1. Paste real writing samples (Slack posts, emails, LinkedIn posts, etc.) into `references/corpus.md` under the matching heading
2. Once you have 3+ samples for a surface, fill in the rules in SKILL.md under that surface's section

Your voice skill gets sharper over time as you add more samples. The rules follow the corpus — not the other way around."
````

- [ ] **Step 2: Commit**

```bash
cd ~/workspace/write-like-you-skill
git add SKILL.md
git commit -m "feat: add bootstrapping skill with 5-stage voice mining flow"
```

---

### Task 6: Write the README

**Files:**
- Create: `README.md`

The repo README — what someone sees first on GitHub.

- [ ] **Step 1: Write the README**

Write to `~/workspace/write-like-you-skill/README.md`:

```markdown
# write-like-you-skill

A Claude Code skill that mines your iMessages and builds a personalized writing voice skill.

Great for when you're kinda faking it anyways — LinkedIn posts, HackerNews comments, and GitHub READMEs.

## What you get

Run `/build-my-voice` once. It reads your iMessage history, figures out how you write, and generates a Claude Code skill that captures your voice. After that, any time you need to draft something — a text, a LinkedIn post, a Slack message, a README — invoke your voice skill and Claude writes like you, not like Claude.

The iMessage surface is populated automatically. Other surfaces (Slack, email, LinkedIn, tech docs) start as stubs — you add samples over time, and the skill gets sharper.

## How it works

1. **Permissions check** — verifies iMessage MCP access and Full Disk Access
2. **Mining** — pulls your messages from your most active chats over the last 3 months
3. **Analysis** — identifies your acknowledgment style, enthusiasm markers, humor, punctuation habits, sentence structure, and how your register shifts between casual and substantive
4. **Review** — presents findings and asks "does this sound like you?" before generating
5. **Output** — writes a complete voice skill to `~/.claude/skills/` ready to use

## Prerequisites

- **macOS** — iMessage data is local to your Mac
- **Claude Code** — the skill runs inside Claude Code
- **An iMessage MCP server** — reads your local iMessage database. [imessage-mcp](https://github.com/jaredmoskowitz/imessage-mcp) works, or use any compatible iMessage MCP.
- **Full Disk Access** for your terminal app — the MCP needs to read `~/Library/Messages/chat.db`

## Install

```bash
git clone https://github.com/jaredmoskowitz/write-like-you-skill.git ~/.claude/skills/write-like-you-skill
```

Then in Claude Code:

```
/build-my-voice
```

The skill walks you through everything — iMessage MCP setup, Full Disk Access, mining, and generation.

## After setup

Your voice skill lives at `~/.claude/skills/<your-name>-voice/`. Use it by invoking `/<your-name>-voice` whenever you want Claude to write in your voice.

### Expanding to other surfaces

The generated skill starts with iMessage data only. To add more surfaces:

1. Paste real writing samples (Slack posts, emails, LinkedIn posts, docs) into `references/corpus.md` under the matching heading
2. Add a "Distinctive:" note and "Patterns to notice:" section for each sample
3. Once you have 3+ samples for a surface, fill in the rules in SKILL.md for that surface
4. When a pattern shows up across 3+ samples, promote it to "Phrases and patterns you actually use"

## Privacy

- Your messages **never leave your machine**. The MCP reads your local iMessage database directly.
- The generated skill files are stored locally in `~/.claude/skills/`.
- Phone numbers are stripped and contact names are reduced automatically during generation.
- Private content (medical, financial, intimate) is excluded from corpus samples.

## Credits

Built by [Jared Moskowitz](https://github.com/jaredmoskowitz). Inspired by building a voice skill the hard way and realizing everyone's iMessages are sitting right there.
```

- [ ] **Step 2: Commit**

```bash
cd ~/workspace/write-like-you-skill
git add README.md
git commit -m "docs: add README with install guide, usage, and privacy info"
```

---

### Task 7: Final review

- [ ] **Step 1: Verify all files exist**

```bash
cd ~/workspace/write-like-you-skill
find . -not -path './.git/*' -type f | sort
```

Expected output:
```
./.gitignore
./README.md
./SKILL.md
./examples/README.md
./templates/SKILL.md.template
./templates/corpus.md.template
```

- [ ] **Step 2: Read through each file for consistency**

Verify:
- SKILL.md references the correct output paths (`~/.claude/skills/<name>-voice/`)
- SKILL.md references the iMessage MCP repo URL consistently
- Templates match the structure described in SKILL.md Stage 4
- README install path matches how skills are loaded
- examples/README.md doesn't reference any real person's data
- No placeholder text (TBD, TODO, etc.) in any file

- [ ] **Step 3: Verify git log is clean**

```bash
cd ~/workspace/write-like-you-skill
git log --oneline
```

Expected: 6 commits, one per task.
