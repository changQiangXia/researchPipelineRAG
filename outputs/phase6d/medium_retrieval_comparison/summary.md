# DomainRAG-Bench Comparison

## Leaderboard

| method | questions | answer_score | retrieval_hit | correctness | faithfulness | hallucination_risk | api_calls | errors | unsupported_claims |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| flashrag_bm25_oracle_reader | 20 | 0.8583 | 0.9500 |  |  |  | 0 | 0 | 0 |
| lexical_rag | 20 | 0.8583 | 0.9500 |  |  |  | 0 | 0 | 0 |

## Method Details

### flashrag_bm25_oracle_reader

- Questions: 20
- Answer API calls: 0
- Judge API calls: 0
- Total tokens: 1048
- Answer errors: 0
- Judge errors: 0
- Unsupported claims: 0
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

### lexical_rag

- Questions: 20
- Answer API calls: 0
- Judge API calls: 0
- Total tokens: 1048
- Answer errors: 0
- Judge errors: 0
- Unsupported claims: 0
- answer.fill_blank_alias_match: 1.0000
- answer.fill_blank_normalized_em: 1.0000
- answer.key_point_coverage: 0.0667
- answer.multiple_choice_exact_match: 1.0000
- answer.multiple_choice_jaccard: 1.0000
- answer.multiple_choice_micro_f1: 1.0000
- answer.retrieval_hit: 0.9500
- answer.retrieval_mrr: 0.9250
- answer.retrieval_recall: 0.9250
- answer.short_answer_token_f1: 1.0000
- answer.single_choice_accuracy: 0.8000
