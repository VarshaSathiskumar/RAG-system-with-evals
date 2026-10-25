"""Ablation of rerank: the same reranker with the prompt's domain line changed to match the own corpus.

rerank.py tells Claude the questions are about US mine safety and health regulations (30 CFR), which is the
shared corpus. This variant says US immigration, work authorization and tax rules instead. Nothing else
differs: same hybrid first stage, same top 20, same 300-word passages, same schema.

Reranking: ask Claude to reorder hybrid's top 20, listwise.

The first stage is hybrid (RRF of bm25 and dense). Its top 20 go to Claude as numbered passages in one
claude -p call, and Claude answers with the order it wants, {"order": [20 numbers]}. A reranker can only
reorder what the first stage hands it, so a document outside hybrid's top 20 stays outside the top 20.

The reply is forced into SCHEMA, whose numbers are limited to 1..N, the count of passages, so Claude cannot
name a passage that does not exist. A reply that is not each number once, or a call that fails, keeps the
first-stage order for that query and prints a warning under the query (nothing is hidden). Documents below
the top 20 keep their first-stage order underneath.

NEEDS_CLAUDE = True: searching calls claude -p, so CI never runs this system again. p2 run writes the run
file and a trace (traces/) of the calls; commit them together, because p2 check compares the two.

search_chunks does the same over hybrid's top 20 chunks, which `p2 answer --system rerank` needs.
"""

from __future__ import annotations

from p2 import claude, retrievers

NEEDS_CLAUDE = True
BASE = "rerank"

TOP = 20  # how many first-stage candidates Claude reorders
PASSAGE_WORDS = 300  # how much of each candidate Claude reads (one chunk's worth)

PROMPT = """You are reranking search results for a question about US immigration, work authorization and tax rules for students and workers.

Question: {query}

Below are {n} passages, numbered [1] to [{n}]. Order them from the most useful to the least useful for answering the question.
A passage that states the rule the question asks about comes before one that is only on the same topic.
A passage that does not help answers last. Use every number from 1 to {n} exactly once.

{passages}

Reply with the order as a list of the {n} passage numbers, best first."""


def schema(n: int) -> dict:
    return {
        "type": "object",
        "properties": {"order": {"type": "array", "items": {"type": "integer", "minimum": 1, "maximum": n}, "minItems": n, "maxItems": n}},
        "required": ["order"],
        "additionalProperties": False,
    }


def first_words(text: str, words: int) -> str:
    parts = text.split()
    return " ".join(parts[:words]) + (" ..." if len(parts) > words else "")


class Rerank:
    def __init__(self, corpus, cfg):
        self.corpus = corpus
        self.cfg = cfg
        self.model = cfg.model
        self.first_stage = retrievers.build("hybrid", corpus, cfg)
        self.chunk_text = corpus.chunk_texts(cfg.chunk_words, cfg.chunk_overlap)

    def reorder(self, query: str, hits: list[tuple[str, float]], texts: dict[str, str]) -> list[tuple[str, float]]:
        """Reorder the first TOP of `hits` (best first, (id, score)); the rest follow in their order. Scores are positions, so they only fall."""
        head, tail = hits[:TOP], hits[TOP:]
        order = list(range(len(head)))
        if len(head) > 1:
            passages = "\n\n".join(f"[{i}] {first_words(texts[item], PASSAGE_WORDS)}" for i, (item, _) in enumerate(head, 1))
            reply = claude.call(
                PROMPT.format(query=query, n=len(head), passages=passages), schema(len(head)),
                model=self.cfg.model, cache_dir=claude.cache_folder(self.cfg),
            )  # fmt: skip
            numbers = (reply.output or {}).get("order")
            if reply.error or not isinstance(numbers, list) or sorted(numbers) != list(range(1, len(head) + 1)):
                why = reply.error or "the reply was not each passage number once"
                print(f"    warning: keeping the first-stage order for this query ({why})", flush=True)
            else:
                order = [n - 1 for n in numbers]
        ranked = [head[i][0] for i in order] + [item for item, _ in tail]
        return [(item, float(len(ranked) - i)) for i, item in enumerate(ranked)]

    def search(self, text: str, k: int) -> list[tuple[str, float]]:
        hits = self.first_stage.search(text, max(k, TOP))
        texts = {d: self.corpus.docs[d].text for d, _ in hits[:TOP]}
        return self.reorder(text, hits, texts)[:k]

    def search_chunks(self, text: str, k: int) -> list[tuple[str, float]]:
        hits = self.first_stage.search_chunks(text, max(k, TOP))
        texts = {c: self.chunk_text[c] for c, _ in hits[:TOP]}
        return self.reorder(text, hits, texts)[:k]


def build(corpus, cfg):
    return Rerank(corpus, cfg)
