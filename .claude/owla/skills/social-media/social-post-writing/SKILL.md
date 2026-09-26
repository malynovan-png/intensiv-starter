---
name: social-post-writing
description: "Use when drafting short social posts. Keep voice natural."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: social-media
    tags: [writing, social, telegram, posts, tone, style, editing]
---

# Social post writing

Use this skill when the user wants a short post for Telegram, Instagram, X, or similar social channels.

## Core goal
Write copy that feels natural, readable aloud, and suited to the channel. Preserve the user's voice instead of flattening it into generic promo text.

## Default workflow
1. Identify the platform and purpose.
2. Match the user's language mix and tone.
3. Keep the post short unless the user asks for a longer version.
4. Prefer one clear idea per paragraph.
5. End with a concise, memorable closing line when the post is meant to feel personal.
6. Show the polished text directly unless the user asks for variants.

## Canonical style memory
When the user says they like a version, says "remember this", or gives a rewritten post they prefer, treat that rewrite as the active style target for future drafts.

For warm Telegram posts in mixed Russian-English, default to this structure:
- greeting or hook
- short emotional setup
- one concrete scene/detail paragraph
- a separate sensory or mood line
- a warm closing wish
- a punchy sign-off

When the user asks for a back-to-school or event announcement post, preserve her preferred formatting details exactly when they are requested:
- use an ALL CAPS hook if it fits the draft
- end with autumn emojis when the topic is seasonal
- use hyphen-minus instead of long dashes when the user asks for that formatting
- omit closing clarification sentences when the user wants copy-ready text only
- keep mixed Russian-English phrasing natural, not forced
- for event posts, offer a full version and a shorter version when the user wants both
- for important topics, the full version may be 4 paragraphs; otherwise keep it tighter
- lightly mix in English words and an American-girl vibe when the user asks for that style, but do not overdo it

When the user gives a final approved version, treat that exact formatting as the active target for similar future posts.

Preserve the user's chosen rhythm when it is explicit: short paragraphs, light code-switching, vivid class-room / life details, and a final line that lands with energy rather than polish.

When the user asks for a content plan, social post, or caption about her work/life, bias the framing toward *her* as the main character: specific lived-in details, first-person angle, and real routines over generic audience-facing language.

If the user says a post should be "more about me", make that the organizing principle for the draft, not just a tone tweak.

## Preferred structure for warm Telegram posts
See `references/telegram-post-style.md` for the preferred mixed-language structure and an approved example.

Use this pattern when it fits:
- short greeting or hook
- brief emotional setup
- one concrete scene or detail paragraph
- a separate sensory or mood line
- a warm closing wish
- a punchy sign-off

## Writing rules
- Mirror the user's language if they mix Russian and English.
- Keep the tone warm, playful, and direct.
- Preserve real details the user provides, including numbers, names, and punctuation style when it matters.
- Avoid over-explaining the rewrite process.
- Avoid turning a post into a polished press release.
- Avoid adding extra sections unless the user asks for options.
- Prefer line breaks over long blocks when the rhythm matters.
- If the user explicitly says a newer rewrite is the preferred style, treat it as the current target and follow it closely.

## Common pitfalls
- Making the post too generic or too polished.
- Replacing the user's informal voice with neutral corporate language.
- Removing the mixed-language feel when the user clearly wants it.
- Expanding a short post into a long essay.
- Over-formatting with labels, bullets, or meta commentary when the user asked for ready-to-post text.

## Output
Return the ready-to-post text first. If helpful, offer one or two alternative tones after the main version.
