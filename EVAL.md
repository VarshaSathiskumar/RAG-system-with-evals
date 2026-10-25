# Evaluation report

This is the report on what you built and what the numbers let you claim.
Two kinds of text live here.

The tables between a `p2:begin` comment line and its matching `p2:end` comment line are written by `uv run p2 score` from your committed run files and answers files.
Please do not edit anything between those two lines, because `uv run p2 check` recomputes them and fails when they differ.
A table that says no runs or answers exist yet is waiting for data; run `uv run p2 score` after you commit the files it needs.

Everything else is yours.
Each prompt ends with a marker line that you replace with your own writing; `uv run p2 check --final` fails while one is left.
Write what you measured, including what did not work.
What I read for is whether each claim matches its interval, not whether the result is good news.

Words used below: recall@10, MRR@10 and nDCG@10 are the three scores, each averaged over the queries of a set; step 7 of stage 1 in the README defines them, and lecture 14 goes deeper.
A paired interval is the 95% interval of the mean difference between two systems on the same queries, found by resampling the queries 10,000 times.
When an interval includes zero, the gold set cannot tell the two systems apart, and the right words are "not distinguishable on this gold set".
The minimum detectable difference is the smallest gap this many queries could reliably show, so a difference below it is invisible to this gold set, not absent.

---

## 1. Stage 1 - the shared corpus (30 CFR Chapter I)

### What you built

For each of `dense`, `hybrid` and `rerank`, one or two sentences: the embedding model, how documents were chunked, what was fused and how, how many candidates the reranker saw, and anything you changed from the 12 and 13 lab code.

##### 1.Dense Retrieval

- Compared OpenAI text-embedding-3-small and text-embedding-3-large on retrieval quality, storage, and embedding cost. Selected text-embedding-3-small because it achieved similar Recall and MRR while text-embedding-3-large cost ~6.5× more and produced ~2× larger vector files.
- Embeds 300-word chunks with 50-word overlap.
- Aggregates chunk similarity into document rankings using each document's best-scoring chunk.

##### 2.Hybrid Retrieval
- Combines BM25 and dense retrieval using Reciprocal Rank Fusion (RRF, `k=60`).
- Balances exact-term matching with semantic relevance.
- Changed from the lab: Fused the full rankings instead of only the top 10 results, while dropping zero-score BM25 results before fusion.
##### 3.Reranking
- The top 20 hybrid results are reranked by Claude in a single listwise call, using the first 300 words of each candidate and the results outside the top 20 keep their original order
- Uses structured output validation with fallback to the original ranking on failure.

##### 4.Reviewer

- It makes one claude -p call per answer. Each call receives the question, generated answer with its cited claims, and retrieved chunks, then scores correctness, groundedness, completeness, and relevance on a scale of 1 to 5. 
- The final verdict follows a fixed rule: PASS if all scores are at least 4, FAIL if any score is 2 or below, and PARTIAL otherwise.

### Practice queries (20)

Scores per system.

<!-- p2:begin shared-practice -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.625 | 0.507 | 0.518 |
| dense | 0.633 | 0.620 | 0.582 |
| hybrid | 0.592 | 0.511 | 0.487 |
| rerank | 0.800 | 0.800 | 0.785 |

20 judged queries; nDCG uses binary labels; a random ranking of the 2,484 documents would get recall@10 near 0.004.
<!-- p2:end shared-practice -->

The same scores per query class.

<!-- p2:begin shared-practice-classes -->
| System | Metric | identifier (n=7) | paraphrase (n=7) | mixed (n=6) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 1.000 | 0.000 | 0.917 |
| bm25 | MRR@10 | 0.810 | 0.000 | 0.746 |
| bm25 | nDCG@10 | 0.857 | 0.000 | 0.728 |
| dense | Recall@10 | 0.214 | 0.810 | 0.917 |
| dense | MRR@10 | 0.235 | 0.679 | 1.000 |
| dense | nDCG@10 | 0.180 | 0.691 | 0.922 |
| hybrid | Recall@10 | 0.429 | 0.405 | 1.000 |
| hybrid | MRR@10 | 0.449 | 0.250 | 0.889 |
| hybrid | nDCG@10 | 0.374 | 0.261 | 0.882 |
| rerank | Recall@10 | 0.857 | 0.571 | 1.000 |
| rerank | MRR@10 | 0.857 | 0.571 | 1.000 |
| rerank | nDCG@10 | 0.816 | 0.571 | 1.000 |
<!-- p2:end shared-practice-classes -->

Differences between every pair of systems, each with its paired interval and the minimum detectable difference.

