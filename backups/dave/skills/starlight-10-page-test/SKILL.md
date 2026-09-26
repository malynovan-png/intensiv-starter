---
name: starlight-10-page-test
description: "Builds Starlight 10 page tests from supplied pages."
version: 1.0.0
author: Natalie, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Starlight, Grade-10, tests, worksheet, docx]
---

# Starlight 10_Page Test'

## 1. Purpose

This skill creates short classroom tests for **Starlight 10** based ONLY on the textbook pages,
screenshots, grammar references, vocabulary exercises, and explicit teacher instructions supplied
by the user.

The skill is designed for a Grade 10 teacher who wants:
- a **STANDARD** test at approximately **A2+**;
- a **PLUS** test at approximately **B1+**;
- **Version 1** and **Version 2** for each level;
- equivalent scope across versions, but different sentence contexts;
- separate **Answer Keys**;
- printable, economical **A4 portrait** formatting;
- vocabulary tasks that train active recall and paraphrase;
- PLUS tasks that support exam-style paraphrasing skills;
- no invented target vocabulary outside the supplied textbook material.

The skill must behave as a careful test designer, not as a generic worksheet generator.

## 2. Core non-negotiable principles

### 2.1 Source grounding

Use ONLY target language that is explicitly present in the user-supplied Starlight material.

For vocabulary, permitted sources are:
1. words and phrases printed in **bold** in the reading text;
2. lexical items explicitly practised in vocabulary exercises specified by the teacher;
3. collocations / phrases from those exercises;
4. definitions from the textbook may be used to understand meaning, but should not be treated as
   additional target vocabulary unless the teacher explicitly asks.

Do NOT:
- add unrelated phrasal verbs;
- add synonyms as target answers unless they are part of the supplied material;
- use generic "Unit vocabulary" from memory;
- rely on an external Starlight edition;
- assume that a word belongs to the unit merely because it fits the topic.

Neutral context words are allowed only to build natural sentences.

### 2.2 Grammar grounding

Use ONLY the grammar areas explicitly shown in the supplied pages or explicitly named by the teacher.

If the teacher specifies different grammar scope for STANDARD and PLUS, preserve that distinction.

Do not silently add past tenses, future forms, modals, conditionals, passive voice, articles, or
prepositions as tested grammar points unless explicitly included.

### 2.3 Parallelism

Version 1 and Version 2 must:
- test the same skill categories;
- contain the same number of items per exercise;
- be comparable in difficulty;
- use different sentence contexts;
- avoid simply changing one noun or place name;
- have independent, unambiguous answer keys.

STANDARD and PLUS should cover the same broad lexical field but at different cognitive difficulty.

### 2.4 No verbatim copying

Do not copy textbook exercise sentences verbatim.
Create new contexts that practise the same target material.
Short lexical items themselves may of course be reused because they are the target language.

## 3. Default output package

Unless the teacher requests otherwise, create:
1. STANDARD Version 1
2. STANDARD Version 2
3. PLUS Version 1
4. PLUS Version 2
5. Answer Key — STANDARD Version 1
6. Answer Key — STANDARD Version 2
7. Answer Key — PLUS Version 1
8. Answer Key — PLUS Version 2

When file creation is available, provide Word `.docx` files and one ZIP package.

## 4. Naming conventions

Use the exact module/page-test label supplied by the teacher.

Default heading pattern:
**STARLIGHT 10 • MODULE X.X**

Then:
**UNIT / MODULE X.X TEST**

Then level/version:
- STANDARD • Version 1
- STANDARD • Version 2
- PLUS • Version 1
- PLUS • Version 2

Important:
- If the teacher says `Module 1.1`, do NOT shorten it to `Module 1`.
- Preserve decimal module numbering exactly.

## 5. Level architecture

### 5.1 STANDARD

Target level: approximately **A2+**.

STANDARD should:
- use shorter sentences;
- use transparent contexts;
- minimise syntactic load;
- test recognition and controlled production;
- avoid unnecessarily abstract paraphrases;
- avoid trick questions;
- still require actual knowledge, not only visual matching.

### 5.2 PLUS

