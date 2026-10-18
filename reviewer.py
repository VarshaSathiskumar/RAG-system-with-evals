"""reviewer.py: the last step of the pipeline. Claude (claude -p) reviews each answer in an answers file.

    uv run python reviewer.py answers/shared/rerank.json [--only a01,a09] [--dry] [--yes] [--fresh]

For every question the reviewer gets the question, the generated answer with its cited claims, and the
chunks that were retrieved for it (all from the answers file that `p2 answer` wrote). It scores the answer
from 1 to 5 on four dimensions and says what is wrong, if anything:

    correctness    is the answer consistent with the chunks?
    groundedness   is every claim supported by the chunks it cites?
    completeness   does the answer include what is needed to answer the question?
    relevance      does the answer address the question that was asked?

PASS, PARTIAL or FAIL then comes from the four scores by verdict() below, a rule and not a second opinion
from Claude, so the same scores always give the same result. Change the rule there if you want another.

The reviewer sees no gold sections and no relevance labels. Its calls go through p2.claude.call, so replies
are saved in .cache/claude/ (--fresh asks again), a run of more than 5 calls asks first (--yes), and the
model is [claude] model in p2.toml. --dry prints what Claude would be sent for the first question and
calls nothing.

The result is written to reviews/<corpus>/<label>.review.json, outside answers/ on purpose: p2 check reads
every answers/<corpus>/*.json as an answers file. These scores come from one call of a model that is not
checked against a person's judgment (p2 judge and the calibration file do that for claims), so read the
issues, not only the numbers.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from p2 import answer, claude, config, paths, verify

ROOT = Path(__file__).resolve().parent
DIMENSIONS = ("correctness", "groundedness", "completeness", "relevance")
SCHEMA = {
    "type": "object",
    "properties": {
        **{d: {"type": "integer", "minimum": 1, "maximum": 5} for d in DIMENSIONS},
        "issues": {"type": "string", "description": "a short explanation of each problem found, or an empty string if there is none"},
    },
    "required": [*DIMENSIONS, "issues"],
    "additionalProperties": False,
}
SYSTEM_PROMPT = """You review one answer from a question-answering system over US mine safety and health regulations (30 CFR).
You get the question, the answer with the claims it cites, and the chunks the system retrieved. Judge the answer only from those chunks; do not use what you already know about the regulations.

Score each dimension from 1 (very poor) to 5 (excellent):
- correctness: is the answer consistent with the chunks? 5 means nothing in it contradicts them, 1 means it says something the chunks do not say or contradict.
- groundedness: is every claim supported by the chunk it cites and by its quote? 5 means all are, 1 means most are not.
- completeness: does the answer include the important information the question needs, as far as the chunks allow? 5 means nothing important is missing.
- relevance: does the answer directly address the question that was asked? 5 means it does, 1 means it answers something else.

If the answer says it cannot be answered from the chunks, check whether that is true: if the chunks really lack the answer, the decline is correct and scores high; if the chunks do contain the answer, the decline is wrong and completeness and relevance score low.

In issues, name each problem in a short sentence and point at the claim or chunk it concerns. Leave it empty if you found none."""
USER_PROMPT = """Question: {question}

{answer}

