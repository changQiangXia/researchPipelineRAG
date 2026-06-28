# DomainRAG-Bench Comparison

## Leaderboard

| method | questions | answer_score | retrieval_hit | correctness | faithfulness | hallucination_risk | api_calls | errors | unsupported_claims |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| oracle_context | 20 | 0.8358 | 1.0000 | 4.8500 | 5.0000 | 0.0000 | 40 | 0 | 0 |
| lexical_rag | 20 | 0.8251 | 0.9500 | 4.7000 | 4.7500 | 0.2500 | 40 | 0 | 1 |
| flashrag_bm25_live_deepseek | 20 | 0.6573 | 0.9500 | 4.3500 | 4.7500 | 0.2500 | 40 | 0 | 0 |
| flashrag_bm25_oracle_reader | 20 | 0.8583 | 0.9500 | 4.7500 | 4.4500 | 0.5500 | 20 | 0 | 4 |
| no_rag | 20 | 0.5153 | 0.0000 | 3.4500 | 2.5000 | 2.5000 | 40 | 0 | 17 |

## Method Details

### flashrag_bm25_live_deepseek

- Questions: 20
- Answer API calls: 20
- Judge API calls: 20
- Total tokens: 54480
- Answer errors: 0
- Judge errors: 0
- Unsupported claims: 0
- answer.fill_blank_alias_match: 1.0000
- answer.fill_blank_normalized_em: 1.0000
- answer.key_point_coverage: 0.1333
- answer.multiple_choice_exact_match: 0.2000
- answer.multiple_choice_jaccard: 0.6500
- answer.multiple_choice_micro_f1: 0.7562
- answer.retrieval_hit: 0.9500
- answer.retrieval_mrr: 0.9000
- answer.retrieval_recall: 0.8542
- answer.short_answer_token_f1: 0.5189
- answer.single_choice_accuracy: 1.0000
- judge.context_support: 4.7000
- judge.correctness: 4.3500
- judge.faithfulness: 4.7500
- judge.hallucination_risk: 0.2500
- judge.relevance: 4.8500

### flashrag_bm25_oracle_reader

- Questions: 20
- Answer API calls: 0
- Judge API calls: 20
- Total tokens: 28642
- Answer errors: 0
- Judge errors: 0
- Unsupported claims: 4
- answer.fill_blank_alias_match: 1.0000
- answer.fill_blank_normalized_em: 1.0000
- answer.key_point_coverage: 0.0667
- answer.multiple_choice_exact_match: 1.0000
- answer.multiple_choice_jaccard: 1.0000
- answer.multiple_choice_micro_f1: 1.0000
- answer.retrieval_hit: 0.9500
- answer.retrieval_mrr: 0.9000
- answer.retrieval_recall: 0.8542
- answer.short_answer_token_f1: 1.0000
- answer.single_choice_accuracy: 0.8000
- judge.context_support: 4.2000
- judge.correctness: 4.7500
- judge.faithfulness: 4.4500
- judge.hallucination_risk: 0.5500
- judge.relevance: 4.7500

### lexical_rag

- Questions: 20
- Answer API calls: 20
- Judge API calls: 20
- Total tokens: 51473
- Answer errors: 0
- Judge errors: 0
- Unsupported claims: 1
- answer.fill_blank_alias_match: 1.0000
- answer.fill_blank_normalized_em: 1.0000
- answer.key_point_coverage: 0.1333
- answer.multiple_choice_exact_match: 1.0000
- answer.multiple_choice_jaccard: 1.0000
- answer.multiple_choice_micro_f1: 1.0000
- answer.retrieval_hit: 0.9500
- answer.retrieval_mrr: 0.9250
- answer.retrieval_recall: 0.9250
- answer.short_answer_token_f1: 0.4675
- answer.single_choice_accuracy: 1.0000
- judge.context_support: 4.7500
- judge.correctness: 4.7000
- judge.faithfulness: 4.7500
- judge.hallucination_risk: 0.2500
- judge.relevance: 4.9500

### no_rag

- Questions: 20
- Answer API calls: 20
- Judge API calls: 20
- Total tokens: 51420
- Answer errors: 0
- Judge errors: 0
- Unsupported claims: 17
- answer.fill_blank_alias_match: 0.8000
- answer.fill_blank_normalized_em: 0.8000
- answer.key_point_coverage: 0.0000
- answer.multiple_choice_exact_match: 0.2000
- answer.multiple_choice_jaccard: 0.5000
- answer.multiple_choice_micro_f1: 0.5429
- answer.retrieval_hit: 0.0000
- answer.retrieval_mrr: 0.0000
- answer.retrieval_recall: 0.0000
- answer.short_answer_token_f1: 0.2798
- answer.single_choice_accuracy: 1.0000
- judge.context_support: 0.0000
- judge.correctness: 3.4500
- judge.faithfulness: 2.5000
- judge.hallucination_risk: 2.5000
- judge.relevance: 4.9000

### oracle_context

- Questions: 20
- Answer API calls: 20
- Judge API calls: 20
- Total tokens: 42016
- Answer errors: 0
- Judge errors: 0
- Unsupported claims: 0
- answer.fill_blank_alias_match: 1.0000
- answer.fill_blank_normalized_em: 1.0000
- answer.key_point_coverage: 0.1333
- answer.multiple_choice_exact_match: 1.0000
- answer.multiple_choice_jaccard: 1.0000
- answer.multiple_choice_micro_f1: 1.0000
- answer.retrieval_hit: 1.0000
- answer.retrieval_mrr: 1.0000
- answer.retrieval_recall: 1.0000
- answer.short_answer_token_f1: 0.5533
- answer.single_choice_accuracy: 1.0000
- judge.context_support: 4.7500
- judge.correctness: 4.8500
- judge.faithfulness: 5.0000
- judge.hallucination_risk: 0.0000
- judge.relevance: 5.0000
