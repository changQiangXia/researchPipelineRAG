# DomainRAG-Bench Comparison

## Leaderboard

| method | questions | answer_score | retrieval_hit | correctness | faithfulness | hallucination_risk | api_calls | errors | unsupported_claims |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| flashrag_bm25_live_deepseek | 4 | 0.9320 | 1.0000 | 5.0000 | 5.0000 | 0.0000 | 8 | 0 | 0 |
| flashrag_bm25_oracle_reader | 4 | 0.9167 | 1.0000 | 5.0000 | 5.0000 | 0.0000 | 4 | 0 | 0 |
| lexical_rag | 4 | 0.8631 | 1.0000 | 5.0000 | 5.0000 | 0.0000 | 8 | 0 | 0 |
| oracle_context | 4 | 0.9088 | 1.0000 | 5.0000 | 4.7500 | 0.2500 | 8 | 0 | 1 |
| no_rag | 4 | 0.1504 | 0.0000 | 1.7500 | 1.2500 | 3.7500 | 8 | 0 | 5 |

## Method Details

### flashrag_bm25_live_deepseek

- Questions: 4
- Answer API calls: 4
- Judge API calls: 4
- Total tokens: 11176
- Answer errors: 0
- Judge errors: 0
- Unsupported claims: 0
- answer.fill_blank_alias_match: 1.0000
- answer.fill_blank_normalized_em: 1.0000
- answer.key_point_coverage: 0.6667
- answer.multiple_choice_exact_match: 1.0000
- answer.multiple_choice_jaccard: 1.0000
- answer.multiple_choice_micro_f1: 1.0000
- answer.retrieval_hit: 1.0000
- answer.retrieval_mrr: 1.0000
- answer.retrieval_recall: 1.0000
- answer.short_answer_token_f1: 0.7895
- answer.single_choice_accuracy: 1.0000
- judge.context_support: 5.0000
- judge.correctness: 5.0000
- judge.faithfulness: 5.0000
- judge.hallucination_risk: 0.0000
- judge.relevance: 5.0000

### flashrag_bm25_oracle_reader

- Questions: 4
- Answer API calls: 0
- Judge API calls: 4
- Total tokens: 4450
- Answer errors: 0
- Judge errors: 0
- Unsupported claims: 0
- answer.fill_blank_alias_match: 1.0000
- answer.fill_blank_normalized_em: 1.0000
- answer.key_point_coverage: 0.3333
- answer.multiple_choice_exact_match: 1.0000
- answer.multiple_choice_jaccard: 1.0000
- answer.multiple_choice_micro_f1: 1.0000
- answer.retrieval_hit: 1.0000
- answer.retrieval_mrr: 1.0000
- answer.retrieval_recall: 1.0000
- answer.short_answer_token_f1: 1.0000
- answer.single_choice_accuracy: 1.0000
- judge.context_support: 5.0000
- judge.correctness: 5.0000
- judge.faithfulness: 5.0000
- judge.hallucination_risk: 0.0000
- judge.relevance: 5.0000

### lexical_rag

- Questions: 4
- Answer API calls: 4
- Judge API calls: 4
- Total tokens: 9964
- Answer errors: 0
- Judge errors: 0
- Unsupported claims: 0
- answer.fill_blank_alias_match: 1.0000
- answer.fill_blank_normalized_em: 1.0000
- answer.key_point_coverage: 0.3333
- answer.multiple_choice_exact_match: 1.0000
- answer.multiple_choice_jaccard: 1.0000
- answer.multiple_choice_micro_f1: 1.0000
- answer.retrieval_hit: 1.0000
- answer.retrieval_mrr: 1.0000
- answer.retrieval_recall: 1.0000
- answer.short_answer_token_f1: 0.5714
- answer.single_choice_accuracy: 1.0000
- judge.context_support: 5.0000
- judge.correctness: 5.0000
- judge.faithfulness: 5.0000
- judge.hallucination_risk: 0.0000
- judge.relevance: 5.0000

### no_rag

- Questions: 4
- Answer API calls: 4
- Judge API calls: 4
- Total tokens: 7630
- Answer errors: 0
- Judge errors: 0
- Unsupported claims: 5
- answer.fill_blank_alias_match: 0.0000
- answer.fill_blank_normalized_em: 0.0000
- answer.key_point_coverage: 0.0000
- answer.multiple_choice_exact_match: 0.0000
- answer.multiple_choice_jaccard: 0.0000
- answer.multiple_choice_micro_f1: 0.0000
- answer.retrieval_hit: 0.0000
- answer.retrieval_mrr: 0.0000
- answer.retrieval_recall: 0.0000
- answer.short_answer_token_f1: 0.2034
- answer.single_choice_accuracy: 1.0000
- judge.context_support: 0.0000
- judge.correctness: 1.7500
- judge.faithfulness: 1.2500
- judge.hallucination_risk: 3.7500
- judge.relevance: 4.5000

### oracle_context

- Questions: 4
- Answer API calls: 4
- Judge API calls: 4
- Total tokens: 8825
- Answer errors: 0
- Judge errors: 0
- Unsupported claims: 1
- answer.fill_blank_alias_match: 1.0000
- answer.fill_blank_normalized_em: 1.0000
- answer.key_point_coverage: 0.6667
- answer.multiple_choice_exact_match: 1.0000
- answer.multiple_choice_jaccard: 1.0000
- answer.multiple_choice_micro_f1: 1.0000
- answer.retrieval_hit: 1.0000
- answer.retrieval_mrr: 1.0000
- answer.retrieval_recall: 1.0000
- answer.short_answer_token_f1: 0.6038
- answer.single_choice_accuracy: 1.0000
- judge.context_support: 5.0000
- judge.correctness: 5.0000
- judge.faithfulness: 4.7500
- judge.hallucination_risk: 0.2500
- judge.relevance: 5.0000
