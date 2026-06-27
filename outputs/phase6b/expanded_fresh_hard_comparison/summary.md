# DomainRAG-Bench Comparison

## Leaderboard

| method | questions | answer_score | retrieval_hit | correctness | faithfulness | hallucination_risk | api_calls | errors | unsupported_claims |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| lexical_rag | 8 | 0.8673 | 1.0000 | 5.0000 | 5.0000 | 0.0000 | 17 | 0 | 0 |
| oracle_context | 8 | 0.8631 | 1.0000 | 4.8750 | 5.0000 | 0.0000 | 16 | 0 | 0 |
| no_rag | 8 | 0.1572 | 0.0000 | 1.8750 | 0.7500 | 4.2500 | 18 | 0 | 10 |

## Method Details

### lexical_rag

- Questions: 8
- Answer API calls: 9
- Judge API calls: 8
- Total tokens: 20165
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
- answer.short_answer_token_f1: 0.6051
- answer.single_choice_accuracy: 1.0000
- judge.context_support: 5.0000
- judge.correctness: 5.0000
- judge.faithfulness: 5.0000
- judge.hallucination_risk: 0.0000
- judge.relevance: 5.0000

### no_rag

- Questions: 8
- Answer API calls: 10
- Judge API calls: 8
- Total tokens: 21404
- Answer errors: 0
- Judge errors: 0
- Unsupported claims: 10
- answer.fill_blank_alias_match: 0.0000
- answer.fill_blank_normalized_em: 0.0000
- answer.key_point_coverage: 0.0000
- answer.multiple_choice_exact_match: 0.0000
- answer.multiple_choice_jaccard: 0.0000
- answer.multiple_choice_micro_f1: 0.0000
- answer.retrieval_hit: 0.0000
- answer.retrieval_mrr: 0.0000
- answer.retrieval_recall: 0.0000
- answer.short_answer_token_f1: 0.2574
- answer.single_choice_accuracy: 1.0000
- judge.context_support: 0.0000
- judge.correctness: 1.8750
- judge.faithfulness: 0.7500
- judge.hallucination_risk: 4.2500
- judge.relevance: 3.3750

### oracle_context

- Questions: 8
- Answer API calls: 8
- Judge API calls: 8
- Total tokens: 13464
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
- answer.short_answer_token_f1: 0.5717
- answer.single_choice_accuracy: 1.0000
- judge.context_support: 5.0000
- judge.correctness: 4.8750
- judge.faithfulness: 5.0000
- judge.hallucination_risk: 0.0000
- judge.relevance: 5.0000