Target level: approximately **B1+**.

PLUS should:
- use more natural, richer contexts;
- require paraphrase recognition;
- require active lexical recall;
- include sentence transformation;
- distinguish close grammar meanings in context;
- train flexible processing rather than simple form matching;
- be useful as preparation for paraphrase-heavy school/exam tasks.

PLUS must be harder because of processing and context, not because it introduces vocabulary that
was never taught.

## 6. Vocabulary design rules

### 6.1 Build a lexical inventory first

Before writing any tasks, silently construct a lexical inventory from the supplied pages.

Recommended internal table:

| Source | Target lexical item | Meaning | Form constraints | Suitable level |
|---|---|---|---|---|
| reading bold | opted for | chose | fixed phrase | Standard / Plus |
| reading bold | picturesque | attractive | adjective | Standard / Plus |
| Ex. 6 | tight budget | little money available | collocation | Standard / Plus |

Then divide items across exercises so that repetition is minimal.

**Critical rule: minimise repetition.**
Do not recycle the same target item across Vocabulary Exercise 1 and Vocabulary Exercise 2 unless
the lexical inventory is too small.

Prefer:
- Exercise 1: one subset;
- Exercise 2: another subset.

Across Version 1 and Version 2, the same overall target inventory may be tested, but sentence contexts
must differ.

## 7. STANDARD vocabulary task patterns

STANDARD vocabulary should normally contain two exercises.

### STANDARD Vocabulary Exercise 1
Controlled contextual completion.

Preferred instruction:
**Complete the sentences with a suitable word or phrase.**

Use clear contexts that strongly support one intended answer.

Example logic:
> We travelled on a __________ budget, so we stayed in a small hostel.

Target:
> tight

or, if testing the full collocation:
> tight budget

Choose the blank position so the expected form is natural.

### STANDARD Vocabulary Exercise 2
Simple definition-to-word / synonym-to-target mapping in sentence context.

Preferred instruction:
**Complete the sentences with a suitable word or phrase.**

Example:
> An **achievement** can also be called a __________.

Answer:
> feat

This exercise may use a simple paraphrase, but the paraphrase should be easier than PLUS.

## 8. PLUS vocabulary task patterns

PLUS vocabulary uses a fixed two-step progression.

### PLUS Vocabulary Exercise 1 — paraphrase cue in brackets

This format is IMPORTANT and should be treated as the default.

Instruction:
**Complete the sentences with a suitable word or phrase. The words in brackets explain the meaning of the missing word or phrase.**

Pattern:
> 1. The advertisement immediately ____________________________  
> (**made me interested because the idea sounded so unusual**).

Rules:
- The bracketed phrase is a natural-language paraphrase of the target item.
- The bracketed paraphrase is NOT a dictionary definition copied from the textbook.
- It should explain meaning in context.
- The student must retrieve the target lexical item actively.
- The missing expression should normally be 1–4 words.
- The paraphrase must lead to one defensible target answer.
- Avoid giving the target word morphology away.

Preferred examples:
> We had to travel on a ____________________________  
> (**with very little money available to spend**).

Answer: `tight budget`

> The ferry crossing was unpleasant because of the ____________________________  
> (**stormy and difficult conditions at sea**).

Answer: `rough seas`

Formatting rule: in this exercise, the explanatory phrase in brackets may be **bold** because it is
semantically functional. Do not bold the whole sentence.

### PLUS Vocabulary Exercise 2 — sentence transformation without lexical prompts

This is a core format.

Instruction:
**Complete each second sentence so that it has a similar meaning to the first sentence. Use TWO to FIVE words.**

If the teacher explicitly requests another word limit, follow the teacher.

Pattern:
> 1. After considering all the possibilities, we **chose** the train rather than the plane.  
> After considering all the possibilities, we ____________________________ the train rather than the plane.

Answer: `opted for`

Essential formatting rule:
In the FIRST sentence, bold ONLY the word or phrase that must be replaced / paraphrased.

Correct:
> We **chose** the train.

Incorrect:
> We **chose the train rather than the plane**.

The bold span should mark the exact semantic unit being transformed.

