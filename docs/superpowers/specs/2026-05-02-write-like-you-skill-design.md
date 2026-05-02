# write-like-you-skill — Design Spec

A Claude Code skill that mines your iMessages and builds a personalized writing voice skill. Great for when you're kinda faking it anyways — LinkedIn posts, HackerNews comments, and GitHub READMEs.

**Audience:** Claude Code power users who know what skills are.
**Platform:** macOS only (iMessage database is local to Mac).
**Output:** A ready-to-use Claude Code voice skill installed at `~/.claude/skills/<name>-voice/`.

---

## Repo Structure

```
write-like-you-skill/
├── README.md
├── SKILL.md                           # The bootstrapping skill (/build-my-voice)
├── templates/
│   ├── SKILL.md.template              # Empty voice skill skeleton
│   └── corpus.md.template             # Empty corpus skeleton with surface headings
└── examples/
    └── README.md                      # Annotated excerpts of what good output looks like
```

No Python, no dependencies. The entire repo is a Claude Code skill + markdown templates.

---

## Installation

Clone the repo, symlink or copy into `~/.claude/skills/`. Run `/build-my-voice`.

---

## Skill Flow: `/build-my-voice`

Five sequential stages. The skill walks the user through each.

### Stage 1: Permissions & Prerequisites

1. Try to call `list_chats` via the iMessage MCP.
2. If it works → skip to Stage 2.
3. If MCP not configured:
   - Explain they need an iMessage MCP server. Link to recommended options.
   - Show the exact JSON block to add to `~/.claude/settings.json`:
     ```json
     {
       "mcpServers": {
         "imessage": {
           "command": "<path-to-python>",
           "args": ["-m", "imessage_mcp"]
         }
       }
     }
     ```
   - Tell them to install the MCP server (pip install or clone + install).
4. If MCP configured but access denied:
   - Walk through **System Settings → Privacy & Security → Full Disk Access**.
   - Identify their terminal app (Terminal, iTerm2, Ghostty, Warp, etc.) and tell them to add it.
   - Tell them to restart Claude Code after granting access.
5. Verify by calling `list_chats` again. If it returns results → proceed.

### Stage 2: Mining

1. Pull the user's 15-20 most active chats via `list_chats`.
2. For each chat, pull recent messages (last ~3 months) via `get_messages`, using the `since` parameter.
3. Filter to only messages where `sender` is `"Me"`.
4. Run targeted `search_messages` calls for signal-rich phrases:
   - "I think", "I believe", "honestly", "I'm down", "not gonna lie"
   - These are starting points — the skill should also identify user-specific markers during analysis.
5. Bucket the user's messages by length:
   - **Ultra-short** (1-5 words) — acknowledgments, reactions
   - **Medium** (1-2 sentences) — coordination, quick thoughts
   - **Long** (3+ sentences) — stories, assessments, substantive messages
6. Identify most active 1:1 chats vs. group chats (the user may behave differently in each).

### Stage 3: Analysis

Across all collected messages, identify:

- **Default acknowledgment style** — What words do they use for "yes", "ok", "sounds good"? Are they playful ("Bet", "Rad") or standard ("Sounds good", "Got it")?
- **Enthusiasm markers** — Extended vowels ("sickkkk")? Emoji? Caps? Specific phrases ("Hell yeah")?
- **Signal-carrying register** — When they write full sentences, what's the structure? Do they lead with the point? Use "I think" framing?
- **Self-assessment style** — How do they talk about their own work? Hedged? Direct? Self-deprecating?
- **Humor patterns** — Dry? Playful? Absurdist? Rare?
- **Punctuation habits** — Trailing ellipses? Dropped periods? Exclamation points? Question marks mid-thought?
- **Multi-message vs. single-block** — Rapid-fire bursts or composed paragraphs?
- **Group chat vs. 1:1 behavior** — Quieter in groups? Same register everywhere?

**User review checkpoint:** Present a summary of findings and ask: "Does this sound like you? Anything I'm getting wrong?" Adjust based on feedback before generating.

### Stage 4: Generation

1. Read `templates/SKILL.md.template` and `templates/corpus.md.template` from the repo.
2. Fill in the SKILL.md template:
   - **Cross-context invariants** — 5-8 rules derived from analysis (e.g., "Lead with the point", "Fragments for acknowledgments, full sentences for signal").
   - **Context-specific voice: Text messages (iMessage)** — Detailed rules from the mining.
   - **Context-specific voice: [Other surfaces]** — Leave as stubs with instructions.
   - **Phrases and patterns you actually use** — Organized by function (acknowledgments, enthusiasm, staking positions, admitting limits, closings).
   - **Phrases and patterns to avoid** — Generic anti-patterns plus any the user flags.
   - **Before sending checklist** — 6-8 items.
3. Fill in the corpus.md:
   - **iMessage / Texting section** — 8-12 real curated samples, each with "Distinctive:" note and "Patterns to notice:" analysis.
   - **Other surface sections** — Empty with instructions.
   - **Cross-corpus observations** — Seeded with promoted patterns from iMessage analysis and patterns to watch.
