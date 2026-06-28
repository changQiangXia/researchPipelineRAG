# DomainRAG-Bench Comparison

## Leaderboard

| method | questions | answer_score | retrieval_hit | correctness | faithfulness | hallucination_risk | api_calls | errors | unsupported_claims |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| flashrag_bm25_live_deepseek | 12 | 0.8554 | 0.9167 | 5.0000 | 5.0000 | 0.0000 | 24 | 0 | 0 |
| lexical_rag | 12 | 0.8540 | 0.9167 | 5.0000 | 5.0000 | 0.0000 | 24 | 0 | 0 |
| no_rag | 12 | 0.3074 | 0.0000 | 2.5833 | 1.2500 | 3.7500 | 27 | 0 | 18 |

## Method Details

### flashrag_bm25_live_deepseek

- Questions: 12
- Answer API calls: 12
- Judge API calls: 12
- Total tokens: 32147
- Answer errors: 0
- Judge errors: 0
- Unsupported claims: 0
- answer.fill_blank_alias_match: 1.0000
- answer.fill_blank_normalized_em: 1.0000
- answer.key_point_coverage: 0.1111
- answer.multiple_choice_exact_match: 1.0000
- answer.multiple_choice_jaccard: 1.0000
- answer.multiple_choice_micro_f1: 1.0000
- answer.retrieval_hit: 0.9167
- answer.retrieval_mrr: 0.4028
- answer.retrieval_recall: 0.7569
- answer.short_answer_token_f1: 0.7324
- answer.single_choice_accuracy: 1.0000
- judge.context_support: 5.0000
- judge.correctness: 5.0000
- judge.faithfulness: 5.0000
- judge.hallucination_risk: 0.0000
- judge.relevance: 5.0000

### lexical_rag

- Questions: 12
- Answer API calls: 12
- Judge API calls: 12
- Total tokens: 31399
- Answer errors: 0
- Judge errors: 0
- Unsupported claims: 0
- answer.fill_blank_alias_match: 1.0000
- answer.fill_blank_normalized_em: 1.0000
- answer.key_point_coverage: 0.1111
- answer.multiple_choice_exact_match: 1.0000
- answer.multiple_choice_jaccard: 1.0000
- answer.multiple_choice_micro_f1: 1.0000
- answer.retrieval_hit: 0.9167
- answer.retrieval_mrr: 0.4097
- answer.retrieval_recall: 0.7361
- answer.short_answer_token_f1: 0.7209
- answer.single_choice_accuracy: 1.0000
- judge.context_support: 5.0000
- judge.correctness: 5.0000
- judge.faithfulness: 5.0000
- judge.hallucination_risk: 0.0000
- judge.relevance: 5.0000

### no_rag

- Questions: 12
- Answer API calls: 15
- Judge API calls: 12
- Total tokens: 36107
- Answer errors: 0
- Judge errors: 0
- Unsupported claims: 18
- answer.fill_blank_alias_match: 0.3333
- answer.fill_blank_normalized_em: 0.3333
- answer.key_point_coverage: 0.0000
- answer.multiple_choice_exact_match: 0.0000
- answer.multiple_choice_jaccard: 0.2500
- answer.multiple_choice_micro_f1: 0.2857
- answer.retrieval_hit: 0.0000
- answer.retrieval_mrr: 0.0000
- answer.retrieval_recall: 0.0000
- answer.short_answer_token_f1: 0.2570
- answer.single_choice_accuracy: 1.0000
- judge.context_support: 0.0000
- judge.correctness: 2.5833
- judge.faithfulness: 1.2500
- judge.hallucination_risk: 3.7500
- judge.relevance: 5.0000
