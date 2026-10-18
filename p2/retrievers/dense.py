"""Dense retrieval with OpenAI embeddings: embed every chunk once, embed the query, rank chunks by cosine similarity.

The model is text-embedding-3-small unless p2.toml has a [dense] table with `model = "..."`.
Like bm25.py it scores chunks and ChunkScorer lifts them to documents by each document's best chunk.

`p2 check` (and CI) run your retrievers again with no key and no network, so a vector that was only ever
fetched from OpenAI could not be reproduced there. Every vector this file fetches is therefore saved in
vectors/ (which git tracks, unlike .cache/), keyed by the hash of its text:

    vectors/<model>.chunks.npz     the chunks of a corpus
    vectors/<model>.queries.npz    the queries

A text that is already stored costs nothing and needs no key. Only a text that is not stored calls OpenAI,
and that needs OPENAI_API_KEY, from the file .env at the repo root (git ignores it, and it must stay that
way) or from your shell. New chunk text, for example a changed [chunking] setting or a document that was
added, is such a text.
"""

from __future__ import annotations

import hashlib
import http.client
import json
import os
import re
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

import numpy as np

from p2 import embed
from p2.retrievers import ChunkScorer

NEEDS_CLAUDE = False  # OpenAI is not Claude; the check never needs to switch it off

DEFAULT_MODEL = "text-embedding-3-small"
URL = "https://api.openai.com/v1/embeddings"
BLOCK = 256  # texts per request, and per save of the store
RETRIES = 5
RETRY_CODES = (429, 500, 502, 503, 504)


# The saved vectors: vectors/<model>.<kind>.npz, one unit vector per text, keyed by the hash of the text.


def _slug(model: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", model)


def _key(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:24]


def store_path(root: Path, model: str, kind: str) -> Path:
    return Path(root) / "vectors" / f"{_slug(model)}.{kind}.npz"


def _read(path: Path) -> dict[str, np.ndarray]:
    if not path.is_file():
        return {}
    try:
        with np.load(path, allow_pickle=False) as saved:
            keys, vectors = saved["keys"].tolist(), saved["vectors"]
        return {k: vectors[i] for i, k in enumerate(keys)}
    except (OSError, ValueError, KeyError):
        return {}  # a damaged file is fetched again


def _write(path: Path, store: dict[str, np.ndarray]) -> None:
    """Write the store in one step, so an interrupted run never leaves half a file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    keys = list(store)
    vectors = np.stack([store[k] for k in keys]).astype(np.float32) if keys else np.zeros((0, 0), dtype=np.float32)
    handle, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(handle, "wb") as out:
            np.savez(out, keys=np.array(keys), vectors=vectors)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


# Asking OpenAI, only for texts that are not stored yet.


def _api_key(root: Path) -> str:
    """OPENAI_API_KEY from the .env file at the repo root (git ignores it), else from the shell; "" if neither has it."""
    env_file = Path(root) / ".env"
    if env_file.is_file():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            name, sep, value = line.removeprefix("export ").partition("=")
            if sep and name.strip() == "OPENAI_API_KEY":
                value = value.strip().strip("\"'")
                if value:
                    return value
    return os.environ.get("OPENAI_API_KEY", "").strip()


def _fetch(model: str, texts: list[str], root: Path) -> np.ndarray:
    """One request: a unit-length row per text, in the order of `texts`."""
    key = _api_key(root)
    if not key:
        raise RuntimeError(
            f"{len(texts)} text(s) are not in vectors/ yet, so {model} must ask OpenAI for them, and no OPENAI_API_KEY was found. "
            "Put `OPENAI_API_KEY=...` in the file .env at the repo root (git ignores it) or export it in your shell."
        )
    body = json.dumps({"model": model, "input": texts, "encoding_format": "float"}).encode("utf-8")
    request = urllib.request.Request(URL, data=body, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    for attempt in range(RETRIES):
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                data = json.load(response)
            rows = sorted(data["data"], key=lambda item: item["index"])  # the reply lists them by index
            return embed.unit([row["embedding"] for row in rows])
        except urllib.error.HTTPError as error:
            if error.code in RETRY_CODES and attempt < RETRIES - 1:
                time.sleep(2**attempt)
                continue
            detail = error.read().decode("utf-8", "replace")[:300]
            raise RuntimeError(f"OpenAI embeddings request failed with HTTP {error.code}: {detail}") from None
        except (urllib.error.URLError, TimeoutError, ConnectionError, http.client.HTTPException) as error:  # a dropped connection too
            if attempt < RETRIES - 1:
                time.sleep(2**attempt)
                continue
            raise RuntimeError(f"OpenAI embeddings request failed: {error}") from None
    raise RuntimeError("unreachable")


def vectors(model: str, texts: list[str], root: Path, kind: str) -> np.ndarray:
    """One unit vector per text (rows in the order of `texts`), from vectors/ where stored, else from OpenAI.

    `kind` is "chunks" or "queries" and picks the file. New vectors are saved after every block, so an
    interrupted run keeps what it fetched.
    """
    path = store_path(root, model, kind)
    store = _read(path)
    keys = [_key(t) for t in texts]
    first = {k: t for k, t in zip(keys, texts) if k not in store}
    missing = list(first)
    if missing:
        print(f"Asking OpenAI ({model}) for {len(missing):,} {kind} vector(s); saved in {path.parent.name}/ for next time.", flush=True)
        for start in range(0, len(missing), BLOCK):
            block = missing[start : start + BLOCK]
            rows = _fetch(model, [first[k] for k in block], root)
            for k, row in zip(block, rows):
                store[k] = row
            _write(path, store)
    if not texts:
        return np.zeros((0, 0), dtype=np.float32)
    return np.stack([store[k] for k in keys]).astype(np.float32)


# The retriever.


class Dense(ChunkScorer):
    def __init__(self, corpus, cfg, model: str = DEFAULT_MODEL):
        super().__init__(corpus, cfg)
        self.model = model
        self.vectors = vectors(model, [c.text for c in self.chunks], cfg.root, "chunks")

    def score_chunks(self, text: str) -> list[float]:
        query = vectors(self.model, [text], self.cfg.root, "queries")[0]
        return (self.vectors @ query).tolist()  # unit vectors, so the dot product is the cosine


def build(corpus, cfg):
    return Dense(corpus, cfg, cfg.table("dense").get("model", DEFAULT_MODEL))
