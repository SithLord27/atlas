import re

def tokenize(text):
    # keep only words + basic math symbols
    text = text.lower()
    return re.findall(r"[a-z0-9λ∇∫]+", text)


def term_frequency_score(text, words):
    tokens = tokenize(text)
    score = 0

    for w in words:
        score += tokens.count(w) * 2

    return score


def coverage_score(text, words):
    text = text.lower()
    found = sum(1 for w in words if w in text)

    # reward pages containing many of the query words
    return found * 5


def proximity_score(text, words):
    text = text.lower()

    score = 0
    for i in range(len(words) - 1):
        pair = words[i] + " " + words[i+1]
        if pair in text:
            score += 8

    return score


def heading_bonus(text, words):
    # simple heuristic: headings often have capitals or numbers like "5.2"
    first_lines = "\n".join(text.split("\n")[:6]).lower()

    bonus = 0
    for w in words:
        if w in first_lines:
            bonus += 6

    return bonus


def score_page(text, query_words):
    return (
        term_frequency_score(text, query_words) +
        coverage_score(text, query_words) +
        proximity_score(text, query_words) +
        heading_bonus(text, query_words)
    )