Retrieved chunks:
{chunks}"""


def describe_answer(record: dict) -> str:
    """The answer, and the claims it cites, as text."""
    if record.get("not_found"):
        return f"Answer: (the system declined: it said the chunks do not answer the question)\n{record.get('answer', '').strip()}".rstrip()
    lines = [f"Answer: {record.get('answer', '').strip()}", "", "Claims it cites:"]
    claims = [c for c in record.get("claims") or [] if isinstance(c, dict)]
    for n, claim in enumerate(claims, 1):
        lines.append(f"{n}. {claim.get('text', '')}\n   cites {claim.get('chunk_id', '?')}, quote: \"{claim.get('quote', '')}\"")
    if not claims:
        lines.append("(none)")
    return "\n".join(lines)


def build_prompt(record: dict, texts: dict[str, str]) -> str:
    ids = [cid for cid in record.get("retrieved") or [] if cid in texts]
    return USER_PROMPT.format(
        question=record.get("question", ""), answer=describe_answer(record),
        chunks=answer.format_chunks([(cid, 0.0) for cid in ids], texts),
    )  # fmt: skip


def verdict(scores: dict[str, int]) -> str:
    """PASS when all four scores are 4 or 5, FAIL when any is 1 or 2, PARTIAL otherwise."""
    lowest = min(scores[d] for d in DIMENSIONS)
    if lowest >= 4:
        return "PASS"
    if lowest <= 2:
        return "FAIL"
    return "PARTIAL"


def review_one(record: dict, texts: dict[str, str], cfg) -> tuple[dict, bool]:
    """Review one question's answer; returns its review record and whether Claude's reply was a saved one."""
    out = {"qid": record["qid"], "kind": record.get("kind"), "scores": None, "verdict": None, "issues": "", "seconds": 0.0, "input_tokens": 0, "output_tokens": 0, "model": cfg.model}
    if record.get("error"):
        out["error"] = f"the answer itself failed ({record['error']}), so there is nothing to review"
        return out, False
    reply = claude.call(build_prompt(record, texts), SCHEMA, system=SYSTEM_PROMPT, model=cfg.model, cache_dir=claude.cache_folder(cfg))
    out.update(seconds=round(reply.seconds, 1), input_tokens=reply.input_tokens, output_tokens=reply.output_tokens, model=reply.model)
    scores = {d: (reply.output or {}).get(d) for d in DIMENSIONS}
    if reply.error or not all(isinstance(s, int) and 1 <= s <= 5 for s in scores.values()):
        out["error"] = reply.error or "the reply did not give four scores from 1 to 5"
        return out, reply.cached
    out.update(scores=scores, verdict=verdict(scores), issues=str((reply.output or {}).get("issues", "")).strip())
    return out, reply.cached


def short(text: str, width: int) -> str:
    text = " ".join(text.split())
    return text if len(text) <= width else text[: width - 3] + "..."


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Review each answer of an answers file with claude -p.")
    parser.add_argument("file", help="an answers file, such as answers/shared/rerank.json")
    parser.add_argument("--only", help="comma-separated question ids to review, such as a01,a09")
    parser.add_argument("--dry", action="store_true", help="print what Claude would be sent for the first question and call nothing")
    parser.add_argument("--yes", action="store_true", help="go ahead with more than 5 calls (say yes only after you have seen the number)")
    parser.add_argument("--fresh", action="store_true", help="ask Claude again instead of using saved replies")
    args = parser.parse_args(argv)

    path = Path(args.file)
    path = path if path.is_absolute() else ROOT / path
    try:
        data = verify.load_answers(path)
    except verify.AnswersError as error:
        print(f"{paths.rel(ROOT, path)} {error}.")
        return 1
    cfg = config.load(ROOT)
    if args.fresh:
        cfg = cfg.replace(cache_claude=False)
    records = data["answers"]
    if args.only:
        wanted = [q.strip() for q in args.only.split(",") if q.strip()]
        unknown = [q for q in wanted if q not in {r["qid"] for r in records}]
        if unknown:
            print(f"{', '.join(unknown)} is not a question in {paths.rel(ROOT, path)}.")
            return 2
        records = [r for r in records if r["qid"] in wanted]
    if not records:
        print("There is nothing to review.")
        return 1
    texts = verify.chunk_texts(data, ROOT, cfg)

    if args.dry:
        print(f"--- system prompt ---\n{SYSTEM_PROMPT}\n\n--- message for {records[0]['qid']} ---\n{build_prompt(records[0], texts)}")
        return 0

    cache = claude.cache_folder(cfg)
    reviewable = [r for r in records if not r.get("error")]
    saved = 0
    if cache is not None:
        saved = sum((cache / f"{claude.cache_key(build_prompt(r, texts), SCHEMA, cfg.model, SYSTEM_PROMPT)}.json").is_file() for r in reviewable)
    calls = len(reviewable) - saved
    if not claude.confirm_calls(calls, "This reviewer", args.yes):
        return 2
    note = f", and {saved} saved repl{'y' if saved == 1 else 'ies'} that cost nothing" if saved else ""
    print(f"{len(records)} answer(s) from {paths.rel(ROOT, path)}: {calls} new claude -p call(s) on {cfg.model}{note}.\n")

    reviews = []
    started = time.perf_counter()
    print(f"{'qid':<5}{'kind':<5}{'result':<9}{'corr':>5}{'grnd':>5}{'comp':>5}{'rel':>5}  issues")
    for record in records:
        review, _ = review_one(record, texts, cfg)
        reviews.append(review)
        if review.get("error"):
            print(f"{review['qid']:<5}{review['kind'] or '':<5}{'ERROR':<9}{'':>20}  {short(review['error'], 90)}")
            continue
        s = review["scores"]
        print(f"{review['qid']:<5}{review['kind'] or '':<5}{review['verdict']:<9}{s['correctness']:>5}{s['groundedness']:>5}{s['completeness']:>5}{s['relevance']:>5}  {short(review['issues'] or '-', 90)}")

    out = ROOT / "reviews" / data.get("corpus", path.parent.name) / f"{paths.answers_stem(path)}.review.json"
    result = {
        "label": paths.answers_stem(path), "answers_file": paths.rel(ROOT, path), "corpus": data.get("corpus", path.parent.name),
        "model": cfg.model, "rule": "PASS: all four scores 4-5; FAIL: any score 1-2; PARTIAL: otherwise",
        "only": [q.strip() for q in args.only.split(",") if q.strip()] if args.only else None, "reviews": reviews,
    }  # fmt: skip
    paths.write_text(out, json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    done = [r for r in reviews if r["verdict"]]
    counts = {v: sum(1 for r in done if r["verdict"] == v) for v in ("PASS", "PARTIAL", "FAIL")}
    tokens = sum(r["input_tokens"] for r in reviews)
    print(f"\nReviewed {len(done)} of {len(reviews)} answer(s): {counts['PASS']} PASS, {counts['PARTIAL']} PARTIAL, {counts['FAIL']} FAIL "
          f"({tokens:,} input tokens, {time.perf_counter() - started:.0f} s). Wrote {paths.rel(ROOT, out)}.")  # fmt: skip
    return 0 if len(done) == len(reviews) else 1


if __name__ == "__main__":
    sys.exit(main())
