# DomainRAG Human Calibration Audit

Reviewed rows: 15
Priority rows: 14
Rows with judge unsupported claims: 7

## Overall

- Human: correctness=3.5333, context_support=2.9000, faithfulness=2.9000
- Judge: correctness=3.4000, context_support=2.6000, faithfulness=2.6000
- Mean absolute delta: correctness=0.1333, context_support=0.3667, faithfulness=0.3667

## Methods

| method | reviewed_rows | human_correctness | human_context_support | human_faithfulness | judge_correctness | judge_context_support | judge_faithfulness |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| flashrag_bm25_live_deepseek | 3 | 3.3333 | 3.3333 | 3.3333 | 3.3333 | 3.3333 | 3.3333 |
| flashrag_bm25_oracle_reader | 3 | 5.0000 | 3.0000 | 3.0000 | 5.0000 | 1.3333 | 1.3333 |
| lexical_rag | 3 | 3.3333 | 3.1667 | 3.1667 | 3.0000 | 3.3333 | 3.3333 |
| no_rag | 3 | 2.0000 | 0.0000 | 0.0000 | 1.6667 | 0.0000 | 0.0000 |
| oracle_context | 3 | 4.0000 | 5.0000 | 5.0000 | 4.0000 | 5.0000 | 5.0000 |

## Decisions

- agree_with_judge: 10
- disagree_with_judge: 2
- mostly_agree_with_judge: 3

## Disagreements

- fresh_hard::flashrag_bm25_oracle_reader::ns_ht_q024 context_support: human=2.5000, judge=0.0000, abs_delta=2.5000
- fresh_hard::flashrag_bm25_oracle_reader::ns_ht_q024 faithfulness: human=2.5000, judge=0.0000, abs_delta=2.5000
- fresh_hard::flashrag_bm25_oracle_reader::ns_ht_q060 context_support: human=2.5000, judge=0.0000, abs_delta=2.5000
- fresh_hard::flashrag_bm25_oracle_reader::ns_ht_q060 faithfulness: human=2.5000, judge=0.0000, abs_delta=2.5000
