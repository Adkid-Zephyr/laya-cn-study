# Laya-CN Study

An independent, open collection of Chinese-first post-training experiments on Laya. Each study keeps its model version, data provenance, evaluation records, code, and limitations together. This repository is not an official Laya release.

| Experiment | Research | Model | Status |
|---|---|---|---|
| **Laya-CN-A** | [Three-seed intent adaptation study](studies/laya-cn-a/README.md) · [中文](studies/laya-cn-a/README.zh-CN.md) | [Full FP32 model on Hugging Face](https://huggingface.co/Adkid/laya-cn-a) | Experimental; not a reliable Feishu task router |

The A in **Laya-CN-A** names the first public model in this series. Internally, its selected weights came from experiment V3 seed42. The earlier training checkpoint also called A is an intermediate baseline, not this release.

The current study archives 31,200 predictions across original and adapted tasks, 128 Feishu diagnostic responses, and a standard-library audit. To verify the records without model downloads or API keys:

```bash
python studies/laya-cn-a/audit.py
python -m unittest discover -s studies/laya-cn-a -p 'test_*.py'
```

The included Feishu cases are synthetic Chinese workplace-message scenarios, not private chat exports or an official benchmark. Original dataset authors and licenses are credited in the study; source corpora are not redistributed. Later experiments can be added under `studies/` with separate model versions and evidence. The model weights live in their Hugging Face repositories.

[Original Jev/Laya Feishu benchmark](https://github.com/Adkid-Zephyr/chinese-workflow-decision-bench) · [Upstream Laya project](https://github.com/NandhaKishorM/laya)