4. **Privacy pass:** Strip all phone numbers, replace contact names with generic labels or first names only, remove any message content that's clearly private (medical, financial, intimate). When in doubt, leave it out.

### Stage 5: Output

1. Ask the user what they want their skill name and slash command to be (default: `<firstname>-voice`).
2. Write the completed files to `~/.claude/skills/<name>-voice/SKILL.md` and `~/.claude/skills/<name>-voice/references/corpus.md`.
3. Tell the user how to invoke it.
4. Suggest a test: "Try asking Claude to draft a text to a friend about weekend plans using `/your-voice`."
5. Mention that the skill only covers iMessage for now — they can add Slack, email, LinkedIn, etc. by pasting samples into the corpus under the right heading and updating the SKILL.md rules.

---

## Templates

### `templates/SKILL.md.template`

Sections (all empty, with structural comments explaining what goes in each):

1. **Header** — Skill name, description
2. **How to use this skill** — 5-step process: identify surface → pull invariants → layer context rules → before-sending checklist → consult corpus
3. **Cross-context invariants** — `<!-- 5-8 rules that hold everywhere -->`
4. **Context-specific voice: Text messages (iMessage)** — `<!-- Populated by /build-my-voice -->`
5. **Context-specific voice: Slack DMs** — `<!-- Add samples to corpus, then fill this in -->`
6. **Context-specific voice: Slack public posts** — stub
7. **Context-specific voice: Short emails** — stub
8. **Context-specific voice: Long-form emails** — stub
9. **Context-specific voice: LinkedIn posts** — stub
10. **Context-specific voice: Technical docs** — stub
11. **Context-specific voice: PR descriptions** — stub
12. **Phrases and patterns you actually use** — organized by function
13. **Phrases and patterns to avoid** — anti-patterns
14. **Before sending checklist** — 6-8 items
15. **Corpus and updating** — pointer to corpus.md, instructions

### `templates/corpus.md.template`

Sections (all empty except iMessage which gets populated):

1. **Header** — What this file is, how to use it
2. **iMessage / Texting** — `<!-- Populated by /build-my-voice -->`
3. **Slack DMs** — empty with "Add samples here" instructions
4. **Slack public posts** — empty
5. **Emails (short)** — empty
6. **Emails (long-form / pitch)** — empty
7. **LinkedIn posts** — empty
8. **Technical docs** — empty
9. **PR descriptions** — empty
10. **Cross-corpus observations** — "Promoted patterns" and "Patterns to watch", seeded from iMessage analysis
11. **How to add to this corpus** — 6-step process for adding new samples

---

## `examples/README.md`

Not a full example skill (that would be someone's real voice data). Annotated excerpts showing:

- What a good cross-context invariant looks like vs. a bad one (too vague, too specific)
- What a good corpus sample looks like (with Distinctive + Patterns to notice)
- What a good "phrases you actually use" entry looks like
- Common mistakes: rules that don't earn their spot, samples that are too short to learn from, confusing surface-specific conventions with universal ones

---

## README.md

Sections:

1. **One-line description** — "A Claude Code skill that mines your iMessages and builds a personalized writing voice skill."
2. **The hook** — "Great for when you're kinda faking it anyways — LinkedIn posts, HackerNews comments, and GitHub READMEs."
3. **What you get** — After running `/build-my-voice`, you have a skill that writes in your voice. iMessage populated automatically, other surfaces you add over time.
3. **How it works** — Brief stage overview (permissions → mining → analysis → generation → output).
4. **Prerequisites** — macOS, Claude Code, an iMessage MCP server, Full Disk Access for terminal.
5. **Install** — Clone, symlink into `~/.claude/skills/`, run `/build-my-voice`.
6. **After setup** — How to use the voice skill, how to add surfaces, how the corpus grows.
7. **Privacy** — Messages never leave your machine. MCP reads local database. Skill files stored locally. Phone numbers and contact names stripped automatically.
8. **Expanding your skill** — Adding Slack, email, LinkedIn, etc.
9. **Credits**

---

## Key Design Decisions

- **iMessage-only automation.** Other surfaces are manual. This keeps the skill focused and avoids needing MCP servers for Slack, email, etc.
- **User review checkpoint in Stage 3.** The analysis summary must be confirmed before generation. Voice is personal — the user should validate the patterns before they become rules.
- **Privacy by default.** Phone numbers stripped, contact names reduced, private content excluded. The corpus should demonstrate voice mechanics, not expose personal life.
- **Templates are embedded in the skill, not read at runtime.** The SKILL.md bootstrapping prompt contains the template structures inline (as instructions for what to generate), rather than reading separate template files at runtime. This avoids path-resolution issues — the skill doesn't need to know where the repo is installed. The `templates/` directory in the repo exists as human-readable reference for what the output looks like, not as runtime dependencies.
- **Stub sections for unpopulated surfaces.** Rather than generating rules for surfaces we have no data on, we leave them as clear "add your own" stubs. Wrong rules are worse than no rules.