<!-- p2:begin shared-practice-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | +0.008 | [-0.300, +0.325] | 0.459 | not distinguishable |
| dense minus bm25 | MRR@10 | +0.113 | [-0.172, +0.396] | 0.418 | not distinguishable |
| dense minus bm25 | nDCG@10 | +0.063 | [-0.224, +0.348] | 0.417 | not distinguishable |
| hybrid minus bm25 | Recall@10 | -0.033 | [-0.275, +0.208] | 0.355 | not distinguishable |
| hybrid minus bm25 | MRR@10 | +0.004 | [-0.185, +0.193] | 0.274 | not distinguishable |
| hybrid minus bm25 | nDCG@10 | -0.031 | [-0.224, +0.156] | 0.278 | not distinguishable |
| hybrid minus dense | Recall@10 | -0.042 | [-0.225, +0.125] | 0.253 | not distinguishable |
| hybrid minus dense | MRR@10 | -0.108 | [-0.300, +0.075] | 0.272 | not distinguishable |
| hybrid minus dense | nDCG@10 | -0.095 | [-0.274, +0.073] | 0.253 | not distinguishable |
| rerank minus bm25 | Recall@10 | +0.175 | [-0.025, +0.400] | 0.309 | not distinguishable |
| rerank minus bm25 | MRR@10 | +0.293 | [+0.100, +0.500] | 0.288 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.267 | [+0.075, +0.470] | 0.286 | rerank higher |
| rerank minus dense | Recall@10 | +0.167 | [-0.058, +0.375] | 0.318 | not distinguishable |
| rerank minus dense | MRR@10 | +0.180 | [-0.045, +0.404] | 0.326 | not distinguishable |
| rerank minus dense | nDCG@10 | +0.204 | [-0.016, +0.415] | 0.313 | not distinguishable |
| rerank minus hybrid | Recall@10 | +0.208 | [+0.075, +0.367] | 0.219 | rerank higher |
| rerank minus hybrid | MRR@10 | +0.289 | [+0.121, +0.468] | 0.257 | rerank higher |
| rerank minus hybrid | nDCG@10 | +0.298 | [+0.146, +0.462] | 0.236 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end shared-practice-pairs -->

The 40 test queries have no answer key in this repo.
Your test run files are scored by the course and the score comes back to you as feedback, so nothing goes here for them.

### What the intervals let you claim

Which differences are distinguishable from zero and which are not?
What is the minimum detectable difference at 20 queries, and what does that say about any gap smaller than it?
Which claim from lecture 12 or 13 did your numbers support, and which did they leave open?

The results show that reranking significantly outperforms hybrid retrieval across Recall@10, MRR@10, and nDCG@10, and also beats BM25 in MRR@10 and nDCG@10. All other comparisons are not statistically distinguishable from zero because their 95% intervals include zero. With only 20 queries, the minimum detectable difference ranges from 0.219 to 0.459, with most comparisons around 0.25 to 0.33. For example, dense retrieval’s average MRR@10 was 0.113 higher than BM25, but the difference was not statistically distinguishable from zero, and its MDD was 0.418. This doesn’t mean the systems perform equally.

The results are consistent with Lecture 12’s point that no retriever works best for every query type. In this sample, BM25 achieved 1.000 Recall@10 on identifier queries but 0.000 on paraphrases, while dense retrieval reached 0.810 on paraphrases. However, these patterns come from just 7 queries per class and have no confidence intervals, so they aren’t conclusive. The results also support Lecture 13’s emphasis on measuring each pipeline stage, since reranking significantly improved all three metrics over hybrid retrieval. Whether hybrid retrieval consistently outperforms BM25 or dense retrieval remains an open question.

---

## 2. Stage 1 - cited answers on the 12 shared questions

<!-- p2:begin answers -->
| Label | System | Verified (in) | 95% interval | not_found (in) | Declined (out) | 95% interval | Quotes found |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| rerank-nodecline | rerank | 8 of 8 (100%) | [0.676, 1.000] | 0 of 8 (0%) | 4 of 4 (100%) | [0.510, 1.000] | 15 of 15 |
| rerank | rerank | 8 of 8 (100%) | [0.676, 1.000] | 0 of 8 (0%) | 4 of 4 (100%) | [0.510, 1.000] | 12 of 12 |
<!-- p2:end answers -->

Which system answered, and why that one?
The rerank system correctly answered all 8 in-scope questions, verified all 12 supporting quotes, and declined all 4 out-of-scope questions. It reranks the top 20 hybrid-retrieved chunks using Claude Sonnet 5.5 to prioritize relevant evidence before passing the top 5 chunks for citation-grounded answer generation.
What did you change in `prompts/answer.txt`, if anything, and did the verified share or the declined share move?
I commented out the third line, but the results remained unchanged because the first line already restricts answers to the provided chunks, and the output schema includes a not_found field for unsupported questions.

Then read three in-corpus answers that `uv run p2 verify` passed.
For each one, open the cited chunk and say whether the quote really supports the claim next to it.
The check proves a quote is a real piece of the chunk and cannot prove that it supports the claim, so this reading is the part only you can do.

- a01 : Both quotes directly support their claims. The first quote establishes the 15-minute notification requirement, while the second identifies death at a mine as a covered accident. Although the second quote only includes option (a) and omits options (b), (c), and (d) from the full chunk, those additional accident categories are not relevant to the question. The evidence is sufficient to support the answer.

- a02 :  The quote directly supports the 80% minimum incombustible content requirement. The answer also correctly explains that the additional 0.4% increase applies only when methane is present. However, this statement is supported only by the full chunk and does not have a separate claim or supporting quote. So the answer is factually correct, but the evidence coverage is incomplete.

- a03 : The quote directly supports the claim that an approved self-rescue device must provide protection for 1 hour or longer. Although the quote omits the beginning of the sentence identifying the operator’s responsibility to provide the device, that information is present in the full chunk. The answer is correct and fully supported, with no evidence gap affecting the question asked.


---

## 3. Stage 2 - your corpus and your gold set

### The corpus

What is it, where did it come from, how many documents and how many megabytes, and what is the license basis for publishing it?
Name the one or two documents you were least sure about and what you decided.
Say which of the allowed sources in the brief it comes from.

