# Data recipe — existing labels, no redistributed source corpus

This contribution contains prediction records, a source manifest and a deterministic transformation script. It does not claim a new original dataset and does not bundle source corpora or private Feishu messages.

| Source | Revision used | Source-declared license | Supervision |
|---|---|---|---|
| [AmazonScience/MASSIVE](https://huggingface.co/datasets/AmazonScience/massive) | ff6bd8e4b27c3543e4f8fe2108f32bb95a6f8740 | CC-BY-4.0 | zh-CN/zh-TW/en-US intent labels |
| [CrossWOZ / ConvLab mirror](https://huggingface.co/datasets/ConvLab/crosswoz) | 4a3e56082543ed9eecb9c76ef5eadc1aa0cc5ca0 | Apache-2.0 | Original dialogue-act presence |
| [THUIR/T2Ranking](https://huggingface.co/datasets/THUIR/T2Ranking) | 2a369a430a70979223f1b9a41b1919774d46b432 | Apache-2.0 | Original four-level relevance labels |

Source cards and license evidence were fetched on2026-09-23 into the [companion model release provenance folder](https://huggingface.co/Adkid/laya-cn-a/tree/97f1604aca185393887b9a5cc78380fdb008f4a4/provenance). CrossWOZ's upstream LICENSE and T2Ranking's upstream license statement were checked alongside the pinned dataset cards. Preserve MASSIVE/SLURP, CrossWOZ and T2Ranking author attribution when preparing derived data; this package does not relicense their contents.

## Actual recipe

The training manifest has95,708 rows: MASSIVE30,264 across three locales, CrossWOZ29,986 binary judgements, T2Ranking35,458 labelled query-document pairs. Judgement count is not conversation count or independent person/query count. Tune/calibration derive from training groups; officialdev/test subsets are separate. The exact filtering, grouping, exclusions, hashes and counts are in the [companion model release training recipe](https://huggingface.co/Adkid/laya-cn-a/tree/97f1604aca185393887b9a5cc78380fdb008f4a4/recipe).

`transform.py` preserves original labels while changing presentation: Chinese intent label descriptions, deterministic positive/negative intent matching, JSON message lists with target IDs and a same-split distractor, and structured relevance query/document fields. Descriptions are manually specified metadata, not independently human-reviewed new gold. Transformations are evaluated separately from original format. No ownership/urgency/cancellation gold is inferred from unrelated labels, and no benchmark examples are used as training rows.

CrossWOZ contains role-played task dialogues, not enterprise group-chat logs. MASSIVE is assistant intent data; T2Ranking is relevance data. These sources do not by themselves teach Feishu task ownership. That domain gap remains visible in the poor Feishu diagnostic results.

The frozen64-case Feishu benchmark is AI-assisted synthetic input with real inference outputs. It is not training data and not extracted private messages. Existing test panels and Feishu diagnostics have been used during development; no claim of a new independent blind benchmark is made. Pretraining contamination remains unknown.
