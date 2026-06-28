# Source Review Status

来源审核当前分成三层理解：候选来源、人工终审包、最终签核白名单。

## 当前入口

人工终审包：

```text
outputs/archive/provenance/source-workflow/manual-finalization-packet/manual_finalization_packet/
```

human sign-off workflow：

```text
outputs/archive/provenance/source-workflow/human-signoff/human_signoff/
```

## 当前状态

| item | count |
| --- | ---: |
| source rows in manual packet | 115 |
| candidate final whitelist queue | 108 |
| pending human review | 108 |
| accepted final sources | 0 |
| rejected final sources | 0 |

## 含义

`manual_finalization_packet` 把可进入人工终审的来源整理成队列，但它不等于最终认可。

`human_signoff` 提供最终签核模板和 workflow。只有真实人工 reviewer 填入 accept/reject 等标签后，才能产生可信的 `final_source_whitelist.jsonl`。

当前 `final_source_whitelist.jsonl` 存在是为了固定工作流输出形状，不代表已经完成 100-180 篇 human-final 文献白名单。

## 仍需完成

- 人工来源签核。
- 从 human-accepted final sources 重新抽取 chunk。
- 基于 accepted chunks 生成正式 300-500 题 benchmark。

