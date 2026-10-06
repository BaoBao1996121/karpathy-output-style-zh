---
name: clear-writing
description: Write or revise explanations in concise English inspired by Karpathy's ASD-STE100 suggestion. Use for clear prose, technical explanations, or an explicitly requested STE draft.
---

# Clear writing

Explain the subject so the reader can understand it without decoding the prose.
Follow Karpathy's suggestion to get "80% of the way to ASD-STE100."
That phrase describes a style preference, not a compliance score.

Read [the standard reference](references/asd-ste100.md) for the exact standard,
examples, and corrections to [the tweet's attached image](references/karpathy-asd-ste100.png).
The baseline is **ASD-STE100 Simplified Technical English, Issue 9 (2025-01-15)**.

## Default: readable, STE-inspired

1. Identify the reader's question and the facts that answer it.
2. Give the main idea, then build the explanation in a useful order.
3. Use common words, concrete subjects, and active verbs. Define necessary terms.
4. Keep one name for each concept. Remove decorative synonyms and stock phrases.
5. Aim for 25 words or fewer per descriptive sentence and 20 per instruction.
   Keep one topic per paragraph; split paragraphs longer than six sentences.
6. Give one instruction per sentence. Put a prerequisite before the action.
   Break long noun groups into phrases that show how the parts relate.
7. Remove needless words, then read for meaning. Preserve facts, uncertainty,
   units, exceptions, and the user's voice. Keep natural phrasing when it helps.

Return the requested text. Add explanation about edits only when useful or requested.

## When the user requests strict ASD-STE100

Read the relevant writing rules **and** dictionary in an official copy of the
requested issue. Otherwise use Issue 9, after checking the official site for updates.
Identify technical nouns and verbs from the user's subject field or approved glossary.
Check words by their approved meaning, part of speech, and allowed form.
Apply the procedural or descriptive rules as appropriate, including the standard's
word-count conventions. Use the reference's rule map to locate the relevant sections.

If the official rules, dictionary, or required terminology are unavailable, produce
a clearly labeled STE-inspired draft and state what remains unverified. Request the
missing reference when strict verification is needed. Do not claim compliance from
short sentences, a model's memory, or the attached image. For a strict draft, report
the issue used and the checks completed; distinguish drafting from verified compliance.

## Example

Before: "It is imperative that the operator ensures the valve is closed prior to operation."

After: "Before you start the operation, close the valve."

This illustrates the style; it is not a claim that the complete document is compliant.