No lexical prompts. Do NOT provide:
- a keyword in capitals;
- a word bank;
- the first letter;
- a list of possible expressions.

The learner must infer the target expression.

Structural rule: keep as much of the second sentence identical to the first as possible.
The transformation should test the lexical unit, not unrelated grammar manipulation.

Good examples:
> Building the Channel Tunnel was an impressive engineering **achievement**.  
> Building the Channel Tunnel was an impressive engineering ____________________________.

Answer: `feat`

> The train began to **speed up** after leaving the station.  
> The train began to ____________________________ after leaving the station.

Answer: `accelerate`

> I **reprimanded myself** for worrying so much about the journey.  
> I ____________________________ for worrying so much about the journey.

Answer: `scolded myself`

Avoid:
- changes that introduce a second equally valid answer;
- unnatural English;
- transformations requiring a grammar point not being tested;
- answers longer than the stated word limit;
- transformations whose second sentence forces a different meaning.

## 9. Grammar design

Grammar architecture depends on the supplied page.

For the established Module 1.1 pattern:

### STANDARD grammar
Focus:
- Comparatives
- Superlatives
- extended comparison structures if supplied:
  - less + adjective + than
  - the least + adjective
  - as + adjective + as
  - half / twice / three times as + adjective + as
  - much / a lot / far + comparative
  - a little / a bit / slightly + comparative
  - comparative and comparative
  - the comparative ..., the comparative ...
  - by far + superlative

#### STANDARD Grammar Exercise 3
Preferred format:
**Complete the sentences with the comparative or superlative form of the adjective in brackets.**

Use 8 items by default.

#### STANDARD Grammar Exercise 4
Prefer a second format rather than repeating Exercise 3.
Options:
- choose the correct answer;
- complete comparison structures;
- short sentence completion.

The second exercise should test comparison patterns, not just adjective spelling.

### PLUS grammar
For Module 1.1 established scope:

#### Exercise 3
Present Simple vs Present Continuous, including:
- routines vs actions around now;
- fixed schedules;
- temporary situations;
- changing situations;
- stative verbs;
- verbs with stative/action meaning changes, e.g. think, see, have, taste, smell, be where context permits.

Instruction:
**Put the verbs in brackets into the Present Simple or Present Continuous.**

#### Exercise 4
Present Perfect vs Present Perfect Continuous, plus:
- have been to
- have gone to
- have been in

Instruction:
**Complete the sentences using the Present Perfect or Present Perfect Continuous. Use have been to / have gone to / have been in where appropriate.**

PLUS grammar quality rule: every item must have one intended answer based on context.
Do not write items where two forms are equally natural unless the key intentionally accepts both.

## 10. Item count

Default:
- Vocabulary Exercise 1: 8 items
- Vocabulary Exercise 2: 8 items
- Grammar Exercise 3: 8 items
- Grammar Exercise 4: 8 items

Total: 32 responses per test.

This can be reduced only if required by print layout.
If reducing:
- keep the same number of items in Version 1 and Version 2;
- preserve proportional coverage;
- do not delete all examples of a key grammar sub-area.

## 11. Version 1 vs Version 2

Version 2 is NOT created by superficial substitution.
Do not merely change Paris → London, Anna → Kate, train → bus.

Instead:
- change the scenario;
- change grammatical subject where appropriate;
- vary sentence syntax;
- use a different contextual clue;
- preserve the exact target skill and difficulty.

Example:
Version 1:
> The train began to **speed up** after leaving the station.

Version 2:
> Once outside the tunnel, the train **increased its speed** rapidly.

Both may target `accelerate / accelerated`.

## 12. Answer key requirements

Every test must have a separate answer key.

Key format:
- Vocabulary
  - Exercise 1
  - Exercise 2
- Grammar
  - Exercise 3
  - Exercise 4

Answers must match the exact grammatical form required by the sentence.
Examples:
- `opted for`, not merely `opt`
- `has gone`, not `gone`
- `most comfortable`, not `comfortable`

If an alternative is legitimately acceptable, write it explicitly, e.g. `farther / further`.
Do not list speculative alternatives.

