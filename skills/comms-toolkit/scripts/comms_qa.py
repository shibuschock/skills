#!/usr/bin/env python3
"""
comms_qa.py — plain-language QA for a comms draft. Computes a Flesch-Kincaid
grade level (stdlib syllable heuristic), flags over-long sentences, and flags a
small AI-slop / jargon word list. Prints a report and whether the draft meets
the reading-grade 5-7 target. Stdlib only.

Usage:
  python3 comms_qa.py --file draft.md [--target-low 5] [--target-high 7]
                      [--max-words 25]

The plain-language standard: reading grade 5-7, short sentences, de-slopped.
"""
import argparse
import re
from pathlib import Path

# Small, deliberately conservative AI-slop / corporate-jargon list.
SLOP = [
    "leverage", "leveraging", "synergy", "synergies", "utilize", "utilization",
    "delve", "seamless", "seamlessly", "robust", "holistic", "paradigm",
    "cutting-edge", "best-in-class", "world-class", "game-changer", "game-changing",
    "empower", "empowering", "unlock", "unlocking", "elevate", "elevating",
    "streamline", "streamlining", "at the end of the day", "moving forward",
    "circle back", "touch base", "low-hanging fruit", "boil the ocean",
    "it is important to note", "in today's fast-paced", "furthermore", "moreover",
    "navigate the complexities", "tapestry", "underscore", "underscores",
    "pivotal", "transformative", "revolutionize", "revolutionary", "dive deep",
]

VOWELS = "aeiouy"


def count_syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    count = 0
    prev_vowel = False
    for ch in w:
        is_vowel = ch in VOWELS
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    # silent trailing 'e'
    if w.endswith("e") and count > 1:
        count -= 1
    return max(1, count)


def strip_markdown(text):
    text = re.sub(r"`{1,3}[^`]*`{1,3}", " ", text)          # code
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)        # images
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)     # links -> label
    text = re.sub(r"^\s{0,3}#{1,6}\s*", "", text, flags=re.M)  # headings
    text = re.sub(r"[*_>#|-]", " ", text)                     # md punctuation
    text = re.sub(r"\{\{[^}]*\}\}", " ", text)               # {{placeholders}}
    return text


def split_sentences(text):
    # Blank lines are paragraph boundaries, so a heading or salutation with no terminal
    # punctuation doesn't glue onto the next paragraph. Wrapped lines inside a paragraph
    # are joined so a hard-wrapped long sentence is still counted as one sentence.
    out = []
    for block in re.split(r"\n\s*\n", text.strip()):
        block = re.sub(r"\s*\n\s*", " ", block).strip()
        for p in re.split(r"(?<=[.!?])\s+", block):
            if re.search(r"[a-zA-Z]", p):
                out.append(p.strip())
    return out


def words_in(s):
    return re.findall(r"[A-Za-z][A-Za-z'-]*", s)


def analyze(raw):
    text = strip_markdown(raw)
    sentences = split_sentences(text)
    all_words = words_in(text)
    n_sent = max(1, len(sentences))
    n_words = max(1, len(all_words))
    n_syll = sum(count_syllables(w) for w in all_words)
    fk = 0.39 * (n_words / n_sent) + 11.8 * (n_syll / n_words) - 15.59
    long_sents = [(len(words_in(s)), s) for s in sentences if len(words_in(s)) > 0]
    return {
        "sentences": len(sentences),
        "words": len(all_words),
        "syllables": n_syll,
        "fk_grade": round(fk, 1),
        "avg_sentence_words": round(n_words / n_sent, 1),
        "long_sents": long_sents,
    }


def find_slop(raw):
    low = raw.lower()
    return [term for term in SLOP if re.search(r"\b" + re.escape(term) + r"\b", low)]


def main():
    ap = argparse.ArgumentParser(description="Plain-language QA for a comms draft.")
    ap.add_argument("--file", required=True, help="draft markdown/text file")
    ap.add_argument("--target-low", type=int, default=5)
    ap.add_argument("--target-high", type=int, default=7)
    ap.add_argument("--max-words", type=int, default=25)
    a = ap.parse_args()

    raw = Path(a.file).read_text(encoding="utf-8")
    r = analyze(raw)
    slop = find_slop(raw)
    long_flagged = [(n, s) for n, s in r["long_sents"] if n > a.max_words]

    grade = r["fk_grade"]
    meets = a.target_low <= grade <= a.target_high
    verdict = "PASS" if meets else ("TOO COMPLEX" if grade > a.target_high else "OK (simpler than target)")

    print(f"=== Comms QA: {a.file} ===")
    print(f"Flesch-Kincaid grade level : {grade}   (target {a.target_low}-{a.target_high})  -> {verdict}")
    print(f"Words / Sentences          : {r['words']} / {r['sentences']}  (avg {r['avg_sentence_words']} words/sentence)")
    print()

    if long_flagged:
        print(f"Long sentences (> {a.max_words} words) - split these:")
        for n, s in long_flagged:
            snippet = (s[:90] + "...") if len(s) > 90 else s
            print(f"  [{n}w] {snippet}")
        print()
    else:
        print(f"No sentences over {a.max_words} words. Good.")
        print()

    if slop:
        print("AI-slop / jargon flagged - replace with plain words:")
        for t in slop:
            print(f"  - {t}")
        print()
    else:
        print("No AI-slop / jargon terms flagged. Good.")
        print()

    issues = (0 if meets else 1) + len(long_flagged) + len(slop)
    print(f"Result: {'CLEAN' if issues == 0 else str(issues) + ' issue(s) to address'} "
          f"({'meets' if meets else 'does not meet'} the grade {a.target_low}-{a.target_high} standard).")


if __name__ == "__main__":
    main()