My corpus contains 406 documents (3.6 MB, approximately 772,300 estimated tokens) covering U.S. immigration regulations, international student requirements, employment authorization, and taxation.The documents were collected from official U.S. federal government websites, primarily IRS (198), eCFR (140), Department of Labor (31), and USCIS (17), along with GovInfo (12) and additional sources from DHS, CBP, the Department of State, FinCEN, and ICE. 
All documents are classified as us-gov-public-domain. The license check returned zero flagged or failing documents.
I also ran audit.py script to detect potential third-party copyrighted content. Two documents, cfr8-214.2-h-p05-petition-for-alien-to.md and cfr8-245.10.md, initially raised concerns due to references to third-party work and licensing. These were confirmed as regulatory terminology rather than copyright issues. The improved audit returned zero findings, so no documents were removed.

### The gold set

How many queries, how many with origin `hand` and how many with origin `claude`, and which query classes did you use and why?
How did you decide that a document is relevant: write your relevance rule in two or three sentences, the way the brief does for the shared corpus.
How did you find candidates (the systems' top 10, a keyword search, reading), and did you read every document before you labeled it?
Your labels are binary (`rel` 1) unless you say otherwise: if you use graded labels, declare the scale here, for example 2 means the document answers the query fully and 1 means it helps.

The gold set contains 34 queries: 14 hand-written and 20 Claude-generated. Queries span five classes: Scenario (12), Direct (7), Semantic (7), Exact-match (5), and Multi-document (3). These classes test real-world scenerios, straightforward factual retrieval, paraphrased questions, exact terminologies, and questions requiring evidence from multiple documents. A document is relevant (rel = 1) if it directly answers the query. Other irrelavent topic mentions, cross-references, or rules applying only to other visa categories are irrelevant (rel = 0). For each query, I collected candidate documents using Claude (top 5), BM25 keyword search (top 10), and dense retrieval (top 10). I merged and deduplicated the results, then manually reviewed the candidates and assigned binary relevance labels. I also removed duplicate queries to maintain topic diversity. I did not review all 406 documents, so some relevant documents may remain unidentified.


---

## 4. Stage 2 - results on your corpus

Scores per system on your gold set.

<!-- p2:begin own -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.833 | 0.555 | 0.599 |
| dense | 0.775 | 0.641 | 0.639 |
| hybrid | 0.858 | 0.623 | 0.660 |
| rerank | 0.902 | 0.763 | 0.780 |
| ablation/rerank_prompt | 0.892 | 0.740 | 0.761 |

34 judged queries; nDCG uses binary labels; a random ranking of the 406 documents would get recall@10 near 0.025.
<!-- p2:end own -->

The same scores per query class.

<!-- p2:begin own-classes -->
| System | Metric | Direct (n=7) | Scenario (n=12) | Semantic (n=7) | Multi-document (n=3) | Exact-match (n=5) |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| bm25 | Recall@10 | 0.929 | 0.833 | 0.833 | 0.556 | 0.867 |
| bm25 | MRR@10 | 0.523 | 0.592 | 0.544 | 0.500 | 0.562 |
| bm25 | nDCG@10 | 0.616 | 0.622 | 0.583 | 0.445 | 0.631 |
| dense | Recall@10 | 0.786 | 0.792 | 0.762 | 0.667 | 0.800 |
| dense | MRR@10 | 0.661 | 0.591 | 0.679 | 0.778 | 0.600 |
| dense | nDCG@10 | 0.672 | 0.612 | 0.673 | 0.602 | 0.636 |
| hybrid | Recall@10 | 0.786 | 1.000 | 0.762 | 0.778 | 0.800 |
| hybrid | MRR@10 | 0.679 | 0.652 | 0.565 | 0.548 | 0.600 |
| hybrid | nDCG@10 | 0.688 | 0.711 | 0.611 | 0.515 | 0.652 |
| rerank | Recall@10 | 0.929 | 0.917 | 0.929 | 0.889 | 0.800 |
| rerank | MRR@10 | 0.821 | 0.792 | 0.643 | 1.000 | 0.640 |
| rerank | nDCG@10 | 0.811 | 0.821 | 0.721 | 0.889 | 0.653 |
| ablation/rerank_prompt | Recall@10 | 0.929 | 0.917 | 0.881 | 0.889 | 0.800 |
| ablation/rerank_prompt | MRR@10 | 0.833 | 0.764 | 0.636 | 1.000 | 0.540 |
| ablation/rerank_prompt | nDCG@10 | 0.821 | 0.805 | 0.698 | 0.896 | 0.579 |
<!-- p2:end own-classes -->

The same scores for the queries you wrote yourself (`hand`) and the ones a model drafted (`claude`), with the difference between the two groups and its interval.
Once both groups have queries, the table also says whether `bm25`'s lead over `dense` differs between them, and what share of each query's content words its best relevant document contains, which is stretch option 6.

<!-- p2:begin own-origins -->
| System | Metric | hand (n=14) | claude (n=20) | hand minus claude | 95% interval | Reading |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| bm25 | Recall@10 | 1.000 | 0.717 | +0.283 | [+0.125, +0.467] | hand higher |
| bm25 | MRR@10 | 0.510 | 0.587 | -0.077 | [-0.330, +0.177] | not distinguishable |
| bm25 | nDCG@10 | 0.632 | 0.575 | +0.058 | [-0.157, +0.272] | not distinguishable |
| dense | Recall@10 | 0.833 | 0.733 | +0.100 | [-0.156, +0.342] | not distinguishable |
| dense | MRR@10 | 0.722 | 0.584 | +0.138 | [-0.145, +0.403] | not distinguishable |
| dense | nDCG@10 | 0.738 | 0.571 | +0.167 | [-0.090, +0.405] | not distinguishable |
| hybrid | Recall@10 | 0.929 | 0.808 | +0.120 | [-0.089, +0.320] | not distinguishable |
| hybrid | MRR@10 | 0.654 | 0.601 | +0.053 | [-0.221, +0.311] | not distinguishable |
| hybrid | nDCG@10 | 0.725 | 0.614 | +0.111 | [-0.121, +0.331] | not distinguishable |
| rerank | Recall@10 | 1.000 | 0.833 | +0.167 | [+0.042, +0.325] | hand higher |
| rerank | MRR@10 | 0.839 | 0.710 | +0.129 | [-0.084, +0.344] | not distinguishable |
| rerank | nDCG@10 | 0.873 | 0.714 | +0.159 | [-0.012, +0.337] | not distinguishable |
| ablation/rerank_prompt | Recall@10 | 1.000 | 0.817 | +0.183 | [+0.058, +0.342] | hand higher |
| ablation/rerank_prompt | MRR@10 | 0.798 | 0.699 | +0.098 | [-0.120, +0.323] | not distinguishable |
| ablation/rerank_prompt | nDCG@10 | 0.844 | 0.703 | +0.141 | [-0.039, +0.327] | not distinguishable |

The hand and claude queries are different queries, so the interval of hand minus claude comes from resampling the queries within each group (10,000 times), not from pairing them.

Do model-written queries favor keyword search? bm25's lead over dense (bm25 minus dense, per query) on the claude queries and on the hand queries, and claude minus hand:

| Metric | Lead on claude | Lead on hand | Claude minus hand | 95% interval | Reading |
| --- | ---: | ---: | ---: | ---: | --- |
| Recall@10 | -0.017 | +0.167 | -0.183 | [-0.443, +0.044] | not distinguishable |
| MRR@10 | +0.003 | -0.212 | +0.215 | [-0.020, +0.449] | not distinguishable |
| nDCG@10 | +0.004 | -0.105 | +0.109 | [-0.099, +0.320] | not distinguishable |

Mean content-word overlap, the share of a query's content words found in its best relevant document: hand 0.65 (14 queries), claude 0.67 (20 queries).

Stretch option 6 asks for at least 20 judged queries of each origin; here there are 14 hand and 20 claude.
<!-- p2:end own-origins -->

Differences between every pair of systems.

<!-- p2:begin own-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | -0.059 | [-0.181, +0.069] | 0.182 | not distinguishable |
| dense minus bm25 | MRR@10 | +0.086 | [-0.025, +0.197] | 0.162 | not distinguishable |
| dense minus bm25 | nDCG@10 | +0.041 | [-0.058, +0.139] | 0.145 | not distinguishable |
| hybrid minus bm25 | Recall@10 | +0.025 | [-0.093, +0.152] | 0.176 | not distinguishable |
| hybrid minus bm25 | MRR@10 | +0.068 | [+0.006, +0.137] | 0.095 | hybrid higher |
| hybrid minus bm25 | nDCG@10 | +0.061 | [-0.0003, +0.126] | 0.091 | not distinguishable |
| hybrid minus dense | Recall@10 | +0.083 | [+0.010, +0.176] | 0.122 | hybrid higher |
| hybrid minus dense | MRR@10 | -0.018 | [-0.096, +0.060] | 0.113 | not distinguishable |
| hybrid minus dense | nDCG@10 | +0.021 | [-0.042, +0.086] | 0.092 | not distinguishable |
| rerank minus bm25 | Recall@10 | +0.069 | [-0.010, +0.167] | 0.129 | not distinguishable |
| rerank minus bm25 | MRR@10 | +0.208 | [+0.066, +0.350] | 0.207 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.181 | [+0.071, +0.292] | 0.161 | rerank higher |
| rerank minus dense | Recall@10 | +0.127 | [+0.005, +0.255] | 0.180 | rerank higher |
| rerank minus dense | MRR@10 | +0.122 | [-0.028, +0.276] | 0.221 | not distinguishable |
| rerank minus dense | nDCG@10 | +0.140 | [+0.009, +0.272] | 0.194 | rerank higher |
| rerank minus hybrid | Recall@10 | +0.044 | [-0.049, +0.142] | 0.138 | not distinguishable |
| rerank minus hybrid | MRR@10 | +0.140 | [+0.009, +0.275] | 0.194 | rerank higher |
| rerank minus hybrid | nDCG@10 | +0.120 | [+0.010, +0.230] | 0.161 | rerank higher |
| ablation/rerank_prompt minus bm25 | Recall@10 | +0.059 | [-0.010, +0.147] | 0.121 | not distinguishable |
| ablation/rerank_prompt minus bm25 | MRR@10 | +0.184 | [+0.041, +0.326] | 0.209 | ablation/rerank_prompt higher |
| ablation/rerank_prompt minus bm25 | nDCG@10 | +0.162 | [+0.053, +0.274] | 0.161 | ablation/rerank_prompt higher |
| ablation/rerank_prompt minus dense | Recall@10 | +0.118 | [+0.000, +0.240] | 0.175 | not distinguishable |
| ablation/rerank_prompt minus dense | MRR@10 | +0.099 | [-0.053, +0.255] | 0.224 | not distinguishable |
| ablation/rerank_prompt minus dense | nDCG@10 | +0.121 | [-0.010, +0.257] | 0.195 | not distinguishable |
| ablation/rerank_prompt minus hybrid | Recall@10 | +0.034 | [-0.059, +0.127] | 0.130 | not distinguishable |
| ablation/rerank_prompt minus hybrid | MRR@10 | +0.117 | [-0.017, +0.254] | 0.198 | not distinguishable |
| ablation/rerank_prompt minus hybrid | nDCG@10 | +0.101 | [-0.009, +0.212] | 0.161 | not distinguishable |
| ablation/rerank_prompt minus rerank | Recall@10 | -0.010 | [-0.029, +0.000] | 0.027 | not distinguishable |
| ablation/rerank_prompt minus rerank | MRR@10 | -0.024 | [-0.060, +0.001] | 0.046 | not distinguishable |
| ablation/rerank_prompt minus rerank | nDCG@10 | -0.019 | [-0.046, +0.001] | 0.034 | not distinguishable |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end own-pairs -->

Which differences are distinguishable and which are not, at your gold-set size?


On my 34-query gold set, reranking achieved the highest scores (Recall@10: 0.902, MRR@10: 0.763, NDCG@10: 0.780). Paired 95% confidence intervals showed distinguishable improvements over BM25 in MRR and NDCG, over dense retrieval in Recall and NDCG, and over hybrid retrieval in MRR and NDCG. Hybrid also outperformed BM25 in MRR and dense retrieval in Recall. All other differences were not distinguishable at this sample size.


Do the `hand` queries and the `claude` queries tell the same story?
Mostly yes. Reranking performed best overall on both groups, although not on every metric. Hand-written queries generally had higher scores than Claude-generated queries. The difference in Recall@10 was statistically distinguishable for BM25 and reranking, but not for dense or hybrid retrieval. There was also no clear evidence that Claude-generated queries favored keyword search over dense retrieval.


Did your prediction in `DECISIONS.md` prompt 1 hold?

My prediction was correct. Reranking performed best overall, with the highest Recall@10 (0.902), MRR@10 (0.763), and NDCG@10 (0.780). However, not all improvements were statistically distinguishable. The results show stronger evidence that reranking helps rank relevant documents higher than that it consistently retrieves more relevant documents.

---

## 5. The ablation

Change one thing and keep everything else the same.
Write your hypothesis here before you run it, in one sentence with a direction: "I expect X to raise MRR@10 on my corpus because Y."
The run file for it lives in `runs/own/ablation/`.

<!-- p2:begin own-ablation -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| ablation/rerank_prompt minus bm25 | Recall@10 | +0.059 | [-0.010, +0.147] | 0.121 | not distinguishable |
| ablation/rerank_prompt minus bm25 | MRR@10 | +0.184 | [+0.041, +0.326] | 0.209 | ablation/rerank_prompt higher |
| ablation/rerank_prompt minus bm25 | nDCG@10 | +0.162 | [+0.053, +0.274] | 0.161 | ablation/rerank_prompt higher |
| ablation/rerank_prompt minus dense | Recall@10 | +0.118 | [+0.000, +0.240] | 0.175 | not distinguishable |
| ablation/rerank_prompt minus dense | MRR@10 | +0.099 | [-0.053, +0.255] | 0.224 | not distinguishable |
| ablation/rerank_prompt minus dense | nDCG@10 | +0.121 | [-0.010, +0.257] | 0.195 | not distinguishable |
| ablation/rerank_prompt minus hybrid | Recall@10 | +0.034 | [-0.059, +0.127] | 0.130 | not distinguishable |
| ablation/rerank_prompt minus hybrid | MRR@10 | +0.117 | [-0.017, +0.254] | 0.198 | not distinguishable |
| ablation/rerank_prompt minus hybrid | nDCG@10 | +0.101 | [-0.009, +0.212] | 0.161 | not distinguishable |
| ablation/rerank_prompt minus rerank | Recall@10 | -0.010 | [-0.029, +0.000] | 0.027 | not distinguishable |
| ablation/rerank_prompt minus rerank | MRR@10 | -0.024 | [-0.060, +0.001] | 0.046 | not distinguishable |
| ablation/rerank_prompt minus rerank | nDCG@10 | -0.019 | [-0.046, +0.001] | 0.034 | not distinguishable |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end own-ablation -->

The queries your ablation helped and hurt, against the system it varies, by reciprocal rank.
`p2 score` finds that system from a line such as `BASE = "bm25"` in your variant's file, or else from its name: `bm25_lab` varies `bm25`.

<!-- p2:begin own-ablation-queries -->
ablation/rerank_prompt against rerank (BASE = "rerank" in p2/retrievers/rerank_prompt.py): it helped 1 queries, hurt 4 and left 29 unchanged.

| Query | Class | Origin | rerank RR | ablation/rerank_prompt RR | Change | Effect |
| --- | --- | --- | ---: | ---: | ---: | --- |
| q01 | Direct | hand | 0.250 | 0.333 | +0.083 | helped |
| q16 | Exact-match | hand | 1.000 | 0.500 | -0.500 | hurt |
| q13 | Scenario | hand | 0.500 | 0.333 | -0.167 | hurt |
| q19 | Scenario | claude | 0.500 | 0.333 | -0.167 | hurt |
| q25 | Semantic | claude | 0.250 | 0.200 | -0.050 | hurt |

RR is the reciprocal rank of the first relevant document in the top 10 (0 when none is there), the per-query value behind MRR@10; the queries at the top of each list are the ones to read.
<!-- p2:end own-ablation-queries -->

What did you change, what happened, and does the interval support the claim you want to make?
If the result is not distinguishable, say what size of effect your gold set could have seen.
Read the queries at the top of each list in the second table, and say whether your change explains them.



Hypothesis: I expect changing the reranker prompt from mine safety regulations to immigration regulations will improve nDCG@10 because Claude will have the correct context to rank relevant documents higher.

Result: I changed only the domain description in the reranker prompt. Contrary to my prediction, nDCG@10 decreased from 0.780 to 0.761. However, the 95% confidence interval [-0.046, +0.001] includes zero, so the difference was not statistically distinguishable. With 34 queries, the minimum detectable difference was 0.034.

Only 5 of 34 queries changed. The updated prompt improved q01 by moving the relevant OPT document from rank 4 to 3, but lowered relevant documents for q13, q16, q19, and q25. The largest drop was q16, where the relevant USCIS STEM OPT document moved from rank 1 to 2 for a question about Form I-983. The prompt change may have influenced how Claude prioritized broader regulations over specific guidance, but the rankings alone cannot confirm this.

Overall, my hypothesis was not supported. Correcting the domain description did not produce a statistically distinguishable improvement, suggesting that the original prompt mismatch had limited measurable impact on this gold set.
---

## 6. Failure analysis

Pick the queries where your best system on your own corpus failed: the relevant document is missing from the top 10, or sits far below the top.
Take at least five, and read what the system returned next to what was relevant.
Then sort the failures by cause, for example a vocabulary mismatch, near-duplicate documents, a chunk that cut the answer in half, a query that is ambiguous, or a label that was wrong, because sometimes the gold set is what failed.

| qid | what the best system returned | what was relevant | cause | what you would try |
|---|---|---|---|---|
| q24 | `irs-exempt-individuals-teachers-and-trainees.md`, `irs-pub-519-p04-days-of-presence-in.md`, `irs-instr-1040nr-p04-filing-requirements-through-do.md`, `irs-pub-519-p47-i-am-a-student.md`, `irs-pub-519-p46-what-is-the-difference.md` | `irs-exempt-individual-who-is-a-student.md`, `irs-substantial-presence-test.md`, `irs-instr-1040nr-p06-additional-information-through.md` | Overlapping documents and incomplete relevance labels. Some returned documents also answered the question but weren't labeled relevant. | Review the returned documents and add missing relevance labels where appropriate. |
| q20 | `cfr8-214.2-f-p04-extension-of-stay-through.md`, `sevp-maintaining-status.md`, `sevp-transferring-schools.md`, `cfr8-214.2-f-p03-full-course-of-study.md`, `cfr8-214.2-f-p02-period-of-stay.md` | `cfr8-214.2-f-p09-temporary-absence-from-the.md` | Relevant information was buried in a long document. The reranker only saw the first 300 words, missing the reinstatement paragraph and five-month rule. | Use chunk-level reranking so the model can evaluate the relevant passage instead of truncated document text. |
| q34 | `uscis-opt-f1.md`, `cfr8-214.2-f-p07-general-through-24-month.md`, `uscis-stem-opt.md`, `cfr8-214.2-f-p08-extension-of-stay-for.md`, `cfr8-214.2-f-p02-period-of-stay.md` | `uscis-opt-f1.md`, `cfr8-214.2-f-p06-practical-training-through-cur.md` | Ambiguous query and possible over-labeling. "The most OPT I can get" could refer to the standard 12 months, the STEM extension, or additional OPT at a higher degree level. The top-ranked USCIS document answers the pre-completion deduction question, while the missing CFR document provides only partial supporting information. | Clarify which OPT duration the query asks about and review whether the CFR document should be labeled relevant. |
| q01 | `uscis-i-765-p02-form-details.md`, `cfr8-214.2-f-p08-extension-of-stay-for.md`, `cfr8-214.2-f-p07-general-through-24-month.md`, `uscis-opt-f1.md`, `cfr8-214.2-f-p02-period-of-stay.md` | `uscis-opt-f1.md` | Possible document truncation during reranking. The reranker only sees the first 300 words, so it may miss the filing deadlines in the relevant document. Other documents also contain overlapping information. | Use section-based chunk reranking to capture the relevant filing deadlines and review relevance labels for overlapping documents. |
 q23 | `irs-obtaining-an-itin-from-abroad.md`, `irs-taxpayer-identification-numbers-tins-for-foreign-students-and-scholars.md`, `irs-itin-documentation-frequently-asked-questions-faqs.md`, `irs-instr-w7-p04-additional-documentation-requi.md`, `irs-instr-w7-p03-who-is-eligible-to.md` | `irs-instr-w7-p03-who-is-eligible-to.md` | Reranking favored shorter, overlapping ITIN guidance over the document containing the complete list of acceptable identity documents. The relevant document dropped from rank 2 in hybrid to rank 5. | Rerank using complete relevant passages and prioritize documents that answer both parts of the query. |

---

## 7. Cross-corpus comparison

The two tables to compare are the shared-corpus scores in section 1 and your own-corpus scores in section 4, with their intervals.
If you want them side by side, copy the rows you need into a table here and say that you copied them.

These rows are copied from sections 1 (shared practice, 20 queries, 2,484 documents) and 4 (own corpus, 34 queries, 406 documents); they are not recomputed.

| System | Shared Recall@10 | Shared MRR@10 | Shared nDCG@10 | Own Recall@10 | Own MRR@10 | Own nDCG@10 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| bm25 | 0.625 | 0.507 | 0.518 | 0.833 | 0.555 | 0.599 |
| dense | 0.633 | 0.620 | 0.582 | 0.775 | 0.641 | 0.639 |
| hybrid | 0.592 | 0.511 | 0.487 | 0.858 | 0.623 | 0.660 |
| rerank | 0.800 | 0.800 | 0.785 | 0.902 | 0.763 | 0.780 |

The paired differences for nDCG@10, also copied (95% paired bootstrap interval, then the minimum detectable difference):

| Comparison | Shared (n=20) | Shared MDD | Own (n=34) | Own MDD |
| --- | ---: | ---: | ---: | ---: |
| rerank minus bm25 | +0.267 [+0.075, +0.470] | 0.286 | +0.181 [+0.071, +0.292] | 0.161 |
| rerank minus dense | +0.204 [-0.016, +0.415] | 0.313 | +0.140 [+0.009, +0.272] | 0.194 |
| rerank minus hybrid | +0.298 [+0.146, +0.462] | 0.236 | +0.120 [+0.010, +0.230] | 0.161 |
| dense minus bm25 | +0.063 [-0.224, +0.348] | 0.417 | +0.041 [-0.058, +0.139] | 0.145 |
| hybrid minus bm25 | -0.031 [-0.224, +0.156] | 0.278 | +0.061 [-0.0003, +0.126] | 0.091 |
| hybrid minus dense | -0.095 [-0.274, +0.073] | 0.253 | +0.021 [-0.042, +0.086] | 0.092 |

Document lengths, computed (not copied) as whitespace-separated words per file in `corpora/<name>/docs/`, the same count `rerank.py` uses for its 300-word window:

| | Shared (30 CFR) | Own |
| --- | ---: | ---: |
| Documents | 2,484 | 406 |
| Median words per document | 68 | 1,303 |
| Mean words per document | 158 | 1,359 |
| 25th to 75th percentile | 36 to 166 | 782 to 1,518 |
| 90th percentile | 379 | 2,059 |
| Longest | 3,583 | 6,802 |
| Documents over 300 words | 335 (13.5%) | 390 (96.1%) |
| Documents over 600 words | 128 (5.2%) | 332 (81.8%) |
| Share of all words inside the first 300 words | 71.0% | 21.8% |

Did the winner change between the shared corpus and yours?
Why, or why not: what is different about the two collections (document length, vocabulary, identifiers, near-duplicates, how the queries were written), and which of your explanations did you test and which are guesses?
Say what 20 queries on one side and your gold-set size on the other cannot support.

Reranking achieved the highest nDCG@10 on both corpora (0.785 shared, 0.780 own). Dense ranked second on shared, while hybrid ranked second on mine, but the differences among BM25, dense, and hybrid were not statistically distinguishable. Reranking outperformed BM25 and hybrid on both corpora. Its improvement over dense was distinguishable only on mine (+0.140, 95% CI [+0.009, +0.272]).

The corpora differ considerably in document length and query types. Shared documents have a median of 68 words, compared to 1,303 on mine. The reranker’s 300-word window covers 71% of shared text but only 21.8% of mine. Despite this limitation, reranking still performed best. My failure analysis identified cases where relevant passages fell outside this window. On shared queries, BM25 achieved 1.000 Recall@10 on identifiers but 0.000 on paraphrases, where dense reached 0.810.

I measured document lengths and compared retrieval performance across query classes and query origins. On my corpus, BM25 achieved 1.000 Recall@10 on 14 hand-written queries versus 0.717 on 20 Claude-generated queries, suggesting that query construction may influence retrieval results. I also observed overlapping documents and ambiguous relevance labels. However, I did not test whether truncation, vocabulary differences, identifiers, or near-duplicates caused the ranking changes. The smaller reranking gain over hybrid on mine (+0.120 versus +0.298) could reflect these differences, but the cause remains uncertain.

Finally, 20 shared practice queries and 34 own queries are insufficient for broad generalization. Shared nDCG@10 MDDs range from 0.236 to 0.417, and some query classes contain only 3–7 examples. These results cannot establish which system generalizes better or whether one corpus is easier.


---

## 8. Stretch

498E: the stretch is one of the six options in the brief's "One stretch" section, and that section says what earns the 25 points for each.
It is optional, so `uv run p2 check --final` never waits on this section.
598E: the rider is your stretch, so write "rider" below and put its results in section 9; the other options add no points, because the project is capped at 150.

Whichever option you chose, write these five things:

1. The option's name.
2. What you did, and the files that hold it.
3. The table `p2 score` wrote for it, by name: one of the three below, `own-ablation` and `own-ablation-queries` in section 5 for a second ablation, `own-origins` in section 4 for the hand and claude queries, or `repeats` in section 9 for the rider.
4. What its interval lets you claim, and what it does not.
5. One thing you would do next, and what result would tell you it worked.

For a second ablation, write its hypothesis here before you run it, and commit it, so your history shows that it came first.
For the hand and claude queries, do the same with your prediction before you score.

### Claim-level faithfulness check (option 2)

Claude's verdicts from `p2 judge` against your own verdicts in the calibration file.

<!-- p2:begin stretch-judge -->
_No judged answers yet (stretch option 2): `uv run p2 judge answers/shared/LABEL.json` writes them, your own verdicts go in answers/shared/LABEL.calibration.tsv, and then `uv run p2 score` fills this table._
<!-- p2:end stretch-judge -->

### Cost and latency (option 3)

The Claude calls, tokens and seconds in every trace you committed, and what a cheaper system or answers file saves against what it loses.

<!-- p2:begin stretch-cost -->
Every trace in traces/ that records a Claude call:

| Trace | System | Spans | Claude calls | Saved | Input tokens | Output tokens | Seconds | Input per span | Output per span | Seconds per span |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| traces/answers-rerank-nodecline.jsonl | rerank | 12 | 24 | 14 | 226,039 | 4,940 | 95.9 | 18,837 | 412 | 8.0 |
| traces/answers-rerank.jsonl | rerank | 12 | 24 | 4 | 236,381 | 4,215 | 109.9 | 19,698 | 351 | 9.2 |
| traces/own-own-ablation-rerank_prompt.jsonl | rerank_prompt | 34 | 34 | 2 | 542,696 | 3,151 | 112.7 | 15,962 | 93 | 3.3 |
| traces/own-own-rerank.jsonl | rerank | 34 | 34 | 2 | 539,299 | 3,432 | 101.8 | 15,862 | 101 | 3.0 |
| traces/shared-practice-rerank.jsonl | rerank | 20 | 20 | 20 | 251,587 | 1,820 | 71.9 | 12,579 | 91 | 3.6 |
| traces/shared-test-rerank.jsonl | rerank | 40 | 40 | 40 | 468,534 | 4,120 | 148.4 | 11,713 | 103 | 3.7 |

A span is one query of a run, one question of an answers file, or one claim of a judged file. A saved reply costs nothing now, so it counts the tokens and the seconds of the call that made it.

Every pair of systems on the same queries where at least one calls Claude, the one with fewer Claude input tokens per query first:

| Cheaper minus dearer | Queries | MRR@10 difference | 95% interval | Input tokens saved per query | Seconds saved per query | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| shared practice: bm25 minus rerank | 20 | -0.293 | [-0.500, -0.100] | 12,579 | 3.6 | rerank higher |
| shared practice: dense minus rerank | 20 | -0.180 | [-0.404, +0.045] | 12,579 | 3.6 | not distinguishable |
| shared practice: hybrid minus rerank | 20 | -0.289 | [-0.468, -0.121] | 12,579 | 3.6 | rerank higher |
| own: bm25 minus rerank | 34 | -0.208 | [-0.350, -0.066] | 15,862 | 3.0 | rerank higher |
| own: dense minus rerank | 34 | -0.122 | [-0.276, +0.028] | 15,862 | 3.0 | not distinguishable |
| own: hybrid minus rerank | 34 | -0.140 | [-0.275, -0.009] | 15,862 | 3.0 | rerank higher |

The difference is the cheaper system's score minus the dearer one's, with its paired interval; the savings count Claude calls only, so a system that makes none saves all of the other's.

Every two answers files on the same questions, the one with fewer input tokens per question first:

| Cheaper minus dearer | Questions | Passing share difference | 95% interval | Input tokens saved per question | Seconds saved per question | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| shared: rerank-nodecline minus rerank | 12 | +0.000 | [+0.000, +0.000] | 862 | 1.2 | not distinguishable |

A question passes when its `p2 verify` line is a PASS: every quote is in a chunk that was retrieved, and the question is declined exactly when it should be.

Systems that do not call Claude, from traces/retrieval/ on the machine that last ran `p2 score` (git ignores that folder, so `p2 check` does not compare this part):

| Trace | System | Queries | Seconds | Milliseconds per query |
| --- | --- | ---: | ---: | ---: |
| traces/retrieval/own-own-bm25.jsonl | bm25 | 34 | 0.04 | 1.2 |
| traces/retrieval/own-own-dense.jsonl | dense | 34 | 0.04 | 1.1 |
| traces/retrieval/own-own-hybrid.jsonl | hybrid | 34 | 0.08 | 2.5 |
| traces/retrieval/shared-practice-bm25.jsonl | bm25 | 20 | 0.03 | 1.4 |
| traces/retrieval/shared-practice-dense.jsonl | dense | 20 | 0.04 | 2.0 |
| traces/retrieval/shared-practice-hybrid.jsonl | hybrid | 20 | 0.09 | 4.6 |
| traces/retrieval/shared-test-bm25.jsonl | bm25 | 40 | 0.06 | 1.4 |
| traces/retrieval/shared-test-dense.jsonl | dense | 40 | 0.08 | 2.0 |
| traces/retrieval/shared-test-hybrid.jsonl | hybrid | 40 | 0.19 | 4.7 |
<!-- p2:end stretch-cost -->

### The grep agent (option 5)

Your stretch run on some of your own queries against the four systems on the same queries.

<!-- p2:begin stretch-agent -->
_No stretch runs yet (stretch option 5): `uv run p2 run --corpus own --queries eval/own/agent.queries.tsv --system agent --stretch` writes one to runs/own/stretch/, then `uv run p2 score` fills this table._
<!-- p2:end stretch-agent -->

### Your stretch

Write the five things here.

---

## 9. 598E only - repeats and the pre-registered claim

498E students can leave this section as it is; nothing checks it.
598E students replace each line that starts with "598E: write", and `uv run p2 check --final` counts those lines as work still to do until they are gone.

### Repeats on the shared corpus

Three runs of the reranker on the practice queries, and three answers files, with their run-to-run spread and Wilson intervals.

<!-- p2:begin repeats -->
_No repeated runs or answers files yet (598E: `p2 run ... --repeat 3` and `p2 answer ... --repeat 3`)._
<!-- p2:end repeats -->

Does the reranker's gain over its first stage survive the run-to-run variation?
Write what the spread is, how it compares with the gain, and what the Wilson intervals on the verified share and the declined share say about 8 and 4 questions.

598E: write the repeats result here.

### The pre-registered claim

The claim, the smallest effect, the gold-set size and the test are in `PREREG.md`, committed before your own gold-set judgments.
Here, say whether you followed the plan, what the interval turned out to be, and what that means.
The outcome section of `PREREG.md` holds the short version.

598E: write the claim and its outcome here.
