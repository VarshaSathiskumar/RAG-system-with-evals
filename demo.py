"""A terminal demo of the RAG system: ask a question, get an answer with its evidence.

One question goes through what `p2 answer` does for one question:
- the chosen system's search_chunks(question, top) returns the top chunks,
- Claude answers only from them and cites a chunk id and a quote for every claim (prompts/answer.txt),
- every quote is checked against the chunk it cites, the way `p2 verify` checks it.

Nothing is written to the repo. Claude's replies are cached in .cache/claude/ (git ignores it), so asking the
same question again is instant, and a query vector that OpenAI has to be asked for is kept in memory only, so
vectors/ stays as committed.

    uv run python demo.py                         # your own corpus, the rerank system
    uv run python demo.py --system bm25           # keyword search only; no OpenAI key needed
    uv run python demo.py --ask "How long is the OPT grace period?"

Each question costs two Claude calls with rerank (one to rerank, one to answer) and one with the others.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import textwrap
import time
from pathlib import Path

from p2 import answer, claude, config, retrievers, verify
from p2 import corpus as corpus_mod
from p2.retrievers import dense

try:
    import readline  # noqa: F401  (gives the prompt arrow keys and history)
except ImportError:
    pass

ROOT = Path(__file__).resolve().parent
HELP = """Type a question and press Enter. Commands:
  :system NAME   switch the retriever (bm25, dense, hybrid, rerank, rerank_prompt)
  :top N         how many chunks the answer may use
  :chunks        show or hide the retrieved chunks
  :help          this text
  :quit          leave (so do an empty line, quit, exit and Ctrl-D)"""


def style(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m" if sys.stdout.isatty() else text


def bold(text: str) -> str:
    return style(text, "1")


def dim(text: str) -> str:
    return style(text, "2")


def green(text: str) -> str:
    return style(text, "32")


def red(text: str) -> str:
    return style(text, "31")


def width() -> int:
    return min(100, shutil.get_terminal_size((100, 24)).columns)


def wrap(text: str, indent: int = 2, hang: int | None = None) -> str:
    """Wrap to the terminal; later lines are indented by `hang` (default: like the first)."""
    hang = indent if hang is None else hang
    return textwrap.fill(" ".join(text.split()), width(), initial_indent=" " * indent, subsequent_indent=" " * hang)


def quote_found(claim: dict, retrieved: list[str], texts: dict[str, str]) -> bool:
    """True when the claim cites a chunk that was retrieved and quotes a real piece of it."""
    cid, quote = claim.get("chunk_id"), claim.get("quote")
    return cid in retrieved and cid in texts and bool(quote) and verify.norm(quote) in verify.norm(texts[cid])


class Demo:
    def __init__(self, cfg, corpus_name: str, system: str, top: int, show_chunks: bool):
        self.cfg = cfg
        self.corpus = corpus_mod.load(cfg.root, corpus_name)
        self.texts = self.corpus.chunk_texts(cfg.chunk_words, cfg.chunk_overlap)
        self.system_prompt = answer.load_system_prompt(cfg.root)
        self.name = system
        self.top = top
        self.show_chunks = show_chunks
        self.use(system)

    def use(self, name: str) -> None:
        """Switch to a system; it stays the current one only if it builds and can search chunks."""
        print(dim(f"Loading {name}..."), flush=True)
        try:
            system = retrievers.build(name, self.corpus, self.cfg)
        except retrievers.UnknownSystem:
            print(red(f"There is no system called {name}. Try one of: {', '.join(retrievers.names())}."))
            return
        except (NotImplementedError, RuntimeError) as error:
            print(red(str(error)))
            return
        if not callable(getattr(system, "search_chunks", None)):
            print(red(f"{name} has no search_chunks, so it cannot feed an answer."))
            return
        self.name, self.system = name, system

    def title(self, chunk_id: str) -> str:
        doc = self.corpus.docs.get(corpus_mod.docid_of(chunk_id))
        return textwrap.shorten(doc.title, 60, placeholder="...") if doc else "?"

    def ask(self, question: str) -> None:
        started = time.perf_counter()
        hits = self.system.search_chunks(question, self.top)
        retrieval = time.perf_counter() - started
        ids = [cid for cid, _ in hits]
        prompt = answer.USER_PROMPT.format(chunks=answer.format_chunks(hits, self.texts), question=question)
        print(dim("Asking Claude..."), flush=True)
        reply = claude.call(prompt, answer.SCHEMA, system=self.system_prompt, model=self.cfg.model, cache_dir=claude.cache_folder(self.cfg))
        if reply.error:
            print(red(f"Claude did not answer: {reply.error}"))
            return
        out = reply.output
        claims = [c for c in (out.get("claims") or []) if isinstance(c, dict)]

        print()
        print(bold("Answer"))
        if out.get("not_found"):
            print(wrap("I could not find an answer to this in the corpus."))
        else:
            print(wrap(str(out.get("answer", ""))))
        if claims:
            print()
            print(bold("Evidence"))
            for n, claim in enumerate(claims, 1):
                mark = green("verified") if quote_found(claim, ids, self.texts) else red("NOT FOUND in the chunk")
                cid = str(claim.get("chunk_id"))
                print(wrap(f"[{n}] {claim.get('text', '')}", 2, 6))
                print(wrap(f"{mark}  {cid} - {self.title(cid)}", 6, 8))
                print(dim(wrap(f'"{claim.get("quote", "")}"', 6)))
        print()
        print(bold("Retrieved") + dim(f" ({self.name}, top {self.top})"))
        for n, cid in enumerate(ids, 1):
            print(wrap(f"{n}. {cid} - {self.title(cid)}", 2, 5))
            if self.show_chunks:
                print(dim(textwrap.indent(textwrap.fill(" ".join(self.texts[cid].split()), width() - 6), "      ")))
        saved = "saved reply, no call" if reply.cached else f"{reply.seconds:.1f} s"
        print(dim(f"\nretrieval {retrieval:.1f} s | answer {saved} | {reply.input_tokens:,} input tokens | {reply.model}"))

    def command(self, line: str) -> bool:
        """Run a :command; False when the session should end."""
        word, _, rest = line.partition(" ")
        rest = rest.strip()
        if word in (":quit", ":q", ":exit"):
            return False
        if word == ":help":
            print(HELP)
        elif word == ":system" and rest:
            self.use(rest)
        elif word == ":top" and rest.isdigit() and int(rest) > 0:
            self.top = int(rest)
        elif word == ":chunks":
            self.show_chunks = not self.show_chunks
            print(dim(f"Showing chunks: {'on' if self.show_chunks else 'off'}"))
        else:
            print(HELP)
        return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Ask the RAG system a question in the terminal.")
    parser.add_argument("--corpus", choices=("own", "shared"), default="own", help="the corpus to search (default own)")
    parser.add_argument("--system", default="rerank", help="the retriever (default rerank)")
    parser.add_argument("--top", type=int, help="chunks the answer may use (default [answer] top in p2.toml)")
    parser.add_argument("--chunks", action="store_true", help="print the text of every retrieved chunk")
    parser.add_argument("--fresh", action="store_true", help="ask Claude again instead of using saved replies")
    parser.add_argument("--ask", metavar="QUESTION", help="answer one question and exit")
    args = parser.parse_args()

    cfg = config.load(ROOT)
    if args.fresh:
        cfg = cfg.replace(cache_claude=False)
    dense._write = lambda path, store: None  # a new query vector stays in memory; vectors/ is tracked and must not change
    demo = Demo(cfg, args.corpus, args.system, args.top or cfg.answer_top, args.chunks)
    if not hasattr(demo, "system"):
        return 1

    def run(question: str) -> None:
        try:
            demo.ask(question)
        except (RuntimeError, claude.ClaudeNotFound) as error:
            print(red(str(error)))
            print(dim("Try :system bm25, which needs no OpenAI key."))
        except KeyboardInterrupt:
            print(dim("\nStopped."))

    if args.ask:
        run(args.ask)
        return 0
    print(bold(f"RAG demo - {args.corpus} corpus, {len(demo.corpus.docs):,} documents"))
    print(dim("Type :help for commands, an empty line to leave.\n"))
    while True:
        try:
            line = input(bold(f"[{demo.name}] Question> ")).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not line or line.lower() in ("quit", "exit"):
            return 0
        if line.startswith(":"):
            if not demo.command(line):
                return 0
            continue
        run(line)
        print()


if __name__ == "__main__":
    sys.exit(main())
