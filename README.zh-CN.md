# Laya-CN Study：Laya 中文后训练实验

这是独立开源的 Laya 中文优先后训练研究仓库。每轮实验单独保存方法、模型版本、数据来源、逐条评测和不足；不是 Laya 官方发布。

| 实验 | 报告 | 模型 | 当前状态 |
|---|---|---|---|
| **Laya-CN-A** | [三种子中文意图适配报告](studies/laya-cn-a/README.zh-CN.md) · [English](studies/laya-cn-a/README.md) | [Hugging Face 完整权重](https://huggingface.co/Adkid/laya-cn-a) | 实验模型；Feishu 待办筛选尚不可靠 |

名称中的 A 是此系列**第一个公开版本**。实际公开权重来自内部实验 V3 的 seed42；训练过程中也有一个叫 A 的中间对照模型，两者不是同一版本。

本轮留有 31,200 条跨模型/任务预测记录、128 条 Feishu 场景响应，以及不需要下载模型的离线核验脚本：

```bash
python studies/laya-cn-a/audit.py
python -m unittest discover -s studies/laya-cn-a -p 'test_*.py'
```

Feishu 案例是合成的中文办公消息场景，不是私人群聊转储或官方评测。上游数据及许可见实验目录；不重发原始语料。后续版本可分别放入 `studies/`，模型权重存放在对应的 Hugging Face 仓库。

[原始 Jev/Laya Feishu benchmark](https://github.com/Adkid-Zephyr/chinese-workflow-decision-bench) · [Laya 上游](https://github.com/NandhaKishorM/laya)
