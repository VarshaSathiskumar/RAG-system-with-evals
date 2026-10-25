# Decision log

Your methods section, in your own words.
About one to two pages in total.

Answer these as you go, not the night before it is due.
Each answer is easier to write while the decision is still fresh, and prompt 1 only works if you write it before you see your own-corpus numbers.
Specifics beat polish: a short, honest answer with a number in it is worth more than a long vague one.

Each prompt ends with a marker line.
Replace that line with your answer.
`uv run p2 check` reports a marker as unfinished work, and `uv run p2 check --final` fails while any marker is left, so a finished log is part of being done.

Please do not let the agent write these for you.
These answers are about what you chose and what you knew, and the agent cannot know that.
Prompt 3 in particular only works in your own words.

---

## 1. Why this corpus, and what you expected

Why did you pick the corpus you used in stage 2, and why does it belong to a field or a question you care about?
Then say what you expected before you measured anything: which of `bm25`, `dense`, `hybrid` and `rerank` do you think will win on it, and which will do worst, and why?

Commit this answer before your first `uv run p2 score` on the own corpus.
Git history then shows that the expectation came first, which is what lets it be wrong in a way that teaches you something.
If you were surprised later, say so in prompt 4 or in EVAL.md; do not come back and rewrite this one.

I chose a corpus focused on U.S. immigration, work authorization, and tax regulations. As an international student, I often find it difficult to get reliable information because it is scattered across multiple government websites. I end up switching between several tabs to find answers, and with immigration policies and regulations frequently changing, keeping track of the latest information becomes even harder. I wanted to build a retrieval system that could bring these official sources together and help users find accurate, relevant information without searching through multiple websites.

Before measuring anything, I expect rerank to perform best because it evaluates retrieved passages based on how well they answer the question. I expected hybrid to come next, combining BM25’s exact keyword matching with dense retrieval’s semantic understanding. I expected dense to perform better than bm25 on conversational questions, while bm25 would perform worst because users may not know the exact legal terminology used in government documents.

---

## 2. A fork in the road

Name one real design choice where you could have gone two ways: the chunk size, the embedding model, how the two systems are fused, how many documents the reranker sees, a sentence in `prompts/answer.txt`, how you cleaned the corpus.

Say which you picked, what the alternative was, and what you gave up by not taking it.
If you measured both, give both numbers.
If you rejected the alternative without measuring it, say why that was a fair call, and what it cost you in time, tokens or complexity.

"There was no alternative" is not an answer.
Find the fork.

I chose to use the first 300 words of each document for document-level reranking instead of reranking individual chunks. My system already supports chunk-level reranking for answer generation, but I kept document-level retrieval simpler by using a fixed 300-word window.

The tradeoff was missing relevant information buried deeper in long documents. On my corpus, the window covered only 21.8% of the text. My failure analysis identified this issue in q01 and q20, where relevant information appeared beyond the reranker’s input window.

I didn’t compare both approaches for document-level retrieval because chunk-level reranking would require an extra step to combine chunk rankings into document rankings. Multiple chunks from the same document could also occupy the top 20 slots, reducing document diversity. The existing reranker used approximately 15,862 Claude input tokens and 3.0 seconds per query. I kept the simpler approach to finish the evaluation, but I still don’t know whether chunk-level reranking would improve the results.

---

## 3. Where you overruled the agent

One time Claude suggested, wrote or claimed something and you did not take it.
It might be a relevance judgment you disagreed with, a retriever it called finished when a run file showed otherwise, a number it summarized wrongly, or a license it said was fine.

What did it do?
How did you notice?
What did you do instead?

If it genuinely never happened, say so plainly, and then say what you would have had to check in order to notice.
Being honest here costs you far less than a story you cannot defend when you record your video.

Initially, I relied only on Claude to find the top five relevant documents for each query in my gold set. But when I reviewed its suggestions, I found that some documents contained very little relevant information about the questions.
I noticed this by reading the documents myself and checking whether they actually contained the answers. Even with higher reasoning effort, Claude still suggested irrelevant documents, so I had to manually verify its selections rather than relying on them completely.

---

## 4. A number you do not trust

Pick one number in `EVAL.md` that you do not fully trust, and say why.
It could be a mean over a small query class, a difference whose interval includes zero, a verified share of 100%, a score on a gold set you wrote yourself, or a result you got only once.

What would have to be true for you to trust it?
Did you do anything to test it, and what did that show?

One number I don’t fully trust is the 100% verified answer rate in Section 2 of EVAL.md. All 8 in-scope answers passed verification, but the sample is small, and the 95% Wilson interval is [0.676, 1.000]. This means the result does not establish that the system is consistently reliable.

I repeated the evaluation three times, and all three runs passed 8 of 8 answers. However, they used the same questions, so they do not establish performance on unseen questions. I also manually inspected three passing answers and found that one contained a correct statement without a separate supporting quote.

I would trust the result more after testing a larger, more diverse question set and manually checking whether each cited quote supports its claim.

---

## 5. What is still wrong

One thing in your system, your corpus or your gold set that is not right, not finished, or that you do not fully understand.

What would you do next, and how would you find out whether it matters?
Name the file, the query or the document where someone could look.

One unresolved issue is incomplete relevance judgments in my gold set (eval/own/qrels.txt). I reviewed candidates from Claude, BM25, and dense retrieval, but not all 406 documents, so some relevant documents may have been missed.

For example, query q24 in Section 6 of EVAL.md returned IRS documents that also answered the question but were not marked relevant. This could unfairly penalize systems that retrieved useful documents.

Next, I would review the top 10 results from all four systems, correct any missing relevance judgments, and rerun uv run p2 score. I would compare the updated metrics and confidence intervals against the original results to see whether the missing judgments affected my conclusions. Since changing the relevance judgments after scoring could affect my pre-registered hypothesis, I would report this as a separate sensitivity analysis and preserve the original outcome.