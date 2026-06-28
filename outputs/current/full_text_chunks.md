# Full-Text Chunk Manifests

全文 chunk manifest 的当前入口：

```text
outputs/archive/provenance/source-workflow/full-text-chunk-extraction/full_text_chunk_extraction/
```

关键文件：

| file | purpose |
| --- | --- |
| `chunk_extraction_summary.json` | 机器可读摘要 |
| `chunk_extraction_summary.md` | 人类可读摘要 |
| `chunk_source_manifest.jsonl` | 每个来源的 chunk 状态 |
| `full_text_chunks.jsonl` | chunk manifest 列表 |

当前统计：

| item | count |
| --- | ---: |
| access rows | 115 |
| parseable access rows | 71 |
| sources attempted | 71 |
| sources chunked | 60 |
| chunk manifests | 2,196 |

存储策略：

- `include_text=false`。
- 公开 manifest 不保存全文 chunk text。
- manifest 保留 `text_sha256`，用于追踪和复核。

边界：这批结果是 machine-parseable full-text chunk manifests，不是 human-final accepted-source corpus。后续如果要生成正式 benchmark，应先完成人工来源签核，再只从 human-accepted final sources 抽取和发布 chunk。