## 13. Validation pass before finalising

### 13.1 Source check
For every vocabulary answer ask:
> Is this lexical item explicitly present in the supplied material?
If no → remove or replace.

### 13.2 Uniqueness check
For every blank ask:
> Could a competent learner reasonably give another target answer from the supplied vocabulary?
If yes → rewrite context.

### 13.3 Grammar check
Substitute the answer into the complete sentence.
Check subject-verb agreement, article use, prepositions, tense, word form, collocation, and naturalness.

### 13.4 Word-limit check
For sentence transformations, count words exactly.
Do not write an answer that violates the printed limit.

### 13.5 Difficulty check
STANDARD = clear, direct, controlled.
PLUS = paraphrase-rich, active recall, more demanding context.
Do not make PLUS harder by using untaught words as answers.

### 13.6 Parallel-version check
Compare Version 1 and Version 2 for equal item count, similar difficulty, same grammar coverage, and
comparable lexical coverage.

### 13.7 Repetition check
Within each PLUS test, maximise non-overlap between Vocabulary 1 and Vocabulary 2.

## 14. Word / print formatting standard

When Word generation is available, use the following house style.

### 14.1 Page setup
- Paper: **A4**
- Orientation: **Portrait**
- Margins: narrow but print-safe, approx. 0.5–0.7 cm where supported
- No decorative images
- Black / greyscale printer-friendly design

### 14.2 Combined teacher-preferred layout
When the teacher asks to put both variants on one sheet:
- **Version 1 on the upper half**
- **Version 2 on the lower half**

Within EACH version:
- left column = **VOCABULARY**
- right column = **GRAMMAR**

Conceptual page:

```text
┌────────────────────────────────────────┐
│ STANDARD / PLUS — Version 1            │
│ ┌──────────────┬─────────────────────┐ │
│ │ VOCABULARY   │ GRAMMAR             │ │
│ │ Ex 1 / Ex 2  │ Ex 3 / Ex 4         │ │
│ └──────────────┴─────────────────────┘ │
├────────────────────────────────────────┤
│ STANDARD / PLUS — Version 2            │
│ ┌──────────────┬─────────────────────┐ │
│ │ VOCABULARY   │ GRAMMAR             │ │
│ │ Ex 1 / Ex 2  │ Ex 3 / Ex 4         │ │
│ └──────────────┴─────────────────────┘ │
└────────────────────────────────────────┘
```

### 14.3 Font sizes
Teacher preference:
- **main exercise text: 10 pt**
- **exercise headings/instructions: 12 pt**
- section headings `VOCABULARY` / `GRAMMAR`: 12–14 pt
- document title: compact but clear

Do NOT reduce the body text below 10 pt unless the teacher explicitly approves it.
If PLUS cannot fit on one page at 10 pt, preserve readability and tell the teacher it requires two
pages OR ask whether to reduce item count. Do not silently shrink to 7–8 pt.

### 14.4 Spacing
- Add visible spacing before a new exercise.
- Exercise 2 should not visually run into Exercise 1.
- Exercise 4 should not visually run into Exercise 3.
- Use compact line spacing but not cramped.
- Fill columns sensibly; avoid large unused empty zones if the content can be distributed more evenly.

### 14.5 Bold formatting
CRITICAL house rule:
Do NOT use bold decoratively throughout the test.

Bold ONLY where it has functional meaning.

Allowed:
- the phrase to be paraphrased in PLUS Vocabulary Exercise 2;
- semantic cue in brackets in PLUS Vocabulary Exercise 1, if desired;
- concise section/exercise labels if needed for hierarchy.

Do NOT bold:
- entire question sentences;
- every instruction word;
- arbitrary target contexts;
- whole answer blanks;
- all numbering.

The test should look calm and professional.

## 15. Interaction protocol

When the teacher sends new screenshots/pages:
1. Inspect the material.
2. Identify module number, reading text, bold vocabulary, vocabulary exercises, grammar reference,
   requested STANDARD grammar, and requested PLUS grammar.
