---
name: social-media-content-writing
description: "Use when writing social posts for the user."
version: 1.0.0
author: Hermes + Natalie
license: MIT
metadata:
  hermes:
    tags: [social-media, telegram, instagram, writing, content, rubrics]
    related_skills: []
---

# Social Media Content Writing

Use this skill when the user asks for a Telegram post, Instagram caption, rubric-based educational content, or a post in their established channel voice.

## When to Use

- The user asks to write a Telegram post.
- The user asks to write an Instagram caption.
- The user says `напиши тг пост на тему ...`.
- The user provides a theme and expects the assistant to choose a rubric.
- The user wants help shaping recurring content for their channel.

## What this skill covers
- Telegram channel posts
- Instagram captions and educational carousels/captions
- Grammar posts
- Event / impression posts
- English Life posts
- Tricky phrase / idiom / series-quote posts
- Lightweight adaptation of tone and structure for different platforms

## Default workflow
1. Identify the platform: Telegram, Instagram, or both.
2. Infer the rubric from the topic when it is obvious.
3. If the rubric is ambiguous, ask one short clarifying question only.
4. Draft in a warm, expert, conversational tone.
5. Keep the structure short, visual, and copy-ready.
6. Use examples, not abstract theory.
7. End with a CTA or a small interactive prompt when the rubric calls for it.

## Style rules
- Write in Russian by default.
- If the user's prompt is mixed Russian/English, mirror that mixed style lightly.
- Keep sentences short and readable.
- Prefer short paragraphs and bullet lists.
- Use emojis intentionally, but preserve the user's established emoji-rich rubric style when samples already use it.
- Avoid academic phrasing and long dense blocks.
- Prefer practical examples and clear explanations.
- Do not over-format with tables unless the user explicitly wants one.
- For this user, keep social-media drafts copy-ready, practical, and aligned with their existing rubric patterns instead of generic captions.
- If the user already has a recognized rubric/style, preserve that structure before adding new creative ideas.
- When the user says the draft is "not quite my style", treat it as a signal to preserve the original rubric voice, emoji rhythm, and block structure more faithfully.
- For emoji-rich rubric posts, keep the original block rhythm and emoji placement from the user's samples; do not flatten them into generic marketing copy.
- When a sample post shows a stable emoji pattern, treat that pattern as part of the rubric, not decoration.

## Rubric selection
Choose the most likely rubric automatically when the user says something like:
- `напиши тг пост на тему ...`
- `сделай пост для канала ...`
- `собери пост по этой теме ...`

Use the topic to select the rubric:
- Grammar rules, quantifiers, idioms, vocabulary explanations → grammar post
- Real-life experience, visits, school events, reflections → event / impression post
- Everyday English phrases and practical language → English Life post
- Series lines, idioms with a twist, beginner traps → tricky phrase / idiom post

## Important pitfalls
- Do not ask unnecessary follow-up questions if the rubric is clear.
- Do not write one-size-fits-all captions for the user's established rubrics.
- Do not flatten a grammar post into a generic caption.
- Do not turn a practical English Life post into a theory lesson.
- Do not make a tricky-phrase post too long.
- Do not omit examples in educational posts.

## Required support file
Use `references/telegram-post-style-guide.md` for the user's rubric structures, tone, lengths, and post patterns.
