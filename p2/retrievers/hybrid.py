"""Hybrid retrieval: reciprocal rank fusion (RRF) of bm25 and dense.

Each system ranks everything it can, and an item scores the sum of 1 / (K + rank) over the rankings it is in,
with K = 60 as in the 13 lab's rrf() (change it with `k = ...` in a [hybrid] table of p2.toml). Only ranks
count, so the very different score scales of bm25 (about 10 to 20) and dense (cosine, about 0.3 to 0.6)
need no care. bm25 scores 0 for a chunk that shares no word with the query and ranks those in id order;
an item with a score of 0 or less is left out of a ranking, so that padding adds nothing.

Full rankings are fused, not top-10 lists, because a document that is 11th in both can belong in the fused
top 10. search fuses the document rankings; search_chunks fuses the chunk rankings the same way, which
`p2 answer --system hybrid` and the reranker's first stage need. Equal fused scores fall in id order.
"""

from __future__ import annotations

from p2 import retrievers
from p2.runfile import order

NEEDS_CLAUDE = False

SYSTEMS = ("bm25", "dense")
DEFAULT_K = 60


def rrf(rankings, k: int) -> list[tuple[str, float]]:
    """Fuse rankings, each a best-first list of (id, score), into one list of (id, fused score)."""
    fused: dict[str, float] = {}
    for ranking in rankings:
        rank = 0
        for item, score in ranking:
            if score <= 0:
                continue  # no match at all (bm25's padding): not a rank
            rank += 1
            fused[item] = fused.get(item, 0.0) + 1.0 / (k + rank)
    return order(fused.items())


class Hybrid:
    def __init__(self, corpus, cfg):
        self.k = int(cfg.table("hybrid").get("k", DEFAULT_K))
        self.systems = [retrievers.build(name, corpus, cfg) for name in SYSTEMS]
        self.n_docs = len(corpus.docs)
        self.n_chunks = len(corpus.chunks(cfg.chunk_words, cfg.chunk_overlap))

    def search(self, text: str, k: int) -> list[tuple[str, float]]:
        return rrf([system.search(text, self.n_docs) for system in self.systems], self.k)[:k]

    def search_chunks(self, text: str, k: int) -> list[tuple[str, float]]:
        return rrf([system.search_chunks(text, self.n_chunks) for system in self.systems], self.k)[:k]


def build(corpus, cfg):
    return Hybrid(corpus, cfg)