3. Build the lexical and grammar inventory.
4. If the scope is clear, DO NOT ask unnecessary clarification questions.
5. Produce a draft structure.
6. Apply the teacher's established formats automatically.
7. If files are requested, generate Word files plus keys.

Ask clarification only when:
- screenshots are unreadable;
- module number is unknown and cannot be inferred;
- the teacher has not specified which grammar belongs to which level and multiple interpretations are plausible;
- there is insufficient vocabulary to create the requested number of unique items.

## 16. Established teacher preferences to preserve

1. Test task instructions are in **English**.
2. Teacher-facing explanations may be in **Russian**.
3. STANDARD ≈ **A2+**.
4. PLUS ≈ **B1+**.
5. Two variants per level.
6. Separate answer keys.
7. PLUS Vocabulary 1 = contextual blank + paraphrase in brackets.
8. PLUS Vocabulary 2 = paired sentence transformation, no keyword hints.
9. In PLUS Vocabulary 2, bold ONLY the exact word/phrase to be replaced.
10. Maximise non-repetition of target lexical items between Vocabulary 1 and Vocabulary 2.
11. Do not say vaguely "use vocabulary from Unit X"; use the actual supplied lexical items.
12. Heading must preserve exact module numbering, e.g. **MODULE 1.1**.
13. Preferred print layout: A4 portrait.
14. If combining versions: Version 1 above Version 2.
15. Within each version: Vocabulary left, Grammar right.
16. Main font 10 pt; exercise headings/instructions 12 pt.
17. Bold only when semantically useful.
18. Prioritise readability over forcing too much material onto one page.

## 17. Example template — PLUS

### VOCABULARY

**1 Complete the sentences with a suitable word or phrase. The words in brackets explain the meaning of the missing word or phrase.**

1. The advertisement immediately ____________________________  
   (**made me interested because the idea sounded so unusual**).

2. We had to travel on a ____________________________  
   (**with very little money available to spend**).

**2 Complete each second sentence so that it has a similar meaning to the first sentence. Use TWO to FIVE words.**

1. After considering all the possibilities, we **chose** the train rather than the plane.  
   After considering all the possibilities, we ____________________________ the train rather than the plane.

2. Building the tunnel was an impressive engineering **achievement**.  
   Building the tunnel was an impressive engineering ____________________________.

### GRAMMAR

**3 Put the verbs in brackets into the Present Simple or Present Continuous.**

1. Every summer my sister __________ (travel) abroad, but this year she __________ (stay) in Britain.

**4 Complete the sentences using the Present Perfect or Present Perfect Continuous. Use have been to / have gone to / have been in where appropriate.**

1. We __________________ (wait) for the train for over an hour.

## 18. Example template — STANDARD

### VOCABULARY

**1 Complete the sentences with a suitable word or phrase.**

1. We travelled on a __________ budget, so we stayed in a small hostel.

**2 Complete the sentences with a suitable word or phrase.**

1. An **achievement** can also be called a __________.

### GRAMMAR

**3 Complete the sentences with the comparative or superlative form of the adjective in brackets.**

1. This train is __________ (fast) than the bus.

**4 Choose the correct answer.**

1. This was ___ journey of my life.  
   A the most exciting   B more exciting

## 19. Failure modes to avoid

Never:
- invent a target word because it fits the topic;
- copy the textbook exercise sentence verbatim;
- use the same target lexical item repeatedly across both vocabulary exercises when alternatives exist;
- make a PLUS task difficult merely through obscure non-target vocabulary;
- give keyword prompts in PLUS Vocabulary 2;
- bold the entire phrase around a smaller paraphrase target;
- shrink body font excessively to force one-page output;
- change `Module 1.1` to `Module 1`;
- create a key with forms that do not fit the sentence;
- mix answer keys into the student version;
- create Version 2 as a trivial name/place swap.

## 20. Final response style

When files are generated, respond briefly in Russian:
- say what was created;
- mention STANDARD / PLUS and versions;
- link the Word files and ZIP;
- do not repeat the full test text unless asked.

When only drafting in chat:
- keep test instructions in English;
- teacher notes in Russian;
- show the Answer Key separately.

End of skill.
